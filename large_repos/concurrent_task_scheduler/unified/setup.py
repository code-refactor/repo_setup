from setuptools import setup

setup(
    name="unified-concurrent_task_scheduler",
    version="0.1.0",
    description="Unified libraries for concurrent_task_scheduler with original package names preserved",
    packages=["common", "concurrent_task_scheduler", "render_farm_manager"],
    python_requires=">=3.10",
)
