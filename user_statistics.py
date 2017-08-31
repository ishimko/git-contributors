class UserStatistics:
    def __init__(self):
        self.files = 0
        self.insertions = 0
        self.deletions = 0

    @property
    def is_zero(self):
        return self.files == self.insertions == self.deletions == 0

    def __repr__(self):
        return "files changed: {}, insertions: {}, deletions: {}".format(self.files, self.insertions, self.deletions)
