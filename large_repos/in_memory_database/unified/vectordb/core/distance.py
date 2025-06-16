"""
Distance metrics for vector comparisons.

This module provides various distance and similarity measures
for comparing vectors, optimized for machine learning applications.
"""

from typing import Callable, Union, List, Tuple
from vectordb.core.vector import Vector
from common.core import (
    validate_dimensions,
    euclidean_distance as core_euclidean_distance,
    squared_euclidean_distance as core_squared_euclidean_distance,
    manhattan_distance as core_manhattan_distance,
    chebyshev_distance as core_chebyshev_distance,
    cosine_similarity as core_cosine_similarity,
    cosine_distance as core_cosine_distance,
    angular_distance as core_angular_distance,
    RegistryMixin
)


def euclidean_distance(v1: Vector, v2: Vector) -> float:
    """
    Calculate the Euclidean (L2) distance between two vectors.
    
    Args:
        v1: First vector
        v2: Second vector
        
    Returns:
        The Euclidean distance between the vectors
        
    Raises:
        ValueError: If the vectors have different dimensions
    """
    validate_dimensions(list(v1.values), list(v2.values), "Euclidean distance")
    return core_euclidean_distance(list(v1.values), list(v2.values))


def squared_euclidean_distance(v1: Vector, v2: Vector) -> float:
    """
    Calculate the squared Euclidean distance between two vectors.
    
    This is faster than euclidean_distance when only comparing distances
    (avoids the square root operation).
    
    Args:
        v1: First vector
        v2: Second vector
        
    Returns:
        The squared Euclidean distance between the vectors
        
    Raises:
        ValueError: If the vectors have different dimensions
    """
    validate_dimensions(list(v1.values), list(v2.values), "squared Euclidean distance")
    return core_squared_euclidean_distance(list(v1.values), list(v2.values))


def manhattan_distance(v1: Vector, v2: Vector) -> float:
    """
    Calculate the Manhattan (L1) distance between two vectors.
    
    Args:
        v1: First vector
        v2: Second vector
        
    Returns:
        The Manhattan distance between the vectors
        
    Raises:
        ValueError: If the vectors have different dimensions
    """
    validate_dimensions(list(v1.values), list(v2.values), "Manhattan distance")
    return core_manhattan_distance(list(v1.values), list(v2.values))


def cosine_distance(v1: Vector, v2: Vector) -> float:
    """
    Calculate the cosine distance between two vectors.
    
    The cosine distance is 1 minus the cosine similarity, resulting in a value
    between 0 (identical direction) and 2 (opposite direction).
    
    Args:
        v1: First vector
        v2: Second vector
        
    Returns:
        The cosine distance between the vectors
        
    Raises:
        ValueError: If the vectors have different dimensions or if either has zero magnitude
    """
    validate_dimensions(list(v1.values), list(v2.values), "cosine distance")
    
    # Check for zero magnitude (preserve original behavior)
    mag1 = v1.magnitude()
    mag2 = v2.magnitude()
    if mag1 == 0 or mag2 == 0:
        raise ValueError("Cannot calculate cosine distance for zero magnitude vectors")
    
    return core_cosine_distance(list(v1.values), list(v2.values))


def cosine_similarity(v1: Vector, v2: Vector) -> float:
    """
    Calculate the cosine similarity between two vectors.
    
    The cosine similarity measures the cosine of the angle between two vectors,
    resulting in a value between -1 (opposite) and 1 (identical direction),
    with 0 indicating orthogonality.
    
    Args:
        v1: First vector
        v2: Second vector
        
    Returns:
        The cosine similarity between the vectors
        
    Raises:
        ValueError: If the vectors have different dimensions or if either has zero magnitude
    """
    validate_dimensions(list(v1.values), list(v2.values), "cosine similarity")
    
    # Check for zero magnitude (preserve original behavior)
    mag1 = v1.magnitude()
    mag2 = v2.magnitude()
    if mag1 == 0 or mag2 == 0:
        raise ValueError("Cannot calculate cosine similarity for zero magnitude vectors")
    
    return core_cosine_similarity(list(v1.values), list(v2.values))


def angular_distance(v1: Vector, v2: Vector) -> float:
    """
    Calculate the angular distance between two vectors in radians.
    
    Args:
        v1: First vector
        v2: Second vector
        
    Returns:
        The angular distance between the vectors in radians [0, π]
        
    Raises:
        ValueError: If the vectors have different dimensions or if either has zero magnitude
    """
    validate_dimensions(list(v1.values), list(v2.values), "angular distance")
    
    # Check for zero magnitude (preserve original behavior)
    mag1 = v1.magnitude()
    mag2 = v2.magnitude()
    if mag1 == 0 or mag2 == 0:
        raise ValueError("Cannot calculate angular distance for zero magnitude vectors")
    
    return core_angular_distance(list(v1.values), list(v2.values))


def chebyshev_distance(v1: Vector, v2: Vector) -> float:
    """
    Calculate the Chebyshev (L∞) distance between two vectors.
    
    The Chebyshev distance is the maximum absolute difference between 
    any components of the vectors.
    
    Args:
        v1: First vector
        v2: Second vector
        
    Returns:
        The Chebyshev distance between the vectors
        
    Raises:
        ValueError: If the vectors have different dimensions
    """
    validate_dimensions(list(v1.values), list(v2.values), "Chebyshev distance")
    return core_chebyshev_distance(list(v1.values), list(v2.values))


class DistanceMetricRegistry(RegistryMixin):
    """Registry for distance metric functions."""
    
    def __init__(self):
        super().__init__()
        # Register default distance metrics
        self.register_component("euclidean", euclidean_distance)
        self.register_component("squared_euclidean", squared_euclidean_distance)
        self.register_component("manhattan", manhattan_distance)
        self.register_component("cosine", cosine_distance)
        self.register_component("angular", angular_distance)
        self.register_component("chebyshev", chebyshev_distance)
    
    def get_distance_function(self, metric: str) -> Callable[[Vector, Vector], float]:
        """
        Get the distance function by name.
        
        Args:
            metric: Name of the distance metric
            
        Returns:
            The corresponding distance function
            
        Raises:
            ValueError: If the metric name is not recognized
        """
        if not self.has_component(metric.lower()):
            available_metrics = ", ".join(self.list_components())
            raise ValueError(f"Unknown distance metric: {metric}. Available: {available_metrics}")
        
        return self.get_component(metric.lower())


# Global instance for backward compatibility
_distance_registry = DistanceMetricRegistry()

# Legacy mapping for backward compatibility
DISTANCE_METRICS = {name: _distance_registry.get_component(name) for name in _distance_registry.list_components()}


def get_distance_function(metric: str) -> Callable[[Vector, Vector], float]:
    """
    Get the distance function by name.
    
    Args:
        metric: Name of the distance metric
        
    Returns:
        The corresponding distance function
        
    Raises:
        ValueError: If the metric name is not recognized
    """
    return _distance_registry.get_distance_function(metric)


def register_distance_metric(name: str, function: Callable[[Vector, Vector], float]):
    """
    Register a custom distance metric.
    
    Args:
        name: Name of the distance metric
        function: Distance function that takes two vectors and returns a float
    """
    _distance_registry.register_component(name, function)