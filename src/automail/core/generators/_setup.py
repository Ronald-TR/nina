TEMPLATE = """import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="{project_name}",
    version="{project_version}",
    author="{author_name}",
    author_email="{author_email}",
    description="{project_description}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="{repository_url}",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: {license_type} License",
        "Operating System :: OS Independent",
    ],
)
"""


def build_setup(fields):
    template = TEMPLATE.format(
        **{
            "project_name": fields["project_name"],
            "project_version": fields["project_version"],
            "author_name": fields["author_name"],
            "author_email": fields["author_email"],
            "project_description": fields["project_description"],
            "repository_url": fields["repository_url"],
            "license_type": fields["license_type"],
        }
    )
    return template
