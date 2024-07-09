from abc import ABC, abstractmethod

from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec, Doc2Vec
from sentence_transformers import SentenceTransformer
import logging

import numpy as np
import pandas as pd
import pickle
import os
from pathlib import Path
from typing import Union, List, Any

from slenps.utils import check_memory_usage

# Initialize logging
logging.basicConfig(level=logging.INFO)

class EmbeddingModelRegistry(ABC):
    """All embedding model should implement this base class"""

    # Registry to store all embedding models
    _registry = {}

    def __init__(self):
        self.model = None

    @abstractmethod
    def encode(self, documents):
        """Method to encode documents, to be implemented by all subclasses."""
        pass

    @classmethod
    def register_embedding_model(cls, name, embedding_model): 
        cls._registry[name] = embedding_model

    @classmethod
    def load_embedding_model(cls, name):
        embedding_model = cls._registry.get(name)
        if embedding_model is not None:
            return embedding_model
        else:
            raise ValueError(f"No embedding model found with name: {name}. \nIf model is from huggingface, specify model_name and mode as 'huggingface', or set model_name as 'tfidf', 'word2vec' or 'doc2vec'")


class TfidfEM(EmbeddingModelRegistry):
    def __init__(self, **kwargs):
        super().__init__()
        self.model = TfidfVectorizer(**kwargs)
        logging.info("TfidfEM initialized with specified parameters.")

    def encode(self, documents):
        result = self.model.fit_transform(documents)
        logging.info(f"Output dimensions: {result.shape[1]}")
        return result.toarray()

class Word2VecEM(EmbeddingModelRegistry):
    def __init__(self, size=100, **kwargs):
        super().__init__()
        self.size = size
        self.model = Word2Vec(vector_size=size, min_count=1, **kwargs)
        logging.info(f"Word2Vec model initialized with {size} dimensions")

    def encode(self, documents):
        self.model.build_vocab(documents)
        self.model.train(documents, total_examples=self.model.corpus_count, epochs=self.model.epochs)
        logging.info(f'Output dimensions: {self.size}')
        return np.array(
            [np.mean([self.model.wv[word] for word in doc if word in self.model.wv], axis=0) for doc in documents]
        )

class Doc2VecEM(EmbeddingModelRegistry):
    def __init__(self, size=100, **kwargs):
        super().__init__()
        self.size = size
        self.model = Doc2Vec(vector_size=size, min_count=1, epochs=10, **kwargs)
        logging.info(f"Doc2Vec model initialized with {size} dimensions")

    def encode(self, documents):
        self.model.build_vocab(documents)
        self.model.train(documents, total_examples=self.model.corpus_count, epochs=self.model.epochs)
        return np.array([self.model.infer_vector(doc.words) for doc in documents])

class SbertEM(EmbeddingModelRegistry):
    def __init__(self, model_name, **kwargs):
        super().__init__()
        self.model = SentenceTransformer(model_name, **kwargs)
        logging.info(f'Sbert model initialized with {self.model.get_sentence_embedding_dimension()} dimensions')

    def encode(self, documents):
        embeddings = self.model.encode(documents)
        logging.info(f'Output dimensions: {len(embeddings[0])}')
        return embeddings

def register_embedding_models():
    EmbeddingModelRegistry.register_embedding_model('tfidf', TfidfEM)
    EmbeddingModelRegistry.register_embedding_model('huggingface', SbertEM)
    EmbeddingModelRegistry.register_embedding_model('doc2vec', Doc2VecEM)
    EmbeddingModelRegistry.register_embedding_model('word2vec', Word2VecEM)

