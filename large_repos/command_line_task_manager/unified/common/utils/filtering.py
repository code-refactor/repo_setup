"""Filtering and query utilities for the unified command line task manager."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union
from uuid import UUID

from ..core.models import BaseEntity


class FilterOperator(str, Enum):
    """Operators for filtering."""
    
    EQUALS = "eq"
    NOT_EQUALS = "ne"
    GREATER_THAN = "gt"
    GREATER_EQUAL = "gte"
    LESS_THAN = "lt"
    LESS_EQUAL = "lte"
    IN = "in"
    NOT_IN = "not_in"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"
    MATCHES_REGEX = "regex"


class SortOrder(str, Enum):
    """Sort order options."""
    
    ASC = "asc"
    DESC = "desc"


class SortOptions:
    """Sorting configuration."""
    
    def __init__(self, field: str, order: SortOrder = SortOrder.ASC):
        self.field = field
        self.order = order
    
    def __repr__(self) -> str:
        return f"SortOptions(field='{self.field}', order='{self.order.value}')"


class FilterCondition:
    """Represents a single filter condition."""
    
    def __init__(self, field: str, operator: FilterOperator, value: Any):
        self.field = field
        self.operator = operator
        self.value = value
    
    def matches(self, entity: BaseEntity) -> bool:
        """Check if an entity matches this filter condition."""
        if not hasattr(entity, self.field):
            return False
        
        field_value = getattr(entity, self.field)
        
        return self._evaluate_condition(field_value, self.operator, self.value)
    
    def _evaluate_condition(self, field_value: Any, operator: FilterOperator, filter_value: Any) -> bool:
        """Evaluate a single condition."""
        try:
            if operator == FilterOperator.EQUALS:
                return field_value == filter_value
            
            elif operator == FilterOperator.NOT_EQUALS:
                return field_value != filter_value
            
            elif operator == FilterOperator.GREATER_THAN:
                return field_value > filter_value
            
            elif operator == FilterOperator.GREATER_EQUAL:
                return field_value >= filter_value
            
            elif operator == FilterOperator.LESS_THAN:
                return field_value < filter_value
            
            elif operator == FilterOperator.LESS_EQUAL:
                return field_value <= filter_value
            
            elif operator == FilterOperator.IN:
                if not isinstance(filter_value, (list, set, tuple)):
                    return False
                return field_value in filter_value
            
            elif operator == FilterOperator.NOT_IN:
                if not isinstance(filter_value, (list, set, tuple)):
                    return True
                return field_value not in filter_value
            
            elif operator == FilterOperator.CONTAINS:
                if isinstance(field_value, str) and isinstance(filter_value, str):
                    return filter_value.lower() in field_value.lower()
                elif isinstance(field_value, (list, set)):
                    return filter_value in field_value
                elif isinstance(field_value, (list, set)) and isinstance(filter_value, (list, set)):
                    # Check if any filter values are in field values
                    return bool(set(filter_value).intersection(set(field_value)))
                return False
            
            elif operator == FilterOperator.NOT_CONTAINS:
                return not self._evaluate_condition(field_value, FilterOperator.CONTAINS, filter_value)
            
            elif operator == FilterOperator.STARTS_WITH:
                if isinstance(field_value, str) and isinstance(filter_value, str):
                    return field_value.lower().startswith(filter_value.lower())
                return False
            
            elif operator == FilterOperator.ENDS_WITH:
                if isinstance(field_value, str) and isinstance(filter_value, str):
                    return field_value.lower().endswith(filter_value.lower())
                return False
            
            elif operator == FilterOperator.IS_NULL:
                return field_value is None
            
            elif operator == FilterOperator.IS_NOT_NULL:
                return field_value is not None
            
            elif operator == FilterOperator.MATCHES_REGEX:
                if isinstance(field_value, str) and isinstance(filter_value, str):
                    import re
                    return bool(re.search(filter_value, field_value, re.IGNORECASE))
                return False
            
            else:
                return False
        
        except Exception:
            # If comparison fails (e.g., type mismatch), return False
            return False
    
    def __repr__(self) -> str:
        return f"FilterCondition(field='{self.field}', operator='{self.operator.value}', value={self.value})"


class QueryBuilder:
    """Builder for complex queries with filtering, sorting, and pagination."""
    
    def __init__(self):
        self.conditions: List[FilterCondition] = []
        self.sort_options: List[SortOptions] = []
        self.limit_value: Optional[int] = None
        self.offset_value: int = 0
        self.logical_operator: str = "AND"  # AND or OR
    
    # Filter methods
    def filter(self, field: str, operator: FilterOperator, value: Any) -> 'QueryBuilder':
        """Add a filter condition."""
        self.conditions.append(FilterCondition(field, operator, value))
        return self
    
    def equals(self, field: str, value: Any) -> 'QueryBuilder':
        """Add equals filter."""
        return self.filter(field, FilterOperator.EQUALS, value)
    
    def not_equals(self, field: str, value: Any) -> 'QueryBuilder':
        """Add not equals filter."""
        return self.filter(field, FilterOperator.NOT_EQUALS, value)
    
    def greater_than(self, field: str, value: Any) -> 'QueryBuilder':
        """Add greater than filter."""
        return self.filter(field, FilterOperator.GREATER_THAN, value)
    
    def greater_equal(self, field: str, value: Any) -> 'QueryBuilder':
        """Add greater than or equal filter."""
        return self.filter(field, FilterOperator.GREATER_EQUAL, value)
    
    def less_than(self, field: str, value: Any) -> 'QueryBuilder':
        """Add less than filter."""
        return self.filter(field, FilterOperator.LESS_THAN, value)
    
    def less_equal(self, field: str, value: Any) -> 'QueryBuilder':
        """Add less than or equal filter."""
        return self.filter(field, FilterOperator.LESS_EQUAL, value)
    
    def in_values(self, field: str, values: List[Any]) -> 'QueryBuilder':
        """Add 'in' filter."""
        return self.filter(field, FilterOperator.IN, values)
    
    def not_in_values(self, field: str, values: List[Any]) -> 'QueryBuilder':
        """Add 'not in' filter."""
        return self.filter(field, FilterOperator.NOT_IN, values)
    
    def contains(self, field: str, value: Any) -> 'QueryBuilder':
        """Add contains filter."""
        return self.filter(field, FilterOperator.CONTAINS, value)
    
    def not_contains(self, field: str, value: Any) -> 'QueryBuilder':
        """Add not contains filter."""
        return self.filter(field, FilterOperator.NOT_CONTAINS, value)
    
    def starts_with(self, field: str, value: str) -> 'QueryBuilder':
        """Add starts with filter."""
        return self.filter(field, FilterOperator.STARTS_WITH, value)
    
    def ends_with(self, field: str, value: str) -> 'QueryBuilder':
        """Add ends with filter."""
        return self.filter(field, FilterOperator.ENDS_WITH, value)
    
    def is_null(self, field: str) -> 'QueryBuilder':
        """Add is null filter."""
        return self.filter(field, FilterOperator.IS_NULL, None)
    
    def is_not_null(self, field: str) -> 'QueryBuilder':
        """Add is not null filter."""
        return self.filter(field, FilterOperator.IS_NOT_NULL, None)
    
    def matches_regex(self, field: str, pattern: str) -> 'QueryBuilder':
        """Add regex filter."""
        return self.filter(field, FilterOperator.MATCHES_REGEX, pattern)
    
    # Date/time specific filters
    def created_after(self, date: datetime) -> 'QueryBuilder':
        """Filter entities created after a date."""
        return self.greater_than("created_at", date)
    
    def created_before(self, date: datetime) -> 'QueryBuilder':
        """Filter entities created before a date."""
        return self.less_than("created_at", date)
    
    def created_between(self, start_date: datetime, end_date: datetime) -> 'QueryBuilder':
        """Filter entities created between two dates."""
        return self.greater_equal("created_at", start_date).less_equal("created_at", end_date)
    
    def updated_after(self, date: datetime) -> 'QueryBuilder':
        """Filter entities updated after a date."""
        return self.greater_than("updated_at", date)
    
    def updated_before(self, date: datetime) -> 'QueryBuilder':
        """Filter entities updated before a date."""
        return self.less_than("updated_at", date)
    
    def updated_between(self, start_date: datetime, end_date: datetime) -> 'QueryBuilder':
        """Filter entities updated between two dates."""
        return self.greater_equal("updated_at", start_date).less_equal("updated_at", end_date)
    
    # Tag and metadata filters
    def has_tag(self, tag: str) -> 'QueryBuilder':
        """Filter entities that have a specific tag."""
        return self.contains("tags", tag)
    
    def has_tags(self, tags: List[str]) -> 'QueryBuilder':
        """Filter entities that have all specified tags."""
        return self.contains("tags", tags)
    
    def has_any_tag(self, tags: List[str]) -> 'QueryBuilder':
        """Filter entities that have any of the specified tags."""
        # This requires special handling in the matches method
        for tag in tags:
            self.contains("tags", tag)
        return self
    
    def has_metadata_key(self, key: str) -> 'QueryBuilder':
        """Filter entities that have a specific metadata key."""
        return self.contains("custom_metadata", key)
    
    def metadata_equals(self, key: str, value: Any) -> 'QueryBuilder':
        """Filter entities where metadata key equals value."""
        # This needs special handling - we'll create a custom condition
        condition = FilterCondition(f"custom_metadata.{key}", FilterOperator.EQUALS, value)
        self.conditions.append(condition)
        return self
    
    # Sorting methods
    def sort_by(self, field: str, order: SortOrder = SortOrder.ASC) -> 'QueryBuilder':
        """Add a sort option."""
        self.sort_options.append(SortOptions(field, order))
        return self
    
    def sort_by_created_at(self, order: SortOrder = SortOrder.DESC) -> 'QueryBuilder':
        """Sort by creation date."""
        return self.sort_by("created_at", order)
    
    def sort_by_updated_at(self, order: SortOrder = SortOrder.DESC) -> 'QueryBuilder':
        """Sort by update date."""
        return self.sort_by("updated_at", order)
    
    # Pagination methods
    def limit(self, count: int) -> 'QueryBuilder':
        """Set result limit."""
        self.limit_value = count
        return self
    
    def offset(self, count: int) -> 'QueryBuilder':
        """Set result offset."""
        self.offset_value = count
        return self
    
    def page(self, page_number: int, page_size: int) -> 'QueryBuilder':
        """Set pagination by page number and size."""
        self.limit_value = page_size
        self.offset_value = (page_number - 1) * page_size
        return self
    
    # Logical operators
    def use_or_logic(self) -> 'QueryBuilder':
        """Use OR logic for combining conditions."""
        self.logical_operator = "OR"
        return self
    
    def use_and_logic(self) -> 'QueryBuilder':
        """Use AND logic for combining conditions."""
        self.logical_operator = "AND"
        return self
    
    # Query execution
    def matches(self, entity: BaseEntity) -> bool:
        """Check if an entity matches all query conditions."""
        if not self.conditions:
            return True
        
        results = []
        for condition in self.conditions:
            # Handle special metadata conditions
            if condition.field.startswith("custom_metadata."):
                metadata_key = condition.field.split(".", 1)[1]
                if hasattr(entity, "custom_metadata") and isinstance(entity.custom_metadata, dict):
                    metadata_value = entity.custom_metadata.get(metadata_key)
                    result = condition._evaluate_condition(metadata_value, condition.operator, condition.value)
                else:
                    result = False
            else:
                result = condition.matches(entity)
            
            results.append(result)
        
        # Apply logical operator
        if self.logical_operator == "OR":
            return any(results)
        else:  # AND
            return all(results)
    
    def apply_to_list(self, entities: List[BaseEntity]) -> List[BaseEntity]:
        """Apply the query to a list of entities."""
        # Filter
        if self.conditions:
            entities = [entity for entity in entities if self.matches(entity)]
        
        # Sort
        if self.sort_options:
            def sort_key(entity):
                keys = []
                for sort_option in self.sort_options:
                    value = getattr(entity, sort_option.field, None)
                    # Handle None values by putting them at the end
                    if value is None:
                        value = "" if sort_option.order == SortOrder.ASC else "~"  # ~ sorts after most characters
                    keys.append(value)
                return keys
            
            # Sort by multiple criteria
            reverse_flags = [sort_option.order == SortOrder.DESC for sort_option in self.sort_options]
            
            # For multiple sort criteria, we need to sort in reverse order of importance
            for i in range(len(self.sort_options) - 1, -1, -1):
                sort_option = self.sort_options[i]
                entities.sort(
                    key=lambda x: getattr(x, sort_option.field, None) or ("" if sort_option.order == SortOrder.ASC else "~"),
                    reverse=(sort_option.order == SortOrder.DESC)
                )
        
        # Pagination
        start_index = self.offset_value
        end_index = start_index + self.limit_value if self.limit_value else None
        
        return entities[start_index:end_index]
    
    def __repr__(self) -> str:
        return (f"QueryBuilder(conditions={len(self.conditions)}, "
                f"sorts={len(self.sort_options)}, "
                f"limit={self.limit_value}, offset={self.offset_value})")


# Common query presets
class CommonQueries:
    """Collection of commonly used query patterns."""
    
    @staticmethod
    def recent_entities(days: int = 7) -> QueryBuilder:
        """Get entities created in the last N days."""
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        return QueryBuilder().created_after(cutoff_date).sort_by_created_at(SortOrder.DESC)
    
    @staticmethod
    def recently_updated(days: int = 7) -> QueryBuilder:
        """Get entities updated in the last N days."""
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        return QueryBuilder().updated_after(cutoff_date).sort_by_updated_at(SortOrder.DESC)
    
    @staticmethod
    def by_tags(tags: List[str], match_all: bool = True) -> QueryBuilder:
        """Get entities by tags."""
        query = QueryBuilder()
        if match_all:
            return query.has_tags(tags)
        else:
            return query.has_any_tag(tags)
    
    @staticmethod
    def search_text(text: str, fields: List[str]) -> QueryBuilder:
        """Search for text across multiple fields."""
        query = QueryBuilder().use_or_logic()
        for field in fields:
            query.contains(field, text)
        return query
    
    @staticmethod
    def paginated(page: int, page_size: int = 20) -> QueryBuilder:
        """Get a paginated query."""
        return QueryBuilder().page(page, page_size).sort_by_created_at(SortOrder.DESC)


class AdvancedQueryBuilder(QueryBuilder):
    """Enhanced query builder with domain-specific patterns."""
    
    # Status-based filtering
    def has_status(self, status: str) -> 'AdvancedQueryBuilder':
        """Filter entities by current status."""
        return self.equals("status", status)
    
    def has_any_status(self, statuses: List[str]) -> 'AdvancedQueryBuilder':
        """Filter entities with any of the specified statuses."""
        return self.in_values("status", statuses)
    
    def status_changed_after(self, date: datetime) -> 'AdvancedQueryBuilder':
        """Filter entities where status was changed after a date."""
        # This requires special handling in matches method
        condition = FilterCondition("status_history", FilterOperator.CONTAINS, {
            "timestamp_after": date
        })
        self.conditions.append(condition)
        return self
    
    def has_been_status(self, status: str) -> 'AdvancedQueryBuilder':
        """Filter entities that have ever been in a specific status."""
        condition = FilterCondition("status_history", FilterOperator.CONTAINS, {
            "has_status": status
        })
        self.conditions.append(condition)
        return self
    
    def status_changed_by_user(self, user: str) -> 'AdvancedQueryBuilder':
        """Filter entities where status was changed by a specific user."""
        condition = FilterCondition("status_history", FilterOperator.CONTAINS, {
            "changed_by": user
        })
        self.conditions.append(condition)
        return self
    
    # Annotation-based filtering
    def has_annotation_content(self, content: str) -> 'AdvancedQueryBuilder':
        """Filter entities with annotations containing specific content."""
        condition = FilterCondition("annotations", FilterOperator.CONTAINS, {
            "content_contains": content
        })
        self.conditions.append(condition)
        return self
    
    def has_annotation_type(self, annotation_type: str) -> 'AdvancedQueryBuilder':
        """Filter entities with annotations of a specific type."""
        condition = FilterCondition("annotations", FilterOperator.CONTAINS, {
            "annotation_type": annotation_type
        })
        self.conditions.append(condition)
        return self
    
    def annotation_by_author(self, author: str) -> 'AdvancedQueryBuilder':
        """Filter entities with annotations by a specific author."""
        condition = FilterCondition("annotations", FilterOperator.CONTAINS, {
            "author": author
        })
        self.conditions.append(condition)
        return self
    
    def annotated_after(self, date: datetime) -> 'AdvancedQueryBuilder':
        """Filter entities annotated after a specific date."""
        condition = FilterCondition("annotations", FilterOperator.CONTAINS, {
            "timestamp_after": date
        })
        self.conditions.append(condition)
        return self
    
    # Association-based filtering
    def has_association(self, link_type: str, target_id: Optional[UUID] = None) -> 'AdvancedQueryBuilder':
        """Filter entities that have associations of a specific type."""
        if target_id:
            condition = FilterCondition("associations", FilterOperator.CONTAINS, {
                "link_type": link_type,
                "target_id": target_id
            })
        else:
            condition = FilterCondition("associations", FilterOperator.CONTAINS, {
                "link_type": link_type
            })
        self.conditions.append(condition)
        return self
    
    def associated_with(self, entity_id: UUID, link_type: Optional[str] = None) -> 'AdvancedQueryBuilder':
        """Filter entities associated with a specific entity."""
        if link_type:
            condition = FilterCondition("associations", FilterOperator.CONTAINS, {
                "entity_id": entity_id,
                "link_type": link_type
            })
        else:
            condition = FilterCondition("associations", FilterOperator.CONTAINS, {
                "entity_id": entity_id
            })
        self.conditions.append(condition)
        return self
    
    # Enhanced matches method to handle complex filters
    def matches(self, entity) -> bool:
        """Enhanced matching that handles complex domain-specific filters."""
        if not self.conditions:
            return True
        
        results = []
        for condition in self.conditions:
            if condition.field == "status_history":
                result = self._match_status_history(entity, condition)
            elif condition.field == "annotations":
                result = self._match_annotations(entity, condition)
            elif condition.field == "associations":
                result = self._match_associations(entity, condition)
            elif condition.field.startswith("custom_metadata."):
                metadata_key = condition.field.split(".", 1)[1]
                if hasattr(entity, "custom_metadata") and isinstance(entity.custom_metadata, dict):
                    metadata_value = entity.custom_metadata.get(metadata_key)
                    result = condition._evaluate_condition(metadata_value, condition.operator, condition.value)
                else:
                    result = False
            else:
                result = condition.matches(entity)
            
            results.append(result)
        
        # Apply logical operator
        if self.logical_operator == "OR":
            return any(results)
        else:  # AND
            return all(results)
    
    def _match_status_history(self, entity, condition) -> bool:
        """Match entities based on status history."""
        if not hasattr(entity, 'status_history') or not entity.status_history:
            return False
        
        filter_spec = condition.value
        
        if "timestamp_after" in filter_spec:
            return any(
                change.timestamp > filter_spec["timestamp_after"]
                for change in entity.status_history
            )
        
        if "has_status" in filter_spec:
            target_status = filter_spec["has_status"]
            return (entity.status == target_status or 
                    any(change.old_status == target_status or change.new_status == target_status
                        for change in entity.status_history))
        
        if "changed_by" in filter_spec:
            return any(
                change.user == filter_spec["changed_by"]
                for change in entity.status_history
            )
        
        return False
    
    def _match_annotations(self, entity, condition) -> bool:
        """Match entities based on annotations."""
        if not hasattr(entity, 'annotations') or not entity.annotations:
            return False
        
        filter_spec = condition.value
        
        if "content_contains" in filter_spec:
            search_term = filter_spec["content_contains"].lower()
            return any(
                search_term in annotation.content.lower()
                for annotation in entity.annotations
            )
        
        if "annotation_type" in filter_spec:
            return any(
                annotation.annotation_type == filter_spec["annotation_type"]
                for annotation in entity.annotations
            )
        
        if "author" in filter_spec:
            return any(
                annotation.author == filter_spec["author"]
                for annotation in entity.annotations
            )
        
        if "timestamp_after" in filter_spec:
            return any(
                annotation.timestamp > filter_spec["timestamp_after"]
                for annotation in entity.annotations
            )
        
        return False
    
    def _match_associations(self, entity, condition) -> bool:
        """Match entities based on associations."""
        # This would require access to association data, which might need to be injected
        # For now, return False as this would require service-level coordination
        return False


class StatusQueryBuilder(AdvancedQueryBuilder):
    """Specialized query builder for status-managed entities."""
    
    def active_entities(self, active_statuses: List[str]) -> 'StatusQueryBuilder':
        """Filter for entities in active statuses."""
        return self.has_any_status(active_statuses)
    
    def completed_entities(self, completed_statuses: List[str]) -> 'StatusQueryBuilder':
        """Filter for completed entities."""
        return self.has_any_status(completed_statuses)
    
    def recently_changed_status(self, days: int = 7) -> 'StatusQueryBuilder':
        """Filter entities with recent status changes."""
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        return self.status_changed_after(cutoff_date)
    
    def status_timeline(self, status: str, days: int = 30) -> 'StatusQueryBuilder':
        """Get entities that were in a specific status within the last N days."""
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        return (self.has_been_status(status)
                .status_changed_after(cutoff_date)
                .sort_by_updated_at(SortOrder.DESC))


class AnnotationQueryBuilder(AdvancedQueryBuilder):
    """Specialized query builder for annotated entities."""
    
    def search_annotations(self, search_term: str) -> 'AnnotationQueryBuilder':
        """Search for entities by annotation content."""
        return self.has_annotation_content(search_term)
    
    def by_annotation_author(self, author: str) -> 'AnnotationQueryBuilder':
        """Filter entities by annotation author."""
        return self.annotation_by_author(author)
    
    def by_annotation_type(self, annotation_type: str) -> 'AnnotationQueryBuilder':
        """Filter entities by annotation type."""
        return self.has_annotation_type(annotation_type)
    
    def recently_annotated(self, days: int = 7) -> 'AnnotationQueryBuilder':
        """Filter entities with recent annotations."""
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days)
        return self.annotated_after(cutoff_date)
    
    def discussion_entities(self, min_annotations: int = 3) -> 'AnnotationQueryBuilder':
        """Filter entities with significant discussion (many annotations)."""
        # This would need custom logic in matches method
        condition = FilterCondition("annotations", FilterOperator.CONTAINS, {
            "min_count": min_annotations
        })
        self.conditions.append(condition)
        return self