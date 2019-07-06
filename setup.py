import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="automail",
    version="v0.0.1",
    author="Ronald Rodrigues",
    author_email="ronald@teste.com",
    description="Generate README.md and setup.py quickly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="github.com/teste",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "colorama>=0.4.1",
        "inquirer>=2.6.3",
        "pyfiglet>=0.8.post1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ["create-readme = automail.cli:main"]
    }
)
