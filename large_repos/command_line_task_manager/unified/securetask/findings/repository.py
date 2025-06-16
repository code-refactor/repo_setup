"""Repository for managing security findings."""

import os
import json
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable, Union, Generator

from pydantic import ValidationError as PydanticValidationError

from securetask.findings.models import Finding
from securetask.utils.crypto import CryptoManager
from securetask.utils.validation import ValidationError


class FindingRepository:
    """
    Repository for CRUD operations on security findings.
    
    Provides encrypted storage and retrieval of finding data with
    additional functionality for searching and filtering findings.
    """
    
    def __init__(self, storage_dir: str, crypto_manager: Optional[CryptoManager] = None):
        """
        Initialize the finding repository.
        
        Args:
            storage_dir: Directory where findings will be stored
            crypto_manager: Optional crypto manager for encryption
        """
        self.storage_dir = storage_dir
        self.crypto_manager = crypto_manager or CryptoManager()
        self.findings_dir = os.path.join(storage_dir, "findings")
        
        # Create findings directory if it doesn't exist
        os.makedirs(self.findings_dir, exist_ok=True)
    
    def create(self, finding: Finding) -> Finding:
        """
        Create a new security finding.
        
        Args:
            finding: The finding to create
            
        Returns:
            The created finding with ID
            
        Raises:
            ValidationError: If finding validation fails
        """
        start_time = time.time()
        
        try:
            # Set creation timestamp if not already set
            if not finding.id:
                finding.id = str(uuid.uuid4())
            
            # Save the finding
            self._save_finding(finding)
            
            execution_time = time.time() - start_time
            if execution_time > 0.05:  # 50ms
                print(f"Warning: Finding creation took {execution_time*1000:.2f}ms")
                
            return finding
            
        except PydanticValidationError as e:
            raise ValidationError(str(e))
    
    def get(self, finding_id: str) -> Finding:
        """
        Retrieve a finding by ID.
        
        Args:
            finding_id: ID of the finding to retrieve
            
        Returns:
            The retrieved finding
            
        Raises:
            FileNotFoundError: If the finding does not exist
        """
        start_time = time.time()
        
        file_path = os.path.join(self.findings_dir, f"{finding_id}.json.enc")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Finding not found: {finding_id}")
        
        # Load and decrypt
        with open(file_path, "rb") as f:
            encrypted_data = f.read()
        
        # Load and decrypt the HMAC digest
        digest_path = os.path.join(self.findings_dir, f"{finding_id}.hmac")
        with open(digest_path, "rb") as f:
            digest = f.read()
        
        decrypted_data = self.crypto_manager.decrypt(encrypted_data, digest)
        finding_dict = json.loads(decrypted_data.decode())

        # Track execution time
        execution_time = time.time() - start_time
        if execution_time > 0.05:  # 50ms
            print(f"Warning: Finding retrieval took {execution_time*1000:.2f}ms")

        # Create the Finding object directly
        return Finding(**finding_dict)
    
    def update(self, finding: Finding) -> Finding:
        """
        Update an existing finding.
        
        Args:
            finding: The finding to update
            
        Returns:
            The updated finding
            
        Raises:
            FileNotFoundError: If the finding does not exist
            ValidationError: If finding validation fails
        """
        start_time = time.time()
        
        # Check if finding exists
        file_path = os.path.join(self.findings_dir, f"{finding.id}.json.enc")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Finding not found: {finding.id}")
        
        try:
            # Save the updated finding
            self._save_finding(finding)
            
            execution_time = time.time() - start_time
            if execution_time > 0.05:  # 50ms
                print(f"Warning: Finding update took {execution_time*1000:.2f}ms")
            
            return finding
            
        except PydanticValidationError as e:
            raise ValidationError(str(e))
    
    def delete(self, finding_id: str) -> bool:
        """
        Delete a finding by ID.
        
        Args:
            finding_id: ID of the finding to delete
            
        Returns:
            True if deleted, False if not found
        """
        file_path = os.path.join(self.findings_dir, f"{finding_id}.json.enc")
        digest_path = os.path.join(self.findings_dir, f"{finding_id}.hmac")
        
        if not os.path.exists(file_path):
            return False
        
        # Delete both the encrypted file and HMAC digest
        os.remove(file_path)
        if os.path.exists(digest_path):
            os.remove(digest_path)
            
        return True
    
    def list(
        self, 
        filters: Optional[Dict[str, Any]] = None, 
        sort_by: str = "discovered_date", 
        reverse: bool = True,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Finding]:
        """
        List findings with optional filtering and sorting.
        
        Args:
            filters: Optional filters as field-value pairs
            sort_by: Field to sort by
            reverse: Whether to sort in reverse order
            limit: Maximum number of findings to return
            offset: Number of findings to skip
            
        Returns:
            List of findings matching criteria
        """
        findings = []
        count = 0
        
        # Get all finding IDs from filenames
        for filename in os.listdir(self.findings_dir):
            if not filename.endswith(".json.enc"):
                continue
                
            finding_id = filename.replace(".json.enc", "")
            
            try:
                finding = self.get(finding_id)
                
                # Apply filters if provided
                if filters and not self._matches_filters(finding, filters):
                    continue
                
                count += 1
                if count <= offset:
                    continue
                    
                findings.append(finding)
                
                if limit and len(findings) >= limit:
                    break
                    
            except (FileNotFoundError, ValidationError):
                # Skip invalid files
                continue
        
        # Sort findings
        if hasattr(Finding, sort_by):
            # Handle title field specially to ensure alphabetical sorting
            if sort_by == "title":
                findings.sort(key=lambda f: f.title.lower(), reverse=reverse)
            else:
                findings.sort(key=lambda f: getattr(f, sort_by), reverse=reverse)

        return findings
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count findings matching filters.
        
        Args:
            filters: Optional filters as field-value pairs
            
        Returns:
            Number of findings matching criteria
        """
        if not filters:
            # Just count files without loading
            return sum(1 for f in os.listdir(self.findings_dir) if f.endswith(".json.enc"))
        
        # With filters, we need to load and check each finding
        count = 0
        for filename in os.listdir(self.findings_dir):
            if not filename.endswith(".json.enc"):
                continue
                
            finding_id = filename.replace(".json.enc", "")
            
            try:
                finding = self.get(finding_id)
                if self._matches_filters(finding, filters):
                    count += 1
            except (FileNotFoundError, ValidationError):
                # Skip invalid files
                continue
                
        return count
    
    def _save_finding(self, finding: Finding) -> None:
        """
        Save a finding with encryption.
        
        Args:
            finding: The finding to save
        """
        # Convert to JSON
        finding_json = finding.model_dump_json().encode()
        
        # Encrypt
        encrypted_data, digest = self.crypto_manager.encrypt(finding_json)
        
        # Save encrypted data
        file_path = os.path.join(self.findings_dir, f"{finding.id}.json.enc")
        with open(file_path, "wb") as f:
            f.write(encrypted_data)
            
        # Save HMAC digest separately for integrity verification
        digest_path = os.path.join(self.findings_dir, f"{finding.id}.hmac")
        with open(digest_path, "wb") as f:
            f.write(digest)
    
    def _matches_filters(self, finding: Finding, filters: Dict[str, Any]) -> bool:
        """
        Check if a finding matches the given filters.
        
        Args:
            finding: The finding to check
            filters: Filters as field-value pairs
            
        Returns:
            True if the finding matches all filters
        """
        for field, value in filters.items():
            if not hasattr(finding, field):
                return False
                
            field_value = getattr(finding, field)
            
            # Handle list fields like tags, affected_systems
            if isinstance(field_value, list) and not isinstance(value, list):
                if value not in field_value:
                    return False
            # Handle date ranges
            elif field.endswith("_date") and isinstance(value, dict):
                if "from" in value and field_value < value["from"]:
                    return False
                if "to" in value and field_value > value["to"]:
                    return False
            # Simple equality
            elif field_value != value:
                return False
                
        return True