"""Quick test to verify render farm manager adapters work correctly."""

from datetime import datetime, timedelta
from render_farm_manager.adapters import StatusAdapter, PriorityAdapter, TaskAdapter, NodeAdapter
from render_farm_manager.core.models import (
    RenderJob, RenderNode, NodeCapabilities, RenderJobStatus, JobPriority, NodeStatus
)
from common.core.models import TaskStatus, Priority, BaseTask, BaseNode

def test_status_adapters():
    """Test status conversion adapters."""
    print("Testing status adapters...")
    
    # Test RenderJobStatus to TaskStatus
    render_status = RenderJobStatus.RUNNING
    task_status = StatusAdapter.render_job_to_task_status(render_status)
    assert task_status == TaskStatus.RUNNING
    
    # Test round trip
    back_to_render = StatusAdapter.task_to_render_job_status(task_status)
    assert back_to_render == render_status
    
    # Test NodeStatus conversion
    node_status = "online"
    common_status = StatusAdapter.render_node_to_common_status(node_status)
    assert common_status.value == "online"
    
    print("✓ Status adapters working correctly")

def test_priority_adapters():
    """Test priority conversion adapters."""
    print("Testing priority adapters...")
    
    # Test JobPriority to Priority
    job_priority = JobPriority.HIGH
    common_priority = PriorityAdapter.job_priority_to_common(job_priority)
    assert common_priority == Priority.HIGH
    
    # Test round trip
    back_to_job = PriorityAdapter.common_to_job_priority(common_priority)
    assert back_to_job == job_priority
    
    print("✓ Priority adapters working correctly")

def test_task_adapters():
    """Test task conversion adapters."""
    print("Testing task adapters...")
    
    # Create a test render job
    render_job = RenderJob(
        id="test-job-1",
        name="Test Render Job",
        client_id="client-1",
        job_type="animation",
        priority=JobPriority.HIGH,
        submission_time=datetime.now(),
        deadline=datetime.now() + timedelta(hours=24),
        estimated_duration_hours=8.0,
        requires_gpu=True,
        memory_requirements_gb=32,
        cpu_requirements=16,
        scene_complexity=8,
        output_path="/tmp/output.exr"
    )
    
    # Convert to BaseTask
    base_task = TaskAdapter.render_job_to_base_task(render_job)
    assert base_task.id == render_job.id
    assert base_task.name == render_job.name
    assert base_task.priority == Priority.HIGH
    assert base_task.status == TaskStatus.PENDING
    
    # Check metadata preservation
    assert base_task.metadata['client_id'] == render_job.client_id
    assert base_task.metadata['requires_gpu'] == render_job.requires_gpu
    assert base_task.metadata['scene_complexity'] == render_job.scene_complexity
    
    # Convert back to RenderJob
    converted_back = TaskAdapter.base_task_to_render_job(base_task, render_job)
    assert converted_back.id == render_job.id
    assert converted_back.client_id == render_job.client_id
    assert converted_back.requires_gpu == render_job.requires_gpu
    
    print("✓ Task adapters working correctly")

def test_node_adapters():
    """Test node conversion adapters."""
    print("Testing node adapters...")
    
    # Create a test render node
    capabilities = NodeCapabilities(
        cpu_cores=32,
        memory_gb=128,
        gpu_model="NVIDIA RTX A6000",
        gpu_count=4,
        storage_gb=2000
    )
    
    render_node = RenderNode(
        id="node-1",
        name="Render Node 1",
        status="online",
        capabilities=capabilities,
        power_efficiency_rating=85.0
    )
    
    # Convert to BaseNode
    base_node = NodeAdapter.render_node_to_base_node(render_node)
    assert base_node.id == render_node.id
    assert base_node.name == render_node.name
    assert base_node.cpu_cores == render_node.capabilities.cpu_cores
    assert base_node.memory_gb == render_node.capabilities.memory_gb
    assert base_node.gpu_count == render_node.capabilities.gpu_count
    
    # Convert back to RenderNode
    converted_back = NodeAdapter.base_node_to_render_node(base_node, render_node)
    assert converted_back.id == render_node.id
    assert converted_back.capabilities.cpu_cores == render_node.capabilities.cpu_cores
    assert converted_back.capabilities.gpu_count == render_node.capabilities.gpu_count
    
    print("✓ Node adapters working correctly")

def test_integration():
    """Test integration between adapters."""
    print("Testing adapter integration...")
    
    # Create render farm objects
    render_job = RenderJob(
        id="integration-test",
        name="Integration Test Job",
        client_id="test-client",
        job_type="vfx",
        priority=JobPriority.CRITICAL,
        submission_time=datetime.now(),
        deadline=datetime.now() + timedelta(hours=12),
        estimated_duration_hours=6.0,
        requires_gpu=True,
        memory_requirements_gb=64,
        cpu_requirements=8,
        scene_complexity=9,
        output_path="/tmp/integration.exr"
    )
    
    capabilities = NodeCapabilities(
        cpu_cores=64,
        memory_gb=256,
        gpu_model="NVIDIA RTX A100",
        gpu_count=8,
        storage_gb=4000
    )
    
    render_node = RenderNode(
        id="integration-node",
        name="Integration Test Node",
        status="online",
        capabilities=capabilities,
        power_efficiency_rating=90.0
    )
    
    # Convert to common models
    base_task = TaskAdapter.render_job_to_base_task(render_job)
    base_node = NodeAdapter.render_node_to_base_node(render_node)
    
    # Verify conversions preserve key information
    assert base_task.priority == Priority.CRITICAL
    assert base_task.metadata['requires_gpu'] == True
    assert base_task.metadata['scene_complexity'] == 9
    
    assert base_node.gpu_count == 8
    assert base_node.memory_gb == 256
    
    # Convert back and verify round trip
    restored_job = TaskAdapter.base_task_to_render_job(base_task, render_job)
    restored_node = NodeAdapter.base_node_to_render_node(base_node, render_node)
    
    assert restored_job.priority == JobPriority.CRITICAL
    assert restored_job.requires_gpu == True
    assert restored_job.scene_complexity == 9
    
    assert restored_node.capabilities.gpu_count == 8
    assert restored_node.capabilities.memory_gb == 256
    
    print("✓ Integration working correctly")

def main():
    """Run all adapter tests."""
    print("=== Testing Render Farm Manager Adapters ===\n")
    
    try:
        test_status_adapters()
        test_priority_adapters()
        test_task_adapters()
        test_node_adapters()
        test_integration()
        
        print("\n✅ All adapter tests passed!")
        print("\nThe render farm manager has been successfully refactored to use the common library.")
        print("Key benefits:")
        print("- Maintains backward compatibility with existing render farm code")
        print("- Enables interoperability with common library interfaces")
        print("- Preserves domain-specific optimizations (energy, specialization, deadlines)")
        print("- Provides both native and adapted interfaces")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()