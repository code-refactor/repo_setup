"""
Secure Virtual Machine implementation using the unified common library.

This module refactors the original VirtualMachine to extend BaseVirtualMachine
from the common library while preserving all security-specific functionality.
"""

import random
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple, Union, Any, BinaryIO

from common.core import (
    BaseVirtualMachine, VirtualMachineConfig, VMState,
    BaseProcessor, ProcessorState,
    UnifiedMemorySystem, MemoryAccessType, MemorySegment,
    ExecutionTracer, PerformanceMetrics
)

from .memory import (
    Memory, MemoryPermission, MemoryProtectionLevel, MemoryProtection
)
from .cpu import CPU, PrivilegeLevel, CPUException


class SecurityVMConfig(VirtualMachineConfig):
    """Configuration for security virtual machine."""
    
    def __init__(
        self,
        memory_size: int = 65536,
        enable_tracing: bool = True,
        enable_metrics: bool = True,
        random_seed: Optional[int] = None,
        protection_level: MemoryProtectionLevel = MemoryProtectionLevel.STANDARD,
        dep_enabled: bool = True,
        aslr_enabled: bool = False,
        stack_canaries: bool = False,
        shadow_memory: bool = False,
        enable_forensics: bool = True,
        detailed_logging: bool = False,
    ):
        super().__init__(memory_size, enable_tracing, enable_metrics, random_seed)
        self.protection_level = protection_level
        self.dep_enabled = dep_enabled
        self.aslr_enabled = aslr_enabled
        self.stack_canaries = stack_canaries
        self.shadow_memory = shadow_memory
        self.enable_forensics = enable_forensics
        self.detailed_logging = detailed_logging


class ExecutionResult:
    """Result of executing a program in the VM."""
    
    def __init__(
        self,
        success: bool,
        cycles: int,
        execution_time: float,
        cpu_state: Dict[str, Any],
        control_flow_events: List[Dict[str, Any]],
        protection_events: List[Dict[str, Any]],
    ):
        self.success = success
        self.cycles = cycles
        self.execution_time = execution_time
        self.cpu_state = cpu_state
        self.control_flow_events = control_flow_events
        self.protection_events = protection_events
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the execution result."""
        return {
            "success": self.success,
            "cycles": self.cycles,
            "execution_time": self.execution_time,
            "control_flow_events": len(self.control_flow_events),
            "protection_events": len(self.protection_events),
            "instructions_per_second": self.cycles / max(self.execution_time, 0.001),
        }


class ForensicLog:
    """Forensic logging system for the VM."""
    
    def __init__(self, enabled: bool = True, detailed: bool = False):
        self.enabled = enabled
        self.detailed = detailed
        self.logs: List[Dict[str, Any]] = []
        self.start_time = time.time()
    
    def log_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Log an event if logging is enabled."""
        if not self.enabled:
            return
        
        entry = {
            "timestamp": time.time() - self.start_time,
            "event_type": event_type,
            "data": data,
        }
        self.logs.append(entry)
    
    def log_memory_access(
        self,
        address: int,
        access_type: str,
        size: int,
        value: Optional[int] = None,
        context: Dict[str, Any] = None,
    ) -> None:
        """Log a memory access event."""
        if not self.enabled or not self.detailed:
            return
        
        data = {
            "address": address,
            "access_type": access_type,
            "size": size,
        }
        if value is not None:
            data["value"] = value
        if context:
            data["context"] = context
        
        self.log_event("memory_access", data)
    
    def log_control_flow(self, event: Dict[str, Any]) -> None:
        """Log a control flow event."""
        if not self.enabled:
            return
        
        self.log_event("control_flow", event)
    
    def log_protection_violation(self, event: Dict[str, Any]) -> None:
        """Log a protection violation event."""
        if not self.enabled:
            return
        
        self.log_event("protection_violation", event)
    
    def log_system_event(self, event_type: str, details: Dict[str, Any]) -> None:
        """Log a system-level event."""
        if not self.enabled:
            return
        
        data = {"system_event": event_type, **details}
        self.log_event("system", data)
    
    def get_logs(self) -> List[Dict[str, Any]]:
        """Get all logged events."""
        return self.logs
    
    def export_logs(self, format_type: str = "dict") -> Union[List[Dict[str, Any]], str]:
        """Export logs in the specified format."""
        if format_type == "dict":
            return self.logs
        elif format_type == "json":
            import json
            return json.dumps(self.logs, indent=2)
        elif format_type == "text":
            text_logs = []
            for log in self.logs:
                timestamp = log["timestamp"]
                event_type = log["event_type"]
                data_str = ", ".join(f"{k}={v}" for k, v in log["data"].items())
                text_logs.append(f"[{timestamp:.6f}] {event_type}: {data_str}")
            return "\n".join(text_logs)
        else:
            raise ValueError(f"Unsupported export format: {format_type}")


class SecurityMemorySystem(UnifiedMemorySystem):
    """Memory system with security-specific features."""
    
    def __init__(self, protection: MemoryProtection, enable_tracking: bool = True):
        super().__init__(size=65536, enable_tracking=enable_tracking)
        
        # Security-specific features
        self.protection = protection
        self.protection_events: List[Any] = []
        
        # Clear default segments and create security segments
        self.segments.clear()
        self._setup_security_segments()
    
    def _setup_security_segments(self) -> None:
        """Set up security-aware memory segments."""
        # Calculate segment sizes
        total_size = self.size
        code_size = total_size // 4
        data_size = total_size // 4
        heap_size = total_size // 4
        stack_size = total_size - code_size - data_size - heap_size
        
        # Create memory segments with security permissions
        self.code_segment = MemorySegment(
            base_address=0x10000,
            size=code_size,
            name="code",
            readable=True,
            writable=False,  # Code should not be writable
            executable=True
        )
        self.segments.append(self.code_segment)
        
        self.data_segment = MemorySegment(
            base_address=0x20000,
            size=data_size,
            name="data",
            readable=True,
            writable=True,
            executable=False
        )
        self.segments.append(self.data_segment)
        
        self.heap_segment = MemorySegment(
            base_address=0x30000,
            size=heap_size,
            name="heap",
            readable=True,
            writable=True,
            executable=False
        )
        self.segments.append(self.heap_segment)
        
        self.stack_segment = MemorySegment(
            base_address=0x70000,
            size=stack_size,
            name="stack",
            readable=True,
            writable=True,
            executable=False
        )
        self.segments.append(self.stack_segment)
    
    def read(self, address: int, size: int = 1, **context) -> int:
        """Read with security checks."""
        # Check segment permissions
        segment = self.find_segment(address)
        if segment and not segment.readable:
            self._log_protection_violation(address, "read", segment, context)
            raise PermissionError(f"Read not allowed in segment {segment.name}")
        
        return super().read(address, size, **context)
    
    def write(self, address: int, value: int, size: int = 1, **context) -> None:
        """Write with security checks."""
        # Check segment permissions
        segment = self.find_segment(address)
        if segment and not segment.writable:
            self._log_protection_violation(address, "write", segment, context)
            raise PermissionError(f"Write not allowed in segment {segment.name}")
        
        super().write(address, value, size, **context)
    
    def _log_protection_violation(self, address: int, access_type: str, segment: MemorySegment, context: Dict[str, Any]) -> None:
        """Log a protection violation."""
        event = {
            "address": address,
            "access_type": access_type,
            "segment": segment.name,
            "context": context
        }
        self.protection_events.append(event)


class SecurityProcessor(BaseProcessor):
    """Processor with security features."""
    
    def __init__(self, processor_id: int, memory: SecurityMemorySystem):
        super().__init__(processor_id)
        
        # Security-specific state
        self.privilege_level = PrivilegeLevel.USER
        self.control_flow_records: List[Any] = []
        self.memory = memory
        
        # CPU state for compatibility
        self.halted = False
        self.cycles = 0
        self.execution_time = 0.0
    
    def run(self, max_instructions: int) -> int:
        """Run CPU for max_instructions."""
        start_time = time.time()
        instructions_executed = 0
        
        while instructions_executed < max_instructions and not self.halted:
            # Simulate instruction execution
            self.cycles += 1
            instructions_executed += 1
            
            # Check for halt condition (simplified)
            if self.pc >= 1000:  # Arbitrary halt condition
                self.halted = True
                break
            
            # Advance PC
            self.pc += 1
        
        self.execution_time = time.time() - start_time
        return instructions_executed
    
    def reset(self) -> None:
        """Reset processor state."""
        super().reset()
        self.privilege_level = PrivilegeLevel.USER
        self.control_flow_records.clear()
        self.halted = False
        self.cycles = 0
        self.execution_time = 0.0


class SecurityVirtualMachine(BaseVirtualMachine):
    """
    Security Virtual Machine extending the unified base implementation.
    
    This class adds security features like memory protection, attack simulation,
    and forensic logging while using the common VM infrastructure.
    """
    
    def __init__(self, config: Optional[SecurityVMConfig] = None):
        """Initialize the security virtual machine."""
        self.security_config = config or SecurityVMConfig()
        
        # Create memory protection configuration before base initialization
        self.protection = MemoryProtection(
            level=self.security_config.protection_level,
            dep_enabled=self.security_config.dep_enabled,
            aslr_enabled=self.security_config.aslr_enabled,
            stack_canaries=self.security_config.stack_canaries,
            shadow_memory=self.security_config.shadow_memory,
        )
        
        # Initialize base VM with common functionality
        super().__init__(self.security_config)
        
        # Initialize forensic logging
        self.forensic_log = ForensicLog(
            enabled=self.security_config.enable_forensics,
            detailed=self.security_config.detailed_logging,
        )
        
        # Initialize CPU with security features
        self.cpu = SecurityProcessor(0, self.memory)
        
        # Track loaded programs
        self.program_loaded = False
        self.program_name = ""
        self.program_entry_point = 0
        
        # Apply memory protections
        self._apply_memory_protections()
    
    def _create_memory_system(self) -> SecurityMemorySystem:
        """Create security-specific memory system."""
        return SecurityMemorySystem(
            protection=self.protection,
            enable_tracking=self.config.enable_tracing
        )
    
    def _create_processors(self) -> List[SecurityProcessor]:
        """Create single processor with security features."""
        return [SecurityProcessor(0, self.memory)]
    
    def _apply_memory_protections(self) -> None:
        """Apply configured memory protections."""
        # Log the memory protection configuration
        self.forensic_log.log_system_event(
            "memory_protection_config",
            {
                "level": self.protection.level.name,
                "dep_enabled": self.protection.dep_enabled,
                "aslr_enabled": self.protection.aslr_enabled,
                "stack_canaries": self.protection.stack_canaries,
                "shadow_memory": self.protection.shadow_memory,
            }
        )
        
        # Log the memory map
        self.forensic_log.log_system_event(
            "memory_map",
            {"segments": self.memory.get_memory_map()}
        )
    
    def load_program(self, program: List[int], entry_point: Optional[int] = None) -> None:
        """Load a program (instruction bytes) into the code segment."""
        if len(program) > self.memory.code_segment.size:
            raise ValueError(f"Program size {len(program)} exceeds code segment size {self.memory.code_segment.size}")

        # Write program bytes to code segment
        for i, byte in enumerate(program):
            self.memory.write(
                self.memory.code_segment.base_address + i,
                byte,
                context={"operation": "program_load"}
            )

        # Set default entry point
        if entry_point is None:
            entry_point = self.memory.code_segment.base_address

        self.program_entry_point = entry_point
        self.program_loaded = True

        # Set instruction pointer to entry point
        self.cpu.pc = entry_point

        # Log program load
        self.forensic_log.log_system_event(
            "program_load",
            {
                "size": len(program),
                "entry_point": entry_point,
            }
        )
        
        if self.tracer:
            self.tracer.log_event("program_loaded", {
                "size": len(program),
                "entry_point": entry_point
            })
    
    def load_program_from_file(self, filename: str, entry_point: Optional[int] = None) -> None:
        """Load a program from a binary file."""
        with open(filename, "rb") as f:
            program = list(f.read())
        
        self.program_name = filename
        self.load_program(program, entry_point)
    
    def load_data(self, data: List[int], data_address: Optional[int] = None) -> int:
        """Load data into the data segment and return the address where it was loaded."""
        if data_address is None:
            data_address = self.memory.data_segment.base_address
        
        if not self.memory.data_segment.contains_address(data_address) or not self.memory.data_segment.contains_address(data_address + len(data) - 1):
            raise ValueError(f"Data doesn't fit in data segment at address 0x{data_address:08x}")
        
        # Write data bytes
        for i, byte in enumerate(data):
            self.memory.write(
                data_address + i,
                byte,
                context={"operation": "data_load"}
            )
        
        # Log data load
        self.forensic_log.log_system_event(
            "data_load",
            {
                "address": data_address,
                "size": len(data),
            }
        )
        
        return data_address
    
    def run(self, max_instructions: int = 10000) -> ExecutionResult:
        """Run the loaded program for up to max_instructions."""
        if not self.program_loaded:
            raise RuntimeError("No program loaded")
        
        # Log execution start
        self.forensic_log.log_system_event(
            "execution_start",
            {
                "entry_point": self.cpu.pc,
                "max_instructions": max_instructions,
            }
        )
        
        if self.tracer:
            self.tracer.log_event("execution_start", {
                "entry_point": self.cpu.pc,
                "max_instructions": max_instructions
            })
        
        # Run the CPU
        try:
            instructions_executed = self.cpu.run(max_instructions)
            success = True
        except Exception as e:
            instructions_executed = self.cpu.cycles
            success = False
            # Log the exception
            self.forensic_log.log_system_event(
                "execution_exception",
                {
                    "exception_type": type(e).__name__,
                    "message": str(e),
                    "instruction_pointer": self.cpu.pc,
                }
            )
            
            if self.tracer:
                self.tracer.log_security_event("execution_exception", {
                    "exception_type": type(e).__name__,
                    "message": str(e),
                    "instruction_pointer": self.cpu.pc,
                })
        
        # Log execution end
        self.forensic_log.log_system_event(
            "execution_end",
            {
                "cycles": self.cpu.cycles,
                "success": success,
                "halted": self.cpu.halted,
            }
        )
        
        # Process control flow records for forensic log
        control_flow_events = []
        for record in self.cpu.control_flow_records:
            event = {
                "from_address": getattr(record, 'from_address', 0),
                "to_address": getattr(record, 'to_address', 0),
                "event_type": getattr(record, 'event_type', 'unknown'),
                "instruction": getattr(record, 'instruction', ''),
                "legitimate": getattr(record, 'legitimate', True),
                "timestamp": getattr(record, 'timestamp', 0),
            }
            
            control_flow_events.append(event)
            self.forensic_log.log_control_flow(event)
        
        # Process protection events
        protection_events = []
        for event in self.memory.protection_events:
            protection_event = {
                "address": event.get("address", 0),
                "access_type": event.get("access_type", "unknown"),
                "segment": event.get("segment", "unknown"),
                "context": event.get("context", {}),
            }
            
            protection_events.append(protection_event)
            self.forensic_log.log_protection_violation(protection_event)
        
        # Create execution result
        result = ExecutionResult(
            success=success,
            cycles=self.cpu.cycles,
            execution_time=self.cpu.execution_time,
            cpu_state={"pc": self.cpu.pc, "registers": self.cpu.registers.copy()},
            control_flow_events=control_flow_events,
            protection_events=protection_events,
        )
        
        return result
    
    def get_memory_snapshot(self, segment_name: str = None) -> Dict[str, Any]:
        """Get a snapshot of memory contents, optionally filtered by segment name."""
        segments = []
        
        for segment in self.memory.segments:
            if segment_name is None or segment.name == segment_name:
                # Create a snapshot of this segment
                snapshot = {
                    "name": segment.name,
                    "base_address": segment.base_address,
                    "size": segment.size,
                    "permissions": {
                        "readable": segment.readable,
                        "writable": segment.writable,
                        "executable": segment.executable
                    },
                    "data": self.memory.dump_memory(segment.base_address, segment.size),
                }
                segments.append(snapshot)
        
        return {"segments": segments}
    
    def inject_vulnerability(
        self,
        vuln_type: str,
        address: int,
        size: int,
        payload: Optional[bytes] = None,
    ) -> Dict[str, Any]:
        """
        Inject a vulnerability into memory for demonstration purposes.
        """
        self.forensic_log.log_system_event(
            "vulnerability_injection",
            {
                "type": vuln_type,
                "address": address,
                "size": size,
                "has_payload": payload is not None,
            }
        )
        
        if self.tracer:
            self.tracer.log_security_event("vulnerability_injection", {
                "type": vuln_type,
                "address": address,
                "size": size,
                "has_payload": payload is not None,
            })
        
        result = {"success": False, "error": None}
        
        try:
            if vuln_type == "buffer_overflow":
                # Create a buffer overflow condition
                segment = self.memory.find_segment(address)
                if segment is None:
                    result["error"] = f"Address 0x{address:08x} not in any memory segment"
                    return result
                
                # Write beyond intended buffer size
                data = payload or bytes([0x41] * size)  # Default to 'A's if no payload
                self.memory.write_bytes(address, data, context={"vulnerability": "buffer_overflow"})
                result["success"] = True
                
            elif vuln_type == "use_after_free":
                # Simulate a use-after-free
                segment = self.memory.find_segment(address)
                if segment is None:
                    result["error"] = f"Address 0x{address:08x} not in any memory segment"
                    return result
                
                data = payload or bytes([0xDD] * size)  # Default to a "freed memory" pattern
                self.memory.write_bytes(address, data, context={"vulnerability": "use_after_free"})
                result["success"] = True
                
            elif vuln_type == "format_string":
                # Simulate a format string vulnerability
                segment = self.memory.find_segment(address)
                if segment is None:
                    result["error"] = f"Address 0x{address:08x} not in any memory segment"
                    return result
                
                format_string = payload or b"%x%x%x%n"
                self.memory.write_bytes(address, format_string, context={"vulnerability": "format_string"})
                result["success"] = True
                
            elif vuln_type == "code_injection":
                # Inject executable code
                segment = self.memory.find_segment(address)
                if segment is None:
                    result["error"] = f"Address 0x{address:08x} not in any memory segment"
                    return result
                
                shellcode = payload or bytes([0x90] * (size - 2) + [0x90, 0xC3])  # NOP sled + RET
                self.memory.write_bytes(address, shellcode, context={"vulnerability": "code_injection"})
                result["success"] = True
                
            else:
                result["error"] = f"Unknown vulnerability type: {vuln_type}"
        
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def get_forensic_logs(self, format_type: str = "dict") -> Union[List[Dict[str, Any]], str]:
        """Get forensic logs in the specified format."""
        return self.forensic_log.export_logs(format_type)
    
    def reset(self) -> None:
        """Reset the VM state while preserving configuration."""
        super().reset()
        
        # Reset CPU
        self.cpu.reset()
        
        # Reset memory protection events
        self.memory.protection_events = []
        
        # Reset program state
        self.program_loaded = False
        self.program_name = ""
        self.program_entry_point = 0
        
        # Reset stack pointer
        self.cpu.pc = 0
        
        # Log reset
        self.forensic_log.log_system_event("reset", {})
    
    def get_control_flow_visualization(self, format_type: str = "dict") -> Union[Dict[str, Any], str]:
        """Generate a visualization of the control flow."""
        records = self.cpu.control_flow_records
        
        nodes = set()
        edges = []
        
        for record in records:
            from_addr = getattr(record, 'from_address', 0)
            to_addr = getattr(record, 'to_address', 0)
            
            nodes.add(from_addr)
            nodes.add(to_addr)
            
            edge = {
                "source": from_addr,
                "target": to_addr,
                "type": getattr(record, 'event_type', 'unknown'),
                "legitimate": getattr(record, 'legitimate', True),
                "instruction": getattr(record, 'instruction', ''),
            }
            edges.append(edge)
        
        nodes_list = [{"address": addr} for addr in sorted(nodes)]
        
        visualization = {
            "nodes": nodes_list,
            "edges": edges,
        }
        
        if format_type == "dict":
            return visualization
        elif format_type == "json":
            import json
            return json.dumps(visualization, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format_type}")


# Backwards compatibility alias
VirtualMachine = SecurityVirtualMachine