"""
Base CPU/Processor abstraction for the unified virtual machine.

This module provides the common processor functionality that can be extended
for both parallel computing and security research use cases.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple, Union

from .instruction import BaseInstruction, InstructionType


class ProcessorState(Enum):
    """States that a processor can be in."""
    IDLE = auto()       # Processor not running any code
    RUNNING = auto()    # Actively executing instructions
    WAITING = auto()    # Waiting on synchronization or I/O
    BLOCKED = auto()    # Blocked on resource
    TERMINATED = auto() # Execution terminated


@dataclass
class ProcessorConfig:
    """Configuration for a processor."""
    register_count: int = 16
    enable_special_registers: bool = True
    enable_performance_counters: bool = True


class ProcessorInterface(ABC):
    """Standard processor interface."""
    
    @abstractmethod
    def execute_instruction(self, instruction: BaseInstruction) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Execute a single instruction."""
        pass
    
    @abstractmethod
    def get_register(self, register: str) -> int:
        """Get register value."""
        pass
    
    @abstractmethod
    def set_register(self, register: str, value: int) -> None:
        """Set register value."""
        pass
    
    @abstractmethod
    def reset(self) -> None:
        """Reset processor state."""
        pass


class BaseProcessor(ProcessorInterface):
    """
    Base processor implementation providing common functionality.
    
    This class provides the foundation for both parallel and security CPUs,
    with extension points for specialized functionality.
    """
    
    def __init__(self, processor_id: int, config: Optional[ProcessorConfig] = None):
        """Initialize the base processor."""
        self.processor_id = processor_id
        self.config = config or ProcessorConfig()
        
        # Register management
        self.registers: Dict[str, int] = {}
        self._initialize_registers()
        
        # Execution state
        self.pc = 0  # Program counter
        self.state = ProcessorState.IDLE
        self.cycle_count = 0
        
        # Performance counters
        if self.config.enable_performance_counters:
            self.performance_counters: Dict[str, int] = {
                "instructions_executed": 0,
                "memory_accesses": 0,
                "branches_taken": 0,
                "stall_cycles": 0,
            }
        else:
            self.performance_counters = {}
        
        # Extension points for subclasses
        self._initialize_additional_state()
    
    def _initialize_registers(self) -> None:
        """Initialize processor registers."""
        # General purpose registers
        for i in range(self.config.register_count):
            self.registers[f"R{i}"] = 0
        
        if self.config.enable_special_registers:
            # Special registers
            self.registers["SP"] = 0    # Stack pointer
            self.registers["FP"] = 0    # Frame pointer
            self.registers["FLAGS"] = 0 # Status flags
    
    def _initialize_additional_state(self) -> None:
        """Initialize additional state - to be implemented by subclasses."""
        pass
    
    def execute_instruction(self, instruction: BaseInstruction) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Execute a single instruction on this processor."""
        if self.state != ProcessorState.RUNNING:
            return False, None
        
        # Update performance counters
        if "instructions_executed" in self.performance_counters:
            self.performance_counters["instructions_executed"] += 1
        
        self.cycle_count += 1
        
        # Execute the instruction based on its type
        completed, side_effects = self._execute_instruction_by_type(instruction)
        
        # Update program counter if instruction completed and no jump occurred
        if completed and (not side_effects or "jump" not in side_effects):
            self.pc += 1
        
        return completed, side_effects
    
    def _execute_instruction_by_type(self, instruction: BaseInstruction) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Execute instruction based on its type."""
        side_effects: Dict[str, Any] = {}
        
        if instruction.type == InstructionType.COMPUTE:
            self._execute_compute_instruction(instruction, side_effects)
        elif instruction.type == InstructionType.MEMORY:
            self._execute_memory_instruction(instruction, side_effects)
        elif instruction.type == InstructionType.BRANCH:
            self._execute_branch_instruction(instruction, side_effects)
        elif instruction.type == InstructionType.SYSTEM:
            self._execute_system_instruction(instruction, side_effects)
        else:
            # Allow subclasses to handle other instruction types
            self._execute_custom_instruction(instruction, side_effects)
        
        return True, side_effects if side_effects else None
    
    def _execute_compute_instruction(self, instruction: BaseInstruction, side_effects: Dict[str, Any]) -> None:
        """Execute a compute instruction."""
        if not instruction.operands:
            return
        
        dest_reg = instruction.operands[0]
        if dest_reg not in self.registers:
            raise ValueError(f"Invalid register: {dest_reg}")
        
        # Simple arithmetic operations
        if instruction.name.startswith("ADD"):
            if len(instruction.operands) >= 3:
                src1 = self.registers.get(instruction.operands[1], 0)
                src2 = self.registers.get(instruction.operands[2], 0)
                self.registers[dest_reg] = src1 + src2
        elif instruction.name.startswith("SUB"):
            if len(instruction.operands) >= 3:
                src1 = self.registers.get(instruction.operands[1], 0)
                src2 = self.registers.get(instruction.operands[2], 0)
                self.registers[dest_reg] = src1 - src2
        elif instruction.name.startswith("MUL"):
            if len(instruction.operands) >= 3:
                src1 = self.registers.get(instruction.operands[1], 0)
                src2 = self.registers.get(instruction.operands[2], 0)
                self.registers[dest_reg] = src1 * src2
        
        # Record register modification
        side_effects["registers_modified"] = [dest_reg]
    
    def _execute_memory_instruction(self, instruction: BaseInstruction, side_effects: Dict[str, Any]) -> None:
        """Execute a memory instruction."""
        if not instruction.operands:
            return
        
        if instruction.name.startswith("LOAD"):
            # Load from memory address
            if len(instruction.operands) >= 2:
                dest_reg = instruction.operands[0]
                addr_operand = instruction.operands[1]
                
                # Address could be register or immediate
                if addr_operand.startswith("R"):
                    addr = self.registers.get(addr_operand, 0)
                else:
                    addr = int(addr_operand)  # Immediate address
                
                side_effects["memory_read"] = addr
                side_effects["registers_modified"] = [dest_reg]
        
        elif instruction.name.startswith("STORE"):
            # Store to memory address
            if len(instruction.operands) >= 2:
                src_reg = instruction.operands[0]
                addr_operand = instruction.operands[1]
                
                # Address could be register or immediate
                if addr_operand.startswith("R"):
                    addr = self.registers.get(addr_operand, 0)
                else:
                    addr = int(addr_operand)  # Immediate address
                
                value = self.registers.get(src_reg, 0)
                side_effects["memory_write"] = (addr, value)
        
        # Update performance counters
        if "memory_accesses" in self.performance_counters:
            self.performance_counters["memory_accesses"] += 1
    
    def _execute_branch_instruction(self, instruction: BaseInstruction, side_effects: Dict[str, Any]) -> None:
        """Execute a branch instruction."""
        if not instruction.operands:
            return
        
        if instruction.name.startswith("JMP"):
            # Unconditional jump
            target = instruction.operands[0]
            if target.startswith("R"):
                target_addr = self.registers.get(target, 0)
            else:
                target_addr = int(target)
            
            self.pc = target_addr
            side_effects["jump"] = target_addr
        
        elif instruction.name.startswith("JZ"):
            # Jump if zero flag set
            if self.registers.get("FLAGS", 0) & 1:  # Zero flag is bit 0
                target = instruction.operands[0]
                if target.startswith("R"):
                    target_addr = self.registers.get(target, 0)
                else:
                    target_addr = int(target)
                
                self.pc = target_addr
                side_effects["jump"] = target_addr
        
        # Update performance counters
        if "branches_taken" in self.performance_counters and "jump" in side_effects:
            self.performance_counters["branches_taken"] += 1
    
    def _execute_system_instruction(self, instruction: BaseInstruction, side_effects: Dict[str, Any]) -> None:
        """Execute a system instruction."""
        if instruction.name == "HALT":
            self.state = ProcessorState.TERMINATED
            side_effects["halt"] = True
        elif instruction.name == "NOP":
            # No operation
            pass
        else:
            # Allow subclasses to handle other system instructions
            self._execute_custom_system_instruction(instruction, side_effects)
    
    def _execute_custom_instruction(self, instruction: BaseInstruction, side_effects: Dict[str, Any]) -> None:
        """Execute custom instruction - to be implemented by subclasses."""
        pass
    
    def _execute_custom_system_instruction(self, instruction: BaseInstruction, side_effects: Dict[str, Any]) -> None:
        """Execute custom system instruction - to be implemented by subclasses."""
        pass
    
    def get_register(self, register: str) -> int:
        """Get register value."""
        return self.registers.get(register, 0)
    
    def set_register(self, register: str, value: int) -> None:
        """Set register value."""
        if register in self.registers:
            self.registers[register] = value
        else:
            raise ValueError(f"Invalid register: {register}")
    
    def is_busy(self) -> bool:
        """Check if the processor is busy."""
        return self.state != ProcessorState.IDLE
    
    def start_execution(self, start_pc: int = 0) -> None:
        """Start execution at the given program counter."""
        self.pc = start_pc
        self.state = ProcessorState.RUNNING
    
    def get_state(self) -> ProcessorState:
        """Get processor state."""
        return self.state
    
    def get_performance_counters(self) -> Dict[str, int]:
        """Get performance counters."""
        return self.performance_counters.copy()
    
    def reset(self) -> None:
        """Reset processor state."""
        # Reset registers
        for reg in self.registers:
            self.registers[reg] = 0
        
        # Reset execution state
        self.pc = 0
        self.state = ProcessorState.IDLE
        self.cycle_count = 0
        
        # Reset performance counters
        for counter in self.performance_counters:
            self.performance_counters[counter] = 0
        
        # Allow subclasses to reset additional state
        self._reset_additional_state()
    
    def _reset_additional_state(self) -> None:
        """Reset additional state - to be implemented by subclasses."""
        pass