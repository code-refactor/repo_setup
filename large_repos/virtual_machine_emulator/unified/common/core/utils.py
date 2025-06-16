"""
Common utilities and helpers for the unified virtual machine.

This module provides utility functions and classes that are used
across different components of the VM system.
"""

import hashlib
import random
import struct
from typing import Any, Dict, List, Optional, Tuple, Union


def align_address(address: int, alignment: int) -> int:
    """Align an address to the specified boundary."""
    return (address + alignment - 1) & ~(alignment - 1)


def is_power_of_two(n: int) -> bool:
    """Check if a number is a power of two."""
    return n > 0 and (n & (n - 1)) == 0


def next_power_of_two(n: int) -> int:
    """Find the next power of two greater than or equal to n."""
    if n <= 0:
        return 1
    if is_power_of_two(n):
        return n
    
    power = 1
    while power < n:
        power <<= 1
    return power


def bytes_to_int(data: bytes, byteorder: str = 'little', signed: bool = False) -> int:
    """Convert bytes to integer."""
    return int.from_bytes(data, byteorder=byteorder, signed=signed)


def int_to_bytes(value: int, length: int, byteorder: str = 'little', signed: bool = False) -> bytes:
    """Convert integer to bytes."""
    return value.to_bytes(length, byteorder=byteorder, signed=signed)


def pack_instruction(opcode: int, operands: List[int], format_str: str = 'I') -> bytes:
    """Pack instruction into binary format."""
    if format_str == 'I':  # 32-bit instruction
        if len(operands) == 0:
            return struct.pack('<I', opcode)
        elif len(operands) == 1:
            return struct.pack('<II', opcode, operands[0])
        elif len(operands) == 2:
            return struct.pack('<III', opcode, operands[0], operands[1])
        else:
            raise ValueError("Too many operands for 32-bit instruction")
    else:
        raise ValueError(f"Unsupported instruction format: {format_str}")


def unpack_instruction(data: bytes, format_str: str = 'I') -> Tuple[int, List[int]]:
    """Unpack instruction from binary format."""
    if format_str == 'I':  # 32-bit instruction
        if len(data) == 4:
            opcode = struct.unpack('<I', data)[0]
            return opcode, []
        elif len(data) == 8:
            opcode, operand1 = struct.unpack('<II', data)
            return opcode, [operand1]
        elif len(data) == 12:
            opcode, operand1, operand2 = struct.unpack('<III', data)
            return opcode, [operand1, operand2]
        else:
            raise ValueError(f"Invalid instruction length: {len(data)}")
    else:
        raise ValueError(f"Unsupported instruction format: {format_str}")


class BitField:
    """Utility class for bit field operations."""
    
    def __init__(self, value: int = 0):
        """Initialize bit field with optional value."""
        self.value = value
    
    def get_bit(self, position: int) -> bool:
        """Get the value of a specific bit."""
        return bool(self.value & (1 << position))
    
    def set_bit(self, position: int, value: bool = True) -> None:
        """Set a specific bit."""
        if value:
            self.value |= (1 << position)
        else:
            self.value &= ~(1 << position)
    
    def get_bits(self, start: int, length: int) -> int:
        """Get a range of bits."""
        mask = (1 << length) - 1
        return (self.value >> start) & mask
    
    def set_bits(self, start: int, length: int, value: int) -> None:
        """Set a range of bits."""
        mask = (1 << length) - 1
        self.value &= ~(mask << start)
        self.value |= (value & mask) << start
    
    def __int__(self) -> int:
        """Convert to integer."""
        return self.value
    
    def __str__(self) -> str:
        """Convert to binary string."""
        return f"0b{self.value:b}"


class AddressSpace:
    """Utility class for address space management."""
    
    def __init__(self, size: int):
        """Initialize address space with given size."""
        self.size = size
        self.allocated_ranges: List[Tuple[int, int]] = []
    
    def allocate(self, size: int, alignment: int = 1) -> Optional[int]:
        """Allocate a contiguous block of addresses."""
        # Find a suitable gap
        for start in range(0, self.size - size + 1, alignment):
            end = start + size
            
            # Check if this range overlaps with any allocated range
            overlaps = False
            for alloc_start, alloc_end in self.allocated_ranges:
                if not (end <= alloc_start or start >= alloc_end):
                    overlaps = True
                    break
            
            if not overlaps:
                # Found a suitable range
                self.allocated_ranges.append((start, end))
                self.allocated_ranges.sort()  # Keep sorted for efficiency
                return start
        
        return None  # No suitable range found
    
    def deallocate(self, address: int, size: int) -> bool:
        """Deallocate a block of addresses."""
        target_range = (address, address + size)
        
        if target_range in self.allocated_ranges:
            self.allocated_ranges.remove(target_range)
            return True
        
        return False
    
    def is_allocated(self, address: int) -> bool:
        """Check if an address is allocated."""
        for start, end in self.allocated_ranges:
            if start <= address < end:
                return True
        return False
    
    def get_free_space(self) -> int:
        """Get the amount of free space."""
        allocated_size = sum(end - start for start, end in self.allocated_ranges)
        return self.size - allocated_size
    
    def get_fragmentation(self) -> float:
        """Calculate fragmentation ratio."""
        if not self.allocated_ranges:
            return 0.0
        
        # Count gaps between allocated ranges
        gaps = 0
        for i in range(len(self.allocated_ranges) - 1):
            if self.allocated_ranges[i][1] < self.allocated_ranges[i + 1][0]:
                gaps += 1
        
        return gaps / len(self.allocated_ranges)


class CircularBuffer:
    """Circular buffer implementation for efficient logging."""
    
    def __init__(self, size: int):
        """Initialize circular buffer with given size."""
        self.size = size
        self.buffer: List[Any] = [None] * size
        self.head = 0
        self.tail = 0
        self.count = 0
    
    def push(self, item: Any) -> None:
        """Add an item to the buffer."""
        self.buffer[self.head] = item
        self.head = (self.head + 1) % self.size
        
        if self.count < self.size:
            self.count += 1
        else:
            # Buffer is full, advance tail
            self.tail = (self.tail + 1) % self.size
    
    def pop(self) -> Optional[Any]:
        """Remove and return the oldest item."""
        if self.count == 0:
            return None
        
        item = self.buffer[self.tail]
        self.buffer[self.tail] = None
        self.tail = (self.tail + 1) % self.size
        self.count -= 1
        
        return item
    
    def peek(self, index: int = 0) -> Optional[Any]:
        """Peek at an item without removing it."""
        if index >= self.count:
            return None
        
        actual_index = (self.tail + index) % self.size
        return self.buffer[actual_index]
    
    def is_empty(self) -> bool:
        """Check if buffer is empty."""
        return self.count == 0
    
    def is_full(self) -> bool:
        """Check if buffer is full."""
        return self.count == self.size
    
    def clear(self) -> None:
        """Clear the buffer."""
        for i in range(self.size):
            self.buffer[i] = None
        self.head = 0
        self.tail = 0
        self.count = 0
    
    def to_list(self) -> List[Any]:
        """Convert buffer contents to list."""
        result = []
        for i in range(self.count):
            result.append(self.peek(i))
        return result


class Random:
    """Deterministic random number generator for reproducible execution."""
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize with optional seed."""
        self.rng = random.Random(seed)
    
    def randint(self, a: int, b: int) -> int:
        """Generate random integer in range [a, b]."""
        return self.rng.randint(a, b)
    
    def random(self) -> float:
        """Generate random float in range [0.0, 1.0)."""
        return self.rng.random()
    
    def choice(self, sequence: List[Any]) -> Any:
        """Choose random element from sequence."""
        return self.rng.choice(sequence)
    
    def shuffle(self, sequence: List[Any]) -> None:
        """Shuffle sequence in place."""
        self.rng.shuffle(sequence)
    
    def bytes(self, length: int) -> bytes:
        """Generate random bytes."""
        return bytes(self.randint(0, 255) for _ in range(length))


def hash_data(data: Union[str, bytes]) -> str:
    """Generate SHA-256 hash of data."""
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    return hashlib.sha256(data).hexdigest()


def format_address(address: int, width: int = 8) -> str:
    """Format address as hexadecimal string."""
    return f"0x{address:0{width}x}"


def format_size(size: int) -> str:
    """Format size in human-readable format."""
    units = ['B', 'KB', 'MB', 'GB']
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    if unit_index == 0:
        return f"{size} {units[unit_index]}"
    else:
        return f"{size:.2f} {units[unit_index]}"


def validate_range(value: int, min_val: int, max_val: int, name: str) -> None:
    """Validate that a value is within a specified range."""
    if not (min_val <= value <= max_val):
        raise ValueError(f"{name} must be between {min_val} and {max_val}, got {value}")


def create_lookup_table(items: List[Tuple[str, Any]]) -> Dict[str, Any]:
    """Create a lookup table from a list of (key, value) pairs."""
    return dict(items)


class Stopwatch:
    """Simple stopwatch for timing operations."""
    
    def __init__(self):
        """Initialize stopwatch."""
        self.start_time = 0.0
        self.end_time = 0.0
        self.running = False
    
    def start(self) -> None:
        """Start the stopwatch."""
        import time
        self.start_time = time.time()
        self.running = True
    
    def stop(self) -> float:
        """Stop the stopwatch and return elapsed time."""
        import time
        if self.running:
            self.end_time = time.time()
            self.running = False
        return self.elapsed()
    
    def elapsed(self) -> float:
        """Get elapsed time."""
        if self.running:
            import time
            return time.time() - self.start_time
        else:
            return self.end_time - self.start_time
    
    def reset(self) -> None:
        """Reset the stopwatch."""
        self.start_time = 0.0
        self.end_time = 0.0
        self.running = False