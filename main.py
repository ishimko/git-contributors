from sys import argv
from git import Git

def main():
    git_path = argv[1] if len(argv) > 1 else None
    git = Git(git_path)
    contributors = git.get_contributors()
    for contributor in contributors:
        print('{}: {}'.format(contributor, git.get_contributor_stat(contributor)))

if __name__ == '__main__':
    main()
