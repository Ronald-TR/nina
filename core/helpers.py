import os
import json
import subprocess

from colorama import Fore, Style
import inquirer

from core.parsers import FactoryParser, Parser

CONFIG_FILENAME = 'readmepy-config.json'


RESERVED_FIELDS = [
    "cov_output",
    "tests_passing"
]


FIELDS = {
    'project_name': '',
    'project_version': '',
    'project_description': '',
    'project_homepage': '',
    'author_name': '',
    'git_username': '',
    'repository_url': '',
    'twitter_username': '',
    'project_prerequisites': '',
    'license_type': '',
    'install_command': '',
    'test_command': ''
}


def inquirer_questions(fields, suggestions, skip=list()):
    questions = []
    for k, v in fields.items():
        if k in skip:
            continue
        
        if k == "license_type":
            questions += [
                inquirer.List(k,
                message="What's the License Type?",
                choices=[
                    "MIT",
                    "GNU AGPLv3",
                    "GNU GPLv3",
                    "GNU LGPLv3",
                    "Unlicense",
                    "Apache 2.0",
                    "Mozilla Public License 2.0",
                    ""
                    ]
                )
            ]
            continue

        msg = "What's the " + ' '.join(k.split('_')).title() + '?'
        sg = suggestions.get(k) or ''
        questions += [
            inquirer.Text(name=k,
            message=Style.BRIGHT + Fore.YELLOW +msg,
            default=Fore.LIGHTBLACK_EX + sg),
        ]
    
    return questions


def suggestions_by(_dict, parser=None):
    if parser:
        sg = parser.__dict__.copy()
    else:
        sg = _dict.copy()
    
    repository_url = sg.get("repository_url") or ''
    project_homepage = sg.get("project_homepage") or ''
    project_description = sg.get("project_description") or 'My Awesome project!'
    
    if parser:
        repository_url = f"https://{parser.gtype}.com/" \
            f"{parser.git_username}/{parser.project_name}"
        
        project_homepage = f"https://{parser.project_name}.{parser.gtype}.io/"
 
    sg["repository_url"] = repository_url 
    sg["project_homepage"] = project_homepage
    sg["project_description"] = project_description
    sg["project_version"] = "v0.0.1"

    return sg


def str_question(question, suggestion, key):
    sg = suggestion.get(key) or ''
    answer = input(
            f'{Fore.LIGHTWHITE_EX}{question} {Fore.LIGHTBLACK_EX}E.g.: {sg}' \
            f'{Fore.LIGHTWHITE_EX}\n'
        ).lower()
    
    if not answer and sg:
        answer = sg

    return answer


def bool_question(question):
    _help = ''
    while True:
        answer = input(f'{Fore.LIGHTWHITE_EX}{question} (Y/N) {Fore.LIGHTBLACK_EX}{_help}\n').lower()
        if answer in 'yn':
            break;
        _help = ' - Just Y or N\n'
    return True if answer == 'y' else False


def readmepy_config_file_question():
    if os.path.isfile(CONFIG_FILENAME):
        msg = 'Há um arquivo de configuração na raiz,' \
            'deseja utiliza-lo para preencher as perguntas?'
        if bool_question(msg):
            with open(CONFIG_FILENAME, 'r') as _f:
                return json.load(_f)
    return None


def get_env_dir():
    return os.path.basename(os.getenv('VIRTUAL_ENV'))


def git_repo_question():
    git = subprocess.run(['git', 'remote', '-v'], stdout=subprocess.PIPE)
    parser = None
    if git.returncode == 0:
        msg = 'Parece que você tem um repositório Git. ' \
         'deseja usa-lo para responder algumas perguntas?'
        if bool_question(msg):
            parser = FactoryParser()
    return parser


def coverage_parser(fields):
    relactory, percent = '', ''
    aux = fields['cov_output'].split('\n')
    for i, v in enumerate(aux):
        if 'coverage: platform' in v:
            relactory = aux[i:-1]
        if 'TOTAL' in v:
            percent = v.replace('\t', ' ').split(' ')[-1].replace('%', '')
    
    return {'relactory': relactory, 'percent': int(percent)}

def fmt(text):
    special = ['-', ' ']
    for i in special:
        text = text.replace(i, '_')
    return text
