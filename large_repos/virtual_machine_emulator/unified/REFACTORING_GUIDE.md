# VM Emulator Refactoring Guide

This guide explains how the vm_emulator package has been refactored to use the common library base classes while preserving all parallel-specific functionality.

## Overview

The refactoring eliminates code duplication by having vm_emulator extend from the common library base classes:

- `VirtualMachine` → `ParallelVirtualMachine` (extends `BaseVirtualMachine`)
- `Processor` → `ParallelProcessor` (extends `BaseProcessor`)
- `MemorySystem` → `ParallelMemorySystem` (extends `UnifiedMemorySystem`)

## Key Benefits

1. **Code Reuse**: Common functionality is inherited from base classes
2. **Consistency**: Unified interface across all VM implementations
3. **Enhanced Features**: Access to advanced tracing and metrics
4. **Maintainability**: Changes to common functionality benefit all VMs
5. **Extensibility**: Easy to add new features to the common base

## Migration Details

### VirtualMachine Changes

**Before:**
```python
from vm_emulator.core.vm import VirtualMachine

vm = VirtualMachine(
    num_processors=4,
    memory_size=65536,
    random_seed=42
)
```

**After:**
```python
from vm_emulator.core.vm import ParallelVirtualMachine, ParallelVMConfig

# Recommended approach with configuration
config = ParallelVMConfig(
    num_processors=4,
    memory_size=65536,
    random_seed=42,
    enable_race_detection=True,
    enable_synchronization=True
)
vm = ParallelVirtualMachine(config)

# Or use backwards compatibility alias
from vm_emulator.core.vm import VirtualMachine  # This is now ParallelVirtualMachine
vm = VirtualMachine(config)
```

### New Features Available

#### Enhanced Tracing
```python
# Access the built-in tracer
if vm.tracer:
    events = vm.tracer.get_events(event_type=EventType.INSTRUCTION)
    timeline = vm.tracer.get_timeline()
    chrome_trace = vm.tracer.export_chrome_trace()
```

#### Performance Metrics
```python
# Access detailed performance metrics
if vm.metrics:
    stats = vm.metrics.get_metrics()
    summary = vm.metrics.get_performance_summary()
    efficiency = vm.metrics.get_efficiency_analysis()
```

#### Advanced Memory System
```python
# Access memory segments and advanced features
memory_map = vm.memory.get_memory_map()
access_pattern = vm.memory.get_access_pattern()
```

### Processor Changes

**Before:**
```python
from vm_emulator.core.processor import Processor

processor = Processor(processor_id=0)
```

**After:**
```python
from vm_emulator.core.processor import ParallelProcessor, ParallelProcessorConfig

config = ParallelProcessorConfig(
    enable_stall_cycles=True,
    enable_latency_simulation=True
)
processor = ParallelProcessor(processor_id=0, config=config)

# Or use backwards compatibility
from vm_emulator.core.processor import Processor  # This is now ParallelProcessor
processor = Processor(processor_id=0)
```

### Memory System Changes

**Before:**
```python
from vm_emulator.core.memory import MemorySystem

memory = MemorySystem(size=65536)
```

**After:**
```python
from vm_emulator.core.memory import ParallelMemorySystem

memory = ParallelMemorySystem(size=65536, enable_tracking=True)

# Access new features
races = memory.detect_potential_races()
stats = memory.get_memory_access_statistics()
```

## Preserved Functionality

All existing parallel-specific functionality is preserved:

### Thread Management
- Thread creation and scheduling
- Context switching
- Thread synchronization

### Race Condition Detection
- Shared memory access tracking
- Race condition detection and reporting
- Memory access pattern analysis

### Synchronization Primitives
- Locks, semaphores, barriers
- Lock contention tracking
- Deadlock detection

### Performance Analysis
- Processor utilization
- Context switch overhead
- Memory access patterns

## Configuration System

The new configuration system provides better control:

```python
from vm_emulator.core.vm import ParallelVMConfig

config = ParallelVMConfig(
    # Base VM config
    memory_size=65536,
    enable_tracing=True,
    enable_metrics=True,
    random_seed=42,
    
    # Parallel-specific config
    num_processors=4,
    enable_race_detection=True,
    enable_synchronization=True,
    enable_detailed_threading=True
)
```

## Testing Compatibility

Run the existing tests to ensure compatibility:

```bash
# Run all vm_emulator tests
python -m pytest tests/parallel_researcher/

# Run specific test categories
python -m pytest tests/parallel_researcher/core/
python -m pytest tests/parallel_researcher/memory/
python -m pytest tests/parallel_researcher/synchronization/
```

## Common Issues and Solutions

### Issue: Import Errors
**Problem**: Old imports not working
**Solution**: Update imports or use backwards compatibility aliases

### Issue: Constructor Arguments
**Problem**: Old constructor signature not working
**Solution**: Use configuration objects or update to new signature

### Issue: Missing Methods
**Problem**: Methods not found on VM instance
**Solution**: Check if method moved to tracer, metrics, or memory components

## Example: Complete Migration

Here's a complete example showing before and after:

**Before:**
```python
from vm_emulator.core.vm import VirtualMachine
from vm_emulator.core.program import Program
from vm_emulator.core.instruction import InstructionSet

# Create VM
vm = VirtualMachine(num_processors=2, memory_size=1024)

# Create and load program
program = Program.create_simple_program("test", [
    ("ADD", ["R1", "R2", "R3"]),
    ("STORE", ["R1", "100"]),
    ("HALT", [])
])
program_id = vm.load_program(program)
thread_id = vm.create_thread(program_id)

# Run simulation
vm.run(max_cycles=100)

# Get results
stats = vm.get_statistics()
races = vm.get_race_conditions()
```

**After:**
```python
from vm_emulator.core.vm import ParallelVirtualMachine, ParallelVMConfig
from vm_emulator.core.program import Program
from vm_emulator.core.instruction import InstructionSet

# Create VM with configuration
config = ParallelVMConfig(
    num_processors=2, 
    memory_size=1024,
    enable_race_detection=True,
    enable_tracing=True
)
vm = ParallelVirtualMachine(config)

# Create and load program (same as before)
program = Program.create_simple_program("test", [
    ("ADD", ["R1", "R2", "R3"]),
    ("STORE", ["R1", "100"]),
    ("HALT", [])
])
program_id = vm.load_program(program)
thread_id = vm.create_thread(program_id)

# Run simulation (same as before)
vm.run(max_cycles=100)

# Get enhanced results
stats = vm.get_statistics()  # Now includes common metrics
races = vm.get_race_conditions()  # Same as before

# Access new features
if vm.tracer:
    trace_events = vm.tracer.get_events()
    timeline = vm.tracer.get_timeline()

if vm.metrics:
    performance = vm.metrics.get_performance_summary()
    efficiency = vm.metrics.get_efficiency_analysis()
```

## Next Steps

1. **Run Migration Script**: Use the provided migration script to automatically update imports
2. **Update Configurations**: Replace constructor arguments with configuration objects
3. **Test Thoroughly**: Run all existing tests to ensure compatibility
4. **Explore New Features**: Take advantage of enhanced tracing and metrics
5. **Update Documentation**: Update any project-specific documentation

The refactoring maintains full backwards compatibility while providing access to enhanced features from the common library.