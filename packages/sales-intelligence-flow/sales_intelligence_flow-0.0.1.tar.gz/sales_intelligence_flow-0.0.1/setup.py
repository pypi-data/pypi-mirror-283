from setuptools import find_packages, setup

PACKAGE_NAME = "sales_intelligence_flow"

setup(
    name=PACKAGE_NAME,
    version="0.0.1",
    description="This is Sales Intelligence prompt flow",
    long_description="This is Sales Intelligence prompt flow",
    packages=find_packages(),
    entry_points={
        "package_tools": ["sales_api_tool = sales.tools.utils:list_package_tools"],
    },
    include_package_data=True,  # This line tells setuptools to include files from MANIFEST.in
)
