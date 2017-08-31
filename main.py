from argparse import ArgumentParser

from git import Git


def main():
    parser = ArgumentParser()
    parser.add_argument('path', nargs='?')
    parser.add_argument('--include-zeros', action='store_true')
    args = parser.parse_args()
    git = Git(args.path)
    for user, statistics in git.get_contribution_statistics(args.include_zeros):
        print('{}: {}'.format(user, statistics))

if __name__ == '__main__':
    main()
