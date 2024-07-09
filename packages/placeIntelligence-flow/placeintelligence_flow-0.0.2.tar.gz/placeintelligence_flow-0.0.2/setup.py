from setuptools import find_packages, setup

PACKAGE_NAME = "placeIntelligence_flow"

setup(
    name=PACKAGE_NAME,
    version="0.0.2",
    description="Import another flow in prompt flow",
    packages=find_packages(),
    entry_points={
        "package_tools": ["call_flow_tool = call_flow.tools.utils:list_package_tools"],
    },
    include_package_data=True,  # This line tells setuptools to include files from MANIFEST.in
)
