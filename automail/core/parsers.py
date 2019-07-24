import re
import subprocess as cmd


class Parser:
    def __init__(self, configs):
        self.__configs = configs
        self.author_name = ""
        self.author_email = ""
        self.gtype = ""
        self.git_username = ""
        self.remote = "origin"
        self.repository_url = ""
        self.project_name = ""
        self.is_ssh = None
        self.is_https = None
        self.__extract_config_data()

    def __extract_config_data(self):
        for item in self.__configs:
            item = item.strip()

            if not item:
                continue

            if "user.name" in item:
                self.author_name = item.replace("user.name=", "")
            elif "user.email" in item:
                self.author_email = item.replace("user.email=", "")
            elif "remote.origin.url" in item:
                self.repository_url = item.replace("remote.origin.url=", "")

        r = re.compile(r"^git@").match(self.repository_url)
        self.is_ssh = True if r else False

        r = re.compile(r"^https://").match(self.repository_url)
        self.is_https = True if r else False

        protocol = ""
        if self.is_ssh:
            protocol = r"git@"
        if self.is_https:
            protocol = r"https:\/\/"

        _regex = protocol + r"(.*).com.(.*)\/(.*)\.git"
        r = re.compile(_regex).match(self.repository_url)
        if r:
            self.gtype = r.groups()[0]
            self.git_username = r.groups()[1]
            self.project_name = r.groups()[2]


class FactoryParser:
    def __new__(cls, *args, **kwargs):
        git = cmd.run(
            ["git", "config", "-l"],
            stdout=cmd.PIPE,
            stderr=cmd.DEVNULL)
        if git.returncode == 0:
            configs = git.stdout.decode().split("\n")
            return Parser(configs)
        return None
