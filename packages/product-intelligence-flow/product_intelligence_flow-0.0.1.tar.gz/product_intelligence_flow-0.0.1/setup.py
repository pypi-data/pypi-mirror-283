from setuptools import find_packages, setup

PACKAGE_NAME = "product_intelligence_flow"

setup(
    name=PACKAGE_NAME,
    version="0.0.1",
    description="This is Product Intelligence prompt flow",
    long_description="Sales Intelligence prompt flow",
    packages=find_packages(),
    entry_points={
        "package_tools": ["product_api_tool = product.tools.utils:list_package_tools"],
    },
    include_package_data=True,  # This line tells setuptools to include files from MANIFEST.in
)
