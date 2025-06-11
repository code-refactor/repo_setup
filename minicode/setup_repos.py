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


def _update_local_imports(new_test_file_path, persona_name, starter_repo_path):
    with open(new_test_file_path, 'r') as f:
        content = f.read()
    # Find import statements (both regular imports and from imports)
    import_pattern = re.compile(r'(?m)^\s*(from\s+|import\s+)([.\w]+)')
    matches = import_pattern.findall(content)

    modified_content = content
    for match in matches:
        import_type, module_path = match
        if '.' not in module_path and module_path in sys.builtin_module_names:
            continue
                    
        # Skip imports that already include the subdirectory
        if persona_name in module_path:
            continue

        # Check if this is a relative import referring to a local module
        module_file = module_path.replace('.', '/') + '.py'
        if os.path.exists(os.path.join(starter_repo_path, persona_name, module_file)):
            # This is a local module that needs to be updated
            old_import = f"{import_type}{module_path}"
            if import_type.strip() == 'import':
                new_import = f"{import_type}{persona_name}.{module_path} as {module_path}"
            else:
                new_import = f"{import_type}{persona_name}.{module_path}"
            modified_content = modified_content.replace(old_import, new_import)
            continue

        module_folder = module_path.replace('.', '/')
        if os.path.exists(os.path.join(starter_repo_path, persona_name, module_folder)):
            # This is a local module that needs to be updated
            old_import = f"{import_type}{module_path}"
            if import_type.strip() == 'import':
                new_import = f"{import_type}{persona_name}.{module_path} as {module_path}"
            else:
                new_import = f"{import_type}{persona_name}.{module_path}"
            modified_content = modified_content.replace(old_import, new_import)


    # Write the updated content back to the file
    if modified_content != content:
        with open(new_test_file_path, 'w') as f:
            f.write(modified_content)

def _place_inits(repo_path):
    init_file = os.path.join(repo_path, "unified", "__init__.py")
    with open(init_file, 'w') as f:
        f.write("")
    init_file = os.path.join(repo_path, "unified", "tests", "__init__.py")
    with open(init_file, 'w') as f:
        f.write("")
    
    for persona_subdir in glob.glob(repo_path):
        if not os.path.isdir(persona_subdir): continue
        init_file = os.path.join(persona_subdir, "__init__.py")
        with open(init_file, 'w') as f:
            f.write("")

def setup_for_refactor(grouped_dir):
    """Move all test_*.py files into a unified test directory structure.

    This function takes test files scattered throughout the repository and
    moves them into a unified test directory at grouped_dir/unified/tests/
    preserving their test names but organizing them consistently.
    """
    # Create unified test directory if it doesn't exist
    unified_test_dir = os.path.join(grouped_dir, "unified", "tests")
    os.makedirs(unified_test_dir, exist_ok=True)

    # Find all test files in the repository (excluding those already in unified/tests)
    test_files = []
    for root, _, files in os.walk(grouped_dir):
        if "unified/tests" in root:
            continue  # Skip files already in unified/tests
        persona_name = root[len(grouped_dir)+1:]
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                mod_filename = f"test_{persona_name}_{os.path.basename(file)[len('test_'):]}"
                test_files.append((os.path.join(root, file), os.path.join(unified_test_dir, mod_filename), persona_name))

    # Move each test file to the unified test directory with appropriate naming
    for (test_file_orig, test_file_dest, persona_name) in test_files:
        # copy the file 
        shutil.copyfile(test_file_orig, test_file_dest)

        # Update local import paths in the moved file. won't be perfect.
        _update_local_imports(test_file_dest, persona_name, grouped_dir)

        # place __init__.py everywhere needed
        _place_inits(grouped_dir)

    # setup.py file for treating the refactored one as a repo
    with open(os.path.join(grouped_dir, "unified", "setup.py"), 'w') as wf:
        wf.write(f"""from setuptools import setup, find_packages

setup(
    name='{grouped_dir}',
    version='1.0.0',
    packages=find_packages(),
)""")


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
            breakpoint()
        # todo remove now-empty folder

if __name__ == "__main__":
    try:
        set_start_method("fork")
    except RuntimeError:
        pass

    setup_grouped("small_repos", "small")