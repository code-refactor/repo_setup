from datasets import load_dataset
from multiprocessing import Pool, cpu_count, set_start_method
from functools import partial
import subprocess, os, glob, itertools, numpy as np
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

if __name__ == "__main__":
    try:
        set_start_method("fork")
    except RuntimeError:
        pass

    setup_grouped("small_repos", "small")