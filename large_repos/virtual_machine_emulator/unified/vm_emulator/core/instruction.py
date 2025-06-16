"""Instruction set for the virtual machine."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple, Union


class InstructionType(Enum):
    """Types of instructions supported by the VM."""
    COMPUTE = auto()  # Arithmetic/logic operations
    MEMORY = auto()   # Memory read/write operations
    BRANCH = auto()   # Conditional and unconditional jumps
    SYNC = auto()     # Synchronization operations
    SYSTEM = auto()   # System calls and VM control


@dataclass
class Instruction:
    """Representation of a single VM instruction."""
    opcode: str
    type: InstructionType
    operands: List[Any]
    latency: int  # Cycles required to execute
    
    def __str__(self) -> str:
        operand_str = ", ".join(str(op) for op in self.operands)
        return f"{self.opcode} {operand_str}"


class InstructionSet:
    """Defines the instruction set for the virtual machine."""
    
    # Compute operations
    ADD = "ADD"       # Add
    SUB = "SUB"       # Subtract
    MUL = "MUL"       # Multiply
    DIV = "DIV"       # Divide
    MOD = "MOD"       # Modulo
    AND = "AND"       # Logical AND
    OR = "OR"         # Logical OR
    XOR = "XOR"       # Logical XOR
    NOT = "NOT"       # Logical NOT
    SHL = "SHL"       # Shift left
    SHR = "SHR"       # Shift right
    
    # Memory operations
    LOAD = "LOAD"     # Load from memory
    STORE = "STORE"   # Store to memory
    
    # Branch operations
    JMP = "JMP"       # Unconditional jump
    JZ = "JZ"         # Jump if zero
    JNZ = "JNZ"       # Jump if not zero
    JGT = "JGT"       # Jump if greater than
    JLT = "JLT"       # Jump if less than
    
    # Synchronization operations
    LOCK = "LOCK"     # Acquire lock
    UNLOCK = "UNLOCK" # Release lock
    FENCE = "FENCE"   # Memory fence
    CAS = "CAS"       # Compare and swap
    
    # System operations
    HALT = "HALT"     # Stop execution
    YIELD = "YIELD"   # Yield to scheduler
    SPAWN = "SPAWN"   # Create new thread
    JOIN = "JOIN"     # Wait for thread completion
    
    # Mapping of instruction opcodes to their types and latencies
    INSTRUCTION_SPECS: Dict[str, Tuple[InstructionType, int]] = {
        # Compute operations - types and cycle counts
        ADD: (InstructionType.COMPUTE, 1),
        SUB: (InstructionType.COMPUTE, 1),
        MUL: (InstructionType.COMPUTE, 3),
        DIV: (InstructionType.COMPUTE, 5),
        MOD: (InstructionType.COMPUTE, 5),
        AND: (InstructionType.COMPUTE, 1),
        OR: (InstructionType.COMPUTE, 1),
        XOR: (InstructionType.COMPUTE, 1),
        NOT: (InstructionType.COMPUTE, 1),
        SHL: (InstructionType.COMPUTE, 1),
        SHR: (InstructionType.COMPUTE, 1),
        
        # Memory operations
        LOAD: (InstructionType.MEMORY, 2),
        STORE: (InstructionType.MEMORY, 2),
        
        # Branch operations
        JMP: (InstructionType.BRANCH, 1),
        JZ: (InstructionType.BRANCH, 1),
        JNZ: (InstructionType.BRANCH, 1),
        JGT: (InstructionType.BRANCH, 1),
        JLT: (InstructionType.BRANCH, 1),
        
        # Synchronization operations
        LOCK: (InstructionType.SYNC, 10),
        UNLOCK: (InstructionType.SYNC, 5),
        FENCE: (InstructionType.SYNC, 10),
        CAS: (InstructionType.SYNC, 8),
        
        # System operations
        HALT: (InstructionType.SYSTEM, 1),
        YIELD: (InstructionType.SYSTEM, 5),
        SPAWN: (InstructionType.SYSTEM, 50),
        JOIN: (InstructionType.SYSTEM, 5),
    }
    
    @classmethod
    def create_instruction(cls, opcode: str, operands: List[Any]) -> Instruction:
        """Create an instruction with the given opcode and operands."""
        if opcode not in cls.INSTRUCTION_SPECS:
            raise ValueError(f"Unknown opcode: {opcode}")
        
        instr_type, latency = cls.INSTRUCTION_SPECS[opcode]
        return Instruction(opcode=opcode, type=instr_type, operands=operands, latency=latency)