"""
Base virtual machine framework for both parallel and security use cases.

This module provides the core virtual machine abstraction that can be extended
for specific use cases while maintaining common functionality.
"""

import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Union

from .cpu import BaseProcessor
from .memory import UnifiedMemorySystem
from .trace import ExecutionTracer
from .metrics import PerformanceMetrics


class VMState(Enum):
    """States of the virtual machine."""
    IDLE = auto()      # VM not running
    RUNNING = auto()   # VM executing
    PAUSED = auto()    # VM paused
    FINISHED = auto()  # VM execution completed


@dataclass
class VirtualMachineConfig:
    """Configuration for the virtual machine."""
    memory_size: int = 65536
    enable_tracing: bool = True
    enable_metrics: bool = True
    random_seed: Optional[int] = None


class VirtualMachineInterface(ABC):
    """Standard interface for all VM implementations."""
    
    @abstractmethod
    def load_program(self, program: Any) -> str:
        """Load a program into the VM."""
        pass
    
    @abstractmethod
    def run(self, max_cycles: Optional[int] = None) -> int:
        """Execute the loaded program."""
        pass
    
    @abstractmethod
    def step(self) -> bool:
        """Execute single instruction, return if more to execute."""
        pass
    
    @abstractmethod
    def reset(self) -> None:
        """Reset VM to initial state."""
        pass
    
    @abstractmethod
    def get_state(self) -> VMState:
        """Get current VM state."""
        pass


class BaseVirtualMachine(VirtualMachineInterface):
    """
    Base virtual machine implementation providing common functionality.
    
    This class provides the foundation for both parallel and security VMs,
    with extension points for specialized functionality.
    """
    
    def __init__(self, config: Optional[VirtualMachineConfig] = None):
        """Initialize the base virtual machine."""
        self.config = config or VirtualMachineConfig()
        
        # Core components
        self.memory = self._create_memory_system()
        self.processors = self._create_processors()
        
        # State management
        self.state = VMState.IDLE
        self.global_clock = 0
        self.start_time = 0.0
        self.end_time = 0.0
        
        # Program management
        self.loaded_programs: Dict[str, Any] = {}
        
        # Tracing and metrics
        if self.config.enable_tracing:
            self.tracer = ExecutionTracer()
        else:
            self.tracer = None
            
        if self.config.enable_metrics:
            self.metrics = PerformanceMetrics()
        else:
            self.metrics = None
        
        # Set random seed if provided
        if self.config.random_seed is not None:
            import random
            random.seed(self.config.random_seed)
    
    def _create_memory_system(self) -> UnifiedMemorySystem:
        """Create the memory system for this VM."""
        return UnifiedMemorySystem(size=self.config.memory_size)
    
    def _create_processors(self) -> List[BaseProcessor]:
        """Create the processor(s) for this VM."""
        # Default to single processor - subclasses can override
        return [BaseProcessor(processor_id=0)]
    
    def load_program(self, program: Any) -> str:
        """Load a program into the VM."""
        program_id = str(uuid.uuid4())
        self.loaded_programs[program_id] = program
        
        # Subclasses can override this method to handle program loading
        self._load_program_into_memory(program)
        
        if self.tracer:
            self.tracer.log_event("program_loaded", {
                "program_id": program_id,
                "timestamp": self.global_clock
            })
        
        return program_id
    
    def _load_program_into_memory(self, program: Any) -> None:
        """Load program into memory - to be implemented by subclasses."""
        pass
    
    def start(self) -> None:
        """Start or resume VM execution."""
        if self.state == VMState.IDLE:
            self.start_time = time.time()
        
        self.state = VMState.RUNNING
        
        if self.tracer:
            self.tracer.log_event("vm_started", {"timestamp": self.global_clock})
    
    def pause(self) -> None:
        """Pause VM execution."""
        self.state = VMState.PAUSED
        
        if self.tracer:
            self.tracer.log_event("vm_paused", {"timestamp": self.global_clock})
    
    def stop(self) -> None:
        """Stop VM execution and clean up."""
        self.state = VMState.FINISHED
        self.end_time = time.time()
        
        if self.tracer:
            self.tracer.log_event("vm_stopped", {"timestamp": self.global_clock})
    
    def step(self) -> bool:
        """Execute a single clock cycle of the VM."""
        if self.state != VMState.RUNNING:
            return self.state != VMState.FINISHED
        
        # Execute one cycle - to be implemented by subclasses
        self._execute_cycle()
        
        # Increment the global clock
        self.global_clock += 1
        
        # Check if execution should continue
        if self._should_continue_execution():
            return True
        else:
            self.stop()
            return False
    
    def _execute_cycle(self) -> None:
        """Execute one cycle of the VM - to be implemented by subclasses."""
        pass
    
    def _should_continue_execution(self) -> bool:
        """Check if execution should continue - to be implemented by subclasses."""
        return True
    
    def run(self, max_cycles: Optional[int] = None) -> int:
        """Run the VM until completion or max_cycles is reached."""
        self.start()
        
        cycles_executed = 0
        running = True
        
        while running and (max_cycles is None or cycles_executed < max_cycles):
            running = self.step()
            cycles_executed += 1
        
        if running and max_cycles is not None and cycles_executed >= max_cycles:
            self.pause()
        
        return cycles_executed
    
    def reset(self) -> None:
        """Reset the VM to initial state."""
        # Reset processors
        for processor in self.processors:
            processor.reset()
        
        # Reset memory
        self.memory.reset()
        
        # Reset state
        self.state = VMState.IDLE
        self.global_clock = 0
        self.start_time = 0.0
        self.end_time = 0.0
        
        # Reset tracing and metrics
        if self.tracer:
            self.tracer.reset()
        if self.metrics:
            self.metrics.reset()
        
        # Subclasses can override this to reset additional state
        self._reset_additional_state()
    
    def _reset_additional_state(self) -> None:
        """Reset additional state - to be implemented by subclasses."""
        pass
    
    def get_state(self) -> VMState:
        """Get current VM state."""
        return self.state
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get various VM statistics."""
        base_stats = {
            "processors": len(self.processors),
            "global_clock": self.global_clock,
            "runtime_seconds": self.end_time - self.start_time if self.end_time > 0 else 0,
        }
        
        if self.metrics:
            base_stats.update(self.metrics.get_metrics())
        
        return base_stats
    
    def get_trace_events(self, **filters) -> List[Dict[str, Any]]:
        """Get filtered trace events."""
        if self.tracer:
            return self.tracer.get_events(**filters)
        return []