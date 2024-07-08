from setuptools import find_packages, setup

PACKAGE_NAME = "recommendation_api"

setup(
    name=PACKAGE_NAME,
    version="0.0.1",
    description="This is recommendation api package",
    packages=find_packages(),
    entry_points={
        "package_tools": [
            "recommendation_api_tool = recommendation.tools.utils:list_package_tools"
        ],
    },
    include_package_data=True,  # This line tells setuptools to include files from MANIFEST.in
)
