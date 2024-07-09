import numpy as np

from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from typing import Union, List, Tuple, Dict, Optional, Any
from sklearn.cluster import KMeans, AffinityPropagation, MeanShift, SpectralClustering
from sklearn.cluster import AgglomerativeClustering, Birch
from sklearn.base import ClusterMixin
 
import os
import csv
from pprint import pprint
from tqdm import tqdm 

def cluster(
    embeddings: np.ndarray, 
    model, 
    metrics: List[str] = ['dbs'],
    distance: str = 'euclidean',
    return_model: bool = False,
) -> Tuple[np.ndarray, Dict[str, float]]:
    """
    Fits a clustering model to the embeddings and calculates specified metrics.
    
    Args:
        embeddings (np.ndarray): Array of embeddings.
        model: A clustering model with the method .fit_transform
        metrics (List[str]): List of metric names to calculate.
        distance (str): Distance measure to use for silhouette score.
    
    Returns:
        Tuple[np.ndarray, Dict[str, float]]: Tuple containing labels and calculated metrics.
    """
    labels = model.fit_predict(embeddings)
    if len(np.unique(labels)) <= 1:
        raise ValueError(f'Only {len(np.unique(labels))} labels are predicted. Increase data size or reduce cluster number.')
    
    metric_funcs = {
        'dbs': davies_bouldin_score,
        'silhouette': lambda x, labels: silhouette_score(x, labels, metric=distance),
        'calinski': calinski_harabasz_score
    }
    
    calculated_metrics = {}
    for metric in metrics:
        if metric in metric_funcs:
            calculated_metrics[metric] = metric_funcs[metric](embeddings, labels)
    if return_model:
        return labels, calculated_metrics, model

    return labels, calculated_metrics


def get_clustering_model_dict():
    model_dict = {
        'kmeans': KMeans(n_init='auto'),
        'affinity_propagation': AffinityPropagation(),
        'mean_shift': MeanShift(),
        'spectral_clustering': SpectralClustering(),
        'agglomerative_clustering': AgglomerativeClustering(),
        'birch': Birch(threshold=0.2),
    }
    return model_dict

def load_clustering_model(model_name: str, model_dict: Dict[str, ClusterMixin] = None) -> ClusterMixin:
    """
    Fetches a clustering model instance by its name from a given dictionary.
    
    Args:
        model_name (str): Name of the model to fetch.
        models (Dict[str, ClusterMixin]): Dictionary mapping model names to model instances.
    
    Returns:
        ClusterMixin: Clustering model instance.
    
    Raises:
        ValueError: If the model name does not exist in the dictionary.
    """
    all_model_dict = get_clustering_model_dict()
    if model_dict is not None:
        all_model_dict.update(model_dict)

    if model_name not in all_model_dict.keys():
        raise ValueError(f"Model {model_name} is not available.")
    return all_model_dict[model_name]

def find_best_algorithm(
    embeddings: np.ndarray,
    model_dict: Dict[str, Any] = None,
    model_names: List[str] = ['kmeans', 'agglomerative_clustering'],
    min_cluster_num: int = 2,
    max_cluster_num: int = 5,
    metrics: List[str] = ['dbs'],
    test_metric: str = 'dbs',
    print_topk: bool = True,
    topk: int = 3,
    result_filepath: str = 'clustering_results.csv',
) -> List[Tuple[str, int, Dict[str, float], Any]]:
    """
    Finds the best clustering algorithm based on specified metrics, using a predefined dictionary of models.
    
    Args:
        embeddings (np.ndarray): Array of embeddings.
        models (Dict[str, ClusterMixin]): Dictionary mapping model names to model instances.
        model_names (List[str]): List of model names to test.
        min_cluster_num (int): Minimum number of clusters.
        max_cluster_num (int): Maximum number of clusters.
        metrics (List[str]): List of metric names to calculate.
        test_metric (str): Metric name to sort results.
        return_topk (bool): Whether to return only the top k results.
        topk (int): Number of top results to return.
    
    Returns:
        List[Tuple[str, int, Dict[str, float], Any]]: List of tuples containing model name, number of clusters, metrics, and the best model.
    """

    if os.path.exists(result_filepath):
        raise ValueError(f'{result_filepath} already exists.')
    if model_dict is None:
        model_dict = get_clustering_model_dict()

    results = []
    
    for model_name in model_names:
        if model_name not in model_dict:
            print(f'{model_name} not included in model_dict')
            continue  # Skip model names that are not in the dictionary
        
        model_base = load_clustering_model(model_name, model_dict) 
        for cluster_num in tqdm(range(min_cluster_num, max_cluster_num + 1)):
            
            model = model_base.set_params(n_clusters=cluster_num) 
            # print(cluster_num, model)
            try:
                _, metrics_results = cluster(embeddings, model, metrics)
                results_dict = {
                    'model_name': model_name,
                    'cluster_num': cluster_num,
                    **metrics_results
                }

                results.append(results_dict)
            except:
                results_dict = {
                    'model_name': model_name,
                    'cluster_num': cluster_num,
                    **{key: float('-inf') for key in metrics}
                }
                results.append(results_dict)


    with open(result_filepath, 'w', newline='') as csvfile:
        fieldnames = ['model_name', 'cluster_num'] + metrics
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result_dict in results:
            # print(result_dict)
            writer.writerow(result_dict)

    print('save results')
    # Sorting results based on the specified test metric.
    results.sort(key=lambda x: x[test_metric] if metric_directions.get(test_metric, True) else -x[test_metric])
    if print_topk:
        pprint(results[:topk])
    return results