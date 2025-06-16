"""Virtual Machine Emulator for Parallel Computing Research."""

# Import the refactored implementation that uses the common library
from .core.vm_wrapper import VirtualMachine
from .core.vm_refactored import ParallelVirtualMachine, ParallelVMConfig

# Legacy imports for backwards compatibility
from .core.vm_refactored import Thread
from .core.instruction import Instruction, InstructionType
from .core.program import Program

__version__ = "0.1.0"

# Make the main classes available at package level
__all__ = [
    'VirtualMachine',           # Backwards compatible wrapper
    'ParallelVirtualMachine',   # New refactored implementation
    'ParallelVMConfig',         # Configuration class
    'Thread',                   # Thread representation
    'Instruction',              # Instruction class
    'InstructionType',          # Instruction types
    'Program',                  # Program class
]
