class Parser:
    def __init__(self, gtype, repo_url):
        self.gtype = gtype
        self.username = ''
        self.project = ''
        self.remote = repo_url[0]
        self.repository = repo_url[-1]
        self.is_ssh = f'git@{self.gtype}.com' in self.repository
        self.is_https = f'https://{self.gtype}.com' in self.repository


    def get_data(self):
        _split_arg = ''

        if self.is_ssh:
            _split_arg = f'git@{self.gtype}.com:'
        elif self.is_https:
            _split_arg = f'https://{self.gtype}.com/'
        else:
            return

        aux = self.repository.split(_split_arg)[-1]
        aux = aux.split('/')

        self.username = aux[0]
        self.project = aux[-1].split('.git')[0]


class GitlabParser(Parser):
    def __init__(self, repo_url):
        super(GitlabParser, self).__init__('gitlab', repo_url)
        self.get_data()
        

class GithubParser(Parser):
    def __init__(self, repo_url):
        super(GithubParser, self).__init__('github', repo_url)
        self.get_data()


def factory_parser(repo_url):
    """
    repo_url has the following pattern:
        remote_name\trepository_url
    """
    repo_url = repo_url.split('\t')
    if 'gitlab' in repo_url[1]:
        return GitlabParser(repo_url)
    elif 'github' in repo_url[1]:
        return GithubParser(repo_url)


class FactoryParser:
    def __new__(cls, repo_url, *args, **kwargs):
        """
        repo_url is an array with two positions
        0 - remote name
        1 - remote url
        """
        repo_url[1] = repo_url[1].split('.git', 1)[0] + '.git'
        if 'gitlab' in repo_url[1]:
            return GitlabParser(repo_url)
        if 'github' in repo_url[1]:
            return GithubParser(repo_url)
