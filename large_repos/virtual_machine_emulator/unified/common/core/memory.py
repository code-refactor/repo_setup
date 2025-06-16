"""
Unified memory system for the virtual machine.

This module provides memory abstraction that supports both simple access patterns
and advanced features like protection, segmentation, and access tracking.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Set, Tuple, Union


class MemoryAccessType(Enum):
    """Types of memory access."""
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()


@dataclass
class MemoryAccess:
    """Record of a memory access."""
    address: int
    access_type: MemoryAccessType
    size: int
    timestamp: int
    processor_id: Optional[int] = None
    thread_id: Optional[str] = None
    value: Optional[int] = None
    context: Optional[Dict[str, Any]] = None


@dataclass
class MemorySegment:
    """A memory segment with base address, size, and properties."""
    base_address: int
    size: int
    name: str = ""
    readable: bool = True
    writable: bool = True
    executable: bool = False
    
    def contains_address(self, address: int) -> bool:
        """Check if an address is within this segment."""
        return self.base_address <= address < self.base_address + self.size
    
    def get_offset(self, address: int) -> int:
        """Get the offset of an address within this segment."""
        if not self.contains_address(address):
            raise ValueError(f"Address 0x{address:x} not in segment")
        return address - self.base_address


class MemoryInterface(ABC):
    """Standard memory access interface."""
    
    @abstractmethod
    def read(self, address: int, size: int = 1) -> int:
        """Read from memory."""
        pass
    
    @abstractmethod
    def write(self, address: int, value: int, size: int = 1) -> None:
        """Write to memory."""
        pass
    
    @abstractmethod
    def is_valid_address(self, address: int) -> bool:
        """Check if address is valid."""
        pass


class UnifiedMemorySystem(MemoryInterface):
    """
    Unified memory system supporting both simple and advanced access patterns.
    
    This class provides the foundation for both parallel and security memory models,
    with extension points for specialized functionality.
    """
    
    def __init__(self, size: int = 65536, enable_tracking: bool = True):
        """Initialize the unified memory system."""
        self.size = size
        self.memory = bytearray(size)
        self.enable_tracking = enable_tracking
        
        # Memory segments
        self.segments: List[MemorySegment] = []
        self._create_default_segments()
        
        # Access tracking
        if self.enable_tracking:
            self.access_log: List[MemoryAccess] = []
            self.access_count: Dict[int, int] = {}
        
        # Extension points for subclasses
        self._initialize_additional_features()
    
    def _create_default_segments(self) -> None:
        """Create default memory segments."""
        # Single unified segment by default - subclasses can override
        self.segments.append(MemorySegment(
            base_address=0,
            size=self.size,
            name="unified",
            readable=True,
            writable=True,
            executable=False
        ))
    
    def _initialize_additional_features(self) -> None:
        """Initialize additional features - to be implemented by subclasses."""
        pass
    
    def add_segment(self, segment: MemorySegment) -> MemorySegment:
        """Add a memory segment."""
        # Check for overlaps
        for existing in self.segments:
            if (segment.base_address < existing.base_address + existing.size and
                segment.base_address + segment.size > existing.base_address):
                raise ValueError(f"Segment overlaps with existing segment")
        
        # Check bounds
        if segment.base_address + segment.size > self.size:
            raise ValueError(f"Segment exceeds memory size")
        
        self.segments.append(segment)
        return segment
    
    def find_segment(self, address: int) -> Optional[MemorySegment]:
        """Find the segment containing the given address."""
        for segment in self.segments:
            if segment.contains_address(address):
                return segment
        return None
    
    def read(self, address: int, size: int = 1, **context) -> int:
        """Read from memory."""
        if not self.is_valid_address(address):
            raise ValueError(f"Invalid memory address: 0x{address:x}")
        
        if address + size > self.size:
            raise ValueError(f"Read beyond memory bounds")
        
        # Check segment permissions
        segment = self.find_segment(address)
        if segment and not segment.readable:
            raise PermissionError(f"Read not allowed in segment {segment.name}")
        
        # Perform the read
        if size == 1:
            value = self.memory[address]
        elif size == 2:
            value = int.from_bytes(self.memory[address:address+2], byteorder='little')
        elif size == 4:
            value = int.from_bytes(self.memory[address:address+4], byteorder='little')
        else:
            raise ValueError(f"Unsupported read size: {size}")
        
        # Track the access
        if self.enable_tracking:
            self._track_access(address, MemoryAccessType.READ, size, value, context)
        
        return value
    
    def write(self, address: int, value: int, size: int = 1, **context) -> None:
        """Write to memory."""
        if not self.is_valid_address(address):
            raise ValueError(f"Invalid memory address: 0x{address:x}")
        
        if address + size > self.size:
            raise ValueError(f"Write beyond memory bounds")
        
        # Check segment permissions
        segment = self.find_segment(address)
        if segment and not segment.writable:
            raise PermissionError(f"Write not allowed in segment {segment.name}")
        
        # Perform the write
        if size == 1:
            self.memory[address] = value & 0xFF
        elif size == 2:
            self.memory[address:address+2] = (value & 0xFFFF).to_bytes(2, byteorder='little')
        elif size == 4:
            self.memory[address:address+4] = (value & 0xFFFFFFFF).to_bytes(4, byteorder='little')
        else:
            raise ValueError(f"Unsupported write size: {size}")
        
        # Track the access
        if self.enable_tracking:
            self._track_access(address, MemoryAccessType.WRITE, size, value, context)
    
    def read_bytes(self, address: int, size: int) -> bytes:
        """Read bytes from memory."""
        if not self.is_valid_address(address):
            raise ValueError(f"Invalid memory address: 0x{address:x}")
        
        if address + size > self.size:
            raise ValueError(f"Read beyond memory bounds")
        
        return bytes(self.memory[address:address+size])
    
    def write_bytes(self, address: int, data: bytes, **context) -> None:
        """Write bytes to memory."""
        if not self.is_valid_address(address):
            raise ValueError(f"Invalid memory address: 0x{address:x}")
        
        if address + len(data) > self.size:
            raise ValueError(f"Write beyond memory bounds")
        
        # Check segment permissions
        segment = self.find_segment(address)
        if segment and not segment.writable:
            raise PermissionError(f"Write not allowed in segment {segment.name}")
        
        self.memory[address:address+len(data)] = data
        
        # Track the access
        if self.enable_tracking:
            self._track_access(address, MemoryAccessType.WRITE, len(data), None, context)
    
    def is_valid_address(self, address: int) -> bool:
        """Check if address is valid."""
        return 0 <= address < self.size
    
    def _track_access(self, address: int, access_type: MemoryAccessType, size: int, 
                     value: Optional[int], context: Dict[str, Any]) -> None:
        """Track a memory access."""
        access = MemoryAccess(
            address=address,
            access_type=access_type,
            size=size,
            timestamp=context.get("timestamp", 0),
            processor_id=context.get("processor_id"),
            thread_id=context.get("thread_id"),
            value=value,
            context=context
        )
        
        self.access_log.append(access)
        self.access_count[address] = self.access_count.get(address, 0) + 1
    
    def get_access_log(self, address: Optional[int] = None, 
                      access_type: Optional[MemoryAccessType] = None) -> List[MemoryAccess]:
        """Get memory access log with optional filtering."""
        if not self.enable_tracking:
            return []
        
        result = self.access_log
        
        if address is not None:
            result = [a for a in result if a.address == address]
        
        if access_type is not None:
            result = [a for a in result if a.access_type == access_type]
        
        return result
    
    def get_access_pattern(self) -> Dict[int, int]:
        """Get memory access pattern (address -> count)."""
        if not self.enable_tracking:
            return {}
        return self.access_count.copy()
    
    def get_memory_map(self) -> List[Dict[str, Any]]:
        """Get memory map information."""
        return [
            {
                "name": segment.name,
                "base_address": f"0x{segment.base_address:08x}",
                "size": segment.size,
                "end_address": f"0x{segment.base_address + segment.size - 1:08x}",
                "permissions": {
                    "readable": segment.readable,
                    "writable": segment.writable,
                    "executable": segment.executable
                }
            }
            for segment in self.segments
        ]
    
    def dump_memory(self, start_address: int = 0, size: Optional[int] = None) -> bytes:
        """Dump memory contents."""
        if size is None:
            size = self.size - start_address
        
        if start_address + size > self.size:
            raise ValueError(f"Dump beyond memory bounds")
        
        return bytes(self.memory[start_address:start_address + size])
    
    def compare_and_swap(self, address: int, expected: int, new_value: int, **context) -> bool:
        """Atomic compare-and-swap operation."""
        if not self.is_valid_address(address):
            raise ValueError(f"Invalid memory address: 0x{address:x}")
        
        current_value = self.read(address, size=4, **context)
        
        if current_value == expected:
            self.write(address, new_value, size=4, **context)
            return True
        
        return False
    
    def clear(self) -> None:
        """Clear all memory contents."""
        for i in range(self.size):
            self.memory[i] = 0
    
    def reset(self) -> None:
        """Reset memory system to initial state."""
        self.clear()
        
        if self.enable_tracking:
            self.access_log.clear()
            self.access_count.clear()
        
        # Allow subclasses to reset additional state
        self._reset_additional_state()
    
    def _reset_additional_state(self) -> None:
        """Reset additional state - to be implemented by subclasses."""
        pass