from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="dgtl_logging",
    version="0.0.4",
    description="DGTL Health BV NEN7513 compliant logging objects ",
    author="Olivier Witteman",
    license="MIT",
    packages=["dgtl_logging"],
    install_requires=[],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
    ]
)
