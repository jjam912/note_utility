import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="noteutil",
    version="0.0.1",
    author="James Song Wang | jjam912",
    author_email="new.jjam912@gmail.com",
    description="A module to turn specifically written notes into terms and categories.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jjam912/noteutil",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)