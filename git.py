import subprocess
from subprocess import check_output
import os
import re

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
        result = []
        output = self._git("shortlog", "-s")
        for contributor_string in output.split('\n'):
            name_elements = contributor_string.split()[1:]
            if name_elements:
                result.append(' '.join(name_elements))
        return result

    def get_contributor_stat(self, contributor):
        result = {
            "files" : 0,
            "insertions": 0,
            "deletions": 0
        }
        output = self._git("log", "--shortstat", "--oneline", "--author", contributor)
        stat_lines = filter(lambda x: not x.startswith(' '*4) and Git.STAT_LINE_PATTERN_FAST.match(x), output.split('\n'))
        
        for line in stat_lines:
            match = Git.STAT_LINE_PATTERN_FULL.match(line)
            if match:
                files = int(match.group(1))
                insertions = match.group(2)
                deletions = match.group(3)
                result['files'] += files
                if insertions is not None:
                    result['insertions'] += int(insertions)
                if deletions is not None:
                    result['deletions'] += int(deletions)
        return result

    def _git(self, *argv):
        command = self.git_command + list(argv)
        result = check_output(command, stderr=subprocess.STDOUT)
        return result.decode('utf-8')