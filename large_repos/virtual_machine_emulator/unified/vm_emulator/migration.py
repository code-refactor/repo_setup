"""
Migration script to update vm_emulator to use common library base classes.

This script handles the migration process and provides utilities to update
existing code to use the refactored classes.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Tuple


class VmEmulatorMigration:
    """Handles migration of vm_emulator to use common library."""
    
    def __init__(self, base_path: str):
        """Initialize migration with base path."""
        self.base_path = Path(base_path)
        self.vm_emulator_path = self.base_path / "vm_emulator"
        self.backup_path = self.base_path / "vm_emulator_backup"
    
    def create_backup(self) -> None:
        """Create backup of original vm_emulator."""
        if self.backup_path.exists():
            shutil.rmtree(self.backup_path)
        
        shutil.copytree(self.vm_emulator_path, self.backup_path)
        print(f"Backup created at: {self.backup_path}")
    
    def migrate_core_files(self) -> None:
        """Migrate core files to use refactored versions."""
        # File mappings: original -> refactored
        file_mappings = {
            "core/vm.py": "core/vm_refactored.py",
            "core/processor.py": "core/processor_refactored.py", 
            "core/memory.py": "core/memory_refactored.py",
        }
        
        for original, refactored in file_mappings.items():
            original_path = self.vm_emulator_path / original
            refactored_path = self.vm_emulator_path / refactored
            
            if refactored_path.exists():
                # Backup original and replace with refactored
                backup_original = original_path.with_suffix(".py.backup")
                if original_path.exists():
                    shutil.move(str(original_path), str(backup_original))
                shutil.move(str(refactored_path), str(original_path))
                print(f"Migrated: {original}")
    
    def update_imports(self) -> None:
        """Update import statements throughout the codebase."""
        import_updates = [
            # VM imports
            (
                "from vm_emulator.core.vm import VirtualMachine",
                "from vm_emulator.core.vm import ParallelVirtualMachine as VirtualMachine"
            ),
            (
                "from .vm import VirtualMachine", 
                "from .vm import ParallelVirtualMachine as VirtualMachine"
            ),
            
            # Processor imports
            (
                "from vm_emulator.core.processor import Processor",
                "from vm_emulator.core.processor import ParallelProcessor as Processor"
            ),
            (
                "from .processor import Processor",
                "from .processor import ParallelProcessor as Processor"
            ),
            
            # Memory imports
            (
                "from vm_emulator.core.memory import MemorySystem",
                "from vm_emulator.core.memory import ParallelMemorySystem as MemorySystem"
            ),
            (
                "from .memory import MemorySystem",
                "from .memory import ParallelMemorySystem as MemorySystem"
            ),
        ]
        
        # Find all Python files in vm_emulator
        python_files = list(self.vm_emulator_path.rglob("*.py"))
        
        for file_path in python_files:
            if file_path.name.endswith("_refactored.py") or file_path.name == "migration.py":
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Apply import updates
                for old_import, new_import in import_updates:
                    content = content.replace(old_import, new_import)
                
                # Write back if changed
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Updated imports in: {file_path.relative_to(self.base_path)}")
                    
            except Exception as e:
                print(f"Error updating {file_path}: {e}")
    
    def update_class_instantiation(self) -> None:
        """Update class instantiation to use new configuration system."""
        # Find files that instantiate VirtualMachine
        python_files = list(self.vm_emulator_path.rglob("*.py"))
        
        for file_path in python_files:
            if file_path.name.endswith("_refactored.py") or file_path.name == "migration.py":
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Update VirtualMachine instantiation
                # Old: VirtualMachine(num_processors=4, memory_size=65536, random_seed=42)
                # New: VirtualMachine(ParallelVMConfig(num_processors=4, memory_size=65536, random_seed=42))
                
                # This is a complex replacement that would need regex or AST parsing
                # For now, we'll add a comment about manual updates needed
                if "VirtualMachine(" in content and "num_processors" in content:
                    # Add import for config class if not present
                    if "from vm_emulator.core.vm import ParallelVMConfig" not in content:
                        # Find the first import line and add after it
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if line.startswith('from vm_emulator.core.vm import'):
                                if 'ParallelVMConfig' not in line:
                                    lines[i] = line + ', ParallelVMConfig'
                                break
                        else:
                            # Add new import line
                            for i, line in enumerate(lines):
                                if line.startswith('from vm_emulator.core'):
                                    lines.insert(i + 1, 'from vm_emulator.core.vm import ParallelVMConfig')
                                    break
                        
                        content = '\n'.join(lines)
                
                # Write back if changed
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Updated class instantiation in: {file_path.relative_to(self.base_path)}")
                    
            except Exception as e:
                print(f"Error updating {file_path}: {e}")
    
    def update_init_files(self) -> None:
        """Update __init__.py files to expose new classes."""
        init_files = {
            "core/__init__.py": [
                "from .vm import ParallelVirtualMachine, ParallelVMConfig",
                "from .processor import ParallelProcessor, ParallelProcessorConfig", 
                "from .memory import ParallelMemorySystem",
                "",
                "# Backwards compatibility aliases",
                "VirtualMachine = ParallelVirtualMachine",
                "Processor = ParallelProcessor",
                "MemorySystem = ParallelMemorySystem",
            ],
            "__init__.py": [
                "from .core.vm import ParallelVirtualMachine, ParallelVMConfig",
                "from .core.processor import ParallelProcessor, ParallelProcessorConfig",
                "from .core.memory import ParallelMemorySystem",
                "",
                "# Backwards compatibility",
                "from .core.vm import ParallelVirtualMachine as VirtualMachine",
                "from .core.processor import ParallelProcessor as Processor",
                "from .core.memory import ParallelMemorySystem as MemorySystem",
                "",
                "__all__ = [",
                "    'ParallelVirtualMachine', 'ParallelVMConfig',",
                "    'ParallelProcessor', 'ParallelProcessorConfig',",
                "    'ParallelMemorySystem',",
                "    'VirtualMachine', 'Processor', 'MemorySystem',  # Backwards compatibility",
                "]",
            ]
        }
        
        for init_file, lines in init_files.items():
            init_path = self.vm_emulator_path / init_file
            
            # Backup existing init file
            if init_path.exists():
                backup_path = init_path.with_suffix(".py.backup")
                shutil.copy2(str(init_path), str(backup_path))
            
            # Write new init file
            with open(init_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            
            print(f"Updated: {init_file}")
    
    def run_migration(self) -> None:
        """Run the complete migration process."""
        print("Starting vm_emulator migration to use common library...")
        
        # Step 1: Create backup
        print("\n1. Creating backup...")
        self.create_backup()
        
        # Step 2: Migrate core files
        print("\n2. Migrating core files...")
        self.migrate_core_files()
        
        # Step 3: Update imports
        print("\n3. Updating import statements...")
        self.update_imports()
        
        # Step 4: Update class instantiation
        print("\n4. Updating class instantiation...")
        self.update_class_instantiation()
        
        # Step 5: Update __init__ files
        print("\n5. Updating __init__.py files...")
        self.update_init_files()
        
        print("\nMigration completed!")
        print("\nManual steps still needed:")
        print("1. Review and test all functionality")
        print("2. Update any VirtualMachine() constructor calls to use ParallelVMConfig")
        print("3. Update any direct processor instantiation")
        print("4. Run tests to ensure compatibility")
        print(f"5. Original files backed up to: {self.backup_path}")
    
    def rollback_migration(self) -> None:
        """Rollback the migration by restoring from backup."""
        if not self.backup_path.exists():
            print("No backup found. Cannot rollback.")
            return
        
        print("Rolling back migration...")
        
        # Remove current vm_emulator
        if self.vm_emulator_path.exists():
            shutil.rmtree(self.vm_emulator_path)
        
        # Restore from backup
        shutil.copytree(self.backup_path, self.vm_emulator_path)
        
        print("Migration rolled back successfully!")


def main():
    """Main migration function."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python migration.py <command>")
        print("Commands: migrate, rollback")
        return
    
    command = sys.argv[1]
    base_path = Path(__file__).parent.parent  # Go up from vm_emulator/migration.py
    
    migrator = VmEmulatorMigration(str(base_path))
    
    if command == "migrate":
        migrator.run_migration()
    elif command == "rollback":
        migrator.rollback_migration()
    else:
        print(f"Unknown command: {command}")
        print("Commands: migrate, rollback")


if __name__ == "__main__":
    main()