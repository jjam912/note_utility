from .note import *
from .errors import *


class Extension(ABC):
    def __init__(self, name: str, content: str, note: Note):
        self.name = name
        self._rcontent = content
        self.content = content
        self.note = note


class LineExtension(Extension):
    def __init__(self, name: str, content: str, note: Note):
        super().__init__(name, content, note)

    def __repr__(self):
        return f"LineExtension(\"{self.name}\", \"{self.content}\", {self.note})"


class PairExtension(Extension):
    def __init__(self, name: str, content: str, note: Note, separator: str):
        super().__init__(name, content, note)
        self.separator = separator

        tokens = tuple(content.split(separator))
        if len(tokens) != 2:
            raise SeparatorError(f"There was either zero or more than one separator in the content: {content}")

        self.term, self.definition = tokens[0].strip(), tokens[1].strip()

    def __repr__(self):
        return f"PairExtension(\"{self.name}\", \"{self.content}\", {self.note}, \"{self.separator}\")"


class ListExtension(Extension, ABC):
    def __init__(self, name: str, content: str, note: Note, separators: list):
        super().__init__(name, content, note)
        self.separators = separators
        self.elements = []


class ListElement:
    def __init__(self, list_ext: ListExtension, content: str, *, parents: list = None, children: list = None):
        self.list_ext = list_ext
        self.content = content
        self.parents = parents
        self.children = children


class BulletListExtension(ListExtension):
    def __init__(self, name: str, content: str, note: Note, separators: list, bullets: list = None):
        super().__init__(name, content, note, separators)
        self.bullets = bullets
        if self.bullets is None:
            self.bullets = ["+ ", "- ", "* "]


class NumberListExtension(ListExtension):
    def __init__(self, name: str, content: str, note: Note, separators: list):
        super().__init__(name, content, note, separators)

