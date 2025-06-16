"""
Core functionality that can be used by all VM packages.

This module provides the fundamental building blocks for virtual machine
implementations including CPU, memory, instructions, tracing, and metrics.
"""

from .vm import BaseVirtualMachine, VirtualMachineConfig, VirtualMachineInterface, VMState
from .cpu import BaseProcessor, ProcessorConfig, ProcessorInterface, ProcessorState
from .memory import UnifiedMemorySystem, MemoryInterface, MemorySegment, MemoryAccess, MemoryAccessType
from .instruction import BaseInstruction, InstructionType, InstructionSet, SimpleInstructionDecoder, InstructionExecutor
from .trace import ExecutionTracer, TraceEvent, EventType
from .metrics import PerformanceMetrics, PerformanceSnapshot
from .visualization import VisualizationSystem
from .utils import *

__all__ = [
    # VM core
    'BaseVirtualMachine', 'VirtualMachineConfig', 'VirtualMachineInterface', 'VMState',
    
    # CPU
    'BaseProcessor', 'ProcessorConfig', 'ProcessorInterface', 'ProcessorState',
    
    # Memory
    'UnifiedMemorySystem', 'MemoryInterface', 'MemorySegment', 'MemoryAccess', 'MemoryAccessType',
    
    # Instructions
    'BaseInstruction', 'InstructionType', 'InstructionSet', 'SimpleInstructionDecoder', 'InstructionExecutor',
    
    # Tracing
    'ExecutionTracer', 'TraceEvent', 'EventType',
    
    # Metrics
    'PerformanceMetrics', 'PerformanceSnapshot',
    
    # Visualization
    'VisualizationSystem',
]
