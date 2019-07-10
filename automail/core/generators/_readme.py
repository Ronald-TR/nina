from automail.core.helpers import coverage_parser, fmt

TEMPLATE = """
# {project_name}

{badges}

## :house: [Homepage]({project_homepage})
{project_description}


## Installation

    {install_command}

## Test Command
To test the application, run the following command:

    {test_command}

## [License](LICENSE.md)
<details>
    <summary>{license_type}</summary>
{license_body}
</details>

## Author
Learn more about: {author_name}

Email: {author_email}

[Github :octocat:](https://github.com/{git_username})
[Twitter](https://twitter.com/{twitter_username})
"""


def create_badge(md_tag, name, value, color):
    BASE = "https://img.shields.io/badge/"
    return f"![{md_tag}]({BASE}{name}-{value}-{color}.svg)"


def create_badges(fields):
    def version():
        return create_badge(
            "version",
            fmt(fields["project_name"]),
            fields["project_version"],
            "brightgreen",
        )

    def coverage():
        if not fields.get("cov_output"):
            return ""

        color_cov = "green"
        cov = coverage_parser(fields)
        if cov["percent"] <= 30:
            color_cov = "yellow"
        elif cov["percent"] <= 70:
            color_cov = "green"
        elif cov["percent"] <= 90:
            color_cov = "brightgreen"

        return create_badge(
            "coverage", "coverage", str(cov["percent"]) + "%25", color_cov
        )

    def test_passing():
        tests = fields.get("tests_passing")
        if tests is None:
            return ""

        res = "passing" if tests else "failing"
        color = "green" if tests else "red"
        return create_badge("tests", "tests", res, color)

    def license():
        license = fmt(fields.get("license_type"))
        if license:
            return create_badge("license", "license", license, "green")
        return ""

    return [version(), coverage(), test_passing(), license()]


def build_readme(fields, _license):
    badges = " ".join(create_badges(fields))

    template = TEMPLATE.format(
        **{
            "project_name": fields["project_name"],
            "badges": badges,
            "project_homepage": fields["project_homepage"],
            "project_description": fields["project_description"],
            "install_command": fields["install_command"],
            "test_command": fields["test_command"],
            "license_type": fields["license_type"],
            "license_body": _license,
            "author_name": fields["author_name"],
            "author_email": fields["author_email"],
            "git_username": fields["git_username"],
            "twitter_username": fields["twitter_username"],
        }
    )
    return template
