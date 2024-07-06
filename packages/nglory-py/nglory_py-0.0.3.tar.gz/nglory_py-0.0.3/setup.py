from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'Easy Access for NationsGlory API in Python'
LONG_DESCRIPTION = 'A package that allows to easily access the NationsGlory API in Python.'

# Setting up
setup(
    name="nglory-py",
    version=VERSION,
    author="BigTallahasee",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)