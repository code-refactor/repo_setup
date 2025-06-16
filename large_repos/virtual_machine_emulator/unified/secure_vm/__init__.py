"""
Secure Systems Vulnerability Simulator.

A specialized virtual machine emulator designed for security research and education,
providing a controlled environment to safely demonstrate and analyze memory corruption,
code injection, privilege escalation, and other low-level security vulnerabilities
without real-world consequences.
"""

# Import the refactored implementation that uses the common library
from .emulator_refactored import SecurityVirtualMachine, SecurityVMConfig, ExecutionResult, ForensicLog

# Legacy imports for backwards compatibility 
from .emulator import VirtualMachine  # Original implementation as fallback
from .memory import Memory, MemoryProtection, MemoryProtectionLevel, MemoryPermission
from .cpu import CPU, PrivilegeLevel, CPUException

__version__ = "0.1.0"

# Make the main classes available at package level
__all__ = [
    'VirtualMachine',           # Original implementation (backwards compatible)
    'SecurityVirtualMachine',   # New refactored implementation
    'SecurityVMConfig',         # Configuration class
    'ExecutionResult',          # Execution result class
    'ForensicLog',              # Forensic logging class
    'Memory',                   # Memory management
    'MemoryProtection',         # Memory protection
    'MemoryProtectionLevel',    # Protection levels
    'MemoryPermission',         # Memory permissions
    'CPU',                      # CPU implementation
    'PrivilegeLevel',           # Privilege levels
    'CPUException',             # CPU exceptions
]