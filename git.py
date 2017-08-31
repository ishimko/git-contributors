import subprocess
from subprocess import check_output
import os
import re
from user import User
from user_statistics import UserStatistics

class _UsersBuilder:
    def __init__(self):
        self.users = []
    
    def add_user(self, name, email):
        existing_users = list(filter(lambda x: email in x.emails or name in x.names, self.users))
        if existing_users:
            assert len(existing_users) == 1
            existing_users[0].add_name(name)
            existing_users[0].add_email(email)
        else:
            self.users.append(User(email=email, name=name))

class Git:
    STAT_LINE_PATTERN_FAST = re.compile(r".*?fil(e|es) changed.*?")
    STAT_LINE_PATTERN_FULL = re.compile( r".*?(\d+) files? changed(?:, (\d+) insertions?\(\+\))?(?:, (\d+) deletions?)?.*?")

    def __init__(self, repository=None):
        self.git_command = ["git"]
        if repository:
            if not repository.endswith(".git"):
                repository = os.path.join(repository, ".git")
            self.git_command += ["--git-dir", repository]

    def get_contributors(self):
        result = _UsersBuilder()
        output = self._git("shortlog", "-s", "-e")
        for contributor_string in output.split('\n'):
            user_info_elements = contributor_string.split()[1:]
            if user_info_elements:
                email = user_info_elements[-1][1:-1]
                name = ' '.join(user_info_elements[:-1])
                result.add_user(name=name, email=email)
        return result.users

    def get_contributor_stat(self, contributor):
        result = UserStatistics()
        for email in contributor.emails:
            output = self._git("log", "--shortstat", "--oneline", "--author", email)
            stat_lines = filter(lambda x: not x.startswith(' '*4) and Git.STAT_LINE_PATTERN_FAST.match(x), output.split('\n'))

            for line in stat_lines:
                match = Git.STAT_LINE_PATTERN_FULL.match(line)
                if match:
                    result.files += int(match.group(1))
                    result.insertions += int(match.group(2) or 0)
                    result.deletions += int(match.group(3) or 0)
        return result

    def _git(self, *argv):
        command = self.git_command + list(argv)
        result = check_output(command, stderr=subprocess.STDOUT)
        return result.decode('utf-8')
