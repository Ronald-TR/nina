import os
import subprocess as subp

from pyfiglet import Figlet
from colorama import Fore

from core.helpers import (
    bool_question, 
    git_repo_question, 
    get_env_dir, 
    readmepy_config_file_question,
    coverage_parser,
    FIELDS
)

from core.parsers import factory_parser, FactoryParser
from core.generator import build_readme

if __name__ == "__main__":
    t = Figlet(font='small').renderText('readme_py')
    print(f'{Fore.LIGHTWHITE_EX}{t}')
    
    config_file = readmepy_config_file_question()
    
    if config_file:
        FIELDS = config_file
    else:
        # ask the questions
        parser = git_repo_question()
        if parser:
            FIELDS['project_name'] = parser.project
            FIELDS['git_username'] = parser.username
            FIELDS['repository_url'] = parser.repository
        for k, v in FIELDS.items():
            if not v:
                question = ' '.join(k.split('_')).title()
                FIELDS[k] = input(f'{question}\n')

    if FIELDS['test_command']:
        answer = bool_question('You want to add coverage information? (for Pytest tests only)')
        if answer:
            # run tests with coverage
            env_dir = get_env_dir()
            if not os.path.isfile('.coveragerc'):
                with open('.coveragerc', 'a+') as _f:
                    covignore = f'[run]\nomit = {env_dir}/*'
                    _f.write(covignore)

            command = subp.run(FIELDS['test_command'].split(' ') + ['--cov'], stdout=subp.PIPE)
            FIELDS['cov_output'] = command.stdout.decode()
            FIELDS['tests_passing'] = not bool(command.returncode)
        else:
            # run test command only
            command = subp.run(FIELDS['test_command'].split(' '), stdout=subp.PIPE)
            FIELDS['tests_passing'] = not bool(command.returncode)

    with open('README-autogen.md', 'w+') as _f:
        _f.write(build_readme(FIELDS))
    