"""
Setup module for the labskit package.  
"""
import glob
from setuptools import setup, find_packages


package_files = list(map(lambda x: x[6:], glob.glob('./labskit_commands/data/**', recursive=True)))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

#TODO: Clone git repositories from config.json at the time of installation

setup(
    name = 'labskit',
    version = '0.0.1',
    license = 'MIT',
    description = 'OW analytics toolkit cli',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    py_modules = ['labskit', 'labskit_commands'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        labskit=labskit:cli
    ''',
    include_package_data=True,
    package_data={'labskit_commands': package_files}
)
