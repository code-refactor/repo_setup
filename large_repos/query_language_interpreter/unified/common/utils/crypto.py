"""
Cryptographic utilities for the unified query language interpreter.

This module provides common cryptographic functions for integrity verification,
hashing, and secure data handling used across audit logging and security features.
"""

import hashlib
import hmac
import secrets
from typing import Optional, Union


class HashUtils:
    """Utilities for hashing and integrity verification."""
    
    @staticmethod
    def sha256_hash(data: Union[str, bytes]) -> str:
        """Generate SHA-256 hash of data."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha256(data).hexdigest()
    
    @staticmethod
    def md5_hash(data: Union[str, bytes]) -> str:
        """Generate MD5 hash of data (use only for non-security purposes)."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.md5(data).hexdigest()
    
    @staticmethod
    def sha1_hash(data: Union[str, bytes]) -> str:
        """Generate SHA-1 hash of data."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.sha1(data).hexdigest()
    
    @staticmethod
    def blake2b_hash(data: Union[str, bytes], digest_size: int = 32) -> str:
        """Generate BLAKE2b hash of data."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return hashlib.blake2b(data, digest_size=digest_size).hexdigest()


class HMACUtils:
    """HMAC utilities for message authentication."""
    
    @staticmethod
    def generate_hmac(key: Union[str, bytes], message: Union[str, bytes], 
                     algorithm: str = 'sha256') -> str:
        """Generate HMAC for message authentication."""
        if isinstance(key, str):
            key = key.encode('utf-8')
        if isinstance(message, str):
            message = message.encode('utf-8')
        
        if algorithm == 'sha256':
            hash_func = hashlib.sha256
        elif algorithm == 'sha1':
            hash_func = hashlib.sha1
        elif algorithm == 'md5':
            hash_func = hashlib.md5
        else:
            raise ValueError(f"Unsupported HMAC algorithm: {algorithm}")
        
        return hmac.new(key, message, hash_func).hexdigest()
    
    @staticmethod
    def verify_hmac(key: Union[str, bytes], message: Union[str, bytes], 
                   signature: str, algorithm: str = 'sha256') -> bool:
        """Verify HMAC signature."""
        expected_signature = HMACUtils.generate_hmac(key, message, algorithm)
        return hmac.compare_digest(expected_signature, signature)


class SecureTokenGenerator:
    """Generate secure tokens and identifiers."""
    
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """Generate a secure random token."""
        return secrets.token_hex(length)
    
    @staticmethod
    def generate_urlsafe_token(length: int = 32) -> str:
        """Generate a URL-safe secure random token."""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_session_id() -> str:
        """Generate a secure session ID."""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def generate_api_key() -> str:
        """Generate a secure API key."""
        return secrets.token_urlsafe(48)


class DataMasking:
    """Utilities for data masking and obfuscation."""
    
    @staticmethod
    def mask_email(email: str) -> str:
        """Mask email address while preserving format."""
        if '@' not in email:
            return email
        
        local, domain = email.split('@', 1)
        
        if len(local) <= 2:
            masked_local = '*' * len(local)
        else:
            masked_local = local[0] + '*' * (len(local) - 2) + local[-1]
        
        if '.' in domain:
            domain_parts = domain.split('.')
            domain_parts[0] = domain_parts[0][0] + '*' * (len(domain_parts[0]) - 1)
            masked_domain = '.'.join(domain_parts)
        else:
            masked_domain = domain[0] + '*' * (len(domain) - 1)
        
        return f"{masked_local}@{masked_domain}"
    
    @staticmethod
    def mask_phone(phone: str) -> str:
        """Mask phone number while preserving format."""
        # Remove non-digit characters for processing
        digits = ''.join(c for c in phone if c.isdigit())
        
        if len(digits) < 4:
            return '*' * len(phone)
        
        # Keep first and last digit, mask the middle
        masked_digits = digits[0] + '*' * (len(digits) - 2) + digits[-1]
        
        # Restore original format
        result = phone
        digit_index = 0
        for i, char in enumerate(phone):
            if char.isdigit():
                result = result[:i] + masked_digits[digit_index] + result[i+1:]
                digit_index += 1
        
        return result
    
    @staticmethod
    def mask_credit_card(card_number: str) -> str:
        """Mask credit card number, showing only last 4 digits."""
        digits = ''.join(c for c in card_number if c.isdigit())
        
        if len(digits) < 4:
            return '*' * len(card_number)
        
        masked_digits = '*' * (len(digits) - 4) + digits[-4:]
        
        # Restore original format
        result = card_number
        digit_index = 0
        for i, char in enumerate(card_number):
            if char.isdigit():
                result = result[:i] + masked_digits[digit_index] + result[i+1:]
                digit_index += 1
        
        return result
    
    @staticmethod
    def mask_string(text: str, mask_char: str = '*', 
                   preserve_first: int = 1, preserve_last: int = 1) -> str:
        """Mask a string while preserving specified characters at start/end."""
        if len(text) <= preserve_first + preserve_last:
            return mask_char * len(text)
        
        start = text[:preserve_first]
        end = text[-preserve_last:] if preserve_last > 0 else ''
        middle = mask_char * (len(text) - preserve_first - preserve_last)
        
        return start + middle + end


class IntegrityChecker:
    """Verify data integrity using checksums and hashes."""
    
    def __init__(self, algorithm: str = 'sha256'):
        self.algorithm = algorithm
        self.hash_func = getattr(hashlib, algorithm, hashlib.sha256)
    
    def generate_checksum(self, data: Union[str, bytes]) -> str:
        """Generate checksum for data."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return self.hash_func(data).hexdigest()
    
    def verify_checksum(self, data: Union[str, bytes], expected_checksum: str) -> bool:
        """Verify data against expected checksum."""
        actual_checksum = self.generate_checksum(data)
        return hmac.compare_digest(actual_checksum, expected_checksum)
    
    def generate_file_checksum(self, file_path: str) -> str:
        """Generate checksum for a file."""
        hash_obj = self.hash_func()
        
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except IOError:
            return ""
    
    def verify_file_checksum(self, file_path: str, expected_checksum: str) -> bool:
        """Verify file against expected checksum."""
        actual_checksum = self.generate_file_checksum(file_path)
        return hmac.compare_digest(actual_checksum, expected_checksum)


class SecureComparison:
    """Utilities for secure comparison operations."""
    
    @staticmethod
    def constant_time_compare(a: Union[str, bytes], b: Union[str, bytes]) -> bool:
        """Compare two values in constant time to prevent timing attacks."""
        if isinstance(a, str):
            a = a.encode('utf-8')
        if isinstance(b, str):
            b = b.encode('utf-8')
        
        return hmac.compare_digest(a, b)
    
    @staticmethod
    def safe_string_compare(a: str, b: str) -> bool:
        """Safely compare two strings."""
        return hmac.compare_digest(a.encode('utf-8'), b.encode('utf-8'))


class PseudoAnonymization:
    """Utilities for pseudo-anonymization of sensitive data."""
    
    def __init__(self, secret_key: Optional[str] = None):
        self.secret_key = secret_key or secrets.token_hex(32)
    
    def pseudonymize(self, identifier: str, salt: Optional[str] = None) -> str:
        """Create a pseudonym for an identifier."""
        if salt is None:
            salt = ""
        
        combined = f"{identifier}{salt}"
        return HMACUtils.generate_hmac(self.secret_key, combined)
    
    def generate_consistent_id(self, identifier: str, context: str = "") -> str:
        """Generate a consistent pseudonymous ID for an identifier."""
        combined = f"{context}:{identifier}" if context else identifier
        return self.pseudonymize(combined)[:16]  # Shorter ID
    
    def hash_identifier(self, identifier: str) -> str:
        """Create a one-way hash of an identifier."""
        return HashUtils.sha256_hash(f"{self.secret_key}:{identifier}")


class KeyDerivation:
    """Utilities for key derivation and management."""
    
    @staticmethod
    def derive_key(password: str, salt: str, iterations: int = 100000) -> str:
        """Derive a key from password using PBKDF2."""
        import hashlib
        
        password_bytes = password.encode('utf-8')
        salt_bytes = salt.encode('utf-8')
        
        derived_key = hashlib.pbkdf2_hmac('sha256', password_bytes, salt_bytes, iterations)
        return derived_key.hex()
    
    @staticmethod
    def generate_salt(length: int = 16) -> str:
        """Generate a random salt for key derivation."""
        return secrets.token_hex(length)
    
    @staticmethod
    def stretch_key(key: str, salt: str, length: int = 32) -> str:
        """Stretch a key to desired length using HKDF-like approach."""
        expanded = ""
        counter = 1
        
        while len(expanded) < length * 2:  # *2 because hex encoding
            info = f"{salt}:{counter}"
            expanded += HMACUtils.generate_hmac(key, info)
            counter += 1
        
        return expanded[:length * 2]