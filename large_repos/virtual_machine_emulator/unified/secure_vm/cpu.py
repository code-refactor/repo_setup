"""
CPU implementation for the secure VM.

This module implements a simplified CPU architecture with registers, instructions,
and support for different privilege levels and security isolation.
"""

from __future__ import annotations
from enum import Enum, auto
from typing import Dict, List, Optional, Set, Tuple, Union, Any, Callable
import struct
import time

from secure_vm.memory import Memory, MemoryPermission


class PrivilegeLevel(Enum):
    """CPU privilege levels, from least to most privileged."""
    USER = 0       # Unprivileged user code
    SUPERVISOR = 1 # Limited system operations
    KERNEL = 2     # Full system access


class CPUException(Exception):
    """Base class for CPU execution exceptions."""
    pass


class SegmentationFault(CPUException):
    """Raised when memory access violates segmentation rules."""
    pass


class ProtectionFault(CPUException):
    """Raised when memory access violates protection rules."""
    pass


class PrivilegeViolation(CPUException):
    """Raised when an operation violates privilege rules."""
    pass


class InvalidInstruction(CPUException):
    """Raised when attempting to execute an invalid instruction."""
    pass


class InstructionType(Enum):
    """Categories of instruction types for the VM."""
    ARITHMETIC = auto()  # Arithmetic operations (add, sub, etc.)
    MEMORY = auto()      # Memory operations (load, store)
    CONTROL = auto()     # Control flow (jump, call, ret)
    SYSTEM = auto()      # System operations (privileged)
    SPECIAL = auto()     # Special operations


class Instruction:
    """Representation of a CPU instruction."""
    
    def __init__(
        self,
        opcode: int,
        name: str,
        instr_type: InstructionType,
        operands: int = 0,
        required_privilege: PrivilegeLevel = PrivilegeLevel.USER,
        handler: Optional[Callable] = None,
    ):
        self.opcode = opcode
        self.name = name
        self.type = instr_type
        self.operands = operands
        self.required_privilege = required_privilege
        self.handler = handler
    
    def __str__(self) -> str:
        return f"{self.name} (0x{self.opcode:02x})"


class CPURegisters:
    """CPU register state."""
    
    def __init__(self, register_count: int = 8):
        # General purpose registers R0-R7
        self.registers = [0] * register_count
        
        # Special registers
        self.ip = 0       # Instruction pointer
        self.sp = 0       # Stack pointer
        self.bp = 0       # Base pointer
        self.flags = 0    # Flags register
        
        # Protection and privilege registers
        self.privilege_level = PrivilegeLevel.USER
        self.protection_key = 0
    
    def get_register(self, reg_num: int) -> int:
        """Get the value of a general-purpose register."""
        if 0 <= reg_num < len(self.registers):
            return self.registers[reg_num]
        raise ValueError(f"Invalid register number: {reg_num}")
    
    def set_register(self, reg_num: int, value: int) -> None:
        """Set the value of a general-purpose register."""
        if 0 <= reg_num < len(self.registers):
            self.registers[reg_num] = value & 0xFFFFFFFF  # 32-bit registers
        else:
            raise ValueError(f"Invalid register number: {reg_num}")
    
    def dump_registers(self) -> Dict[str, int]:
        """Get a snapshot of all register values."""
        result = {f"R{i}": reg for i, reg in enumerate(self.registers)}
        result.update({
            "IP": self.ip,
            "SP": self.sp,
            "BP": self.bp,
            "FLAGS": self.flags,
            "PRIV": self.privilege_level.value,
            "PKEY": self.protection_key,
        })
        return result


class ControlFlowRecord:
    """Records a control flow event for integrity monitoring."""
    
    def __init__(
        self,
        from_address: int,
        to_address: int,
        event_type: str,
        instruction: str,
        legitimate: bool = True,
        context: Dict[str, Any] = None,
    ):
        self.from_address = from_address
        self.to_address = to_address
        self.event_type = event_type
        self.instruction = instruction
        self.legitimate = legitimate
        self.context = context or {}
        self.timestamp = time.time()
    
    def __str__(self) -> str:
        return (
            f"Control flow: {self.event_type} from 0x{self.from_address:x} "
            f"to 0x{self.to_address:x} via {self.instruction} "
            f"{'(legitimate)' if self.legitimate else '(HIJACKED)'}"
        )


class CPU:
    """CPU implementation with privilege levels and execution support."""
    
    # Instruction set definition
    INSTRUCTIONS = {
        # Arithmetic instructions
        0x01: Instruction(0x01, "ADD", InstructionType.ARITHMETIC, 2),
        0x02: Instruction(0x02, "SUB", InstructionType.ARITHMETIC, 2),
        0x03: Instruction(0x03, "MUL", InstructionType.ARITHMETIC, 2),
        0x04: Instruction(0x04, "DIV", InstructionType.ARITHMETIC, 2),
        
        # Memory instructions
        0x10: Instruction(0x10, "MOV", InstructionType.MEMORY, 2),
        0x11: Instruction(0x11, "LOAD", InstructionType.MEMORY, 2),
        0x12: Instruction(0x12, "STORE", InstructionType.MEMORY, 2),
        0x13: Instruction(0x13, "PUSH", InstructionType.MEMORY, 1),
        0x14: Instruction(0x14, "POP", InstructionType.MEMORY, 1),
        
        # Control flow instructions
        0x20: Instruction(0x20, "JMP", InstructionType.CONTROL, 1),
        0x21: Instruction(0x21, "JZ", InstructionType.CONTROL, 1),
        0x22: Instruction(0x22, "JNZ", InstructionType.CONTROL, 1),
        0x23: Instruction(0x23, "CALL", InstructionType.CONTROL, 1),
        0x24: Instruction(0x24, "RET", InstructionType.CONTROL, 0),
        
        # System instructions (privileged)
        0x30: Instruction(0x30, "SYSCALL", InstructionType.SYSTEM, 1),
        0x31: Instruction(0x31, "SYSRET", InstructionType.SYSTEM, 0),
        0x32: Instruction(0x32, "ELEVATE", InstructionType.SYSTEM, 1, PrivilegeLevel.KERNEL),
        0x33: Instruction(0x33, "LOWER", InstructionType.SYSTEM, 1),
        
        # Special instructions
        0xF0: Instruction(0xF0, "NOP", InstructionType.SPECIAL, 0),
        0xF1: Instruction(0xF1, "HALT", InstructionType.SPECIAL, 0),
        0xF2: Instruction(0xF2, "INT", InstructionType.SPECIAL, 1),
    }
    
    def __init__(self, memory: Memory):
        self.registers = CPURegisters()
        self.memory = memory
        self.running = False
        self.halted = False
        self.cycles = 0
        self.control_flow_records: List[ControlFlowRecord] = []
        
        # Security and protection state
        self.protection_keys: Dict[int, Set[MemoryPermission]] = {}
        self.shadow_stack: List[int] = []  # For control flow integrity
        self.syscall_table: Dict[int, Callable] = {}
        
        # Performance tracking
        self.execution_start_time = 0
        self.execution_time = 0
    
    def reset(self) -> None:
        """Reset the CPU state."""
        self.registers = CPURegisters()
        self.running = False
        self.halted = False
        self.cycles = 0
        self.control_flow_records = []
        self.shadow_stack = []
        self.execution_start_time = 0
        self.execution_time = 0
    
    def fetch(self) -> int:
        """Fetch the next instruction byte from memory."""
        try:
            # We use execute here to enforce DEP
            instr_byte = self.memory.execute(
                self.registers.ip,
                {"instruction_pointer": self.registers.ip}
            )
            self.registers.ip += 1
            return instr_byte
        except MemoryError as e:
            # Check if this is due to a non-executable segment
            segment = self.memory.find_segment(self.registers.ip)
            if segment and not segment.check_permission(self.registers.ip, MemoryPermission.EXECUTE):
                raise SegmentationFault(f"Cannot execute code from non-executable memory at 0x{self.registers.ip:x}")
            else:
                raise SegmentationFault(f"Failed to fetch instruction: {str(e)}")
    
    def fetch_word(self) -> int:
        """Fetch a 32-bit word from memory at the instruction pointer."""
        try:
            # For operands we use read_word since they don't need to be executable
            word = self.memory.read_word(
                self.registers.ip,
                {"instruction_pointer": self.registers.ip}
            )
            self.registers.ip += 4
            return word
        except MemoryError as e:
            raise SegmentationFault(f"Failed to fetch word: {str(e)}")
    
    def push(self, value: int) -> None:
        """Push a value onto the stack."""
        self.registers.sp -= 4
        try:
            self.memory.write_word(
                self.registers.sp,
                value,
                {"instruction_pointer": self.registers.ip}
            )
        except MemoryError as e:
            # Restore SP if push failed
            self.registers.sp += 4
            raise SegmentationFault(f"Failed to push value: {str(e)}")
    
    def pop(self) -> int:
        """Pop a value from the stack."""
        try:
            value = self.memory.read_word(
                self.registers.sp,
                {"instruction_pointer": self.registers.ip}
            )
            self.registers.sp += 4
            return value
        except MemoryError as e:
            raise SegmentationFault(f"Failed to pop value: {str(e)}")
    
    def execute_instruction(self, opcode: int) -> bool:
        """Execute a single instruction with the given opcode."""
        if opcode not in self.INSTRUCTIONS:
            raise InvalidInstruction(f"Invalid opcode: 0x{opcode:02x}")
        
        instruction = self.INSTRUCTIONS[opcode]
        
        # Check privilege level
        if self.registers.privilege_level.value < instruction.required_privilege.value:
            self.record_control_flow_event(
                self.registers.ip - 1,  # Previous IP value where opcode was fetched
                self.registers.ip,      # Current IP value
                "privilege-violation",
                instruction.name,
                False
            )
            raise PrivilegeViolation(
                f"Insufficient privilege for instruction {instruction.name}: "
                f"required {instruction.required_privilege.name}, "
                f"current {self.registers.privilege_level.name}"
            )
        
        # Decode and execute the instruction based on type
        if instruction.type == InstructionType.ARITHMETIC:
            self._execute_arithmetic(instruction)
        elif instruction.type == InstructionType.MEMORY:
            self._execute_memory(instruction)
        elif instruction.type == InstructionType.CONTROL:
            self._execute_control(instruction)
        elif instruction.type == InstructionType.SYSTEM:
            self._execute_system(instruction)
        elif instruction.type == InstructionType.SPECIAL:
            return self._execute_special(instruction)
        
        self.cycles += 1
        return True  # Continue execution unless HALT or similar
    
    def _execute_arithmetic(self, instruction: Instruction) -> None:
        """Execute an arithmetic instruction."""
        if instruction.operands == 2:
            # For simplicity, we'll assume reg-reg operations
            dest_reg = self.fetch()
            src_reg = self.fetch()
            dest_val = self.registers.get_register(dest_reg)
            src_val = self.registers.get_register(src_reg)
            
            result = 0
            if instruction.name == "ADD":
                result = (dest_val + src_val) & 0xFFFFFFFF
            elif instruction.name == "SUB":
                result = (dest_val - src_val) & 0xFFFFFFFF
            elif instruction.name == "MUL":
                result = (dest_val * src_val) & 0xFFFFFFFF
            elif instruction.name == "DIV":
                if src_val == 0:
                    raise CPUException("Division by zero")
                result = (dest_val // src_val) & 0xFFFFFFFF
            
            self.registers.set_register(dest_reg, result)
            
            # Update flags (zero flag example)
            if result == 0:
                self.registers.flags |= 0x01  # Set zero flag
            else:
                self.registers.flags &= ~0x01  # Clear zero flag
    
    def _execute_memory(self, instruction: Instruction) -> None:
        """Execute a memory instruction."""
        if instruction.name == "MOV":
            dest_reg = self.fetch()
            src_type = self.fetch()  # 0x01 for immediate, 0x02 for register

            if src_type == 0x01:  # Immediate value
                # Fetch a 32-bit immediate value
                value = self.fetch_word()
                self.registers.set_register(dest_reg, value)
            elif src_type == 0x02:  # Register value
                src_reg = self.fetch()
                value = self.registers.get_register(src_reg)
                self.registers.set_register(dest_reg, value)
            else:
                src_reg = src_type  # Backward compatibility
                value = self.registers.get_register(src_reg)
                self.registers.set_register(dest_reg, value)

        elif instruction.name == "LOAD":
            dest_reg = self.fetch()
            addr_reg = self.fetch()
            addr = self.registers.get_register(addr_reg)
            try:
                value = self.memory.read_word(
                    addr,
                    {"instruction_pointer": self.registers.ip - 2}
                )
                self.registers.set_register(dest_reg, value)
            except MemoryError as e:
                raise SegmentationFault(f"LOAD failed: {str(e)}")

        elif instruction.name == "STORE":
            addr_reg = self.fetch()
            src_reg = self.fetch()
            addr = self.registers.get_register(addr_reg)
            value = self.registers.get_register(src_reg)
            try:
                self.memory.write_word(
                    addr,
                    value,
                    {"instruction_pointer": self.registers.ip - 2}
                )
            except MemoryError as e:
                raise SegmentationFault(f"STORE failed: {str(e)}")

        elif instruction.name == "PUSH":
            reg = self.fetch()
            value = self.registers.get_register(reg)
            self.push(value)

        elif instruction.name == "POP":
            reg = self.fetch()
            value = self.pop()
            self.registers.set_register(reg, value)
    
    def _execute_control(self, instruction: Instruction) -> None:
        """Execute a control flow instruction."""
        if instruction.name == "JMP":
            target_reg = self.fetch()
            target = self.registers.get_register(target_reg)
            
            # Record the control flow event
            self.record_control_flow_event(
                self.registers.ip - 1,  # Where opcode was fetched
                target,
                "jump",
                instruction.name,
                True  # Assumed legitimate for now - CFI would validate this
            )
            
            self.registers.ip = target
        
        elif instruction.name == "JZ":
            target_reg = self.fetch()
            target = self.registers.get_register(target_reg)
            
            # Only jump if zero flag is set
            if self.registers.flags & 0x01:
                # Record the control flow event
                self.record_control_flow_event(
                    self.registers.ip - 1,
                    target,
                    "conditional-jump",
                    instruction.name,
                    True
                )
                self.registers.ip = target
        
        elif instruction.name == "JNZ":
            target_reg = self.fetch()
            target = self.registers.get_register(target_reg)
            
            # Only jump if zero flag is not set
            if not (self.registers.flags & 0x01):
                # Record the control flow event
                self.record_control_flow_event(
                    self.registers.ip - 1,
                    target,
                    "conditional-jump",
                    instruction.name,
                    True
                )
                self.registers.ip = target
        
        elif instruction.name == "CALL":
            target_reg = self.fetch()
            target = self.registers.get_register(target_reg)
            return_addr = self.registers.ip
            
            # Record return address in shadow stack for control flow integrity
            self.shadow_stack.append(return_addr)
            
            # Push return address onto the stack
            self.push(return_addr)
            
            # Record the control flow event
            self.record_control_flow_event(
                self.registers.ip - 1,
                target,
                "call",
                instruction.name,
                True
            )
            
            self.registers.ip = target
        
        elif instruction.name == "RET":
            # Pop return address from stack
            return_addr = self.pop()
            
            # Control flow integrity check using shadow stack
            shadow_valid = True
            if self.shadow_stack:
                expected_return = self.shadow_stack.pop()
                if expected_return != return_addr:
                    shadow_valid = False
                    # We record this but don't stop execution to allow exploits
                    self.record_control_flow_event(
                        self.registers.ip - 1,
                        return_addr,
                        "return",
                        instruction.name,
                        False
                    )
            else:
                shadow_valid = False
                self.record_control_flow_event(
                    self.registers.ip - 1,
                    return_addr,
                    "return",
                    instruction.name,
                    False
                )
            
            if shadow_valid:
                self.record_control_flow_event(
                    self.registers.ip - 1,
                    return_addr,
                    "return",
                    instruction.name,
                    True
                )
            
            self.registers.ip = return_addr
    
    def _execute_system(self, instruction: Instruction) -> None:
        """Execute a system instruction."""
        if instruction.name == "SYSCALL":
            syscall_num = self.fetch()
            
            # Record system call for forensic purposes
            context = {"registers": self.registers.dump_registers()}
            self.record_control_flow_event(
                self.registers.ip - 1,
                self.registers.ip,
                "syscall",
                f"{instruction.name} {syscall_num}",
                True,
                context
            )
            
            # Execute the system call if registered
            if syscall_num in self.syscall_table:
                self.syscall_table[syscall_num](self)
        
        elif instruction.name == "SYSRET":
            # Return from system call - typically adjusts privilege
            prev_privilege = self.registers.privilege_level
            
            # Only lower privilege on return, never elevate
            if prev_privilege != PrivilegeLevel.USER:
                self.registers.privilege_level = PrivilegeLevel.USER
            
            self.record_control_flow_event(
                self.registers.ip - 1,
                self.registers.ip,
                "sysret",
                instruction.name,
                True,
                {"previous_privilege": prev_privilege.name}
            )
        
        elif instruction.name == "ELEVATE":
            # Elevate privilege level (requires KERNEL privilege to use)
            target_level = self.fetch()
            
            # Must be called from kernel mode for security
            # This is checked at the beginning of execute_instruction
            
            if 0 <= target_level <= 2:
                self.registers.privilege_level = PrivilegeLevel(target_level)
                self.record_control_flow_event(
                    self.registers.ip - 2,
                    self.registers.ip,
                    "privilege-change",
                    instruction.name,
                    True,
                    {"new_level": self.registers.privilege_level.name}
                )
            else:
                raise CPUException(f"Invalid privilege level: {target_level}")
        
        elif instruction.name == "LOWER":
            # Voluntarily lower privilege level
            target_level = self.fetch()
            current_level = self.registers.privilege_level.value
            
            # Can only lower privilege, not elevate
            if 0 <= target_level < current_level:
                self.registers.privilege_level = PrivilegeLevel(target_level)
                self.record_control_flow_event(
                    self.registers.ip - 2,
                    self.registers.ip,
                    "privilege-change",
                    instruction.name,
                    True,
                    {"new_level": self.registers.privilege_level.name}
                )
            else:
                raise PrivilegeViolation(
                    f"Cannot elevate privilege from {current_level} to {target_level}"
                )
    
    def _execute_special(self, instruction: Instruction) -> bool:
        """Execute a special instruction. Returns False if execution should stop."""
        if instruction.name == "NOP":
            # No operation, just proceed
            pass
        
        elif instruction.name == "HALT":
            # Stop execution
            self.halted = True
            self.running = False
            return False
        
        elif instruction.name == "INT":
            # Software interrupt
            interrupt_num = self.fetch()
            
            # Record for forensic purposes
            self.record_control_flow_event(
                self.registers.ip - 2,
                self.registers.ip,
                "interrupt",
                f"{instruction.name} {interrupt_num}",
                True
            )
            
            # Handle the interrupt based on number
            # This would call an interrupt handler if implemented
            pass
        
        return True  # Continue execution
    
    def register_syscall(self, syscall_num: int, handler: Callable) -> None:
        """Register a system call handler."""
        self.syscall_table[syscall_num] = handler
    
    def record_control_flow_event(
        self,
        from_address: int,
        to_address: int,
        event_type: str,
        instruction: str,
        legitimate: bool = True,
        context: Dict[str, Any] = None,
    ) -> None:
        """Record a control flow event for integrity monitoring."""
        record = ControlFlowRecord(
            from_address=from_address,
            to_address=to_address,
            event_type=event_type,
            instruction=instruction,
            legitimate=legitimate,
            context=context,
        )
        self.control_flow_records.append(record)
    
    def run(self, max_instructions: int = 10000) -> int:
        """Run the CPU for up to max_instructions instructions."""
        if self.halted:
            return 0
        
        self.running = True
        self.execution_start_time = time.time()
        instructions_executed = 0
        
        try:
            while self.running and instructions_executed < max_instructions:
                # Fetch instruction
                opcode = self.fetch()
                
                # Execute instruction
                continue_execution = self.execute_instruction(opcode)
                if not continue_execution:
                    break
                
                instructions_executed += 1
        
        except (CPUException, SegmentationFault, ProtectionFault) as e:
            self.running = False
            # Record the exception but don't re-raise it to allow exploit demonstration
            self.record_control_flow_event(
                self.registers.ip,
                0,
                "exception",
                str(e),
                False
            )
        
        finally:
            self.execution_time += time.time() - self.execution_start_time
        
        return instructions_executed
    
    def get_control_flow_trace(self) -> List[ControlFlowRecord]:
        """Get the control flow trace for visualization."""
        return self.control_flow_records
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics for the CPU."""
        return {
            "cycles": self.cycles,
            "execution_time": self.execution_time,
            "instructions_per_second": self.cycles / max(self.execution_time, 0.001),
            "control_flow_events": len(self.control_flow_records),
        }