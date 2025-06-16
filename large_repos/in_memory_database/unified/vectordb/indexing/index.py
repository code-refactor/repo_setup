"""
Vector index implementation for efficient similarity searches.

This module provides a base vector index for storing and retrieving
high-dimensional vectors with optimized distance calculations.
"""

import math
import heapq
from typing import List, Dict, Tuple, Callable, Optional, Set, Any, Iterator, Union
import random

from common.core import (
    BaseComponent, PerformanceTrackingMixin, 
    generate_id, get_timestamp,
    ThreadSafeDict, validate_positive
)
from vectordb.core.vector import Vector
from vectordb.core.distance import get_distance_function, euclidean_distance


class VectorIndex(BaseComponent, PerformanceTrackingMixin):
    """
    Base vector index for efficient similarity searches.
    
    This class provides a simple but efficient index for vectors
    with support for nearest neighbor queries using various distance metrics.
    """
    
    def __init__(self, distance_metric: str = "euclidean", **config):
        """
        Initialize a vector index.
        
        Args:
            distance_metric: The distance metric to use for similarity calculations.
                             Supported metrics: euclidean, squared_euclidean, manhattan, 
                             cosine, angular, chebyshev.
                             
        Raises:
            ValueError: If an unsupported distance metric is provided.
        """
        super().__init__(**config)
        
        # Replace basic dict with ThreadSafeDict for thread safety
        self._vectors = ThreadSafeDict()
        self._metadata = ThreadSafeDict()
        
        # Use common distance function getter
        self._distance_function = get_distance_function(distance_metric)
        self._distance_metric = distance_metric
        
    def __len__(self) -> int:
        """Return the number of vectors in the index."""
        return len(self._vectors)
        
    def __contains__(self, id: str) -> bool:
        """Check if a vector with the given ID exists in the index."""
        return id in self._vectors
        
    def __iter__(self) -> Iterator[Vector]:
        """Iterate over all vectors in the index."""
        return iter(self._vectors.values())
    
    @property
    def ids(self) -> List[str]:
        """Get a list of all vector IDs in the index."""
        return list(self._vectors.keys())
    
    @property
    def last_modified(self) -> float:
        """Get the timestamp of the last modification to the index."""
        return super().last_modified  # From TimestampedMixin
    
    @property
    def distance_metric(self) -> str:
        """Get the distance metric used by this index."""
        return self._distance_metric
        
    def add(self, vector: Vector, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Add a vector to the index.
        
        Args:
            vector: The vector to add
            metadata: Optional metadata to associate with the vector
            
        Returns:
            The ID of the added vector
            
        Raises:
            ValueError: If the vector does not have an ID and cannot be added
        """
        start_time = get_timestamp()
        try:
            # Generate an ID if the vector doesn't have one
            vector_id = vector.id
            if vector_id is None:
                vector_id = generate_id()  # Use common ID generation
                # Create a new vector with the generated ID
                vector = Vector(vector.values, vector_id)
        
            self._vectors[vector_id] = vector
            
            if metadata is not None:
                self._metadata[vector_id] = metadata
            elif vector_id not in self._metadata:
                # Initialize empty metadata if not provided
                self._metadata[vector_id] = {}
                
            self._touch()  # From TimestampedMixin
            return vector_id
        finally:
            # Track performance
            duration = get_timestamp() - start_time
            self.track_operation("add_vector", duration)
    
    def add_batch(self, vectors: List[Vector], metadatas: Optional[List[Dict[str, Any]]] = None) -> List[str]:
        """
        Add multiple vectors to the index in a batch.
        
        Args:
            vectors: List of vectors to add
            metadatas: Optional list of metadata dictionaries, one per vector
            
        Returns:
            List of vector IDs that were added
            
        Raises:
            ValueError: If the lengths of vectors and metadatas don't match
        """
        if metadatas is not None and len(vectors) != len(metadatas):
            raise ValueError("Number of vectors and metadata dictionaries must match")
            
        ids = []
        for i, vector in enumerate(vectors):
            metadata = metadatas[i] if metadatas is not None else None
            ids.append(self.add(vector, metadata))
            
        return ids
    
    def get(self, id: str) -> Optional[Vector]:
        """
        Retrieve a vector by its ID.
        
        Args:
            id: The ID of the vector to retrieve
            
        Returns:
            The vector if found, None otherwise
        """
        return self._vectors.get(id)
    
    def get_metadata(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve the metadata associated with a vector.
        
        Args:
            id: The ID of the vector
            
        Returns:
            The metadata dictionary if the vector exists, None otherwise
        """
        return self._metadata.get(id)
    
    def update_metadata(self, id: str, metadata: Dict[str, Any]) -> bool:
        """
        Update the metadata for a vector.
        
        Args:
            id: The ID of the vector
            metadata: The new metadata dictionary
            
        Returns:
            True if the metadata was updated, False if the vector was not found
        """
        if id not in self._vectors:
            return False
            
        self._metadata[id] = metadata
        self._touch()  # From TimestampedMixin
        return True
    
    def remove(self, id: str) -> bool:
        """
        Remove a vector from the index.
        
        Args:
            id: The ID of the vector to remove
            
        Returns:
            True if the vector was removed, False if it was not found
        """
        if id not in self._vectors:
            return False
            
        del self._vectors[id]
        if id in self._metadata:
            del self._metadata[id]
            
        self._touch()  # From TimestampedMixin
        return True
    
    def remove_batch(self, ids: List[str]) -> int:
        """
        Remove multiple vectors from the index.
        
        Args:
            ids: List of vector IDs to remove
            
        Returns:
            Number of vectors actually removed
        """
        removed_count = 0
        for id in ids:
            if self.remove(id):
                removed_count += 1
                
        return removed_count
    
    def clear(self) -> None:
        """Remove all vectors from the index."""
        self._vectors.clear()
        self._metadata.clear()
        self._touch()  # From TimestampedMixin
    
    def distance(self, v1: Union[str, Vector], v2: Union[str, Vector]) -> float:
        """
        Calculate the distance between two vectors.
        
        Args:
            v1: Either a vector ID or a Vector object
            v2: Either a vector ID or a Vector object
            
        Returns:
            The distance between the vectors
            
        Raises:
            ValueError: If either vector ID is not found or vectors have different dimensions
        """
        # Get actual vector objects if IDs were provided
        vec1 = self._get_vector_object(v1)
        vec2 = self._get_vector_object(v2)
        
        return self._distance_function(vec1, vec2)
    
    def nearest(self, query: Union[str, Vector], k: int = 1, filter_fn: Optional[Callable[[str, Dict[str, Any]], bool]] = None) -> List[Tuple[str, float]]:
        """
        Find the k nearest vectors to the query vector.
        
        Args:
            query: Query vector or vector ID
            k: Number of nearest neighbors to return
            filter_fn: Optional function to filter vectors based on ID and metadata
            
        Returns:
            List of (id, distance) tuples for the nearest vectors, sorted by distance
            
        Raises:
            ValueError: If the query vector ID is not found
        """
        if k < 1:
            raise ValueError("k must be at least 1")
            
        if len(self._vectors) == 0:
            return []
            
        # Ensure we have a Vector object
        query_vector = self._get_vector_object(query)
        
        # Calculate distances and filter results
        distances = []
        for vec_id, vector in self._vectors.items():
            # Skip if the filter excludes this vector
            if filter_fn is not None and not filter_fn(vec_id, self._metadata.get(vec_id, {})):
                continue
                
            # Skip if this is the query vector itself
            if isinstance(query, str) and query == vec_id:
                continue
                
            dist = self._distance_function(query_vector, vector)
            distances.append((vec_id, dist))
        
        # Sort by distance and return the k nearest
        return sorted(distances, key=lambda x: x[1])[:k]
    
    def nearest_with_metadata(self, query: Union[str, Vector], k: int = 1, filter_fn: Optional[Callable[[str, Dict[str, Any]], bool]] = None) -> List[Tuple[str, float, Dict[str, Any]]]:
        """
        Find the k nearest vectors to the query vector, including their metadata.
        
        Args:
            query: Query vector or vector ID
            k: Number of nearest neighbors to return
            filter_fn: Optional function to filter vectors based on ID and metadata
            
        Returns:
            List of (id, distance, metadata) tuples for the nearest vectors, sorted by distance
        """
        nearest_results = self.nearest(query, k, filter_fn)
        
        # Add metadata to each result
        return [(id, dist, self._metadata.get(id, {})) for id, dist in nearest_results]
    
    def _get_vector_object(self, vector_or_id: Union[str, Vector]) -> Vector:
        """
        Get a Vector object from either a vector or an ID.
        
        Args:
            vector_or_id: Either a Vector object or a vector ID
            
        Returns:
            The Vector object
            
        Raises:
            ValueError: If the ID doesn't exist in the index
        """
        if isinstance(vector_or_id, str):
            vector = self.get(vector_or_id)
            if vector is None:
                raise ValueError(f"Vector with ID '{vector_or_id}' not found in the index")
            return vector
        return vector_or_id
    
    def sample(self, n: int, seed: Optional[int] = None) -> List[Vector]:
        """
        Sample n random vectors from the index.
        
        Args:
            n: Number of vectors to sample
            seed: Optional random seed for reproducibility
            
        Returns:
            List of sampled Vector objects
            
        Raises:
            ValueError: If n is greater than the number of vectors in the index
        """
        if n > len(self._vectors):
            raise ValueError(f"Cannot sample {n} vectors from an index of size {len(self._vectors)}")
            
        if seed is not None:
            random.seed(seed)
            
        sampled_ids = random.sample(list(self._vectors.keys()), n)
        return [self._vectors[id] for id in sampled_ids]