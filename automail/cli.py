import os
import json
import subprocess as cmd

from pyfiglet import Figlet
from colorama import Fore, Style
import PyInquirer as inquirer

from automail.core.helpers import (
    bool_question,
    inquirer_questions,
    git_repo_question,
    get_env_dir,
    automail_config_file_question,
    suggestions_by,
    template_fields,
    template_reserved_fields,
    get_license
)

from automail.core.generators._readme import build_readme
from automail.core.generators._setup import build_setup


def main():
    FIELDS = template_fields()
    RESERVED_FIELDS = template_reserved_fields()

    t = Figlet(font="big").renderText("nina .md\n")
    print(f"{Fore.LIGHTWHITE_EX}{t}")

    config_file = automail_config_file_question()
    suggestions = {}
    # load the answer suggestions: by nina-config.json or git
    if config_file:
        for i in config_file:
            FIELDS[i] = config_file[i]

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
            # prepare test command
            env_dir = get_env_dir()
            if not os.path.isfile(".coveragerc"):
                with open(".coveragerc", "a+") as _f:
                    covignore = f"[run]\nomit = {env_dir}/*"
                    _f.write(covignore)
            command_line = FIELDS["test_command"].split(" ") + ["--cov"]
        else:
            command_line = FIELDS["test_command"].split(" ")

        # run the test command
        try:
            devnull = open("nina.log", "w+")
            command = cmd.run(
                command_line,
                stdout=cmd.DEVNULL,
                stderr=devnull)
            cov_output = command.stdout.decode()
            tests_passing = not bool(command.returncode)
        except BaseException:
            print(
                Fore.RED + "An error occurred when running test command, "
                "see nina.log")
            cov_output = ""
            tests_passing = False

        FIELDS["cov_output"] = cov_output
        FIELDS["tests_passing"] = tests_passing

    # generating files
    # license
    with open("LICENSE-autogen.md", "w+") as _f:
        try:
            _license = get_license(FIELDS)
            _f.write(_license)
            message = f"{Style.BRIGHT}{Fore.BLACK}LICENSE-autogen.md"\
                "generated! Please revise them! :D"
        except BaseException:
            message = "An error occurred when generating LICENSE.md"
        print(message)

    # readme
    with open("README-autogen.md", "w+") as _f:
        _f.write(build_readme(FIELDS, _license))
        print("README-autogen.md generated! Please revise them! :D")

    question = "Do you want to generate setup.py based on your answers?"
    gen_setup = bool_question(question)

    # setup
    if gen_setup:
        with open("setup-autogen.py", "w+") as _f:
            _f.write(build_setup(FIELDS))
            message = f"{Style.BRIGHT}{Fore.BLACK}setup-autogen.py generated!"\
                " Please revise them! :D"
            print(message)

    # nina-config
    with open("nina-config.json", "w+") as _f:
        _f.write(json.dumps(FIELDS, indent=2))
        message = f"{Style.BRIGHT}{Fore.BLACK}nina-config.json generated!"\
            " Your previous answers are been preserved."
        print(message)


def _cli():
    try:
        main()
    except KeyboardInterrupt:
        print("Bye!")


if __name__ == "__main__":
    _cli()
