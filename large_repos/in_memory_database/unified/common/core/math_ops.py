"""
Mathematical operations for the unified in-memory database library.

This module provides common mathematical functions that can be shared across both
vectordb and syncdb implementations.
"""

import math
import statistics
from typing import List, Tuple, Union, Optional, Callable
from .utils import validate_dimensions, validate_non_empty, validate_positive


# Vector Operations
def dot_product(v1: List[float], v2: List[float]) -> float:
    """Calculate dot product of two vectors."""
    validate_dimensions(v1, v2, "dot product")
    return sum(a * b for a, b in zip(v1, v2))


def vector_magnitude(v: List[float]) -> float:
    """Calculate magnitude (L2 norm) of a vector."""
    validate_non_empty(v, "vector")
    return math.sqrt(sum(x * x for x in v))


def vector_magnitude_squared(v: List[float]) -> float:
    """Calculate squared magnitude of a vector (more efficient than magnitude)."""
    validate_non_empty(v, "vector")
    return sum(x * x for x in v)


def normalize_vector(v: List[float]) -> List[float]:
    """Normalize vector to unit length."""
    validate_non_empty(v, "vector")
    magnitude = vector_magnitude(v)
    if magnitude == 0:
        raise ValueError("Cannot normalize zero vector")
    return [x / magnitude for x in v]


def vector_add(v1: List[float], v2: List[float]) -> List[float]:
    """Add two vectors."""
    validate_dimensions(v1, v2, "vector addition")
    return [a + b for a, b in zip(v1, v2)]


def vector_subtract(v1: List[float], v2: List[float]) -> List[float]:
    """Subtract second vector from first vector."""
    validate_dimensions(v1, v2, "vector subtraction")
    return [a - b for a, b in zip(v1, v2)]


def vector_scale(v: List[float], scalar: float) -> List[float]:
    """Scale vector by scalar value."""
    validate_non_empty(v, "vector")
    return [x * scalar for x in v]


def vector_mean(vectors: List[List[float]]) -> List[float]:
    """Calculate mean of multiple vectors."""
    validate_non_empty(vectors, "vectors")
    if not vectors:
        raise ValueError("Cannot calculate mean of empty vector list")
    
    # Validate all vectors have same dimension
    dim = len(vectors[0])
    for i, v in enumerate(vectors[1:], 1):
        if len(v) != dim:
            raise ValueError(f"Vector {i} has dimension {len(v)}, expected {dim}")
    
    return [sum(v[i] for v in vectors) / len(vectors) for i in range(dim)]


# Distance Functions
def euclidean_distance(v1: List[float], v2: List[float]) -> float:
    """Calculate Euclidean distance between two vectors."""
    validate_dimensions(v1, v2, "Euclidean distance")
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


def squared_euclidean_distance(v1: List[float], v2: List[float]) -> float:
    """Calculate squared Euclidean distance (more efficient than Euclidean)."""
    validate_dimensions(v1, v2, "squared Euclidean distance")
    return sum((a - b) ** 2 for a, b in zip(v1, v2))


def manhattan_distance(v1: List[float], v2: List[float]) -> float:
    """Calculate Manhattan (L1) distance between two vectors."""
    validate_dimensions(v1, v2, "Manhattan distance")
    return sum(abs(a - b) for a, b in zip(v1, v2))


def chebyshev_distance(v1: List[float], v2: List[float]) -> float:
    """Calculate Chebyshev (L∞) distance between two vectors."""
    validate_dimensions(v1, v2, "Chebyshev distance")
    return max(abs(a - b) for a, b in zip(v1, v2))


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    validate_dimensions(v1, v2, "cosine similarity")
    
    dot_prod = dot_product(v1, v2)
    mag1 = vector_magnitude(v1)
    mag2 = vector_magnitude(v2)
    
    if mag1 == 0 or mag2 == 0:
        return 0.0
    
    return dot_prod / (mag1 * mag2)


def cosine_distance(v1: List[float], v2: List[float]) -> float:
    """Calculate cosine distance (1 - cosine similarity)."""
    return 1.0 - cosine_similarity(v1, v2)


def angular_distance(v1: List[float], v2: List[float]) -> float:
    """Calculate angular distance between two vectors."""
    similarity = cosine_similarity(v1, v2)
    # Clamp to avoid numerical issues with acos
    similarity = max(-1.0, min(1.0, similarity))
    return math.acos(similarity)


# Statistical Functions
def mean(values: List[float]) -> float:
    """Calculate arithmetic mean of values."""
    validate_non_empty(values, "values")
    return sum(values) / len(values)


def median(values: List[float]) -> float:
    """Calculate median of values."""
    validate_non_empty(values, "values")
    return statistics.median(values)


def mode(values: List[float]) -> float:
    """Calculate mode of values."""
    validate_non_empty(values, "values")
    return statistics.mode(values)


def standard_deviation(values: List[float], population: bool = False) -> float:
    """Calculate standard deviation of values."""
    validate_non_empty(values, "values")
    if population:
        return statistics.pstdev(values)
    else:
        return statistics.stdev(values)


def variance(values: List[float], population: bool = False) -> float:
    """Calculate variance of values."""
    validate_non_empty(values, "values")
    if population:
        return statistics.pvariance(values)
    else:
        return statistics.variance(values)


def percentile(values: List[float], p: float) -> float:
    """Calculate percentile of values."""
    validate_non_empty(values, "values")
    if not (0 <= p <= 100):
        raise ValueError("Percentile must be between 0 and 100")
    
    sorted_values = sorted(values)
    k = (len(sorted_values) - 1) * (p / 100)
    f = math.floor(k)
    c = math.ceil(k)
    
    if f == c:
        return sorted_values[int(k)]
    
    d0 = sorted_values[int(f)] * (c - k)
    d1 = sorted_values[int(c)] * (k - f)
    return d0 + d1


def quantile(values: List[float], q: float) -> float:
    """Calculate quantile of values."""
    if not (0 <= q <= 1):
        raise ValueError("Quantile must be between 0 and 1")
    return percentile(values, q * 100)


def z_score(value: float, values: List[float]) -> float:
    """Calculate z-score of value relative to values."""
    validate_non_empty(values, "values")
    mu = mean(values)
    sigma = standard_deviation(values)
    if sigma == 0:
        return 0.0
    return (value - mu) / sigma


def min_max_normalize(values: List[float], min_val: float = 0.0, 
                     max_val: float = 1.0) -> List[float]:
    """Normalize values to specified range using min-max scaling."""
    validate_non_empty(values, "values")
    if min_val >= max_val:
        raise ValueError("min_val must be less than max_val")
    
    data_min = min(values)
    data_max = max(values)
    
    if data_min == data_max:
        # All values are the same
        return [(min_val + max_val) / 2] * len(values)
    
    scale = (max_val - min_val) / (data_max - data_min)
    return [min_val + (x - data_min) * scale for x in values]


def z_score_normalize(values: List[float]) -> List[float]:
    """Normalize values using z-score normalization."""
    validate_non_empty(values, "values")
    mu = mean(values)
    sigma = standard_deviation(values)
    
    if sigma == 0:
        return [0.0] * len(values)
    
    return [(x - mu) / sigma for x in values]


# Encoding/Compression Utilities
def variable_length_encode(value: int) -> bytes:
    """Encode integer using variable-length encoding."""
    if value < 0:
        raise ValueError("Value must be non-negative")
    
    result = []
    while value >= 128:
        result.append((value & 0x7F) | 0x80)
        value >>= 7
    result.append(value & 0x7F)
    return bytes(result)


def variable_length_decode(data: bytes) -> Tuple[int, int]:
    """Decode variable-length encoded integer. Returns (value, bytes_consumed)."""
    value = 0
    shift = 0
    bytes_consumed = 0
    
    for byte in data:
        bytes_consumed += 1
        value |= (byte & 0x7F) << shift
        if (byte & 0x80) == 0:
            break
        shift += 7
        if shift >= 64:
            raise ValueError("Variable length integer too large")
    
    return value, bytes_consumed


# Similarity and Ranking Functions
def jaccard_similarity(set1: set, set2: set) -> float:
    """Calculate Jaccard similarity between two sets."""
    if not set1 and not set2:
        return 1.0
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    if union == 0:
        return 0.0
    
    return intersection / union


def dice_coefficient(set1: set, set2: set) -> float:
    """Calculate Dice coefficient between two sets."""
    if not set1 and not set2:
        return 1.0
    
    intersection = len(set1 & set2)
    total = len(set1) + len(set2)
    
    if total == 0:
        return 0.0
    
    return 2 * intersection / total


def rank_items(items: List[Tuple[any, float]], ascending: bool = False) -> List[Tuple[any, float, int]]:
    """Rank items by score. Returns list of (item, score, rank) tuples."""
    sorted_items = sorted(items, key=lambda x: x[1], reverse=not ascending)
    return [(item, score, rank + 1) for rank, (item, score) in enumerate(sorted_items)]


# Interpolation Functions
def linear_interpolate(x: float, x1: float, y1: float, x2: float, y2: float) -> float:
    """Linear interpolation between two points."""
    if x1 == x2:
        return y1
    return y1 + (y2 - y1) * (x - x1) / (x2 - x1)


def bilinear_interpolate(x: float, y: float, x1: float, y1: float, x2: float, y2: float,
                        f11: float, f12: float, f21: float, f22: float) -> float:
    """Bilinear interpolation between four points."""
    if x1 == x2 and y1 == y2:
        return f11
    elif x1 == x2:
        return linear_interpolate(y, y1, f11, y2, f12)
    elif y1 == y2:
        return linear_interpolate(x, x1, f11, x2, f21)
    
    denominator = (x2 - x1) * (y2 - y1)
    return (f11 * (x2 - x) * (y2 - y) +
            f21 * (x - x1) * (y2 - y) +
            f12 * (x2 - x) * (y - y1) +
            f22 * (x - x1) * (y - y1)) / denominator