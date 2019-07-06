import os
import subprocess as cmd

from pyfiglet import Figlet
from colorama import Fore
import inquirer

from core.helpers import (
    bool_question,
    inquirer_questions,
    git_repo_question,
    get_env_dir,
    readmepy_config_file_question,
    suggestions_by,
    FIELDS,
    RESERVED_FIELDS,
)

from core.generators._readme import build_readme
from core.generators._setup import build_setup

if __name__ == "__main__":
    t = Figlet(font="small").renderText("readme_py")
    print(f"{Fore.LIGHTWHITE_EX}{t}")

    config_file = readmepy_config_file_question()
    suggestions = {}
    if config_file:
        FIELDS = config_file
        suggestions = suggestions_by(_dict=config_file)
    else:
        parser = git_repo_question()
        if parser:
            suggestions = suggestions_by(_dict=None, parser=parser)

    # ask the questions
    questions = inquirer_questions(FIELDS, suggestions, RESERVED_FIELDS)
    FIELDS = inquirer.prompt(questions)
    # clean color in answers
    FIELDS = {k: v.replace(Fore.LIGHTBLACK_EX, "") for k, v in FIELDS.items()}

    if FIELDS["test_command"]:
        answer = bool_question(
            "You want to add coverage information? (for Pytest tests only)"
        )
        if answer:
            # run tests with coverage
            env_dir = get_env_dir()
            if not os.path.isfile(".coveragerc"):
                with open(".coveragerc", "a+") as _f:
                    covignore = f"[run]\nomit = {env_dir}/*"
                    _f.write(covignore)

            command = cmd.run(
                FIELDS["test_command"].split(" ") + ["--cov"], stdout=cmd.PIPE
            )
            FIELDS["cov_output"] = command.stdout.decode()
            FIELDS["tests_passing"] = not bool(command.returncode)
        else:
            # run test command only
            command = cmd.run(
                FIELDS["test_command"].split(" "),
                stdout=cmd.PIPE)
            FIELDS["tests_passing"] = not bool(command.returncode)

    with open("README-autogen.md", "w+") as _f:
        _f.write(build_readme(FIELDS))

    question = "Do you want to generate setup.py based on your answers?"
    gen_setup = bool_question(question)

    if gen_setup:
        with open("setup-autogen.py", "w+") as _f:
            _f.write(build_setup(FIELDS))
