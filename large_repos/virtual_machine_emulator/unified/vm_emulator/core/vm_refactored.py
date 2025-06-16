"""
Parallel Virtual Machine implementation using the unified common library.

This module refactors the original VirtualMachine to extend BaseVirtualMachine
from the common library while preserving all parallel-specific functionality.
"""

import json
import random
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from common.core import (
    BaseVirtualMachine, VirtualMachineConfig, VMState,
    BaseProcessor, ProcessorState,
    UnifiedMemorySystem, MemoryAccessType,
    ExecutionTracer, PerformanceMetrics
)

from .instruction import Instruction, InstructionType
from .program import Program


@dataclass
class Thread:
    """Representation of a thread in the parallel VM."""
    thread_id: str
    program: Program
    pc: int  # Program counter
    registers: Dict[str, int] = field(default_factory=dict)
    stack: List[int] = field(default_factory=list)
    state: ProcessorState = ProcessorState.WAITING
    processor_id: Optional[int] = None  # Processor running this thread
    parent_thread_id: Optional[str] = None
    creation_time: int = 0
    execution_cycles: int = 0
    
    def __post_init__(self) -> None:
        """Initialize with default registers if not provided."""
        if not self.registers:
            # General purpose registers R0-R15
            for i in range(16):
                self.registers[f"R{i}"] = 0
            
            # Special registers
            self.registers["SP"] = 0  # Stack pointer
            self.registers["FP"] = 0  # Frame pointer
            self.registers["FLAGS"] = 0  # Status flags


@dataclass
class ParallelVMConfig(VirtualMachineConfig):
    """Configuration for parallel virtual machine."""
    num_processors: int = 4
    enable_race_detection: bool = True
    enable_synchronization: bool = True
    thread_scheduling_policy: str = "round_robin"


class ParallelMemorySystem(UnifiedMemorySystem):
    """Memory system with parallel-specific features."""
    
    def __init__(self, size: int = 65536, enable_tracking: bool = True):
        super().__init__(size, enable_tracking)
        
        # Parallel-specific features
        self.shared_addresses: Set[int] = set()
        self.last_writer: Dict[int, Tuple[str, int]] = {}  # Map of addr -> (thread_id, timestamp)
        self.race_conditions: List[Dict[str, Any]] = []
    
    def read(self, address: int, size: int = 1, **context) -> int:
        """Read with parallel tracking."""
        value = super().read(address, size, **context)
        
        # Check for race conditions if enabled
        if self.enable_tracking and "thread_id" in context:
            thread_id = context["thread_id"]
            timestamp = context.get("timestamp", 0)
            
            if address in self.shared_addresses and address in self.last_writer:
                last_thread, last_time = self.last_writer[address]
                if last_thread != thread_id:
                    # Potential race condition (read after write)
                    self.race_conditions.append({
                        "type": "read_after_write",
                        "address": address,
                        "reader_thread": thread_id,
                        "reader_processor": context.get("processor_id"),
                        "writer_thread": last_thread,
                        "read_time": timestamp,
                        "write_time": last_time,
                    })
        
        return value
    
    def write(self, address: int, value: int, size: int = 1, **context) -> None:
        """Write with parallel tracking."""
        super().write(address, value, size, **context)
        
        # Track parallel access patterns
        if self.enable_tracking and "thread_id" in context:
            thread_id = context["thread_id"]
            timestamp = context.get("timestamp", 0)
            
            # Mark as shared address if accessed by multiple threads
            if address in self.last_writer and self.last_writer[address][0] != thread_id:
                self.shared_addresses.add(address)
            
            # Update last writer
            self.last_writer[address] = (thread_id, timestamp)
    
    def get_race_conditions(self) -> List[Dict[str, Any]]:
        """Get detected race conditions."""
        return self.race_conditions.copy()


class ParallelProcessor(BaseProcessor):
    """Processor with parallel execution support."""
    
    def __init__(self, processor_id: int, config: Optional[Any] = None):
        super().__init__(processor_id, config)
        
        # Parallel-specific state
        self.current_thread_id: Optional[str] = None
        self.stall_cycles: int = 0
    
    def start_thread(self, thread_id: str, start_pc: int) -> None:
        """Start executing a thread on this processor."""
        self.current_thread_id = thread_id
        self.pc = start_pc
        self.state = ProcessorState.RUNNING
        self.stall_cycles = 0
    
    def execute_instruction(self, instruction) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Execute instruction with parallel VM compatibility."""
        # Handle stall cycles for instruction latency
        if self.stall_cycles > 0:
            self.stall_cycles -= 1
            return (False, None)
        
        # Convert to BaseInstruction format if needed
        if hasattr(instruction, 'type') and hasattr(instruction, 'operands'):
            from common.core import BaseInstruction
            base_instruction = BaseInstruction(
                name=getattr(instruction, 'name', 'UNKNOWN'),
                type=instruction.type,
                operands=instruction.operands if hasattr(instruction, 'operands') else [],
                latency=getattr(instruction, 'latency', 1)
            )
        else:
            base_instruction = instruction
        
        # Execute using base implementation
        completed, side_effects = super().execute_instruction(base_instruction)
        
        # Set stall cycles based on instruction latency
        if completed and hasattr(instruction, 'latency'):
            self.stall_cycles = instruction.latency - 1
        
        return completed, side_effects


class ParallelVirtualMachine(BaseVirtualMachine):
    """
    Parallel Virtual Machine extending the unified base implementation.
    
    This class adds parallel computing features like threading, synchronization,
    and race condition detection while using the common VM infrastructure.
    """
    
    def __init__(self, config: Optional[ParallelVMConfig] = None):
        """Initialize the parallel virtual machine."""
        self.parallel_config = config or ParallelVMConfig()
        
        # Initialize base VM with common functionality
        super().__init__(self.parallel_config)
        
        # Parallel-specific state
        self.threads: Dict[str, Thread] = {}
        self.ready_queue: List[str] = []
        self.waiting_threads: Dict[str, Dict[str, Any]] = {}
        
        # Synchronization primitives
        self.locks: Dict[int, Optional[str]] = {}  # Map of lock_id -> thread_id
        self.semaphores: Dict[int, int] = {}  # Map of semaphore_id -> count
        self.barriers: Dict[int, Set[str]] = {}  # Map of barrier_id -> set of thread_ids
        
        # Performance tracking
        self.context_switches = 0
        
        # Debug mode for tests
        self.debug_mode = False
    
    def _create_memory_system(self) -> ParallelMemorySystem:
        """Create parallel-specific memory system."""
        return ParallelMemorySystem(
            size=self.config.memory_size,
            enable_tracking=self.config.enable_tracing
        )
    
    def _create_processors(self) -> List[ParallelProcessor]:
        """Create multiple processors for parallel execution."""
        return [
            ParallelProcessor(processor_id=i)
            for i in range(self.parallel_config.num_processors)
        ]
    
    def load_program(self, program: Program) -> str:
        """Load a program into the VM."""
        program_id = str(uuid.uuid4())
        self.loaded_programs[program_id] = program
        
        # Load the data segment into memory
        for addr, value in program.data_segment.items():
            self.memory.write(addr, value, context={"operation": "program_load"})
        
        if self.tracer:
            self.tracer.log_event("program_loaded", {
                "program_id": program_id,
                "timestamp": self.global_clock
            })
        
        return program_id
    
    def create_thread(
        self,
        program_id: str,
        entry_point: Optional[int] = None,
        parent_thread_id: Optional[str] = None,
    ) -> str:
        """Create a new thread to execute a program."""
        if program_id not in self.loaded_programs:
            raise ValueError(f"Program not found: {program_id}")
        
        program = self.loaded_programs[program_id]
        
        if entry_point is None:
            entry_point = program.entry_point
        
        thread_id = str(uuid.uuid4())
        thread = Thread(
            thread_id=thread_id,
            program=program,
            pc=entry_point,
            parent_thread_id=parent_thread_id,
            creation_time=self.global_clock,
        )
        
        self.threads[thread_id] = thread
        self.ready_queue.append(thread_id)
        
        # Log thread creation
        if self.tracer:
            self.tracer.log_event("thread_created", {
                "thread_id": thread_id,
                "parent_thread_id": parent_thread_id,
                "program_id": program_id,
                "entry_point": entry_point
            })
        
        return thread_id
    
    def _execute_cycle(self) -> None:
        """Execute one cycle of parallel execution."""
        # Schedule threads to processors
        self._schedule_threads()
        
        # Execute one cycle on each processor
        active_processors = 0
        for processor in self.processors:
            if processor.is_busy() and processor.current_thread_id:
                active_processors += 1
                thread_id = processor.current_thread_id
                thread = self.threads[thread_id]
                
                # Get the current instruction
                instruction = thread.program.get_instruction(processor.pc)
                
                if instruction is None:
                    # End of program
                    thread.state = ProcessorState.TERMINATED
                    processor.state = ProcessorState.IDLE
                    processor.current_thread_id = None
                    
                    if self.tracer:
                        self.tracer.log_event("thread_terminated", {
                            "thread_id": thread_id,
                            "processor_id": processor.processor_id
                        })
                    continue
                
                # Execute the instruction
                completed, side_effects = processor.execute_instruction(instruction)
                thread.execution_cycles += 1
                
                if self.metrics:
                    self.metrics.increment_instructions()
                
                # Process side effects
                if side_effects:
                    self._handle_side_effects(processor, thread, instruction, side_effects)
                
                # Update thread state
                thread.pc = processor.pc
                thread.registers = processor.registers.copy()
        
        # Update metrics
        if self.metrics:
            self.metrics.increment_cycles()
            self.metrics.take_snapshot(
                thread_count=len(self.threads),
                active_processors=active_processors
            )
    
    def _should_continue_execution(self) -> bool:
        """Check if execution should continue."""
        # Continue if there are active processors, ready threads, or waiting threads
        active_processors = sum(1 for p in self.processors if p.is_busy())
        return active_processors > 0 or len(self.ready_queue) > 0 or len(self.waiting_threads) > 0
    
    def _schedule_threads(self) -> None:
        """Schedule threads to processors using round-robin."""
        # Find idle processors
        idle_processors = [p for p in self.processors if not p.is_busy()]
        
        # Assign threads to idle processors
        while idle_processors and self.ready_queue:
            processor = idle_processors.pop(0)
            thread_id = self.ready_queue.pop(0)
            thread = self.threads[thread_id]
            
            # Start the thread on the processor
            processor.start_thread(thread_id, thread.pc)
            thread.state = ProcessorState.RUNNING
            thread.processor_id = processor.processor_id
            
            # Copy thread registers to processor
            processor.registers = thread.registers.copy()
            
            # Record context switch
            self.context_switches += 1
            
            if self.tracer:
                self.tracer.log_context_switch(
                    from_thread=None,
                    to_thread=thread_id,
                    processor_id=processor.processor_id,
                    reason="schedule"
                )
    
    def _handle_side_effects(
        self,
        processor: ParallelProcessor,
        thread: Thread,
        instruction,
        side_effects: Dict[str, Any],
    ) -> None:
        """Handle side effects from instruction execution."""
        context = {
            "processor_id": processor.processor_id,
            "thread_id": thread.thread_id,
            "timestamp": self.global_clock
        }
        
        # Handle memory reads
        if "memory_read" in side_effects:
            addr = side_effects["memory_read"]
            value = self.memory.read(address=addr, **context)
            
            # Set the value in the register
            if hasattr(instruction, 'operands') and instruction.operands:
                dest_reg = instruction.operands[0]
                processor.registers[dest_reg] = value
            
            if self.tracer:
                self.tracer.log_memory_access("read", addr, value, thread_id=thread.thread_id)
        
        # Handle memory writes
        if "memory_write" in side_effects:
            addr, value = side_effects["memory_write"]
            self.memory.write(address=addr, value=value, **context)
            
            if self.tracer:
                self.tracer.log_memory_access("write", addr, value, thread_id=thread.thread_id)
        
        # Handle synchronization operations
        if "sync_lock" in side_effects:
            self._handle_lock_acquire(side_effects["sync_lock"], processor, thread)
        
        if "sync_unlock" in side_effects:
            self._handle_lock_release(side_effects["sync_unlock"], processor, thread)
        
        # Handle thread operations
        if "halt" in side_effects:
            thread.state = ProcessorState.TERMINATED
            processor.state = ProcessorState.IDLE
            processor.current_thread_id = None
            
            if self.tracer:
                self.tracer.log_event("thread_halted", {"thread_id": thread.thread_id})
        
        if "yield" in side_effects:
            # Put thread back in ready queue
            self.ready_queue.append(thread.thread_id)
            processor.state = ProcessorState.IDLE
            processor.current_thread_id = None
    
    def _handle_lock_acquire(self, lock_id: int, processor: ParallelProcessor, thread: Thread) -> None:
        """Handle lock acquisition."""
        if lock_id not in self.locks:
            self.locks[lock_id] = None
        
        if self.locks[lock_id] is None:
            # Lock is free, acquire it
            self.locks[lock_id] = thread.thread_id
            
            if self.tracer:
                self.tracer.log_synchronization("acquire", f"lock_{lock_id}", "success",
                                              processor.processor_id, thread.thread_id)
        else:
            # Lock is held, block the thread
            processor.state = ProcessorState.WAITING
            thread.state = ProcessorState.WAITING
            
            self.waiting_threads[thread.thread_id] = {
                "reason": "lock",
                "lock_id": lock_id,
                "blocked_at": self.global_clock
            }
            
            if self.tracer:
                self.tracer.log_synchronization("acquire", f"lock_{lock_id}", "blocked",
                                              processor.processor_id, thread.thread_id)
    
    def _handle_lock_release(self, lock_id: int, processor: ParallelProcessor, thread: Thread) -> None:
        """Handle lock release."""
        if lock_id not in self.locks:
            self.locks[lock_id] = None
        
        # Release the lock
        self.locks[lock_id] = None
        
        # Wake up the first thread waiting for this lock
        waiting_threads = [
            (waiting_id, waiting_info) 
            for waiting_id, waiting_info in self.waiting_threads.items()
            if waiting_info["reason"] == "lock" and waiting_info["lock_id"] == lock_id
        ]
        
        if waiting_threads:
            # Sort by blocked time and wake up the first one
            waiting_threads.sort(key=lambda x: x[1].get("blocked_at", 0))
            waiting_id, waiting_info = waiting_threads[0]
            
            # Remove from waiting and add to ready queue
            del self.waiting_threads[waiting_id]
            self.ready_queue.append(waiting_id)
            
            # Assign lock to the unblocked thread
            self.locks[lock_id] = waiting_id
            
            if self.tracer:
                self.tracer.log_synchronization("release", f"lock_{lock_id}", "success",
                                              processor.processor_id, thread.thread_id)
    
    def get_processor_utilization(self) -> float:
        """Calculate processor utilization across all processors."""
        if self.global_clock == 0:
            return 0.0
        
        # Sum execution cycles across all threads
        total_execution_cycles = sum(t.execution_cycles for t in self.threads.values())
        
        # Calculate utilization
        max_possible_cycles = self.global_clock * self.parallel_config.num_processors
        utilization = (total_execution_cycles / max_possible_cycles) * 100
        
        return utilization
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get VM statistics including parallel-specific metrics."""
        base_stats = super().get_statistics()
        
        parallel_stats = {
            "num_processors": self.parallel_config.num_processors,
            "threads": len(self.threads),
            "context_switches": self.context_switches,
            "processor_utilization": self.get_processor_utilization(),
            "race_conditions": len(self.memory.get_race_conditions()),
            "active_threads": len([t for t in self.threads.values() if t.state == ProcessorState.RUNNING]),
            "waiting_threads": len(self.waiting_threads),
            "ready_threads": len(self.ready_queue),
        }
        
        base_stats.update(parallel_stats)
        return base_stats
    
    def get_race_conditions(self) -> List[Dict[str, Any]]:
        """Get detected race conditions."""
        return self.memory.get_race_conditions()
    
    def _reset_additional_state(self) -> None:
        """Reset parallel-specific state."""
        self.threads.clear()
        self.ready_queue.clear()
        self.waiting_threads.clear()
        self.locks.clear()
        self.semaphores.clear()
        self.barriers.clear()
        self.context_switches = 0
        
        # Reset memory race detection
        if hasattr(self.memory, 'shared_addresses'):
            self.memory.shared_addresses.clear()
            self.memory.last_writer.clear()
            self.memory.race_conditions.clear()


# Backwards compatibility alias
VirtualMachine = ParallelVirtualMachine