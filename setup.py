import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nina",
    version="v0.0.5",
    author="Ronald Rodrigues",
    author_email="ronald-farias@outlook.com",
    description="Generate README.md and setup.py quickly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ronald-TR/nina",
    packages=setuptools.find_packages("."),
    install_requires=[
        "colorama>=0.4.1",
        "PyInquirer>=1.0.3",
        "pyfiglet>=0.8.post1",
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ["create-readme = automail.cli:_cli"]
    }
)
