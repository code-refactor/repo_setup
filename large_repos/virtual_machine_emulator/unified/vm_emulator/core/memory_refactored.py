"""Refactored memory system extending the common unified memory system."""

from typing import Dict, List, Optional, Set, Tuple, Union

from common.core.memory import UnifiedMemorySystem, MemoryAccess, MemoryAccessType, MemorySegment


class ParallelMemorySystem(UnifiedMemorySystem):
    """
    Parallel memory system extending the unified memory system.
    
    This memory system specializes in parallel access patterns with support for
    race condition detection, memory consistency, and access pattern analysis.
    """
    
    def __init__(self, size: int = 65536, enable_tracking: bool = True):
        """Initialize the parallel memory system."""
        super().__init__(size=size, enable_tracking=enable_tracking)
        
        # Parallel-specific state
        self.access_history: List['MemoryAccessRecord'] = []
        self.concurrent_accesses: Dict[int, List[Tuple[str, int]]] = {}  # addr -> [(thread_id, timestamp)]
        
        # Memory consistency model
        self.memory_model = "sequential_consistency"  # Can be changed to other models
        self.pending_writes: Dict[int, List[Tuple[int, str, int]]] = {}  # addr -> [(value, thread_id, timestamp)]
    
    def _initialize_additional_features(self) -> None:
        """Initialize parallel-specific memory features."""
        # Create segments for parallel execution
        self._create_parallel_segments()
    
    def _create_parallel_segments(self) -> None:
        """Create memory segments optimized for parallel execution."""
        # Clear default unified segment and create specialized segments
        self.segments.clear()
        
        # Code segment (read-only, executable)
        self.segments.append(MemorySegment(
            base_address=0,
            size=16384,  # 16KB
            name="code",
            readable=True,
            writable=False,
            executable=True
        ))
        
        # Data segment (read-write)
        self.segments.append(MemorySegment(
            base_address=16384,
            size=32768,  # 32KB
            name="data",
            readable=True,
            writable=True,
            executable=False
        ))
        
        # Stack segment (read-write)
        self.segments.append(MemorySegment(
            base_address=49152,
            size=16384,  # 16KB
            name="stack",
            readable=True,
            writable=True,
            executable=False
        ))
    
    def read(
        self, 
        address: int, 
        processor_id: int, 
        thread_id: str, 
        timestamp: int,
        size: int = 4
    ) -> int:
        """
        Read a value from memory with parallel-specific tracking.
        
        Args:
            address: Memory address to read from
            processor_id: ID of the processor performing the read
            thread_id: ID of the thread performing the read
            timestamp: Current global clock value
            size: Size of the read operation in bytes
            
        Returns:
            Value read from memory
        """
        # Use the base class read method with additional context
        value = super().read(
            address=address,
            size=size,
            processor_id=processor_id,
            thread_id=thread_id,
            timestamp=timestamp
        )
        
        # Track parallel-specific access patterns
        if self.enable_tracking:
            self._track_parallel_access(address, "READ", processor_id, thread_id, timestamp)
        
        return value
    
    def write(
        self, 
        address: int, 
        value: int, 
        processor_id: int, 
        thread_id: str, 
        timestamp: int,
        size: int = 4
    ) -> None:
        """
        Write a value to memory with parallel-specific tracking.
        
        Args:
            address: Memory address to write to
            value: Value to write
            processor_id: ID of the processor performing the write
            thread_id: ID of the thread performing the write
            timestamp: Current global clock value
            size: Size of the write operation in bytes
        """
        # Use the base class write method with additional context
        super().write(
            address=address,
            value=value,
            size=size,
            processor_id=processor_id,
            thread_id=thread_id,
            timestamp=timestamp
        )
        
        # Track parallel-specific access patterns
        if self.enable_tracking:
            self._track_parallel_access(address, "WRITE", processor_id, thread_id, timestamp, value)
    
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
        Atomic compare-and-swap operation with parallel tracking.
        
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
        # Use the base class CAS method with additional context
        success = super().compare_and_swap(
            address=address,
            expected=expected,
            new_value=new_value,
            processor_id=processor_id,
            thread_id=thread_id,
            timestamp=timestamp
        )
        
        # Track the atomic operation
        if self.enable_tracking:
            self._track_parallel_access(
                address, "CAS", processor_id, thread_id, timestamp, 
                new_value if success else None
            )
        
        return success
    
    def _track_parallel_access(
        self, 
        address: int, 
        access_type: str, 
        processor_id: int, 
        thread_id: str, 
        timestamp: int,
        value: Optional[int] = None
    ) -> None:
        """Track memory access for parallel analysis."""
        # Record concurrent accesses to the same address
        if address not in self.concurrent_accesses:
            self.concurrent_accesses[address] = []
        
        self.concurrent_accesses[address].append((thread_id, timestamp))
        
        # Keep only recent accesses (within a window)
        access_window = 10  # Keep accesses within 10 time units
        self.concurrent_accesses[address] = [
            (tid, ts) for tid, ts in self.concurrent_accesses[address]
            if timestamp - ts <= access_window
        ]
        
        # Create access record
        access_record = MemoryAccessRecord(
            address=address,
            access_type=access_type,
            processor_id=processor_id,
            thread_id=thread_id,
            timestamp=timestamp,
            value=value
        )
        
        self.access_history.append(access_record)
        
        # Limit access history size
        max_history = 10000
        if len(self.access_history) > max_history:
            self.access_history = self.access_history[-max_history:]
    
    def get_access_history(
        self,
        address: Optional[int] = None,
        processor_id: Optional[int] = None,
        thread_id: Optional[str] = None,
    ) -> List['MemoryAccessRecord']:
        """
        Get filtered history of memory accesses.
        
        Args:
            address: Filter by memory address
            processor_id: Filter by processor ID
            thread_id: Filter by thread ID
            
        Returns:
            List of memory access records matching the filters
        """
        result = self.access_history
        
        if address is not None:
            result = [access for access in result if access.address == address]
        
        if processor_id is not None:
            result = [access for access in result if access.processor_id == processor_id]
        
        if thread_id is not None:
            result = [access for access in result if access.thread_id == thread_id]
        
        return result
    
    def get_concurrent_accesses(self, address: int) -> List[Tuple[str, int]]:
        """Get recent concurrent accesses to an address."""
        return self.concurrent_accesses.get(address, [])
    
    def detect_potential_races(self) -> List[Dict[str, Union[str, int]]]:
        """Detect potential race conditions in memory access patterns."""
        races = []
        
        for address, accesses in self.concurrent_accesses.items():
            if len(accesses) > 1:
                # Check for overlapping accesses from different threads
                for i, (thread1, time1) in enumerate(accesses):
                    for j, (thread2, time2) in enumerate(accesses[i+1:], i+1):
                        if thread1 != thread2 and abs(time1 - time2) <= 2:
                            # Potential race condition
                            races.append({
                                "address": address,
                                "thread1": thread1,
                                "thread2": thread2,
                                "time1": time1,
                                "time2": time2,
                                "time_diff": abs(time1 - time2)
                            })
        
        return races
    
    def get_memory_access_statistics(self) -> Dict[str, Union[int, float]]:
        """Get statistics about memory access patterns."""
        if not self.access_history:
            return {}
        
        total_accesses = len(self.access_history)
        read_accesses = sum(1 for access in self.access_history if access.access_type == "READ")
        write_accesses = sum(1 for access in self.access_history if access.access_type == "WRITE")
        cas_accesses = sum(1 for access in self.access_history if access.access_type == "CAS")
        
        # Calculate access patterns by thread
        thread_accesses = {}
        for access in self.access_history:
            thread_accesses[access.thread_id] = thread_accesses.get(access.thread_id, 0) + 1
        
        # Calculate access patterns by address
        address_accesses = {}
        for access in self.access_history:
            address_accesses[access.address] = address_accesses.get(access.address, 0) + 1
        
        return {
            "total_accesses": total_accesses,
            "read_accesses": read_accesses,
            "write_accesses": write_accesses,
            "cas_accesses": cas_accesses,
            "read_ratio": read_accesses / total_accesses if total_accesses > 0 else 0,
            "write_ratio": write_accesses / total_accesses if total_accesses > 0 else 0,
            "unique_threads": len(thread_accesses),
            "unique_addresses": len(address_accesses),
            "hottest_address": max(address_accesses.items(), key=lambda x: x[1])[0] if address_accesses else None,
            "max_accesses_per_address": max(address_accesses.values()) if address_accesses else 0,
        }
    
    def clear_logs(self) -> None:
        """Clear all access logs and parallel-specific state."""
        super().reset()  # This clears the base class logs
        self.access_history.clear()
        self.concurrent_accesses.clear()
        self.pending_writes.clear()
    
    def _reset_additional_state(self) -> None:
        """Reset parallel-specific state."""
        self.access_history.clear()
        self.concurrent_accesses.clear()
        self.pending_writes.clear()


class MemoryAccessRecord:
    """Enhanced memory access record for parallel analysis."""
    
    def __init__(
        self,
        address: int,
        access_type: str,
        processor_id: int,
        thread_id: str,
        timestamp: int,
        value: Optional[int] = None,
    ):
        self.address = address
        self.access_type = access_type
        self.processor_id = processor_id
        self.thread_id = thread_id
        self.timestamp = timestamp
        self.value = value
    
    def __str__(self) -> str:
        action = self.access_type
        if self.value is not None:
            return f"[{self.timestamp}] P{self.processor_id} T{self.thread_id} {action} addr={self.address} value={self.value}"
        return f"[{self.timestamp}] P{self.processor_id} T{self.thread_id} {action} addr={self.address}"