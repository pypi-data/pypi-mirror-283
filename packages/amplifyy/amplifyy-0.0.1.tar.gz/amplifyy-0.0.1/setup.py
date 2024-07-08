from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Image Augmentation Tool'

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="amplifyy",
    version=VERSION,
    author="Adarsh Kesharwani",
    author_email="<akesherwani900@gamil.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
    keywords=['python','image augement','augmentation'],
    entry_points={
        "console_scripts":[
            "amplifyy = amplifyy:welcome",
        ],
    },
)
