import re
from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from ..core.buffer import TextBuffer


class BasicStats(BaseModel):
    """Basic text statistics."""
    word_count: int = 0
    char_count: int = 0
    char_count_no_spaces: int = 0
    line_count: int = 0
    paragraph_count: int = 0
    sentence_count: int = 0
    average_words_per_sentence: float = 0.0
    average_chars_per_word: float = 0.0


class ReadabilityStats(BaseModel):
    """Text readability statistics."""
    flesch_kincaid_grade: float = 0.0
    flesch_reading_ease: float = 0.0
    gunning_fog_index: float = 0.0
    smog_index: float = 0.0
    automated_readability_index: float = 0.0
    coleman_liau_index: float = 0.0


class VocabularyStats(BaseModel):
    """Vocabulary analysis statistics."""
    unique_words: int = 0
    vocabulary_richness: float = 0.0  # unique words / total words
    most_common_words: List[tuple] = Field(default_factory=list)
    average_word_length: float = 0.0
    longest_word: str = ""
    shortest_word: str = ""


class DetailedStats(BaseModel):
    """Comprehensive text statistics."""
    basic: BasicStats = Field(default_factory=BasicStats)
    readability: ReadabilityStats = Field(default_factory=ReadabilityStats)
    vocabulary: VocabularyStats = Field(default_factory=VocabularyStats)
    timestamp: datetime = Field(default_factory=datetime.now)


class StatisticsEngine(BaseModel):
    """Engine for calculating text statistics."""
    
    def calculate_basic_stats(self, buffer: TextBuffer) -> BasicStats:
        """Calculate basic text statistics."""
        content = buffer.get_content()
        
        if not content.strip():
            return BasicStats()
        
        # Word count
        words = re.findall(r'\b\w+\b', content)
        word_count = len(words)
        
        # Character counts
        char_count = len(content)
        char_count_no_spaces = len(re.sub(r'\s', '', content))
        
        # Line count
        line_count = buffer.get_line_count()
        
        # Paragraph count (empty lines separate paragraphs)
        paragraphs = re.split(r'\n\s*\n', content.strip())
        paragraph_count = len([p for p in paragraphs if p.strip()])
        
        # Sentence count (approximate)
        sentences = re.split(r'[.!?]+', content)
        sentence_count = len([s for s in sentences if s.strip()])
        
        # Averages
        avg_words_per_sentence = word_count / max(sentence_count, 1)
        avg_chars_per_word = char_count_no_spaces / max(word_count, 1)
        
        return BasicStats(
            word_count=word_count,
            char_count=char_count,
            char_count_no_spaces=char_count_no_spaces,
            line_count=line_count,
            paragraph_count=paragraph_count,
            sentence_count=sentence_count,
            average_words_per_sentence=avg_words_per_sentence,
            average_chars_per_word=avg_chars_per_word
        )
    
    def calculate_readability_stats(self, buffer: TextBuffer) -> ReadabilityStats:
        """Calculate readability statistics."""
        content = buffer.get_content()
        
        if not content.strip():
            return ReadabilityStats()
        
        # Basic counts
        words = re.findall(r'\b\w+\b', content)
        sentences = re.split(r'[.!?]+', content)
        sentences = [s for s in sentences if s.strip()]
        
        word_count = len(words)
        sentence_count = len(sentences)
        
        if word_count == 0 or sentence_count == 0:
            return ReadabilityStats()
        
        # Syllable count (approximate)
        syllable_count = self._count_syllables(words)
        
        # Complex words (3+ syllables)
        complex_words = sum(1 for word in words if self._count_syllables_in_word(word) >= 3)
        
        # Average sentence length
        avg_sentence_length = word_count / sentence_count
        
        # Average syllables per word
        avg_syllables_per_word = syllable_count / word_count
        
        # Flesch-Kincaid Grade Level
        fk_grade = 0.39 * avg_sentence_length + 11.8 * avg_syllables_per_word - 15.59
        
        # Flesch Reading Ease
        flesch_ease = 206.835 - 1.015 * avg_sentence_length - 84.6 * avg_syllables_per_word
        
        # Gunning Fog Index
        gunning_fog = 0.4 * (avg_sentence_length + 100 * (complex_words / word_count))
        
        # SMOG Index (approximate)
        smog = 1.043 * ((complex_words * 30 / sentence_count) ** 0.5) + 3.1291
        
        # Automated Readability Index
        avg_chars_per_word = sum(len(word) for word in words) / word_count
        ari = 4.71 * avg_chars_per_word + 0.5 * avg_sentence_length - 21.43
        
        # Coleman-Liau Index
        l_score = (avg_chars_per_word * 100) / avg_sentence_length  # Letters per 100 words
        s_score = (sentence_count * 100) / word_count  # Sentences per 100 words
        coleman_liau = 0.0588 * l_score - 0.296 * s_score - 15.8
        
        return ReadabilityStats(
            flesch_kincaid_grade=max(0, fk_grade),
            flesch_reading_ease=max(0, min(100, flesch_ease)),
            gunning_fog_index=max(0, gunning_fog),
            smog_index=max(0, smog),
            automated_readability_index=max(0, ari),
            coleman_liau_index=max(0, coleman_liau)
        )
    
    def calculate_vocabulary_stats(self, buffer: TextBuffer) -> VocabularyStats:
        """Calculate vocabulary statistics."""
        content = buffer.get_content()
        
        if not content.strip():
            return VocabularyStats()
        
        # Extract words
        words = re.findall(r'\b\w+\b', content.lower())
        
        if not words:
            return VocabularyStats()
        
        # Unique words
        unique_words = set(words)
        unique_count = len(unique_words)
        total_count = len(words)
        
        # Vocabulary richness
        vocabulary_richness = unique_count / total_count
        
        # Word frequency
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Most common words
        most_common = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Word length statistics
        word_lengths = [len(word) for word in words]
        avg_word_length = sum(word_lengths) / len(word_lengths)
        
        longest_word = max(words, key=len) if words else ""
        shortest_word = min(words, key=len) if words else ""
        
        return VocabularyStats(
            unique_words=unique_count,
            vocabulary_richness=vocabulary_richness,
            most_common_words=most_common,
            average_word_length=avg_word_length,
            longest_word=longest_word,
            shortest_word=shortest_word
        )
    
    def calculate_detailed_stats(self, buffer: TextBuffer) -> DetailedStats:
        """Calculate comprehensive statistics."""
        return DetailedStats(
            basic=self.calculate_basic_stats(buffer),
            readability=self.calculate_readability_stats(buffer),
            vocabulary=self.calculate_vocabulary_stats(buffer)
        )
    
    def _count_syllables(self, words: List[str]) -> int:
        """Count total syllables in a list of words."""
        return sum(self._count_syllables_in_word(word) for word in words)
    
    def _count_syllables_in_word(self, word: str) -> int:
        """Count syllables in a single word (approximate)."""
        word = word.lower()
        
        # Remove non-alphabetic characters
        word = re.sub(r'[^a-z]', '', word)
        
        if not word:
            return 0
        
        # Count vowel groups
        vowels = 'aeiouy'
        syllable_count = 0
        prev_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                syllable_count += 1
            prev_was_vowel = is_vowel
        
        # Handle silent 'e'
        if word.endswith('e'):
            syllable_count -= 1
        
        # Every word has at least one syllable
        return max(1, syllable_count)