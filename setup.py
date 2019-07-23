import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="noteutil",
    version="0.0.4",
    author="James S. Wang",
    author_email="jjameswwang@gmail.com",
    description="A package for handling specially written notes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JJamesWWang/noteutil",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)