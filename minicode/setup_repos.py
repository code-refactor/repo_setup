"""
Setup script for cloning and refactoring repositories MiniCode.small dataset.

This script:
1. Clones repositories from the 'small' dataset split, grouped by library name
2. Creates a unified directory structure for each library
3. Copies code from persona implementations to the unified directories
4. Creates project files (setup.py) for each unified library
5. Fixes import paths

Usage:
  # Clone and process all libraries from the 'large' split
  uv run python -m minicode.setup_large_repos
"""

from datasets import load_dataset
from multiprocessing import Pool, cpu_count, set_start_method
from functools import partial
import subprocess, os, glob, itertools, sys, re, numpy as np
import shutil
from thefuzz import fuzz
from sklearn.cluster import AgglomerativeClustering

# Login using e.g. `huggingface-cli login` to access this dataset
	
def setup_all_flat(target_dir, split):
    ds = load_dataset("celinelee/minicode-repos", split=split)
    for ex in ds:
        subprocess.run(["git", "clone", ex["github_link"]], cwd=target_dir)

def string_similarities(s1, s2):
    return {
        "ratio": fuzz.ratio(s1, s2),
        "partial_ratio": fuzz.partial_ratio(s1, s2),
        "token_sort_ratio": fuzz.token_sort_ratio(s1, s2),
        "token_set_ratio": fuzz.token_set_ratio(s1, s2),
    }

def compute_pairwise_similarity(pair, task_strings):
    i, j = pair
    # compute average fuzzy similarity on tasks
    t_sim = string_similarities(task_strings[i], task_strings[j])
    task_avg = sum(t_sim.values()) / len(t_sim)
    return i, j, task_avg

def compute_string_matrices_parallel(directory_paths, processes=None):
    # read all TASK.md strings and code once
    task_strings = []
    for path in directory_paths:
        with open(os.path.join(path, "TASK.md"), 'r', encoding='utf-8') as f:
            task_strings.append(f.read())

    n = len(directory_paths)
    task_sim = np.zeros((n, n))

    pairs = list(itertools.combinations(range(n), 2))
    procs = min(processes or cpu_count(), cpu_count())

    with Pool(processes=procs) as pool:
        func = partial(compute_pairwise_similarity,
                       task_strings=task_strings)
        for i, j, task_avg in pool.map(func, pairs):
            task_sim[i][j] = task_sim[j][i] = task_avg

    return task_sim

#### CLUSTERING CODE ####
from sklearn.cluster import AgglomerativeClustering

def agglomerative_clustering(embeddings, embedding_clusterer):
    X = np.array(embeddings)
    print("shape of X", X.shape)
    clustering = embedding_clusterer.fit_predict(X)
    return clustering

def get_string_clusters(directory_paths, num_clusters, processes=None):
    # compute similarity matrices in parallel
    task_sim = compute_string_matrices_parallel(directory_paths, processes)

    # convert similarity to distance
    task_dist = 100 - task_sim
    if task_dist.shape[0] <= 1:
        print(f"{task_dist.shape} matrix... will not cluster")
        return (None, task_dist)

    # cluster with precomputed distances
    clusterer = AgglomerativeClustering(
        n_clusters=num_clusters,
        metric='precomputed',
        linkage='average'
    )
    task_labels = clusterer.fit_predict(task_dist)

    task_clusters = [[] for _ in range(num_clusters)]
    for idx, lab in enumerate(task_labels):
        task_clusters[lab].append(idx)

    return (task_clusters, task_dist)

def sort_string_clusters(clusters, dist_matrix):
    avg_dists = []
    for cluster in clusters:
        if len(cluster) < 2:
            avg_dists.append(float('inf'))
        else:
            pairs = list(itertools.combinations(cluster, 2))
            avg = sum(dist_matrix[i][j] for i,j in pairs) / len(pairs)
            avg_dists.append(avg)
    return [cluster for (_, cluster) in sorted(zip(avg_dists, clusters))]

"""
Directory structure created:
- small_repos/{library_name}/
  ├── [persona_repos]/           # Original cloned repositories
  └── unified/                   # Unified library structure
      ├── common/                # Common functionality
      │   └── core/              # Core data structures and algorithms
      ├── [package_name]/        # Original package names preserved
      ├── tests/
      │   └── [persona]/         # Tests for each persona
      ├── pyproject.toml
      └── setup.py
"""

        
def _rewrite_imports(file_path: str, persona: str, search_root: str):
    """
    Generic import-rewriter:
    - prefixes any local imports with unified.<persona>.
    - for `import module`, adds `as module` to preserve symbol names.
    """
    with open(file_path, 'r') as f:
        content = f.read()

    def replace(match):
        imp, mod = match.group(1), match.group(2)
        # skip stdlib modules
        if '.' not in mod and mod in sys.builtin_module_names:
            return match.group(0)
        # already namespaced?
        if mod.startswith(f"{persona}.") or mod.startswith("unified."):
            return match.group(0)
        # check if this module exists in the search_root (either original or unified)
        mod_py = os.path.join(search_root, persona, *mod.split('.')) + '.py'
        mod_pkg = os.path.join(search_root, persona, *mod.split('.'))
        if os.path.exists(mod_py) or os.path.isdir(mod_pkg):
            if imp.strip() == 'import':
                alias = mod.split('.')[-1]
                return f"import unified.{persona}.{mod} as {alias}"
            else:
                return f"{imp}unified.{persona}.{mod}"
        return match.group(0)

    pattern = re.compile(r'^(\s*from\s+|import\s+)([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)', re.MULTILINE)
    new_content = pattern.sub(replace, content)

    if new_content != content:
        with open(file_path, 'w') as f:
            f.write(new_content)


def _place_inits(unified_root: str):
    """Ensure every directory under unified_root is a Python package."""
    for dirpath, _, _ in os.walk(unified_root):
        init = os.path.join(dirpath, "__init__.py")
        if not os.path.exists(init):
            open(init, "w").close()


def setup_for_refactor(root_dir: str):
    unified_dir = os.path.join(root_dir, "unified")
    persona_dirs = [
        d for d in os.listdir(root_dir)
        if os.path.isdir(os.path.join(root_dir, d)) and d != "unified"
    ]

    # 1) Clear/Create unified area
    if os.path.exists(unified_dir):
        shutil.rmtree(unified_dir)
    os.makedirs(unified_dir)

    # 2) Copy each persona package (excluding tests)
    for persona in persona_dirs:
        src = os.path.join(root_dir, persona)
        dst = os.path.join(unified_dir, persona)
        shutil.copytree(
            src, dst,
            ignore=shutil.ignore_patterns("test_*.py", "__pycache__")
        )
        # 2a) Rewrite imports inside the source code
        for py in glob.glob(os.path.join(dst, "**", "*.py"), recursive=True):
            _rewrite_imports(py, persona, unified_dir)

    # 3) Create common/ if needed
    os.makedirs(os.path.join(unified_dir, "common"), exist_ok=True)

    # 4) Gather & move all test_*.py into unified/tests/
    tests_dest = os.path.join(unified_dir, "tests")
    os.makedirs(tests_dest, exist_ok=True)

    for persona in persona_dirs:
        persona_src = os.path.join(root_dir, persona)
        for dirpath, _, files in os.walk(persona_src):
            for fn in files:
                if fn.startswith("test_") and fn.endswith(".py"):
                    orig = os.path.join(dirpath, fn)
                    new_name = f"test_{persona}_{fn[len('test_'):]}"
                    dst = os.path.join(tests_dest, new_name)
                    shutil.copy2(orig, dst)
                    _rewrite_imports(dst, persona, root_dir)

    # 5) Inject __init__.py everywhere under unified/
    _place_inits(unified_dir)

    # 6) Write setup.py for unified package
    with open(os.path.join(unified_dir, "setup.py"), "w") as f:
        f.write(f"""from setuptools import setup, find_packages

setup(
    name=\"{os.path.basename(root_dir)}\",
    version=\"1.0.0\",
    packages=find_packages(),
)
""")
        

    # 7) Write pyproject.toml for unified package
    pyproject = f"""[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{os.path.basename(root_dir)}"
version = "1.0.0"
description = "Unified package for merged {root_dir[:-2]} repositories"
readme = "README.md"
requires-python = ">=3.7"
dependencies = []
"""
    with open(os.path.join(unified_dir, "pyproject.toml"), "w") as f:
        f.write(pyproject)
        
def setup_grouped(target_dir, split, num_groups=3):
    ds = load_dataset("celinelee/minicode-repos", split=split)
    
    # first clone everything
    library_paths = set()
    for ex in ds:
        target_subdir = os.path.join(target_dir, ex["library_name"])
        if not os.path.exists(target_subdir): os.makedirs(target_subdir, exist_ok=True)
        library_paths.add(target_subdir)
        subprocess.run(["git", "clone", ex["github_link"]], cwd=target_subdir)
    
    # then rearrange into group_size
    for library_path in library_paths:
        library_personas = glob.glob(os.path.join(library_path, "*/"))
        clusters, distances = get_string_clusters(library_personas, num_groups)
        if clusters is None:
            continue
        clusters_sorted = sort_string_clusters(clusters, distances)
        for idx, cluster_indices in enumerate(clusters_sorted):
            group_dir = f"{library_path.rstrip(os.path.sep)}_{'ABCD'[idx]}"
            if not os.path.exists(group_dir): os.makedirs(group_dir, exist_ok=True)
            for c_idx in cluster_indices:
                shutil.move(library_personas[c_idx], os.path.join(group_dir, os.path.relpath(library_personas[c_idx], library_path)))

            setup_for_refactor(group_dir)
        # todo remove now-empty folder

if __name__ == "__main__":
    try:
        set_start_method("fork")
    except RuntimeError:
        pass

    setup_grouped("small_repos", "small")
