from slenps.eclusters.embedding_models import register_embedding_models, EmbeddingModelRegistry
from slenps.utils import check_memory_usage

import numpy as np
import pandas as pd
import pickle
import os

from pathlib import Path
from typing import Union, List, Any, Tuple
from abc import ABC, abstractmethod
import logging

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import umap

# Initialize logging
logging.basicConfig(level=logging.INFO)

register_embedding_models()

def load_embedding_model(model_name: str = 'all-MiniLM-L6-v2', mode: str = None, **kwargs):
    """
    Load a model based on the mode and model name.

    Args:
    model_name (str): Name of the model to load.
    mode (str): Type of model to load ('huggingface', 'tfidf', 'word2vec', 'doc2vec').

    Returns:
    Model with an .encode method or equivalent functionality.
    """
    if mode == 'huggingface':
        return EmbeddingModelRegistry.load_embedding_model(mode)(model_name, **kwargs)
    else:
        return EmbeddingModelRegistry.load_embedding_model(model_name)(**kwargs)

def embed_and_save(
    model, documents: Union[np.ndarray, pd.Series, list], 
    output_path: Union[Path, str],
):
    """
    Embeds documents using the embedding model and saves the embeddings along with the documents into a pickle file.

    Args:
    model (EmbeddingModelRegistry): The embedding model to use.
    documents (Union[np.ndarray, pd.Series, list]): The documents to be embedded.
    pickle_filepath (Union[Path, str]): Path where the pickle file will be stored.
    
    Raises:
    ValueError: If the output file already exists to prevent overwriting of data.
    """
    if not isinstance(documents, np.ndarray):
        documents = np.array(documents)
    documents = np.unique(documents)

    embeddings = model.encode(documents)

    if os.path.exists(output_path):
        raise ValueError(f"File already exists at {output_path}")

    with open(output_path, 'wb') as file:
        pickle.dump((embeddings, documents), file)
        logging.info(f"embeddings and documents saved to {output_path}")


def get_data_from_paths(filepaths: List[Union[Path, str]]):
    embeddings_list = []
    documents_list = []

    for filepath in filepaths:

        if not os.path.exists(filepath):
            raise ValueError(f'No file named {filepath}!')

        with open(filepath, 'rb') as file:
            obj = pickle.load(file)

        embeddings_list.append(obj[0])
        documents_list.append(obj[1])

    concatenated_embeddings = np.vstack(embeddings_list) if embeddings_list else np.array([])
    concatenated_documents = np.concatenate(documents_list) if documents_list else np.array([])

    check_memory_usage(concatenated_documents, concatenated_embeddings)

    return concatenated_embeddings, concatenated_documents

def sample(embeddings: np.ndarray, documents: np.ndarray, percent: float = 0.5) -> Tuple[np.ndarray, np.ndarray]:
    """
    Randomly samples a percentage of embeddings and documents.
    
    Args:
        embeddings (np.ndarray): Array of embeddings.
        documents (np.ndarray): Array of documents.
        percent (float): Fraction of the data to sample (between 0 and 1).
    
    Returns:
        Tuple[np.ndarray, np.ndarray]: Tuple containing sampled embeddings and documents.
    
    Raises:
        ValueError: If 'percent' is not within the range (0, 1).
    """
    if not (0 < percent < 1):
        raise ValueError('Percent must be between 0 and 1')
    
    sampled_embeddings, _, sampled_documents, _ = train_test_split(
        embeddings, documents, train_size=percent, random_state=42
    )
    
    return sampled_embeddings, sampled_documents



def reduce_dimension(embeddings: np.ndarray, model_name: str = 'pca', n_dim: int = 2) -> np.ndarray:
    """
    Reduces the dimensionality of embeddings using PCA or UMAP.
    
    Args:
        embeddings (np.ndarray): Array of embeddings.
        model_name (str): Dimensionality reduction model to use ('pca' or 'umap').
        n_dim (int): Number of dimensions to reduce to.
    
    Returns:
        np.ndarray: Array of reduced embeddings.
    """
    if model_name == 'pca':
        embeddings_standardized = StandardScaler().fit_transform(embeddings)
        model = PCA(n_components=n_dim)
        embeddings_reduced = model.fit_transform(embeddings_standardized)
    elif model_name == 'umap':
        model = umap.UMAP(n_components=n_dim)
        embeddings_reduced = model.fit_transform(embeddings)
    else:
        raise ValueError("Model name must be 'pca' or 'umap'")
    return embeddings_reduced

