"""
Compatibility wrapper for the VirtualMachine class.

This module provides a compatibility layer that allows existing code to use
the refactored VirtualMachine while maintaining the original API.
"""

from typing import Any, Dict, List, Optional, Set, Tuple, Union
from .vm_refactored import ParallelVirtualMachine, ParallelVMConfig, Thread
from .program import Program


class VirtualMachine:
    """
    Compatibility wrapper for the refactored parallel virtual machine.
    
    This class maintains the original API while delegating to the new
    implementation based on the common library.
    """
    
    def __init__(
        self,
        num_processors: int = 4,
        memory_size: int = 2**16,
        random_seed: Optional[int] = None,
    ):
        """Initialize the VM with the original API."""
        # Create config from old-style parameters
        config = ParallelVMConfig(
            num_processors=num_processors,
            memory_size=memory_size,
            random_seed=random_seed,
            enable_tracing=True,
            enable_metrics=True
        )
        
        # Initialize the refactored VM
        self._vm = ParallelVirtualMachine(config)
        
        # Expose commonly used attributes for backwards compatibility
        self.num_processors = num_processors
        self.memory = self._vm.memory
        self.state = self._vm.state
        self.global_clock = self._vm.global_clock
        self.processors = self._vm.processors
        self.threads = self._vm.threads
        self.ready_queue = self._vm.ready_queue
        self.waiting_threads = self._vm.waiting_threads
        self.loaded_programs = self._vm.loaded_programs
        self.shared_addresses = getattr(self._vm.memory, 'shared_addresses', set())
        self.last_writer = getattr(self._vm.memory, 'last_writer', {})
        self.race_conditions = getattr(self._vm.memory, 'race_conditions', [])
        self.locks = self._vm.locks
        self.semaphores = self._vm.semaphores
        self.barriers = self._vm.barriers
        self.random_seed = random_seed
        self.debug_mode = self._vm.debug_mode
        self.instruction_count = getattr(self._vm.metrics, 'instructions_executed', 0) if self._vm.metrics else 0
        self.context_switches = self._vm.context_switches
        self.start_time = self._vm.start_time
        self.end_time = self._vm.end_time
        self.execution_trace = []  # Will be populated from tracer
    
    def _sync_attributes(self) -> None:
        """Sync attributes from the internal VM for backwards compatibility."""
        self.state = self._vm.state
        self.global_clock = self._vm.global_clock
        self.threads = self._vm.threads
        self.ready_queue = self._vm.ready_queue
        self.waiting_threads = self._vm.waiting_threads
        self.loaded_programs = self._vm.loaded_programs
        self.locks = self._vm.locks
        self.semaphores = self._vm.semaphores
        self.barriers = self._vm.barriers
        self.debug_mode = self._vm.debug_mode
        self.context_switches = self._vm.context_switches
        self.start_time = self._vm.start_time
        self.end_time = self._vm.end_time
        
        # Sync memory attributes
        if hasattr(self._vm.memory, 'shared_addresses'):
            self.shared_addresses = self._vm.memory.shared_addresses
        if hasattr(self._vm.memory, 'last_writer'):
            self.last_writer = self._vm.memory.last_writer
        if hasattr(self._vm.memory, 'race_conditions'):
            self.race_conditions = self._vm.memory.race_conditions
        
        # Sync metrics
        if self._vm.metrics:
            self.instruction_count = self._vm.metrics.instructions_executed
        
        # Convert tracer events to execution trace format for compatibility
        if self._vm.tracer:
            self.execution_trace = []
            for event in self._vm.tracer.get_events():
                trace_entry = {
                    "timestamp": event.timestamp,
                    "event": event.event_type.name.lower(),
                }
                if event.processor_id is not None:
                    trace_entry["processor_id"] = event.processor_id
                if event.thread_id is not None:
                    trace_entry["thread_id"] = event.thread_id
                if event.address is not None:
                    trace_entry["address"] = event.address
                if event.data:
                    trace_entry.update(event.data)
                
                self.execution_trace.append(trace_entry)
    
    def load_program(self, program: Program) -> str:
        """Load a program into the VM."""
        result = self._vm.load_program(program)
        self._sync_attributes()
        return result
    
    def create_thread(
        self,
        program_id: str,
        entry_point: Optional[int] = None,
        parent_thread_id: Optional[str] = None,
    ) -> str:
        """Create a new thread to execute a program."""
        result = self._vm.create_thread(program_id, entry_point, parent_thread_id)
        self._sync_attributes()
        return result
    
    def start(self) -> None:
        """Start or resume VM execution."""
        self._vm.start()
        self._sync_attributes()
    
    def pause(self) -> None:
        """Pause VM execution."""
        self._vm.pause()
        self._sync_attributes()
    
    def stop(self) -> None:
        """Stop VM execution and clean up."""
        self._vm.stop()
        self._sync_attributes()
    
    def step(self) -> bool:
        """Execute a single clock cycle of the VM."""
        result = self._vm.step()
        self._sync_attributes()
        return result
    
    def run(self, max_cycles: Optional[int] = None) -> int:
        """Run the VM until completion or max_cycles is reached."""
        result = self._vm.run(max_cycles)
        self._sync_attributes()
        return result
    
    def get_processor_utilization(self) -> float:
        """Calculate processor utilization across all processors."""
        return self._vm.get_processor_utilization()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get various VM statistics."""
        return self._vm.get_statistics()
    
    def get_trace_events(
        self,
        event_types: Optional[List[str]] = None,
        thread_id: Optional[str] = None,
        processor_id: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Get filtered trace events."""
        # Convert new tracer events to old format
        if not self._vm.tracer:
            return []
        
        # Convert event types to new format
        from common.core import EventType
        event_type_filter = None
        if event_types:
            # Map old event names to new event types
            event_mapping = {
                "instruction_start": EventType.INSTRUCTION,
                "instruction_complete": EventType.INSTRUCTION,
                "memory_read": EventType.MEMORY_ACCESS,
                "memory_write": EventType.MEMORY_ACCESS,
                "context_switch": EventType.CONTEXT_SWITCH,
                "thread_created": EventType.CUSTOM,
                "thread_terminated": EventType.CUSTOM,
                "vm_started": EventType.CUSTOM,
                "vm_stopped": EventType.CUSTOM,
            }
            
            # Get events from tracer and filter
            events = self._vm.tracer.get_events(
                processor_id=processor_id,
                thread_id=thread_id,
                start_time=start_time,
                end_time=end_time
            )
            
            # Convert to old format and filter by event types
            result = []
            for event in events:
                trace_entry = {
                    "timestamp": event.timestamp,
                    "event": event.event_type.name.lower(),
                }
                if event.processor_id is not None:
                    trace_entry["processor_id"] = event.processor_id
                if event.thread_id is not None:
                    trace_entry["thread_id"] = event.thread_id
                if event.address is not None:
                    trace_entry["address"] = event.address
                if event.data:
                    trace_entry.update(event.data)
                
                # Filter by event types if specified
                if not event_types or trace_entry["event"] in event_types:
                    result.append(trace_entry)
            
            return result
        
        return self._vm.get_trace_events()
    
    def get_race_conditions(self) -> List[Dict[str, Any]]:
        """Get detected race conditions."""
        return self._vm.get_race_conditions()
    
    def reset(self) -> None:
        """Reset the VM to initial state."""
        self._vm.reset()
        self._sync_attributes()
    
    def __getattr__(self, name: str) -> Any:
        """Delegate unknown attributes to the internal VM."""
        if hasattr(self._vm, name):
            return getattr(self._vm, name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")