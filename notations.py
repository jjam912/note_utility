
class Term:

    def __init__(self, text: str, index: int,):
        self.text = text
        self.index = index

    def __str__(self):
        message = "Term: " + self.text
        return message


class Definition:

    def __init__(self, text: str, index: int,):
        self.text = text
        self.index = index

    def __str__(self):
        message = "Definition: " + self.text
        return message


class Category:
    pass


