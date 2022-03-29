import setuptools

with open("template/README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as fr:
    requirements = fr.read().strip().split('\n')

setuptools.setup(
    name="",
    version="v0.0.1",
    author="",
    author_email="",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
)
