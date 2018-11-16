class Group:
    def __init__(self, name):
        self.name = name


class LineGroup(Group):
    def __init__(self, name, prefix):
        super().__init__(name)
        self._prefix = prefix
        self.lines = []


class PairGroup(Group):
    def __init__(self, name, prefix, separator):
        super().__init__(name)
        self._prefix = prefix
        self.separator = separator
        self.pairs = []


class ExtensionGroup(Group):
    def __init__(self, name, lbound: str, rbound: str, placeholder: str =" "):
        super().__init__(name)
        self._lbound = lbound
        self._rbound = rbound
        self._placeholder = placeholder
        self.notes = []

    def __repr__(self):
        return (f"ExtensionGroup(\"{self.name}\", \"{self._lbound}\", \"{self._rbound}\", \"{self._placeholder}\", "
                f"{self.notes})")


class PackGroup(Group):
    def __init__(self, name, prefix, *, packs: list =None):
        super().__init__(name)
        self._prefix = prefix
        self.packs = [] if packs is None else packs
        self.notes = []