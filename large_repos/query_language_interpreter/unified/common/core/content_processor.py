"""
Unified content processing framework for document and data analysis.

This module provides common functionality for analyzing text content,
extracting entities, and processing structured data that can be extended
by domain-specific implementations.
"""

import re
from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from .models import Document


@dataclass
class AnalysisResult:
    """Result of content analysis."""
    analysis_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Content metadata
    content_type: str = ""
    language: Optional[str] = None
    size_bytes: int = 0
    
    # Extracted entities
    entities: Dict[str, List[str]] = field(default_factory=dict)
    patterns: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)
    
    # Content metrics
    word_count: int = 0
    sentence_count: int = 0
    paragraph_count: int = 0
    
    # Classification results
    classifications: Dict[str, float] = field(default_factory=dict)
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    
    # Metadata and context
    metadata: Dict[str, Any] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)


class ContentAnalyzer(ABC):
    """Abstract base class for content analyzers."""
    
    @abstractmethod
    def analyze_content(self, content: str, **kwargs) -> AnalysisResult:
        """
        Analyze content and extract relevant information.
        
        Args:
            content: Text content to analyze
            **kwargs: Additional analysis parameters
            
        Returns:
            AnalysisResult with extracted information
        """
        pass


class TextAnalyzer(ContentAnalyzer):
    """Basic text analysis implementation."""
    
    def __init__(self):
        self.word_pattern = re.compile(r'\b\w+\b')
        self.sentence_pattern = re.compile(r'[.!?]+')
        self.paragraph_pattern = re.compile(r'\n\s*\n')
        
        # Common patterns
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.phone_pattern = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
        self.date_pattern = re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b')
        self.currency_pattern = re.compile(r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?')
        
    def analyze_content(self, content: str, **kwargs) -> AnalysisResult:
        """Perform basic text analysis."""
        result = AnalysisResult(
            analysis_id=f"text_analysis_{int(datetime.now().timestamp())}",
            content_type="text",
            size_bytes=len(content.encode('utf-8'))
        )
        
        # Basic metrics
        result.word_count = len(self.word_pattern.findall(content))
        result.sentence_count = len(self.sentence_pattern.findall(content))
        result.paragraph_count = len(self.paragraph_pattern.split(content))
        
        # Extract common patterns
        result.entities['emails'] = self.email_pattern.findall(content)
        result.entities['phones'] = self.phone_pattern.findall(content)
        result.entities['dates'] = self.date_pattern.findall(content)
        result.entities['currency'] = self.currency_pattern.findall(content)
        
        # Extract pattern details with positions
        result.patterns['emails'] = self._extract_pattern_details(content, self.email_pattern)
        result.patterns['phones'] = self._extract_pattern_details(content, self.phone_pattern)
        result.patterns['dates'] = self._extract_pattern_details(content, self.date_pattern)
        
        # Basic language detection (simplified)
        result.language = self._detect_language(content)
        
        return result
    
    def _extract_pattern_details(self, content: str, pattern: re.Pattern) -> List[Dict[str, Any]]:
        """Extract pattern matches with position information."""
        matches = []
        for match in pattern.finditer(content):
            matches.append({
                'text': match.group(),
                'start': match.start(),
                'end': match.end(),
                'context': content[max(0, match.start()-50):match.end()+50]
            })
        return matches
    
    def _detect_language(self, content: str) -> str:
        """Simple language detection (placeholder)."""
        # This is a very basic implementation
        # In practice, you'd use a proper language detection library
        common_english_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = set(self.word_pattern.findall(content.lower()))
        
        english_word_count = len(words.intersection(common_english_words))
        if english_word_count > 0:
            return 'en'
        
        return 'unknown'


class PatternMatcher:
    """Generic pattern matching utility."""
    
    def __init__(self):
        self.patterns: Dict[str, re.Pattern] = {}
        self.compiled_patterns: Dict[str, re.Pattern] = {}
    
    def add_pattern(self, name: str, pattern: str, flags: int = 0):
        """Add a named pattern for matching."""
        self.patterns[name] = pattern
        self.compiled_patterns[name] = re.compile(pattern, flags)
    
    def match_patterns(self, text: str, pattern_names: Optional[List[str]] = None) -> Dict[str, List[Dict[str, Any]]]:
        """Match specified patterns against text."""
        if pattern_names is None:
            pattern_names = list(self.compiled_patterns.keys())
        
        results = {}
        for name in pattern_names:
            if name in self.compiled_patterns:
                pattern = self.compiled_patterns[name]
                matches = []
                
                for match in pattern.finditer(text):
                    matches.append({
                        'text': match.group(),
                        'start': match.start(),
                        'end': match.end(),
                        'groups': match.groups(),
                        'groupdict': match.groupdict()
                    })
                
                results[name] = matches
        
        return results
    
    def find_pattern(self, text: str, pattern_name: str) -> Optional[Dict[str, Any]]:
        """Find first match of a specific pattern."""
        if pattern_name not in self.compiled_patterns:
            return None
        
        match = self.compiled_patterns[pattern_name].search(text)
        if match:
            return {
                'text': match.group(),
                'start': match.start(),
                'end': match.end(),
                'groups': match.groups(),
                'groupdict': match.groupdict()
            }
        
        return None


class EntityExtractor:
    """Extract and classify entities from text content."""
    
    def __init__(self):
        self.extractors: Dict[str, Callable[[str], List[Dict[str, Any]]]] = {}
        self._setup_default_extractors()
    
    def _setup_default_extractors(self):
        """Set up default entity extractors."""
        self.extractors['person_names'] = self._extract_person_names
        self.extractors['organizations'] = self._extract_organizations
        self.extractors['locations'] = self._extract_locations
        self.extractors['money'] = self._extract_money
        self.extractors['dates'] = self._extract_dates
    
    def extract_entities(self, text: str, entity_types: Optional[List[str]] = None) -> Dict[str, List[Dict[str, Any]]]:
        """Extract specified entity types from text."""
        if entity_types is None:
            entity_types = list(self.extractors.keys())
        
        results = {}
        for entity_type in entity_types:
            if entity_type in self.extractors:
                try:
                    results[entity_type] = self.extractors[entity_type](text)
                except Exception as e:
                    results[entity_type] = []
        
        return results
    
    def _extract_person_names(self, text: str) -> List[Dict[str, Any]]:
        """Extract person names (simplified implementation)."""
        # This is a basic implementation - in practice you'd use NLP libraries
        name_pattern = re.compile(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b')
        matches = []
        
        for match in name_pattern.finditer(text):
            matches.append({
                'text': match.group(),
                'type': 'person',
                'start': match.start(),
                'end': match.end(),
                'confidence': 0.7  # Placeholder confidence
            })
        
        return matches
    
    def _extract_organizations(self, text: str) -> List[Dict[str, Any]]:
        """Extract organization names."""
        # Look for patterns like "Company Inc.", "Corp.", etc.
        org_pattern = re.compile(r'\b[A-Z][a-zA-Z\s]+(?:Inc|Corp|LLC|Ltd|Co)\.?\b')
        matches = []
        
        for match in org_pattern.finditer(text):
            matches.append({
                'text': match.group(),
                'type': 'organization',
                'start': match.start(),
                'end': match.end(),
                'confidence': 0.6
            })
        
        return matches
    
    def _extract_locations(self, text: str) -> List[Dict[str, Any]]:
        """Extract location names."""
        # Simple pattern for US states and common cities
        location_pattern = re.compile(r'\b(?:New York|California|Texas|Florida|Illinois|Pennsylvania|Ohio|Georgia|North Carolina|Michigan)\b')
        matches = []
        
        for match in location_pattern.finditer(text):
            matches.append({
                'text': match.group(),
                'type': 'location',
                'start': match.start(),
                'end': match.end(),
                'confidence': 0.8
            })
        
        return matches
    
    def _extract_money(self, text: str) -> List[Dict[str, Any]]:
        """Extract monetary amounts."""
        money_pattern = re.compile(r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?')
        matches = []
        
        for match in money_pattern.finditer(text):
            matches.append({
                'text': match.group(),
                'type': 'money',
                'start': match.start(),
                'end': match.end(),
                'confidence': 0.9
            })
        
        return matches
    
    def _extract_dates(self, text: str) -> List[Dict[str, Any]]:
        """Extract date mentions."""
        date_patterns = [
            re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'),
            re.compile(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'),
            re.compile(r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b')
        ]
        
        matches = []
        for pattern in date_patterns:
            for match in pattern.finditer(text):
                matches.append({
                    'text': match.group(),
                    'type': 'date',
                    'start': match.start(),
                    'end': match.end(),
                    'confidence': 0.8
                })
        
        return matches


class FieldProcessor:
    """Process structured data fields with metadata."""
    
    def __init__(self):
        self.type_detectors: Dict[str, Callable[[Any], bool]] = {
            'email': self._is_email,
            'phone': self._is_phone,
            'date': self._is_date,
            'number': self._is_number,
            'currency': self._is_currency,
            'boolean': self._is_boolean,
            'url': self._is_url
        }
    
    def process_fields(self, data: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Process structured data fields and infer metadata."""
        if not data:
            return {}
        
        field_metadata = {}
        
        # Get all field names
        all_fields = set()
        for row in data:
            all_fields.update(row.keys())
        
        # Analyze each field
        for field_name in all_fields:
            field_values = [row.get(field_name) for row in data if field_name in row]
            field_metadata[field_name] = self._analyze_field(field_name, field_values)
        
        return field_metadata
    
    def _analyze_field(self, field_name: str, values: List[Any]) -> Dict[str, Any]:
        """Analyze a single field and infer its characteristics."""
        metadata = {
            'name': field_name,
            'total_count': len(values),
            'non_null_count': len([v for v in values if v is not None]),
            'null_count': len([v for v in values if v is None]),
            'unique_count': len(set(values)),
            'data_types': Counter(),
            'inferred_type': 'string',
            'sample_values': values[:5] if values else [],
            'statistics': {}
        }
        
        # Analyze data types
        for value in values:
            if value is None:
                continue
            
            detected_type = self._detect_type(value)
            metadata['data_types'][detected_type] += 1
        
        # Infer primary type
        if metadata['data_types']:
            metadata['inferred_type'] = metadata['data_types'].most_common(1)[0][0]
        
        # Calculate type-specific statistics
        if metadata['inferred_type'] == 'number':
            numeric_values = [float(v) for v in values if v is not None and self._is_number(v)]
            if numeric_values:
                metadata['statistics'] = {
                    'min': min(numeric_values),
                    'max': max(numeric_values),
                    'avg': sum(numeric_values) / len(numeric_values),
                    'median': sorted(numeric_values)[len(numeric_values) // 2] if numeric_values else 0
                }
        
        elif metadata['inferred_type'] == 'string':
            string_values = [str(v) for v in values if v is not None]
            if string_values:
                lengths = [len(s) for s in string_values]
                metadata['statistics'] = {
                    'min_length': min(lengths),
                    'max_length': max(lengths),
                    'avg_length': sum(lengths) / len(lengths)
                }
        
        return metadata
    
    def _detect_type(self, value: Any) -> str:
        """Detect the type of a value."""
        if value is None:
            return 'null'
        
        # Check specialized types first
        for type_name, detector in self.type_detectors.items():
            if detector(value):
                return type_name
        
        # Check basic types
        if isinstance(value, bool):
            return 'boolean'
        elif isinstance(value, int):
            return 'number'
        elif isinstance(value, float):
            return 'number'
        elif isinstance(value, str):
            return 'string'
        else:
            return 'unknown'
    
    def _is_email(self, value: Any) -> bool:
        """Check if value is an email address."""
        if not isinstance(value, str):
            return False
        email_pattern = re.compile(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
        return bool(email_pattern.match(value))
    
    def _is_phone(self, value: Any) -> bool:
        """Check if value is a phone number."""
        if not isinstance(value, str):
            return False
        phone_pattern = re.compile(r'^\d{3}[-.]?\d{3}[-.]?\d{4}$')
        return bool(phone_pattern.match(value))
    
    def _is_date(self, value: Any) -> bool:
        """Check if value is a date."""
        if not isinstance(value, str):
            return False
        date_patterns = [
            re.compile(r'^\d{1,2}[/-]\d{1,2}[/-]\d{2,4}$'),
            re.compile(r'^\d{4}-\d{2}-\d{2}$')
        ]
        return any(pattern.match(value) for pattern in date_patterns)
    
    def _is_number(self, value: Any) -> bool:
        """Check if value is a number."""
        if isinstance(value, (int, float)):
            return True
        if isinstance(value, str):
            try:
                float(value)
                return True
            except ValueError:
                return False
        return False
    
    def _is_currency(self, value: Any) -> bool:
        """Check if value is a currency amount."""
        if not isinstance(value, str):
            return False
        currency_pattern = re.compile(r'^\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?$')
        return bool(currency_pattern.match(value))
    
    def _is_boolean(self, value: Any) -> bool:
        """Check if value is a boolean."""
        if isinstance(value, bool):
            return True
        if isinstance(value, str):
            return value.lower() in ('true', 'false', 'yes', 'no', '1', '0')
        return False
    
    def _is_url(self, value: Any) -> bool:
        """Check if value is a URL."""
        if not isinstance(value, str):
            return False
        url_pattern = re.compile(r'^https?://[^\s/$.?#].[^\s]*$')
        return bool(url_pattern.match(value))


class DocumentAnalyzer:
    """High-level document analysis combining multiple analyzers."""
    
    def __init__(self):
        self.text_analyzer = TextAnalyzer()
        self.entity_extractor = EntityExtractor()
        self.pattern_matcher = PatternMatcher()
        self.field_processor = FieldProcessor()
    
    def analyze_document(self, document: Document, **kwargs) -> AnalysisResult:
        """Perform comprehensive document analysis."""
        # Start with basic text analysis
        result = self.text_analyzer.analyze_content(document.content, **kwargs)
        
        # Extract entities
        entities = self.entity_extractor.extract_entities(document.content)
        result.entities.update(entities)
        
        # Add document metadata
        result.metadata.update({
            'document_id': document.document_id,
            'source': document.source,
            'created_at': document.created_at.isoformat() if document.created_at else None,
            'tags': list(document.tags),
            'classification': document.classification
        })
        
        return result
    
    def analyze_structured_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze structured data and return field metadata."""
        return self.field_processor.process_fields(data)