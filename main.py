from sys import argv
from git import Git

def main():
    git_path = argv[1] if len(argv) > 1 else None
    git = Git(git_path)
    for user, statistics in git.get_contribution_statistics().items():
        print('{}: {}'.format(user, statistics))

if __name__ == '__main__':
    main()
