"""Evidence Vault for secure storage of vulnerability evidence."""

import os
import shutil
import json
import base64
import hashlib
import uuid
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, BinaryIO, Tuple, Union, Set

from pydantic import ValidationError as PydanticValidationError

from securetask.evidence.models import Evidence, EvidenceType, AccessLevel
from securetask.utils.crypto import CryptoManager
from securetask.utils.validation import ValidationError, validate_file_size


class EvidenceVault:
    """
    Secure storage system for vulnerability evidence.
    
    Provides encrypted storage and retrieval of evidence files with
    access controls, integrity verification, and metadata management.
    """
    
    def __init__(
        self, 
        storage_dir: str, 
        crypto_manager: Optional[CryptoManager] = None,
        max_file_size_mb: int = 100
    ):
        """
        Initialize the evidence vault.
        
        Args:
            storage_dir: Directory where evidence will be stored
            crypto_manager: Optional crypto manager for encryption
            max_file_size_mb: Maximum allowed file size in megabytes
        """
        self.storage_dir = storage_dir
        self.crypto_manager = crypto_manager or CryptoManager()
        self.max_file_size_mb = max_file_size_mb
        
        # Set up directories
        self.evidence_dir = os.path.join(storage_dir, "evidence")
        self.metadata_dir = os.path.join(storage_dir, "metadata")
        
        os.makedirs(self.evidence_dir, exist_ok=True)
        os.makedirs(self.metadata_dir, exist_ok=True)
    
    def store(
        self, 
        file_path: str, 
        title: str,
        description: str,
        evidence_type: Union[str, EvidenceType],
        uploaded_by: str,
        access_level: Union[str, AccessLevel] = AccessLevel.RESTRICTED,
        authorized_users: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        related_finding_ids: Optional[List[str]] = None
    ) -> Evidence:
        """
        Store evidence securely with encryption and metadata.
        
        Args:
            file_path: Path to the evidence file to store
            title: Title of the evidence
            description: Description of the evidence
            evidence_type: Type of evidence (e.g., screenshot, log)
            uploaded_by: ID of the user uploading the evidence
            access_level: Access level for the evidence
            authorized_users: List of users authorized to access the evidence
            tags: List of tags for the evidence
            related_finding_ids: List of related findings
            
        Returns:
            Evidence object with metadata
            
        Raises:
            FileNotFoundError: If the file does not exist
            ValidationError: If validation fails
        """
        start_time = time.time()
        
        # Validate file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        # Validate file size
        validate_file_size(file_path, self.max_file_size_mb)
        
        # Get file info
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        
        # Determine content type (simplified)
        content_type = self._guess_content_type(file_name)
        
        # Generate ID for the evidence
        evidence_id = str(uuid.uuid4())
        
        # Hash the original file
        hash_original = self._hash_file(file_path)
        
        # Create encrypted storage path
        encrypted_path = os.path.join(self.evidence_dir, f"{evidence_id}.enc")
        
        # Encrypt the file
        with open(file_path, "rb") as f:
            file_data = f.read()
            
        encrypted_data, digest = self.crypto_manager.encrypt(file_data)
        
        # Store encrypted file
        with open(encrypted_path, "wb") as f:
            f.write(encrypted_data)
            
        # Store HMAC digest separately
        digest_path = os.path.join(self.evidence_dir, f"{evidence_id}.hmac")
        with open(digest_path, "wb") as f:
            f.write(digest)
            
        # Hash the encrypted file
        hash_encrypted = hashlib.sha256(encrypted_data).hexdigest()
        
        # Create evidence metadata
        evidence = Evidence(
            id=evidence_id,
            title=title,
            description=description,
            type=evidence_type,
            file_path=encrypted_path,
            original_filename=file_name,
            content_type=content_type,
            hash_original=hash_original,
            hash_encrypted=hash_encrypted,
            size_bytes=file_size,
            uploaded_by=uploaded_by,
            access_level=access_level,
            authorized_users=authorized_users or [],
            tags=tags or [],
            related_finding_ids=related_finding_ids or [],
            encryption_info={
                "algorithm": "AES-256-GCM",
                "key_id": self.crypto_manager.hash_data(self.crypto_manager.key)[:8]
            }
        )
        
        # Save metadata
        self._save_metadata(evidence)
        
        execution_time = time.time() - start_time
        if execution_time > 0.05:  # 50ms
            print(f"Warning: Evidence storage took {execution_time*1000:.2f}ms")
            
        return evidence
    
    def get_metadata(self, evidence_id: str, user_id: Optional[str] = None) -> Evidence:
        """
        Retrieve evidence metadata by ID, checking access if user_id is provided.
        
        Args:
            evidence_id: ID of the evidence
            user_id: Optional ID of the user retrieving the metadata
            
        Returns:
            Evidence object with metadata
            
        Raises:
            FileNotFoundError: If the evidence does not exist
            PermissionError: If the user does not have access
        """
        metadata_path = os.path.join(self.metadata_dir, f"{evidence_id}.json.enc")
        
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Evidence not found: {evidence_id}")
            
        # Load and decrypt metadata
        with open(metadata_path, "rb") as f:
            encrypted_data = f.read()
            
        # Load HMAC digest
        digest_path = os.path.join(self.metadata_dir, f"{evidence_id}.hmac")
        with open(digest_path, "rb") as f:
            digest = f.read()
            
        decrypted_data = self.crypto_manager.decrypt(encrypted_data, digest)
        metadata_dict = json.loads(decrypted_data.decode())

        # Create the Evidence object directly instead of using model_validate
        evidence = Evidence(**metadata_dict)

        # Check access if user_id is provided
        if user_id and not evidence.is_accessible_by(user_id):
            raise PermissionError(f"User {user_id} does not have access to evidence {evidence_id}")
            
        return evidence
    
    def retrieve(self, evidence_id: str, output_path: str, user_id: Optional[str] = None) -> Evidence:
        """
        Retrieve and decrypt evidence, writing to output_path.
        
        Args:
            evidence_id: ID of the evidence to retrieve
            output_path: Path where decrypted evidence will be written
            user_id: Optional ID of the user retrieving the evidence
            
        Returns:
            Evidence metadata
            
        Raises:
            FileNotFoundError: If the evidence does not exist
            PermissionError: If the user does not have access
            ValueError: If integrity verification fails
        """
        start_time = time.time()
        
        # Get metadata (will check access if user_id is provided)
        evidence = self.get_metadata(evidence_id, user_id)
        
        # Load encrypted evidence
        encrypted_path = evidence.file_path
        
        if not os.path.exists(encrypted_path):
            raise FileNotFoundError(f"Evidence file not found: {encrypted_path}")
            
        # Load data and HMAC digest
        with open(encrypted_path, "rb") as f:
            encrypted_data = f.read()
            
        digest_path = os.path.join(self.evidence_dir, f"{evidence_id}.hmac")
        with open(digest_path, "rb") as f:
            digest = f.read()
            
        # Decrypt data
        try:
            decrypted_data = self.crypto_manager.decrypt(encrypted_data, digest)
        except ValueError as e:
            raise ValueError(f"Evidence integrity verification failed: {str(e)}")
            
        # Calculate hash of decrypted data to verify
        hash_decrypted = hashlib.sha256(decrypted_data).hexdigest()
        
        if hash_decrypted != evidence.hash_original:
            raise ValueError(
                "Evidence integrity check failed: hash of decrypted data does not match original hash"
            )
            
        # Write decrypted data to output path
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(decrypted_data)
            
        execution_time = time.time() - start_time
        if execution_time > 0.05:  # 50ms
            print(f"Warning: Evidence retrieval took {execution_time*1000:.2f}ms")
            
        return evidence
    
    def update_metadata(self, evidence: Evidence) -> Evidence:
        """
        Update evidence metadata.
        
        Args:
            evidence: Evidence object with updated metadata
            
        Returns:
            Updated evidence
            
        Raises:
            FileNotFoundError: If the evidence does not exist
        """
        # Check if evidence exists
        metadata_path = os.path.join(self.metadata_dir, f"{evidence.id}.json.enc")
        
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Evidence not found: {evidence.id}")
            
        # Save updated metadata
        self._save_metadata(evidence)
        
        return evidence
    
    def delete(self, evidence_id: str) -> bool:
        """
        Delete evidence and its metadata.
        
        Args:
            evidence_id: ID of the evidence to delete
            
        Returns:
            True if deleted, False if not found
        """
        # Check if evidence exists
        metadata_path = os.path.join(self.metadata_dir, f"{evidence_id}.json.enc")
        
        if not os.path.exists(metadata_path):
            return False
            
        # Get metadata to find file path
        try:
            evidence = self.get_metadata(evidence_id)
            
            # Delete evidence file and digest
            if os.path.exists(evidence.file_path):
                os.remove(evidence.file_path)
                
            digest_path = os.path.join(self.evidence_dir, f"{evidence_id}.hmac")
            if os.path.exists(digest_path):
                os.remove(digest_path)
        except Exception:
            # Continue with deletion even if metadata retrieval fails
            pass
            
        # Delete metadata and digest
        os.remove(metadata_path)
        
        digest_path = os.path.join(self.metadata_dir, f"{evidence_id}.hmac")
        if os.path.exists(digest_path):
            os.remove(digest_path)
            
        return True
    
    def list(
        self, 
        user_id: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: str = "uploaded_date",
        reverse: bool = True,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Evidence]:
        """
        List evidence with optional filtering and access control.
        
        Args:
            user_id: Optional ID of the user for access control
            filters: Optional filters as field-value pairs
            sort_by: Field to sort by
            reverse: Whether to sort in reverse order
            limit: Maximum number of items to return
            offset: Number of items to skip
            
        Returns:
            List of evidence matching criteria and accessible to the user
        """
        evidence_list = []
        count = 0
        
        # Iterate over metadata files
        for filename in os.listdir(self.metadata_dir):
            if not filename.endswith(".json.enc"):
                continue
                
            evidence_id = filename.replace(".json.enc", "")
            
            try:
                # Get metadata (will check access if user_id is provided)
                evidence = self.get_metadata(evidence_id, user_id)
                
                # Apply filters if provided
                if filters and not self._matches_filters(evidence, filters):
                    continue
                    
                count += 1
                if count <= offset:
                    continue
                    
                evidence_list.append(evidence)
                
                if limit and len(evidence_list) >= limit:
                    break
                    
            except (FileNotFoundError, PermissionError, ValidationError):
                # Skip inaccessible or invalid evidence
                continue
                
        # Sort evidence
        if hasattr(Evidence, sort_by):
            # Handle filename and title fields specially for alphabetical sorting
            if sort_by in ("filename", "title"):
                evidence_list.sort(key=lambda e: getattr(e, sort_by).lower(), reverse=reverse)
            else:
                evidence_list.sort(key=lambda e: getattr(e, sort_by), reverse=reverse)

        return evidence_list
    
    def count(
        self, 
        user_id: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Count evidence matching filters and accessible to the user.
        
        Args:
            user_id: Optional ID of the user for access control
            filters: Optional filters as field-value pairs
            
        Returns:
            Number of evidence items matching criteria
        """
        if not filters and not user_id:
            # Just count files without loading
            return sum(1 for f in os.listdir(self.metadata_dir) if f.endswith(".json.enc"))
            
        # With filters or user_id, we need to load and check each evidence
        count = 0
        for filename in os.listdir(self.metadata_dir):
            if not filename.endswith(".json.enc"):
                continue
                
            evidence_id = filename.replace(".json.enc", "")
            
            try:
                # Get metadata (will check access if user_id is provided)
                evidence = self.get_metadata(evidence_id, user_id)
                
                if filters and not self._matches_filters(evidence, filters):
                    continue
                    
                count += 1
                
            except (FileNotFoundError, PermissionError, ValidationError):
                # Skip inaccessible or invalid evidence
                continue
                
        return count
    
    def verify_integrity(self, evidence_id: str) -> bool:
        """
        Verify the integrity of stored evidence.
        
        Args:
            evidence_id: ID of the evidence to verify
            
        Returns:
            True if integrity check passes
            
        Raises:
            FileNotFoundError: If the evidence does not exist
            ValueError: If integrity verification fails
        """
        # Get metadata
        evidence = self.get_metadata(evidence_id)
        
        # Load encrypted evidence
        encrypted_path = evidence.file_path
        
        if not os.path.exists(encrypted_path):
            raise FileNotFoundError(f"Evidence file not found: {encrypted_path}")
            
        # Verify hash of encrypted file
        hash_encrypted = self._hash_file(encrypted_path)
        
        if hash_encrypted != evidence.hash_encrypted:
            raise ValueError("Evidence integrity check failed: encrypted file hash mismatch")
            
        # Load data and HMAC digest
        with open(encrypted_path, "rb") as f:
            encrypted_data = f.read()
            
        digest_path = os.path.join(self.evidence_dir, f"{evidence_id}.hmac")
        
        if not os.path.exists(digest_path):
            raise FileNotFoundError(f"Evidence digest not found: {digest_path}")
            
        with open(digest_path, "rb") as f:
            digest = f.read()
            
        # Decrypt to verify HMAC
        try:
            decrypted_data = self.crypto_manager.decrypt(encrypted_data, digest)
        except ValueError as e:
            raise ValueError(f"Evidence integrity verification failed: {str(e)}")
            
        # Verify hash of decrypted data
        hash_decrypted = hashlib.sha256(decrypted_data).hexdigest()
        
        if hash_decrypted != evidence.hash_original:
            raise ValueError(
                "Evidence integrity check failed: hash of decrypted data does not match original hash"
            )
            
        return True
    
    def _save_metadata(self, evidence: Evidence) -> None:
        """
        Save evidence metadata with encryption.
        
        Args:
            evidence: Evidence metadata to save
        """
        # Convert to JSON
        metadata_json = evidence.model_dump_json().encode()
        
        # Encrypt metadata
        encrypted_data, digest = self.crypto_manager.encrypt(metadata_json)
        
        # Save encrypted metadata
        metadata_path = os.path.join(self.metadata_dir, f"{evidence.id}.json.enc")
        with open(metadata_path, "wb") as f:
            f.write(encrypted_data)
            
        # Save HMAC digest
        digest_path = os.path.join(self.metadata_dir, f"{evidence.id}.hmac")
        with open(digest_path, "wb") as f:
            f.write(digest)
    
    def _hash_file(self, file_path: str) -> str:
        """
        Calculate SHA-256 hash of a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Hex digest of the hash
        """
        h = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
                
        return h.hexdigest()
    
    def _guess_content_type(self, filename: str) -> str:
        """
        Guess the content type from a filename.
        
        Args:
            filename: Name of the file
            
        Returns:
            Guessed content type
        """
        extension = os.path.splitext(filename)[1].lower()
        
        content_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".pdf": "application/pdf",
            ".txt": "text/plain",
            ".log": "text/plain",
            ".py": "text/x-python",
            ".js": "text/javascript",
            ".html": "text/html",
            ".xml": "application/xml",
            ".json": "application/json",
            ".pcap": "application/vnd.tcpdump.pcap",
            ".sql": "application/sql"
        }
        
        return content_types.get(extension, "application/octet-stream")
    
    def _matches_filters(self, evidence: Evidence, filters: Dict[str, Any]) -> bool:
        """
        Check if evidence matches the given filters.
        
        Args:
            evidence: The evidence to check
            filters: Filters as field-value pairs
            
        Returns:
            True if the evidence matches all filters
        """
        for field, value in filters.items():
            if not hasattr(evidence, field):
                return False
                
            field_value = getattr(evidence, field)
            
            # Handle list fields like tags, related_finding_ids
            if isinstance(field_value, list) and not isinstance(value, list):
                if value not in field_value:
                    return False
            # Handle date ranges
            elif field.endswith("_date") and isinstance(value, dict):
                if "from" in value and field_value < value["from"]:
                    return False
                if "to" in value and field_value > value["to"]:
                    return False
            # Handle enums
            elif field in ["type", "access_level"] and isinstance(value, str):
                if str(field_value.value) != value:
                    return False
            # Simple equality
            elif field_value != value:
                return False
                
        return True