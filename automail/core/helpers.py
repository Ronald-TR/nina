import os
import json
import subprocess
import requests
from datetime import datetime

import PyInquirer as inquirer

from automail.core.parsers import FactoryParser

CONFIG_FILENAME = "nina-config.json"
LICENSES = {
    "MIT": "mit",
    "GNU AGPLv3": "agpl-3.0",
    "GNU GPLv3": "gpl-3.0",
    "GNU LGPLv3": "lgpl-3.0",
    "Unlicense": "unlicense",
    "Apache 2.0": "apache-2.0",
    "Mozilla Public License 2.0": "mpl-2.0"
}


def get_license(fields):
    license_type = LICENSES.get(fields["license_type"])
    URL = "https://api.github.com/licenses/"
    _license = ""

    if license_type:
        r = requests.get(URL + license_type)
        _license = r.json().get("body")
        _license = _license.replace("[year]", str(datetime.now().year))
        _license = _license.replace("[fullname]", fields.get("author_name"))

    return _license


def template_reserved_fields():
    return ["cov_output", "tests_passing"]


def template_fields():
    return {
        "project_name": "",
        "project_version": "",
        "project_description": "",
        "project_homepage": "",
        "author_name": "",
        "author_email": "",
        "git_username": "",
        "repository_url": "",
        "twitter_username": "",
        "project_prerequisites": "",
        "license_type": "",
        "install_command": "",
        "test_command": "",
    }


def inquirer_questions(fields, suggestions, skip=list()[:]):
    questions = []
    for k, _ in fields.items():
        if k in skip:
            continue

        if k == "license_type":
            questions += [
                {
                    "type": "list",
                    "name": k,
                    "message": "What's the License Type?",
                    "choices": [
                        "MIT",
                        "GNU AGPLv3",
                        "GNU GPLv3",
                        "GNU LGPLv3",
                        "Unlicense",
                        "Apache 2.0",
                        "Mozilla Public License 2.0",
                    ]
                }
            ]
            continue

        msg = "What's the " + " ".join(k.split("_")).title() + "?"
        sg = suggestions.get(k) or ""
        questions += [
            {
                "type": "input",
                "name": k,
                "message": msg,
                "default": sg
            }
        ]

    return questions


def suggestions_by(_dict, parser=None):
    if parser:
        sg = parser.__dict__.copy()
    else:
        sg = _dict.copy()

    default_description = "My Awesome project!"
    repository_url = sg.get("repository_url") or ""
    project_homepage = sg.get("project_homepage") or ""
    project_description = sg.get("project_description") or default_description

    if parser:
        repository_url = (
            f"https://{parser.gtype}.com/"
            f"{parser.git_username}/{parser.project_name}"
        )

        project_homepage = f"https://{parser.project_name}.{parser.gtype}.io/"

    sg["repository_url"] = repository_url
    sg["project_homepage"] = project_homepage
    sg["project_description"] = project_description
    sg["project_version"] = "v0.0.1"

    return sg


def bool_question(question):
    question = [
        {
            "name": "question",
            "type": "list",
            "message": question,
            "choices": ["YES", "NO"]
        }
    ]
    answer = inquirer.prompt(question)
    if not answer:
        raise KeyboardInterrupt

    return True if answer.get("question") == "YES" else False


def automail_config_file_question():
    if os.path.isfile(CONFIG_FILENAME):
        msg = (
            "Have a configuration file in the root,"
            "do you want to use them to fill the questions?"
        )
        if bool_question(msg):
            with open(CONFIG_FILENAME, "r") as _f:
                return json.load(_f)
    return None


def get_env_dir():
    return os.path.basename(os.getenv("VIRTUAL_ENV") or "")


def git_repo_question():
    git = subprocess.run(
        ["git", "remote", "-v"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)
    parser = None
    if git.returncode == 0:
        msg = (
            "Seems that you have a GIT repository. "
            "Do you want to use it to answer some questions?"
        )
        if bool_question(msg):
            parser = FactoryParser()
    return parser


def coverage_parser(fields):
    relactory, percent = "", "0"
    aux = fields["cov_output"].split("\n")
    for i, v in enumerate(aux):
        if "coverage: platform" in v:
            relactory = aux[i:-1]
        if "TOTAL" in v:
            percent = v.replace("\t", " ").split(" ")[-1].replace("%", "")

    return {"relactory": relactory, "percent": int(percent)}


def fmt(text):
    """used specially for badge fields"""
    special = ["-", " "]
    for i in special:
        text = text.replace(i, "_")
    return text
