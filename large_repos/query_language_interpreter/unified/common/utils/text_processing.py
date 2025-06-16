"""
Text processing utilities for the unified query language interpreter.

This module provides common text processing functions that are used
across multiple components for content analysis, pattern matching,
and text manipulation.
"""

import re
import string
from collections import Counter
from typing import Dict, List, Optional, Set, Tuple


class TextNormalizer:
    """Text normalization utilities."""
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Normalize whitespace in text."""
        return re.sub(r'\s+', ' ', text.strip())
    
    @staticmethod
    def remove_punctuation(text: str, keep_chars: str = "") -> str:
        """Remove punctuation from text, optionally keeping specific characters."""
        if keep_chars:
            punct_to_remove = ''.join(c for c in string.punctuation if c not in keep_chars)
        else:
            punct_to_remove = string.punctuation
        
        translator = str.maketrans('', '', punct_to_remove)
        return text.translate(translator)
    
    @staticmethod
    def to_lowercase(text: str) -> str:
        """Convert text to lowercase."""
        return text.lower()
    
    @staticmethod
    def normalize_case(text: str, mode: str = "lower") -> str:
        """Normalize text case."""
        if mode == "lower":
            return text.lower()
        elif mode == "upper":
            return text.upper()
        elif mode == "title":
            return text.title()
        elif mode == "sentence":
            return text.capitalize()
        else:
            return text


class TextTokenizer:
    """Text tokenization utilities."""
    
    def __init__(self):
        self.word_pattern = re.compile(r'\b\w+\b')
        self.sentence_pattern = re.compile(r'[.!?]+')
    
    def tokenize_words(self, text: str, normalize: bool = True) -> List[str]:
        """Tokenize text into words."""
        words = self.word_pattern.findall(text)
        if normalize:
            words = [word.lower() for word in words]
        return words
    
    def tokenize_sentences(self, text: str) -> List[str]:
        """Tokenize text into sentences."""
        sentences = self.sentence_pattern.split(text)
        return [s.strip() for s in sentences if s.strip()]
    
    def tokenize_lines(self, text: str, remove_empty: bool = True) -> List[str]:
        """Tokenize text into lines."""
        lines = text.split('\n')
        if remove_empty:
            lines = [line.strip() for line in lines if line.strip()]
        return lines


class TextSearcher:
    """Text searching and pattern matching utilities."""
    
    def __init__(self):
        self.compiled_patterns: Dict[str, re.Pattern] = {}
    
    def search_patterns(self, text: str, patterns: List[str], 
                       flags: int = re.IGNORECASE) -> Dict[str, List[Dict[str, any]]]:
        """Search for multiple patterns in text."""
        results = {}
        
        for pattern in patterns:
            pattern_key = f"{pattern}_{flags}"
            
            if pattern_key not in self.compiled_patterns:
                self.compiled_patterns[pattern_key] = re.compile(pattern, flags)
            
            compiled_pattern = self.compiled_patterns[pattern_key]
            matches = []
            
            for match in compiled_pattern.finditer(text):
                matches.append({
                    'text': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'line_number': text[:match.start()].count('\n') + 1,
                    'context': self._get_context(text, match.start(), match.end())
                })
            
            results[pattern] = matches
        
        return results
    
    def find_keywords(self, text: str, keywords: List[str], 
                     case_sensitive: bool = False) -> Dict[str, List[int]]:
        """Find keyword positions in text."""
        if not case_sensitive:
            text = text.lower()
            keywords = [kw.lower() for kw in keywords]
        
        results = {}
        for keyword in keywords:
            positions = []
            start = 0
            while True:
                pos = text.find(keyword, start)
                if pos == -1:
                    break
                positions.append(pos)
                start = pos + 1
            results[keyword] = positions
        
        return results
    
    def highlight_text(self, text: str, keywords: List[str], 
                      highlight_format: str = "**{}**") -> str:
        """Highlight keywords in text."""
        highlighted_text = text
        
        for keyword in sorted(keywords, key=len, reverse=True):  # Longest first
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            highlighted_text = pattern.sub(
                lambda m: highlight_format.format(m.group()),
                highlighted_text
            )
        
        return highlighted_text
    
    def _get_context(self, text: str, start: int, end: int, 
                    context_size: int = 50) -> str:
        """Get context around a match."""
        context_start = max(0, start - context_size)
        context_end = min(len(text), end + context_size)
        return text[context_start:context_end]


class TextSimilarity:
    """Text similarity and comparison utilities."""
    
    @staticmethod
    def jaccard_similarity(text1: str, text2: str) -> float:
        """Calculate Jaccard similarity between two texts."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    @staticmethod
    def word_overlap(text1: str, text2: str) -> float:
        """Calculate word overlap between two texts."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        return len(intersection) / min(len(words1), len(words2))
    
    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings."""
        if len(s1) < len(s2):
            return TextSimilarity.levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]


class TextStatistics:
    """Text statistics and analysis utilities."""
    
    def __init__(self):
        self.tokenizer = TextTokenizer()
    
    def get_word_frequency(self, text: str, top_n: Optional[int] = None) -> Dict[str, int]:
        """Get word frequency counts."""
        words = self.tokenizer.tokenize_words(text, normalize=True)
        word_freq = Counter(words)
        
        if top_n:
            return dict(word_freq.most_common(top_n))
        return dict(word_freq)
    
    def get_character_frequency(self, text: str) -> Dict[str, int]:
        """Get character frequency counts."""
        return dict(Counter(text.lower()))
    
    def calculate_readability_score(self, text: str) -> Dict[str, float]:
        """Calculate basic readability metrics."""
        sentences = self.tokenizer.tokenize_sentences(text)
        words = self.tokenizer.tokenize_words(text)
        
        if not sentences or not words:
            return {'flesch_reading_ease': 0.0, 'avg_sentence_length': 0.0}
        
        # Basic metrics
        avg_sentence_length = len(words) / len(sentences)
        
        # Count syllables (simplified)
        total_syllables = sum(self._count_syllables(word) for word in words)
        avg_syllables_per_word = total_syllables / len(words) if words else 0
        
        # Flesch Reading Ease (simplified)
        flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        flesch_score = max(0, min(100, flesch_score))  # Clamp to 0-100
        
        return {
            'flesch_reading_ease': flesch_score,
            'avg_sentence_length': avg_sentence_length,
            'avg_syllables_per_word': avg_syllables_per_word,
            'total_sentences': len(sentences),
            'total_words': len(words),
            'total_syllables': total_syllables
        }
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word (simplified)."""
        word = word.lower()
        vowels = 'aeiouy'
        syllable_count = 0
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        # Handle silent e
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1
        
        return max(1, syllable_count)  # At least one syllable


class TextExtractor:
    """Extract specific information from text."""
    
    def __init__(self):
        self.patterns = {
            'urls': re.compile(r'https?://[^\s/$.?#].[^\s]*'),
            'emails': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'phone_numbers': re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'),
            'dates': re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'),
            'times': re.compile(r'\b\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM)?\b', re.IGNORECASE),
            'currency': re.compile(r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?'),
            'percentages': re.compile(r'\b\d+(?:\.\d+)?%\b'),
            'ip_addresses': re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
            'hashtags': re.compile(r'#\w+'),
            'mentions': re.compile(r'@\w+')
        }
    
    def extract_all(self, text: str) -> Dict[str, List[str]]:
        """Extract all patterns from text."""
        results = {}
        for pattern_name, pattern in self.patterns.items():
            matches = pattern.findall(text)
            results[pattern_name] = matches
        return results
    
    def extract_pattern(self, text: str, pattern_name: str) -> List[str]:
        """Extract specific pattern from text."""
        if pattern_name in self.patterns:
            return self.patterns[pattern_name].findall(text)
        return []
    
    def extract_sentences_containing(self, text: str, keywords: List[str]) -> List[str]:
        """Extract sentences containing any of the specified keywords."""
        tokenizer = TextTokenizer()
        sentences = tokenizer.tokenize_sentences(text)
        
        matching_sentences = []
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for keyword in keywords:
                if keyword.lower() in sentence_lower:
                    matching_sentences.append(sentence)
                    break
        
        return matching_sentences
    
    def extract_paragraphs_containing(self, text: str, keywords: List[str]) -> List[str]:
        """Extract paragraphs containing any of the specified keywords."""
        paragraphs = text.split('\n\n')
        
        matching_paragraphs = []
        for paragraph in paragraphs:
            paragraph_lower = paragraph.lower()
            for keyword in keywords:
                if keyword.lower() in paragraph_lower:
                    matching_paragraphs.append(paragraph.strip())
                    break
        
        return matching_paragraphs


class TextCleaner:
    """Text cleaning and preprocessing utilities."""
    
    @staticmethod
    def remove_extra_whitespace(text: str) -> str:
        """Remove extra whitespace while preserving structure."""
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        # Replace multiple newlines with double newline (paragraph break)
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        return text.strip()
    
    @staticmethod
    def remove_special_characters(text: str, keep_chars: str = "") -> str:
        """Remove special characters, optionally keeping some."""
        if keep_chars:
            pattern = f'[^a-zA-Z0-9\\s{re.escape(keep_chars)}]'
        else:
            pattern = r'[^a-zA-Z0-9\s]'
        return re.sub(pattern, '', text)
    
    @staticmethod
    def remove_html_tags(text: str) -> str:
        """Remove HTML tags from text."""
        return re.sub(r'<[^>]+>', '', text)
    
    @staticmethod
    def remove_urls(text: str) -> str:
        """Remove URLs from text."""
        return re.sub(r'https?://[^\s/$.?#].[^\s]*', '', text)
    
    @staticmethod
    def remove_emails(text: str) -> str:
        """Remove email addresses from text."""
        return re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
    
    @staticmethod
    def standardize_quotes(text: str) -> str:
        """Standardize quote characters."""
        # Replace curly quotes with straight quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        return text
    
    @staticmethod
    def fix_common_typos(text: str) -> str:
        """Fix common typos and formatting issues."""
        # Common typo corrections
        corrections = {
            r'\bteh\b': 'the',
            r'\band\s+and\b': 'and',
            r'\bthe\s+the\b': 'the',
            r'\s+,': ',',
            r'\s+\.': '.',
            r'\s+;': ';',
            r'\s+:': ':',
            r'\(\s+': '(',
            r'\s+\)': ')',
        }
        
        for pattern, replacement in corrections.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text