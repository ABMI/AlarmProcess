import sys
from cx_Freeze import setup, Executable

setup(
        name="newMedicalTermsDbBuildingTool",
        version="1.0",
        description="",
        author="DongsuPark",
        executables = [Executable("Crawling.py")]
)


