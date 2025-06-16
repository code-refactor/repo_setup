import json
import os
import hashlib
from typing import Dict, List, Optional, Any
from datetime import datetime
from .models import BaseCheckpoint, CheckpointMetadata
from .interfaces import CheckpointManagerInterface
from .utils import generate_id, calculate_checksum


class BaseCheckpointManager(CheckpointManagerInterface):
    """Base checkpoint manager with common checkpoint operations"""
    
    def __init__(self, checkpoint_dir: str = "./checkpoints"):
        self.checkpoint_dir = checkpoint_dir
        os.makedirs(checkpoint_dir, exist_ok=True)
        self.checkpoints: Dict[str, BaseCheckpoint] = {}
    
    def create_checkpoint(self, entity: Any, checkpoint_type: str) -> BaseCheckpoint:
        """Create a checkpoint for an entity"""
        checkpoint_id = generate_id("ckpt_")
        
        # Serialize entity data
        if hasattr(entity, 'dict'):
            # Pydantic model
            data = entity.dict()
        elif hasattr(entity, '__dict__'):
            # Regular object
            data = {k: v for k, v in entity.__dict__.items() 
                   if not k.startswith('_')}
        else:
            # Fallback
            data = {'entity': str(entity)}
        
        # Write checkpoint data to file
        checkpoint_path = os.path.join(self.checkpoint_dir, f"{checkpoint_id}.json")
        checkpoint_data = json.dumps(data, default=str, indent=2)
        
        with open(checkpoint_path, 'w') as f:
            f.write(checkpoint_data)
        
        # Calculate checksum
        checksum = calculate_checksum(checkpoint_data.encode())
        
        # Create checkpoint metadata
        metadata = CheckpointMetadata(
            creation_time=datetime.now(),
            size_bytes=len(checkpoint_data.encode()),
            checksum=checksum,
            entity_type=type(entity).__name__,
            entity_id=getattr(entity, 'id', checkpoint_id)
        )
        
        # Create checkpoint object
        checkpoint = BaseCheckpoint(
            id=checkpoint_id,
            metadata=metadata,
            status="created",
            path=checkpoint_path,
            data=data
        )
        
        self.checkpoints[checkpoint_id] = checkpoint
        return checkpoint
    
    def validate_checkpoint(self, checkpoint_id: str) -> bool:
        """Validate a checkpoint by checking its integrity"""
        if checkpoint_id not in self.checkpoints:
            return False
        
        checkpoint = self.checkpoints[checkpoint_id]
        
        # Check if file exists
        if not os.path.exists(checkpoint.path):
            return False
        
        # Check file integrity
        try:
            with open(checkpoint.path, 'r') as f:
                content = f.read()
            
            current_checksum = calculate_checksum(content.encode())
            return current_checksum == checkpoint.metadata.checksum
        except Exception:
            return False
    
    def restore_from_checkpoint(self, checkpoint_id: str) -> bool:
        """Restore from a checkpoint"""
        if not self.validate_checkpoint(checkpoint_id):
            return False
        
        try:
            checkpoint = self.checkpoints[checkpoint_id]
            with open(checkpoint.path, 'r') as f:
                data = json.load(f)
            
            # Update checkpoint data
            checkpoint.data = data
            checkpoint.status = "restored"
            return True
        except Exception:
            return False
    
    def list_checkpoints(self, entity_id: Optional[str] = None) -> List[BaseCheckpoint]:
        """List all checkpoints, optionally filtered by entity ID"""
        checkpoints = list(self.checkpoints.values())
        
        if entity_id:
            checkpoints = [cp for cp in checkpoints 
                          if cp.metadata.entity_id == entity_id]
        
        # Sort by creation time, newest first
        return sorted(checkpoints, 
                     key=lambda cp: cp.metadata.creation_time, 
                     reverse=True)
    
    def get_latest_checkpoint(self, entity_id: str) -> Optional[BaseCheckpoint]:
        """Get the latest checkpoint for an entity"""
        entity_checkpoints = self.list_checkpoints(entity_id)
        return entity_checkpoints[0] if entity_checkpoints else None
    
    def delete_checkpoint(self, checkpoint_id: str) -> bool:
        """Delete a checkpoint"""
        if checkpoint_id not in self.checkpoints:
            return False
        
        checkpoint = self.checkpoints[checkpoint_id]
        
        # Remove file
        try:
            if os.path.exists(checkpoint.path):
                os.remove(checkpoint.path)
        except Exception:
            pass
        
        # Remove from memory
        del self.checkpoints[checkpoint_id]
        return True
    
    def cleanup_old_checkpoints(self, entity_id: str, keep_count: int = 5) -> int:
        """Clean up old checkpoints, keeping only the most recent ones"""
        entity_checkpoints = self.list_checkpoints(entity_id)
        
        if len(entity_checkpoints) <= keep_count:
            return 0
        
        # Delete old checkpoints
        checkpoints_to_delete = entity_checkpoints[keep_count:]
        deleted_count = 0
        
        for checkpoint in checkpoints_to_delete:
            if self.delete_checkpoint(checkpoint.id):
                deleted_count += 1
        
        return deleted_count
    
    def get_checkpoint_info(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a checkpoint"""
        if checkpoint_id not in self.checkpoints:
            return None
        
        checkpoint = self.checkpoints[checkpoint_id]
        
        return {
            'id': checkpoint.id,
            'entity_type': checkpoint.metadata.entity_type,
            'entity_id': checkpoint.metadata.entity_id,
            'creation_time': checkpoint.metadata.creation_time.isoformat(),
            'size_bytes': checkpoint.metadata.size_bytes,
            'status': checkpoint.status,
            'is_valid': self.validate_checkpoint(checkpoint_id),
            'path': checkpoint.path
        }