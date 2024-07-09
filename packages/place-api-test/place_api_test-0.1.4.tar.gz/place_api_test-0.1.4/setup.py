from setuptools import find_packages, setup

PACKAGE_NAME = "place_api_test"

setup(
    name=PACKAGE_NAME,
    version="0.1.4",
    description="This is my tools package",
    packages=find_packages(),
    entry_points={
        "package_tools": ["place_api_tool = place.tools.utils:list_package_tools"],
    },
    include_package_data=True,  # This line tells setuptools to include files from MANIFEST.in
)
