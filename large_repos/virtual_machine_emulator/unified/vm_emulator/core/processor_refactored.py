"""Refactored processor implementation extending common base classes."""

import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Set, Tuple

from common.core.cpu import BaseProcessor, ProcessorConfig, ProcessorState
from common.core.instruction import BaseInstruction, InstructionType
from vm_emulator.core.instruction import Instruction, InstructionSet


@dataclass
class ParallelProcessorConfig(ProcessorConfig):
    """Configuration for parallel processor."""
    enable_stall_cycles: bool = True
    enable_latency_simulation: bool = True
    enable_branch_prediction: bool = False


class ParallelProcessor(BaseProcessor):
    """
    Parallel processor implementation extending the common base processor.
    
    This processor specializes in parallel execution with support for
    synchronization operations, memory consistency, and thread management.
    """
    
    def __init__(self, processor_id: int, config: Optional[ParallelProcessorConfig] = None):
        """Initialize the parallel processor."""
        self.parallel_config = config or ParallelProcessorConfig()
        super().__init__(processor_id, self.parallel_config)
        
        # Parallel-specific state
        self.current_thread_id: Optional[str] = None
        self.stall_cycles: int = 0  # Cycles the processor is stalled
        
        # Synchronization state
        self.pending_sync_operations: List[Dict[str, Any]] = []
        
        # Memory consistency state
        self.pending_memory_operations: List[Dict[str, Any]] = []
    
    def _initialize_additional_state(self) -> None:
        """Initialize parallel-specific state."""
        # Initialize any additional registers or state needed for parallel execution
        pass
    
    def start_thread(self, thread_id: str, start_pc: int) -> None:
        """Start executing a thread on this processor."""
        self.current_thread_id = thread_id
        self.pc = start_pc
        self.state = ProcessorState.RUNNING
        self.stall_cycles = 0  # Reset stall cycles to ensure immediate execution
    
    def execute_instruction(self, instruction: Any) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Execute a single instruction on this processor."""
        # Convert vm_emulator Instruction to BaseInstruction if needed
        if isinstance(instruction, Instruction):
            base_instruction = self._convert_to_base_instruction(instruction)
        else:
            base_instruction = instruction
        
        # Check if we're still stalled from previous instruction
        if self.parallel_config.enable_stall_cycles and self.stall_cycles > 0:
            self.stall_cycles -= 1
            return (False, None)
        
        # Execute the instruction using the base class functionality
        completed, side_effects = super().execute_instruction(base_instruction)
        
        # Apply parallel-specific execution logic
        if completed and side_effects:
            self._apply_parallel_side_effects(instruction, side_effects)
        
        # Set stall cycles based on instruction latency
        if self.parallel_config.enable_latency_simulation and hasattr(instruction, 'latency'):
            self.stall_cycles = max(0, instruction.latency - 1)
        
        return (completed, side_effects)
    
    def _convert_to_base_instruction(self, instruction: Instruction) -> BaseInstruction:
        """Convert vm_emulator Instruction to BaseInstruction."""
        # Map vm_emulator operands to string format expected by BaseInstruction
        operands = [str(op) for op in instruction.operands]
        
        return BaseInstruction(
            name=instruction.opcode,
            type=self._map_instruction_type(instruction.type),
            operands=operands,
            latency=instruction.latency
        )
    
    def _map_instruction_type(self, vm_instruction_type: InstructionType) -> InstructionType:
        """Map vm_emulator InstructionType to common InstructionType."""
        # The types should be compatible, but ensure mapping
        type_mapping = {
            InstructionType.COMPUTE: InstructionType.COMPUTE,
            InstructionType.MEMORY: InstructionType.MEMORY,
            InstructionType.BRANCH: InstructionType.BRANCH,
            InstructionType.SYNC: InstructionType.SYNC,
            InstructionType.SYSTEM: InstructionType.SYSTEM,
        }
        return type_mapping.get(vm_instruction_type, InstructionType.COMPUTE)
    
    def _execute_custom_instruction(self, instruction: BaseInstruction, side_effects: Dict[str, Any]) -> None:
        """Execute parallel-specific custom instructions."""
        if instruction.type == InstructionType.SYNC:
            self._execute_sync_instruction(instruction, side_effects)
        elif instruction.name in ["SPAWN", "JOIN", "YIELD"]:
            self._execute_thread_instruction(instruction, side_effects)
    
    def _execute_sync_instruction(self, instruction: BaseInstruction, side_effects: Dict[str, Any]) -> None:
        """Execute synchronization instructions."""
        if instruction.name == "LOCK":
            # Request a lock
            lock_id = self._get_operand_value(instruction.operands[0])
            side_effects["sync_lock"] = lock_id
            # Actual locking is handled by the VM
        
        elif instruction.name == "UNLOCK":
            # Release a lock
            lock_id = self._get_operand_value(instruction.operands[0])
            side_effects["sync_unlock"] = lock_id
        
        elif instruction.name == "FENCE":
            # Memory fence
            side_effects["memory_fence"] = True
        
        elif instruction.name == "CAS":
            # Compare-and-swap
            addr = self._get_operand_value(instruction.operands[0])
            expected = self._get_operand_value(instruction.operands[1])
            new_value = self._get_operand_value(instruction.operands[2])
            result_reg = instruction.operands[3]
            side_effects["cas_operation"] = (addr, expected, new_value, result_reg)
    
    def _execute_thread_instruction(self, instruction: BaseInstruction, side_effects: Dict[str, Any]) -> None:
        """Execute thread management instructions."""
        if instruction.name == "SPAWN":
            # Create a new thread
            func_addr = self._get_operand_value(instruction.operands[0])
            arg_addr = self._get_operand_value(instruction.operands[1])
            result_reg = instruction.operands[2]
            side_effects["spawn_thread"] = (func_addr, arg_addr, result_reg)
        
        elif instruction.name == "JOIN":
            # Wait for another thread to complete
            thread_id = self._get_operand_value(instruction.operands[0])
            side_effects["join_thread"] = thread_id
            self.state = ProcessorState.WAITING
        
        elif instruction.name == "YIELD":
            # Voluntarily yield the processor
            side_effects["yield"] = True
            self.state = ProcessorState.WAITING
    
    def _apply_parallel_side_effects(self, instruction: Instruction, side_effects: Dict[str, Any]) -> None:
        """Apply parallel-specific side effects."""
        # Handle parallel-specific instruction execution
        if instruction.type == InstructionType.COMPUTE:
            self._handle_compute_side_effects(instruction, side_effects)
        elif instruction.type == InstructionType.MEMORY:
            self._handle_memory_side_effects(instruction, side_effects)
        elif instruction.type == InstructionType.BRANCH:
            self._handle_branch_side_effects(instruction, side_effects)
    
    def _handle_compute_side_effects(self, instruction: Instruction, side_effects: Dict[str, Any]) -> None:
        """Handle compute instruction side effects."""
        # Compute operations change register values
        dest_reg = instruction.operands[0]
        if dest_reg not in self.registers:
            raise ValueError(f"Invalid register: {dest_reg}")
        
        # Record the register being modified
        side_effects["registers_modified"] = [dest_reg]
        
        # Execute the appropriate compute operation
        if instruction.opcode == "ADD":
            op1_value = self._get_operand_value(instruction.operands[1])
            op2_value = self._get_operand_value(instruction.operands[2])
            self.registers[dest_reg] = op1_value + op2_value
        elif instruction.opcode == "SUB":
            self.registers[dest_reg] = self._get_operand_value(instruction.operands[1]) - self._get_operand_value(instruction.operands[2])
        elif instruction.opcode == "MUL":
            self.registers[dest_reg] = self._get_operand_value(instruction.operands[1]) * self._get_operand_value(instruction.operands[2])
        elif instruction.opcode == "DIV":
            divisor = self._get_operand_value(instruction.operands[2])
            if divisor == 0:
                raise ZeroDivisionError("Division by zero")
            self.registers[dest_reg] = self._get_operand_value(instruction.operands[1]) // divisor
    
    def _handle_memory_side_effects(self, instruction: Instruction, side_effects: Dict[str, Any]) -> None:
        """Handle memory instruction side effects."""
        if instruction.opcode == "LOAD":
            # Load from memory to register
            dest_reg = instruction.operands[0]
            operand = instruction.operands[1]
            
            # Check if this is a direct load of immediate value (not a memory address)
            if isinstance(operand, int) or (isinstance(operand, str) and operand.isdigit()):
                # This is an immediate value load, not a memory access
                value = self._get_operand_value(operand)
                self.registers[dest_reg] = value
                side_effects["registers_modified"] = [dest_reg]
            else:
                # This is a memory address load
                addr = self._get_operand_value(operand)
                side_effects["memory_read"] = addr
                side_effects["registers_modified"] = [dest_reg]
                # Actual value loading happens in the VM which has access to memory
        
        elif instruction.opcode == "STORE":
            # Store from register to memory
            src_reg = instruction.operands[0]
            addr = self._get_operand_value(instruction.operands[1])
            value = self.registers[src_reg]
            side_effects["memory_write"] = (addr, value)
    
    def _handle_branch_side_effects(self, instruction: Instruction, side_effects: Dict[str, Any]) -> None:
        """Handle branch instruction side effects."""
        increment_pc = True
        
        if instruction.opcode == "JMP":
            # Unconditional jump
            target = self._get_operand_value(instruction.operands[0])
            self.pc = target
            increment_pc = False
        
        elif instruction.opcode == "JZ":
            # Jump if zero
            condition_reg = instruction.operands[0]
            target = self._get_operand_value(instruction.operands[1])
            if self.registers[condition_reg] == 0:
                self.pc = target
                increment_pc = False
        
        elif instruction.opcode == "JNZ":
            # Jump if not zero
            condition_reg = instruction.operands[0]
            target = self._get_operand_value(instruction.operands[1])
            if self.registers[condition_reg] != 0:
                self.pc = target
                increment_pc = False
        
        elif instruction.opcode == "JGT":
            # Jump if greater than
            condition_reg = instruction.operands[0]
            target = self._get_operand_value(instruction.operands[1])
            if self.registers[condition_reg] > 0:
                self.pc = target
                increment_pc = False
        
        elif instruction.opcode == "JLT":
            # Jump if less than
            condition_reg = instruction.operands[0]
            target = self._get_operand_value(instruction.operands[1])
            if self.registers[condition_reg] < 0:
                self.pc = target
                increment_pc = False
        
        # Record jump information
        if not increment_pc:
            side_effects["jump"] = self.pc
    
    def _get_operand_value(self, operand: Any) -> int:
        """Get the value of an operand, which could be a register name or immediate value."""
        if isinstance(operand, str) and operand in self.registers:
            return self.registers[operand]
        return int(operand)  # Convert to int if it's an immediate value
    
    def _reset_additional_state(self) -> None:
        """Reset parallel-specific state."""
        self.current_thread_id = None
        self.stall_cycles = 0
        self.pending_sync_operations.clear()
        self.pending_memory_operations.clear()
    
    def get_thread_id(self) -> Optional[str]:
        """Get the current thread ID."""
        return self.current_thread_id
    
    def get_stall_cycles(self) -> int:
        """Get remaining stall cycles."""
        return self.stall_cycles
    
    def is_stalled(self) -> bool:
        """Check if processor is stalled."""
        return self.stall_cycles > 0