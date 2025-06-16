"""Repository for storing and retrieving compliance frameworks."""

import os
import json
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Set, Union, Tuple

from pydantic import ValidationError as PydanticValidationError

from securetask.compliance.frameworks import (
    ComplianceControl, ComplianceFramework, ComplianceControlStatus, ComplianceMapping
)
from securetask.utils.crypto import CryptoManager
from securetask.utils.validation import ValidationError


class ComplianceRepository:
    """
    Repository for managing compliance frameworks.
    
    Provides storage, retrieval, and management of compliance frameworks,
    controls, and their mappings to security findings.
    """
    
    def __init__(self, storage_dir: str, crypto_manager: Optional[CryptoManager] = None):
        """
        Initialize the compliance repository.
        
        Args:
            storage_dir: Directory where compliance data will be stored
            crypto_manager: Optional crypto manager for encryption
        """
        self.storage_dir = storage_dir
        self.crypto_manager = crypto_manager or CryptoManager()
        
        # Set up directories
        self.frameworks_dir = os.path.join(storage_dir, "frameworks")
        
        os.makedirs(self.frameworks_dir, exist_ok=True)
        
        # Initialize compliance mapping
        self.mapping = ComplianceMapping()
        
        # Load existing frameworks
        self._load_frameworks()
    
    def create_framework(
        self,
        id: str,
        name: str,
        description: str,
        version: str,
        references: Optional[List[Dict[str, str]]] = None,
        tags: Optional[List[str]] = None
    ) -> ComplianceFramework:
        """
        Create a new compliance framework.
        
        Args:
            id: Identifier for the framework
            name: Name of the framework
            description: Description of the framework
            version: Version of the framework
            references: Optional list of references
            tags: Optional list of tags
            
        Returns:
            The created framework
            
        Raises:
            ValidationError: If validation fails
        """
        start_time = time.time()
        
        try:
            # Create the framework
            framework = ComplianceFramework(
                id=id,
                name=name,
                description=description,
                version=version,
                references=references or [],
                tags=tags or []
            )
            
            # Save the framework
            self._save_framework(framework)
            
            # Add to mapping
            self.mapping.add_framework(framework)
            
            execution_time = time.time() - start_time
            if execution_time > 0.05:  # 50ms
                print(f"Warning: Framework creation took {execution_time*1000:.2f}ms")
                
            return framework
            
        except PydanticValidationError as e:
            raise ValidationError(str(e))
    
    def get_framework(self, framework_id: str) -> ComplianceFramework:
        """
        Retrieve a compliance framework by ID.
        
        Args:
            framework_id: ID of the framework to retrieve
            
        Returns:
            The retrieved framework
            
        Raises:
            FileNotFoundError: If the framework does not exist
        """
        file_path = os.path.join(self.frameworks_dir, f"{framework_id}.json.enc")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Framework not found: {framework_id}")
        
        # Load and decrypt
        with open(file_path, "rb") as f:
            encrypted_data = f.read()
        
        # Load HMAC digest
        digest_path = os.path.join(self.frameworks_dir, f"{framework_id}.hmac")
        with open(digest_path, "rb") as f:
            digest = f.read()
        
        decrypted_data = self.crypto_manager.decrypt(encrypted_data, digest)
        framework_dict = json.loads(decrypted_data.decode())

        # Create the ComplianceFramework object directly
        return ComplianceFramework(**framework_dict)
    
    def update_framework(self, framework: ComplianceFramework) -> ComplianceFramework:
        """
        Update an existing compliance framework.
        
        Args:
            framework: The framework to update
            
        Returns:
            The updated framework
            
        Raises:
            FileNotFoundError: If the framework does not exist
            ValidationError: If validation fails
        """
        start_time = time.time()
        
        # Check if framework exists
        file_path = os.path.join(self.frameworks_dir, f"{framework.id}.json.enc")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Framework not found: {framework.id}")
        
        try:
            # Save the updated framework
            self._save_framework(framework)
            
            # Update mapping
            self.mapping.add_framework(framework)
            
            execution_time = time.time() - start_time
            if execution_time > 0.05:  # 50ms
                print(f"Warning: Framework update took {execution_time*1000:.2f}ms")
            
            return framework
            
        except PydanticValidationError as e:
            raise ValidationError(str(e))
    
    def delete_framework(self, framework_id: str) -> bool:
        """
        Delete a compliance framework.
        
        Args:
            framework_id: ID of the framework to delete
            
        Returns:
            True if deleted, False if not found
        """
        file_path = os.path.join(self.frameworks_dir, f"{framework_id}.json.enc")
        digest_path = os.path.join(self.frameworks_dir, f"{framework_id}.hmac")
        
        if not os.path.exists(file_path):
            return False
        
        # Delete framework files
        os.remove(file_path)
        if os.path.exists(digest_path):
            os.remove(digest_path)
            
        # Remove from mapping
        self.mapping.remove_framework(framework_id)
            
        return True
    
    def add_control(
        self,
        framework_id: str,
        id: str,
        name: str,
        description: str,
        section: str,
        parent_id: Optional[str] = None,
        guidance: Optional[str] = None,
        links: Optional[List[Dict[str, str]]] = None,
        tags: Optional[List[str]] = None
    ) -> ComplianceControl:
        """
        Add a control to a framework.
        
        Args:
            framework_id: ID of the framework
            id: ID for the control
            name: Name of the control
            description: Description of the control
            section: Section identifier
            parent_id: Optional ID of parent control
            guidance: Optional implementation guidance
            links: Optional list of reference links
            tags: Optional list of tags
            
        Returns:
            The created control
            
        Raises:
            FileNotFoundError: If the framework does not exist
            ValidationError: If validation fails
        """
        start_time = time.time()
        
        # Get the framework
        framework = self.get_framework(framework_id)
        
        try:
            # Create the control
            control = ComplianceControl(
                id=id,
                name=name,
                description=description,
                section=section,
                parent_id=parent_id,
                guidance=guidance,
                links=links or [],
                tags=tags or []
            )
            
            # Add to framework
            framework.add_control(control)
            
            # Save the updated framework
            self._save_framework(framework)
            
            # Update mapping
            self.mapping.add_framework(framework)
            
            execution_time = time.time() - start_time
            if execution_time > 0.05:  # 50ms
                print(f"Warning: Control addition took {execution_time*1000:.2f}ms")
                
            return control
            
        except PydanticValidationError as e:
            raise ValidationError(str(e))
    
    def get_control(self, framework_id: str, control_id: str) -> Optional[ComplianceControl]:
        """
        Get a control from a framework.
        
        Args:
            framework_id: ID of the framework
            control_id: ID of the control
            
        Returns:
            The control or None if not found
            
        Raises:
            FileNotFoundError: If the framework does not exist
        """
        # Get the framework
        framework = self.get_framework(framework_id)
        
        # Get the control
        return framework.get_control(control_id)
    
    def update_control(
        self,
        framework_id: str,
        control: ComplianceControl
    ) -> ComplianceControl:
        """
        Update a control in a framework.
        
        Args:
            framework_id: ID of the framework
            control: The control to update
            
        Returns:
            The updated control
            
        Raises:
            FileNotFoundError: If the framework or control does not exist
            ValidationError: If validation fails
        """
        start_time = time.time()
        
        # Get the framework
        framework = self.get_framework(framework_id)
        
        # Check if control exists
        existing_control = framework.get_control(control.id)
        if not existing_control:
            raise FileNotFoundError(f"Control not found: {control.id}")
        
        try:
            # Update control in framework
            framework.add_control(control)
            
            # Save the updated framework
            self._save_framework(framework)
            
            # Update mapping
            self.mapping.add_framework(framework)
            
            execution_time = time.time() - start_time
            if execution_time > 0.05:  # 50ms
                print(f"Warning: Control update took {execution_time*1000:.2f}ms")
                
            return control
            
        except PydanticValidationError as e:
            raise ValidationError(str(e))
    
    def remove_control(self, framework_id: str, control_id: str) -> bool:
        """
        Remove a control from a framework.
        
        Args:
            framework_id: ID of the framework
            control_id: ID of the control
            
        Returns:
            True if removed, False if not found
            
        Raises:
            FileNotFoundError: If the framework does not exist
        """
        # Get the framework
        framework = self.get_framework(framework_id)
        
        # Remove the control
        if not framework.remove_control(control_id):
            return False
            
        # Save the updated framework
        self._save_framework(framework)
        
        # Update mapping
        self.mapping.add_framework(framework)
        
        return True
    
    def list_frameworks(
        self,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: str = "name",
        reverse: bool = False
    ) -> List[ComplianceFramework]:
        """
        List compliance frameworks.
        
        Args:
            filters: Optional filters as field-value pairs
            sort_by: Field to sort by
            reverse: Whether to sort in reverse order
            
        Returns:
            List of frameworks matching criteria
        """
        frameworks = []
        
        # Get all framework IDs from filenames
        for filename in os.listdir(self.frameworks_dir):
            if not filename.endswith(".json.enc"):
                continue
                
            framework_id = filename.replace(".json.enc", "")
            
            try:
                framework = self.get_framework(framework_id)
                
                # Apply filters if provided
                if filters and not self._matches_filters(framework, filters):
                    continue
                    
                frameworks.append(framework)
                    
            except Exception:
                # Skip invalid files
                continue
        
        # Sort frameworks
        if hasattr(ComplianceFramework, sort_by):
            # Handle name field specially to ensure alphabetical sorting
            if sort_by == "name":
                frameworks.sort(key=lambda f: f.name.lower(), reverse=reverse)
            else:
                frameworks.sort(key=lambda f: getattr(f, sort_by), reverse=reverse)

        return frameworks
    
    def count_frameworks(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count frameworks matching filters.
        
        Args:
            filters: Optional filters as field-value pairs
            
        Returns:
            Number of frameworks matching criteria
        """
        if not filters:
            # Just count files without loading
            return sum(1 for f in os.listdir(self.frameworks_dir) if f.endswith(".json.enc"))
        
        # With filters, we need to load and check each framework
        count = 0
        for filename in os.listdir(self.frameworks_dir):
            if not filename.endswith(".json.enc"):
                continue
                
            framework_id = filename.replace(".json.enc", "")
            
            try:
                framework = self.get_framework(framework_id)
                if self._matches_filters(framework, filters):
                    count += 1
            except Exception:
                # Skip invalid files
                continue
                
        return count
    
    def map_finding_to_control(
        self, 
        finding_id: str, 
        framework_id: str, 
        control_id: str
    ) -> bool:
        """
        Map a finding to a control.
        
        Args:
            finding_id: ID of the finding
            framework_id: ID of the framework
            control_id: ID of the control
            
        Returns:
            True if mapping successful, False if control not found
            
        Raises:
            FileNotFoundError: If the framework does not exist
        """
        start_time = time.time()
        
        # Check if mapping exists in memory
        if not self.mapping.map_finding_to_control(finding_id, framework_id, control_id):
            return False
            
        # Get updated framework from mapping
        framework = self.mapping.get_framework(framework_id)
        if not framework:
            return False
            
        # Save the updated framework to disk
        self._save_framework(framework)
        
        execution_time = time.time() - start_time
        if execution_time > 0.05:  # 50ms
            print(f"Warning: Mapping creation took {execution_time*1000:.2f}ms")
            
        return True
    
    def unmap_finding_from_control(
        self, 
        finding_id: str, 
        framework_id: str, 
        control_id: str
    ) -> bool:
        """
        Remove a mapping between a finding and a control.
        
        Args:
            finding_id: ID of the finding
            framework_id: ID of the framework
            control_id: ID of the control
            
        Returns:
            True if mapping removed, False if mapping or control not found
            
        Raises:
            FileNotFoundError: If the framework does not exist
        """
        start_time = time.time()
        
        # Remove mapping in memory
        if not self.mapping.unmap_finding_from_control(finding_id, framework_id, control_id):
            return False
            
        # Get updated framework from mapping
        framework = self.mapping.get_framework(framework_id)
        if not framework:
            return False
            
        # Save the updated framework to disk
        self._save_framework(framework)
        
        execution_time = time.time() - start_time
        if execution_time > 0.05:  # 50ms
            print(f"Warning: Mapping removal took {execution_time*1000:.2f}ms")
            
        return True
    
    def get_controls_for_finding(self, finding_id: str) -> Dict[str, List[ComplianceControl]]:
        """
        Get all controls mapped to a finding, grouped by framework.

        Args:
            finding_id: ID of the finding

        Returns:
            Dictionary mapping framework IDs to lists of controls
        """
        # Use the mapping's method which has been fixed to sort control IDs
        return self.mapping.get_controls_for_finding(finding_id)
    
    def get_findings_for_control(
        self, 
        framework_id: str, 
        control_id: str
    ) -> List[str]:
        """
        Get all findings mapped to a control.
        
        Args:
            framework_id: ID of the framework
            control_id: ID of the control
            
        Returns:
            List of finding IDs
            
        Raises:
            FileNotFoundError: If the framework does not exist
        """
        # Check if framework exists
        if framework_id not in self.mapping.frameworks:
            raise FileNotFoundError(f"Framework not found: {framework_id}")
            
        return self.mapping.get_findings_for_control(framework_id, control_id)
    
    def update_control_status(
        self,
        framework_id: str,
        control_id: str,
        status: Union[ComplianceControlStatus, str],
        justification: Optional[str] = None
    ) -> bool:
        """
        Update the compliance status of a control.
        
        Args:
            framework_id: ID of the framework
            control_id: ID of the control
            status: New compliance status
            justification: Optional justification for the status
            
        Returns:
            True if status updated, False if control not found
            
        Raises:
            FileNotFoundError: If the framework does not exist
        """
        start_time = time.time()
        
        # Update status in memory
        if not self.mapping.update_control_status(framework_id, control_id, status, justification):
            return False
            
        # Get updated framework from mapping
        framework = self.mapping.get_framework(framework_id)
        if not framework:
            return False
            
        # Save the updated framework to disk
        self._save_framework(framework)
        
        execution_time = time.time() - start_time
        if execution_time > 0.05:  # 50ms
            print(f"Warning: Status update took {execution_time*1000:.2f}ms")
            
        return True
    
    def get_framework_compliance_status(self, framework_id: str) -> Optional[Dict[str, int]]:
        """
        Get the compliance status for a framework.
        
        Args:
            framework_id: ID of the framework
            
        Returns:
            Dictionary mapping status values to counts, or None if framework not found
        """
        return self.mapping.get_framework_compliance_status(framework_id)
    
    def get_overall_compliance_status(self) -> Dict[str, Dict[str, int]]:
        """
        Get the compliance status across all frameworks.
        
        Returns:
            Dictionary mapping framework IDs to status counts
        """
        return self.mapping.get_overall_compliance_status()
    
    def import_framework_from_dict(self, framework_dict: Dict[str, Any]) -> ComplianceFramework:
        """
        Import a framework from a dictionary.
        
        Args:
            framework_dict: Dictionary representation of a framework
            
        Returns:
            The imported framework
            
        Raises:
            ValidationError: If validation fails
        """
        try:
            # Create the framework directly from the dictionary
            framework = ComplianceFramework(**framework_dict)

            # Save the framework
            self._save_framework(framework)

            # Add to mapping
            self.mapping.add_framework(framework)
            
            return framework
            
        except PydanticValidationError as e:
            raise ValidationError(str(e))
    
    def _save_framework(self, framework: ComplianceFramework) -> None:
        """
        Save a framework with encryption.
        
        Args:
            framework: The framework to save
        """
        # Convert to JSON
        framework_json = framework.model_dump_json().encode()
        
        # Encrypt
        encrypted_data, digest = self.crypto_manager.encrypt(framework_json)
        
        # Save encrypted data
        file_path = os.path.join(self.frameworks_dir, f"{framework.id}.json.enc")
        with open(file_path, "wb") as f:
            f.write(encrypted_data)
            
        # Save HMAC digest separately for integrity verification
        digest_path = os.path.join(self.frameworks_dir, f"{framework.id}.hmac")
        with open(digest_path, "wb") as f:
            f.write(digest)
    
    def _load_frameworks(self) -> None:
        """Load all frameworks from disk into memory."""
        for filename in os.listdir(self.frameworks_dir):
            if not filename.endswith(".json.enc"):
                continue
                
            framework_id = filename.replace(".json.enc", "")
            
            try:
                framework = self.get_framework(framework_id)
                self.mapping.add_framework(framework)
            except Exception:
                # Skip invalid files
                continue
    
    def _matches_filters(self, framework: ComplianceFramework, filters: Dict[str, Any]) -> bool:
        """
        Check if a framework matches the given filters.
        
        Args:
            framework: The framework to check
            filters: Filters as field-value pairs
            
        Returns:
            True if the framework matches all filters
        """
        for field, value in filters.items():
            if not hasattr(framework, field):
                return False
                
            field_value = getattr(framework, field)
            
            # Handle list fields like tags
            if isinstance(field_value, list) and not isinstance(value, list):
                if value not in field_value:
                    return False
            # Simple equality
            elif field_value != value:
                return False
                
        return True