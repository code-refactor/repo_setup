"""Program representation for the virtual machine."""

import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Union

from vm_emulator.core.instruction import Instruction, InstructionSet


@dataclass
class Program:
    """
    Represents a program that can be executed on the virtual machine.
    A program contains a list of instructions and metadata.
    """
    name: str
    instructions: List[Instruction]
    entry_point: int = 0
    data_segment: Dict[int, int] = field(default_factory=dict)
    symbols: Dict[str, int] = field(default_factory=dict)
    
    def get_instruction(self, pc: int) -> Optional[Instruction]:
        """Get the instruction at the given program counter."""
        if 0 <= pc < len(self.instructions):
            return self.instructions[pc]
        return None
    
    def get_instruction_count(self) -> int:
        """Get the total number of instructions in the program."""
        return len(self.instructions)
    
    def add_instruction(self, instruction: Instruction) -> int:
        """
        Add an instruction to the program and return its position.
        
        Args:
            instruction: The instruction to add
            
        Returns:
            The position (PC) of the added instruction
        """
        pos = len(self.instructions)
        self.instructions.append(instruction)
        return pos
    
    def add_data(self, address: int, value: int) -> None:
        """
        Add a value to the data segment.
        
        Args:
            address: The memory address
            value: The value to store
        """
        self.data_segment[address] = value
    
    def add_symbol(self, name: str, address: int) -> None:
        """
        Add a symbol (label) to the program.
        
        Args:
            name: The symbol name
            address: The corresponding address (usually a PC value)
        """
        self.symbols[name] = address
    
    def get_symbol_address(self, name: str) -> Optional[int]:
        """
        Get the address for a symbol.
        
        Args:
            name: The symbol name
            
        Returns:
            The address or None if the symbol doesn't exist
        """
        return self.symbols.get(name)
    
    def to_dict(self) -> Dict:
        """
        Convert the program to a dictionary representation.
        
        Returns:
            A dictionary representing the program
        """
        instructions_data = []
        for instr in self.instructions:
            instructions_data.append({
                "opcode": instr.opcode,
                "type": instr.type.name,
                "operands": instr.operands,
                "latency": instr.latency,
            })
        
        return {
            "name": self.name,
            "entry_point": self.entry_point,
            "instructions": instructions_data,
            "data_segment": self.data_segment,
            "symbols": self.symbols,
        }
    
    def to_json(self) -> str:
        """
        Convert the program to a JSON string.
        
        Returns:
            A JSON string representing the program
        """
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Program":
        """
        Create a program from a dictionary representation.
        
        Args:
            data: A dictionary representing the program
            
        Returns:
            A new Program instance
        """
        instructions = []
        for instr_data in data["instructions"]:
            instr_type = getattr(InstructionType, instr_data["type"])
            instr = Instruction(
                opcode=instr_data["opcode"],
                type=instr_type,
                operands=instr_data["operands"],
                latency=instr_data["latency"],
            )
            instructions.append(instr)
        
        return cls(
            name=data["name"],
            entry_point=data["entry_point"],
            instructions=instructions,
            data_segment=data["data_segment"],
            symbols=data["symbols"],
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> "Program":
        """
        Create a program from a JSON string.
        
        Args:
            json_str: A JSON string representing the program
            
        Returns:
            A new Program instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    @classmethod
    def create_simple_program(cls, name: str, instructions_data: List[Tuple[str, List[Union[str, int]]]]) -> "Program":
        """
        Create a program from a simple format of opcode and operands.
        
        Args:
            name: The program name
            instructions_data: List of tuples with (opcode, operands)
            
        Returns:
            A new Program instance
        """
        instructions = []
        for opcode, operands in instructions_data:
            instr = InstructionSet.create_instruction(opcode, operands)
            instructions.append(instr)
        
        return cls(name=name, instructions=instructions)