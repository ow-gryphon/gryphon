"""
Setup module for the gryphon package.
"""
import glob
from pathlib import Path
from setuptools import setup, find_packages

package_files = [
    str(Path('data') / 'gryphon_config.json'),
    str(Path('data') / 'library_tree.json'),
    str(Path('data') / 'links_about.json'),
    str(Path('data') / 'category_tree.json'),
    str(Path('data') / 'settings_tree.json'),
    str(Path('data') / 'python_versions_observations.json')
]

template_files = glob.glob(
    str(Path('gryphon') / 'data' / 'template_scaffolding' / "**" ),
    recursive=True
)
template_files.extend(
    glob.glob(
        str(Path('gryphon') / 'data' / 'template_scaffolding' / "template" / ".github" / "**") ,
        recursive=True
    )
)

template_files = set(map(lambda x: x[8:], template_files))

print(template_files)
package_files.extend(template_files)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name='gryphon',
    version='0.0.2',
    license='MIT',
    description='OW analytics toolkit cli',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['gryphon'],
    packages=find_packages(),
    install_requires=[requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points='''
        [console_scripts]
        gryphon=gryphon.gryphon_wizard:main
        griffin=gryphon.gryphon_wizard:did_you_mean_gryphon
    ''',
    # gryph=gryphon.gryphon_cli: cli
    include_package_data=True,
    package_data={'gryphon': package_files}
)
