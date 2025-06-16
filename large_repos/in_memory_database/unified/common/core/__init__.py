"""
Core functionality for the unified in-memory database library.
"""

from .base import (
    SerializableMixin, TimestampedMixin, MetadataMixin, ConfigurableMixin,
    ThreadSafeMixin, BaseComponent, VersionedMixin, PerformanceTrackingMixin
)
from .utils import (
    generate_id, generate_client_id, generate_deterministic_id,
    validate_type, validate_range, validate_dimensions, validate_non_empty,
    validate_positive, validate_non_negative,
    get_timestamp, format_timestamp, timestamp_to_datetime, datetime_to_timestamp,
    safe_json_serialize, safe_json_deserialize,
    flatten_dict, unflatten_dict, deep_merge, filter_dict,
    camel_to_snake, snake_to_camel,
    hash_object, hash_vector,
    retry_on_exception, batch_process, chunk_list,
    approximately_equal, compare_vectors
)
from .math_ops import (
    dot_product, vector_magnitude, vector_magnitude_squared, normalize_vector,
    vector_add, vector_subtract, vector_scale, vector_mean,
    euclidean_distance, squared_euclidean_distance, manhattan_distance,
    chebyshev_distance, cosine_similarity, cosine_distance, angular_distance,
    mean, median, mode, standard_deviation, variance, percentile, quantile,
    z_score, min_max_normalize, z_score_normalize,
    variable_length_encode, variable_length_decode,
    jaccard_similarity, dice_coefficient, rank_items,
    linear_interpolate, bilinear_interpolate
)
from .exceptions import (
    UnifiedDatabaseError, ValidationError, ConfigurationError, SerializationError,
    VectorError, IndexError, SynchronizationError, ConflictError, SchemaError,
    CompressionError, PowerManagementError, FeatureStoreError, BatchProcessingError,
    TransactionError, NetworkError, PerformanceError,
    handle_exception, create_error_response
)
from .collections import (
    ThreadSafeDict, LRUCache, TimestampedCollection, VersionedContainer,
    CircularBuffer, CountingDict
)
from .performance import (
    PerformanceTracker, MetricsCollector, BenchmarkRunner, ResourceMonitor
)
from .config import (
    ConfigValidator, ProfileManager, SettingsManager,
    create_database_config_validator, create_vector_config_validator,
    create_sync_config_validator
)
from .factory import (
    ComponentFactory, RegistryMixin, SingletonMeta, AbstractFactory,
    ConfigurableFactory, ChainFactory, PluginManager, DependencyInjector,
    register_component, singleton
)

__all__ = [
    # Base classes
    "SerializableMixin", "TimestampedMixin", "MetadataMixin", "ConfigurableMixin",
    "ThreadSafeMixin", "BaseComponent", "VersionedMixin", "PerformanceTrackingMixin",
    
    # Utilities
    "generate_id", "generate_client_id", "generate_deterministic_id",
    "validate_type", "validate_range", "validate_dimensions", "validate_non_empty",
    "validate_positive", "validate_non_negative",
    "get_timestamp", "format_timestamp", "timestamp_to_datetime", "datetime_to_timestamp",
    "safe_json_serialize", "safe_json_deserialize",
    "flatten_dict", "unflatten_dict", "deep_merge", "filter_dict",
    "camel_to_snake", "snake_to_camel",
    "hash_object", "hash_vector",
    "retry_on_exception", "batch_process", "chunk_list",
    "approximately_equal", "compare_vectors",
    
    # Math operations
    "dot_product", "vector_magnitude", "vector_magnitude_squared", "normalize_vector",
    "vector_add", "vector_subtract", "vector_scale", "vector_mean",
    "euclidean_distance", "squared_euclidean_distance", "manhattan_distance",
    "chebyshev_distance", "cosine_similarity", "cosine_distance", "angular_distance",
    "mean", "median", "mode", "standard_deviation", "variance", "percentile", "quantile",
    "z_score", "min_max_normalize", "z_score_normalize",
    "variable_length_encode", "variable_length_decode",
    "jaccard_similarity", "dice_coefficient", "rank_items",
    "linear_interpolate", "bilinear_interpolate",
    
    # Exceptions
    "UnifiedDatabaseError", "ValidationError", "ConfigurationError", "SerializationError",
    "VectorError", "IndexError", "SynchronizationError", "ConflictError", "SchemaError",
    "CompressionError", "PowerManagementError", "FeatureStoreError", "BatchProcessingError",
    "TransactionError", "NetworkError", "PerformanceError",
    "handle_exception", "create_error_response",
    
    # Collections
    "ThreadSafeDict", "LRUCache", "TimestampedCollection", "VersionedContainer",
    "CircularBuffer", "CountingDict",
    
    # Performance
    "PerformanceTracker", "MetricsCollector", "BenchmarkRunner", "ResourceMonitor",
    
    # Configuration
    "ConfigValidator", "ProfileManager", "SettingsManager",
    "create_database_config_validator", "create_vector_config_validator",
    "create_sync_config_validator",
    
    # Factory
    "ComponentFactory", "RegistryMixin", "SingletonMeta", "AbstractFactory",
    "ConfigurableFactory", "ChainFactory", "PluginManager", "DependencyInjector",
    "register_component", "singleton"
]
