"""Basic memory system for the virtual machine."""

from enum import Enum, auto
from typing import Dict, List, Optional, Set, Tuple, Union


class MemoryAccessType(Enum):
    """Types of memory accesses."""
    READ = auto()
    WRITE = auto()
    READ_MODIFY_WRITE = auto()  # For atomic operations like CAS


class MemoryAccess:
    """Representation of a memory access operation."""
    
    def __init__(
        self,
        address: int,
        access_type: MemoryAccessType,
        processor_id: int,
        thread_id: str,
        timestamp: int,
        value: Optional[int] = None,
    ):
        self.address = address
        self.access_type = access_type
        self.processor_id = processor_id
        self.thread_id = thread_id
        self.timestamp = timestamp  # Global clock timestamp
        self.value = value  # For WRITE and READ_MODIFY_WRITE
    
    def __str__(self) -> str:
        action = self.access_type.name
        if self.value is not None:
            return f"[{self.timestamp}] P{self.processor_id} T{self.thread_id} {action} addr={self.address} value={self.value}"
        return f"[{self.timestamp}] P{self.processor_id} T{self.thread_id} {action} addr={self.address}"


class MemorySystem:
    """
    Base memory system for the virtual machine.
    
    This is a simple memory model with no caching. More complex models
    implementing cache coherence protocols will extend this.
    """
    
    def __init__(self, size: int = 2**16):
        """
        Initialize the memory system.
        
        Args:
            size: Size of the memory in words (not bytes)
        """
        self.size = size
        self.memory = [0] * size
        self.access_log: List[MemoryAccess] = []
    
    def read(
        self, address: int, processor_id: int, thread_id: str, timestamp: int
    ) -> int:
        """
        Read a value from memory.
        
        Args:
            address: Memory address to read from
            processor_id: ID of the processor performing the read
            thread_id: ID of the thread performing the read
            timestamp: Current global clock value
            
        Returns:
            Value read from memory
        """
        if not 0 <= address < self.size:
            raise IndexError(f"Memory address out of bounds: {address}")
        
        value = self.memory[address]
        
        # Log the memory access
        access = MemoryAccess(
            address=address,
            access_type=MemoryAccessType.READ,
            processor_id=processor_id,
            thread_id=thread_id,
            timestamp=timestamp,
        )
        self.access_log.append(access)
        
        return value
    
    def write(
        self, address: int, value: int, processor_id: int, thread_id: str, timestamp: int
    ) -> None:
        """
        Write a value to memory.
        
        Args:
            address: Memory address to write to
            value: Value to write
            processor_id: ID of the processor performing the write
            thread_id: ID of the thread performing the write
            timestamp: Current global clock value
        """
        if not 0 <= address < self.size:
            raise IndexError(f"Memory address out of bounds: {address}")
        
        self.memory[address] = value
        
        # Log the memory access
        access = MemoryAccess(
            address=address,
            access_type=MemoryAccessType.WRITE,
            processor_id=processor_id,
            thread_id=thread_id,
            timestamp=timestamp,
            value=value,
        )
        self.access_log.append(access)
    
    def compare_and_swap(
        self,
        address: int,
        expected: int,
        new_value: int,
        processor_id: int,
        thread_id: str,
        timestamp: int,
    ) -> bool:
        """
        Atomic compare-and-swap operation.
        
        Args:
            address: Memory address to operate on
            expected: Expected current value
            new_value: New value to set if current matches expected
            processor_id: ID of the processor performing the operation
            thread_id: ID of the thread performing the operation
            timestamp: Current global clock value
            
        Returns:
            True if the swap was performed, False otherwise
        """
        if not 0 <= address < self.size:
            raise IndexError(f"Memory address out of bounds: {address}")
        
        # Perform the CAS operation atomically
        current = self.memory[address]
        success = current == expected
        
        if success:
            self.memory[address] = new_value
        
        # Log the memory access
        access = MemoryAccess(
            address=address,
            access_type=MemoryAccessType.READ_MODIFY_WRITE,
            processor_id=processor_id,
            thread_id=thread_id,
            timestamp=timestamp,
            value=new_value if success else None,
        )
        self.access_log.append(access)
        
        return success
    
    def get_access_history(
        self,
        address: Optional[int] = None,
        processor_id: Optional[int] = None,
        thread_id: Optional[str] = None,
    ) -> List[MemoryAccess]:
        """
        Get a filtered history of memory accesses.
        
        Args:
            address: Filter by memory address
            processor_id: Filter by processor ID
            thread_id: Filter by thread ID
            
        Returns:
            List of memory access logs matching the filters
        """
        result = self.access_log
        
        if address is not None:
            result = [access for access in result if access.address == address]
        
        if processor_id is not None:
            result = [access for access in result if access.processor_id == processor_id]
        
        if thread_id is not None:
            result = [access for access in result if access.thread_id == thread_id]
        
        return result
    
    def clear_logs(self) -> None:
        """Clear all access logs."""
        self.access_log = []
        
    def get_memory_dump(self, start: int = 0, length: Optional[int] = None) -> List[int]:
        """
        Get a dump of memory contents.
        
        Args:
            start: Starting address
            length: Number of words to include, or None for all remaining memory
            
        Returns:
            List of memory values
        """
        if length is None:
            length = self.size - start
            
        end = min(start + length, self.size)
        return self.memory[start:end]