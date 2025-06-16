"""
Instruction system framework for the unified virtual machine.

This module provides the common instruction handling that can be extended
for both parallel computing and security research use cases.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Union


class InstructionType(Enum):
    """Categories of instruction types for the VM."""
    COMPUTE = auto()     # Arithmetic and logical operations
    MEMORY = auto()      # Memory operations (load, store)
    BRANCH = auto()      # Control flow (jump, branch)
    SYSTEM = auto()      # System operations
    SYNC = auto()        # Synchronization operations
    SPECIAL = auto()     # Special operations


@dataclass
class BaseInstruction:
    """Base instruction representation."""
    name: str
    type: InstructionType
    operands: List[str]
    latency: int = 1
    opcode: Optional[int] = None
    
    def __str__(self) -> str:
        if self.operands:
            return f"{self.name} {', '.join(self.operands)}"
        return self.name


class InstructionDecoder(ABC):
    """Abstract base class for instruction decoding."""
    
    @abstractmethod
    def decode(self, raw_instruction: Union[int, bytes, str]) -> BaseInstruction:
        """Decode a raw instruction into a BaseInstruction object."""
        pass


class InstructionSet:
    """Instruction set definition and management."""
    
    def __init__(self):
        """Initialize the instruction set."""
        self.instructions: Dict[str, Dict[str, Any]] = {}
        self.opcodes: Dict[int, str] = {}
        self._initialize_base_instructions()
    
    def _initialize_base_instructions(self) -> None:
        """Initialize base instruction set."""
        # Arithmetic instructions
        self.add_instruction("ADD", InstructionType.COMPUTE, operands=3, latency=1, opcode=0x01)
        self.add_instruction("SUB", InstructionType.COMPUTE, operands=3, latency=1, opcode=0x02)
        self.add_instruction("MUL", InstructionType.COMPUTE, operands=3, latency=3, opcode=0x03)
        self.add_instruction("DIV", InstructionType.COMPUTE, operands=3, latency=10, opcode=0x04)
        
        # Memory instructions
        self.add_instruction("LOAD", InstructionType.MEMORY, operands=2, latency=3, opcode=0x10)
        self.add_instruction("STORE", InstructionType.MEMORY, operands=2, latency=3, opcode=0x11)
        
        # Branch instructions
        self.add_instruction("JMP", InstructionType.BRANCH, operands=1, latency=1, opcode=0x20)
        self.add_instruction("JZ", InstructionType.BRANCH, operands=1, latency=1, opcode=0x21)
        self.add_instruction("JNZ", InstructionType.BRANCH, operands=1, latency=1, opcode=0x22)
        
        # System instructions
        self.add_instruction("NOP", InstructionType.SYSTEM, operands=0, latency=1, opcode=0x00)
        self.add_instruction("HALT", InstructionType.SYSTEM, operands=0, latency=1, opcode=0xFF)
    
    def add_instruction(self, name: str, instr_type: InstructionType, 
                       operands: int = 0, latency: int = 1, opcode: Optional[int] = None) -> None:
        """Add an instruction to the instruction set."""
        self.instructions[name] = {
            "type": instr_type,
            "operands": operands,
            "latency": latency,
            "opcode": opcode
        }
        
        if opcode is not None:
            self.opcodes[opcode] = name
    
    def get_instruction_info(self, name: str) -> Optional[Dict[str, Any]]:
        """Get information about an instruction."""
        return self.instructions.get(name)
    
    def get_instruction_by_opcode(self, opcode: int) -> Optional[str]:
        """Get instruction name by opcode."""
        return self.opcodes.get(opcode)
    
    def create_instruction(self, name: str, operands: List[str]) -> BaseInstruction:
        """Create an instruction instance."""
        info = self.get_instruction_info(name)
        if not info:
            raise ValueError(f"Unknown instruction: {name}")
        
        return BaseInstruction(
            name=name,
            type=info["type"],
            operands=operands,
            latency=info["latency"],
            opcode=info["opcode"]
        )


class SimpleInstructionDecoder(InstructionDecoder):
    """Simple instruction decoder for text-based instructions."""
    
    def __init__(self, instruction_set: InstructionSet):
        """Initialize the decoder with an instruction set."""
        self.instruction_set = instruction_set
    
    def decode(self, raw_instruction: Union[int, bytes, str]) -> BaseInstruction:
        """Decode a raw instruction."""
        if isinstance(raw_instruction, str):
            return self._decode_text_instruction(raw_instruction)
        elif isinstance(raw_instruction, int):
            return self._decode_opcode_instruction(raw_instruction)
        elif isinstance(raw_instruction, bytes):
            return self._decode_binary_instruction(raw_instruction)
        else:
            raise ValueError(f"Unsupported instruction format: {type(raw_instruction)}")
    
    def _decode_text_instruction(self, text: str) -> BaseInstruction:
        """Decode a text instruction like 'ADD R1, R2, R3'."""
        parts = text.strip().split()
        if not parts:
            raise ValueError("Empty instruction")
        
        name = parts[0].upper()
        operands = []
        
        if len(parts) > 1:
            # Parse operands, removing commas
            operand_text = " ".join(parts[1:])
            operands = [op.strip().rstrip(',') for op in operand_text.split(',')]
        
        return self.instruction_set.create_instruction(name, operands)
    
    def _decode_opcode_instruction(self, opcode: int) -> BaseInstruction:
        """Decode an instruction from its opcode."""
        name = self.instruction_set.get_instruction_by_opcode(opcode)
        if not name:
            raise ValueError(f"Unknown opcode: 0x{opcode:02x}")
        
        return self.instruction_set.create_instruction(name, [])
    
    def _decode_binary_instruction(self, binary: bytes) -> BaseInstruction:
        """Decode a binary instruction."""
        if len(binary) < 1:
            raise ValueError("Empty binary instruction")
        
        opcode = binary[0]
        return self._decode_opcode_instruction(opcode)


class InstructionExecutor:
    """Handles instruction execution logic."""
    
    def __init__(self, instruction_set: InstructionSet):
        """Initialize the executor with an instruction set."""
        self.instruction_set = instruction_set
        self.custom_handlers: Dict[str, callable] = {}
    
    def add_custom_handler(self, instruction_name: str, handler: callable) -> None:
        """Add a custom handler for an instruction."""
        self.custom_handlers[instruction_name] = handler
    
    def execute(self, instruction: BaseInstruction, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an instruction and return side effects."""
        # Check for custom handler first
        if instruction.name in self.custom_handlers:
            return self.custom_handlers[instruction.name](instruction, context)
        
        # Default execution logic based on instruction type
        side_effects: Dict[str, Any] = {}
        
        if instruction.type == InstructionType.COMPUTE:
            self._execute_compute(instruction, context, side_effects)
        elif instruction.type == InstructionType.MEMORY:
            self._execute_memory(instruction, context, side_effects)
        elif instruction.type == InstructionType.BRANCH:
            self._execute_branch(instruction, context, side_effects)
        elif instruction.type == InstructionType.SYSTEM:
            self._execute_system(instruction, context, side_effects)
        
        return side_effects
    
    def _execute_compute(self, instruction: BaseInstruction, context: Dict[str, Any], 
                        side_effects: Dict[str, Any]) -> None:
        """Execute compute instruction."""
        side_effects["type"] = "compute"
        side_effects["instruction"] = instruction.name
    
    def _execute_memory(self, instruction: BaseInstruction, context: Dict[str, Any], 
                       side_effects: Dict[str, Any]) -> None:
        """Execute memory instruction."""
        side_effects["type"] = "memory"
        side_effects["instruction"] = instruction.name
    
    def _execute_branch(self, instruction: BaseInstruction, context: Dict[str, Any], 
                       side_effects: Dict[str, Any]) -> None:
        """Execute branch instruction."""
        side_effects["type"] = "branch"
        side_effects["instruction"] = instruction.name
    
    def _execute_system(self, instruction: BaseInstruction, context: Dict[str, Any], 
                       side_effects: Dict[str, Any]) -> None:
        """Execute system instruction."""
        side_effects["type"] = "system"
        side_effects["instruction"] = instruction.name


class InstructionPipeline:
    """Instruction pipeline for advanced execution models."""
    
    def __init__(self, stages: int = 5):
        """Initialize the pipeline with the specified number of stages."""
        self.stages = stages
        self.pipeline: List[Optional[BaseInstruction]] = [None] * stages
        self.stall_cycles = 0
    
    def insert_instruction(self, instruction: BaseInstruction) -> bool:
        """Insert an instruction into the pipeline."""
        if self.pipeline[0] is not None:
            return False  # Pipeline is full
        
        self.pipeline[0] = instruction
        return True
    
    def advance(self) -> Optional[BaseInstruction]:
        """Advance the pipeline by one cycle."""
        if self.stall_cycles > 0:
            self.stall_cycles -= 1
            return None
        
        # Get the instruction completing this cycle
        completed = self.pipeline[-1]
        
        # Shift pipeline stages
        for i in range(self.stages - 1, 0, -1):
            self.pipeline[i] = self.pipeline[i - 1]
        self.pipeline[0] = None
        
        return completed
    
    def stall(self, cycles: int) -> None:
        """Stall the pipeline for the specified number of cycles."""
        self.stall_cycles = cycles
    
    def flush(self) -> None:
        """Flush the entire pipeline."""
        self.pipeline = [None] * self.stages
        self.stall_cycles = 0
    
    def is_empty(self) -> bool:
        """Check if the pipeline is empty."""
        return all(stage is None for stage in self.pipeline)
    
    def get_utilization(self) -> float:
        """Get pipeline utilization (percentage of occupied stages)."""
        occupied = sum(1 for stage in self.pipeline if stage is not None)
        return (occupied / self.stages) * 100.0