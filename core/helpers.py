import os
import json
import subprocess

from colorama import Fore

from core.parsers import FactoryParser

CONFIG_FILENAME = 'readmepy-config.json'

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
            repo_url = git.stdout.decode().split('\n')[0]
            parser = FactoryParser(repo_url.split('\t'))
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

def remove_special_characters(text):
    return text.replace('-', '_')
