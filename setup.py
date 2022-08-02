"""
Setup module for the gryphon package.
"""
import glob
from pathlib import Path

from setuptools import setup, find_packages

from gryphon import __version__


def glob_hidden(*args, **kwargs):
    """A glob.glob that include dot files and hidden files"""
    old_is_hidden = glob._ishidden
    glob._ishidden = lambda x: False

    try:
        result = glob.glob(*args, **kwargs)
    finally:
        glob._ishidden = old_is_hidden

    return result


data_path = Path('gryphon') / 'data'

json_pattern = str(data_path / '*.json')
yml_pattern = str(data_path / '*.yaml')
project_scaffolding_pattern = str(data_path / 'template_scaffolding' / "**")
ci_cd_pattern = str(data_path / 'ci_cd' / "**")

config_files = glob_hidden(json_pattern, recursive=True)
yaml_config_files = glob_hidden(yml_pattern, recursive=True)
scaffolding_files = glob_hidden(project_scaffolding_pattern, recursive=True)
ci_cd_files = glob_hidden(ci_cd_pattern, recursive=True)

package_files = []
package_files.extend(config_files)
package_files.extend(yaml_config_files)
package_files.extend(scaffolding_files)
package_files.extend(ci_cd_files)

# package_files = list(set(map(lambda x: str(Path(x).relative_to(data_path)), package_files)))
package_files = list(set(map(lambda x: x[8:], package_files)))
package_files = sorted(package_files)


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name='gryphon',
    version=__version__,
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
        grifon=gryphon.gryphon_wizard:did_you_mean_gryphon
        gryfon=gryphon.gryphon_wizard:did_you_mean_gryphon
    ''',
    # gryph=gryphon.gryphon_cli: cli
    include_package_data=True,
    package_data={'gryphon': package_files}
)
