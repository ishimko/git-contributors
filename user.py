class User:
    def __init__(self, name, email):
        self.names = {name}
        self.emails = {email}

    def add_name(self, name):
        self.names.add(name)

    def add_email(self, email):
        self.emails.add(email)

    def __repr__(self):
        names_repr = self._repr_strings(self.names,  ('(', ')'))
        emails_repr = self._repr_strings(self.emails)
        return '{} <{}>'.format(names_repr, emails_repr)

    def _repr_strings(self, strings, list_brackets=('', '')):
        start, end = list_brackets
        strings = list(strings)
        if len(strings) == 1:
            result = strings[0]
        else:
            result = start + ', '.join(strings) + end
        return result