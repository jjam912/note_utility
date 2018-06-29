class IndexedDict(dict):

    def item_at(self, index: int):
        """
        Returns a (key, value) tuple given a specific index in the dictionary.

        Parameters
        ----------
        index : int
            The index of the desired item.

        Returns
        -------
        object
            Key at the given index.
        object
            Value at the given index.

        Raises
        ------
        IndexError
            If index >= len(self.items) or index < 0.
        """

        return list(self.keys())[index], list(self.values())[index]

    def key_at(self, index: int):
        """
        Returns a key given a specific index in the dictionary.

        Parameters
        ----------
        index : int
            The index of the desired key.

        Returns
        -------
        object
            Key at the given index.

        Raises
        ------
        IndexError
            If index >= len(self.items) or index < 0.
        """

        return list(self.keys())[index]

    def val_at(self, index: int):
        """
        Returns a value given a specific index in the dictionary.

        Parameters
        ----------
        index : int
            The index of the desired value.

        Returns
        -------
        object
            Value at the given index.

        Raises
        ------
        IndexError
            If index >= len(self.items) or index < 0.
        """

        return list(self.values())[index]

    def index_with(self, *, key=None, val=None, case_sensitive: bool=True):
        """
        Returns the first index where the key or value matches exactly as the given key or value.

        Parameters
        ----------
        key : object, optional if val is provided
            Specific key that exists in the dictionary's keys.
        val : object, optional if key is provided
            Specific value that exists in the dictionary's values.
        case_sensitive : bool, optional
            Whether case matters (for strings).

        Returns
        -------
        int
            The first index where the specific key or value was found.

        Raises
        ------
        ValueError
            If the key or value doesn't exist in the dictionary.
        """

        for i, kv in enumerate(self.items()):
            k, v = kv
            if not case_sensitive:
                if key:
                    if key.lower() == k.lower():
                        return i
                if val:
                    if val.lower() == v.lower():
                        return i
            if key == k or val == v:
                return i
        raise ValueError("Equivalent key or value not found in items.")

    def indexes_with(self, *, key=None, val=None, case_sensitive: bool=True):
        """
        Returns multiple indexes where the provided key or value is in a key or value of the dictionary.

        If the "in" operator does not work, the TypeError will be caught and == will be used instead.

        Parameters
        ----------
        key : object
            Part of a key that exists in the dictionary's keys.
        val : object
            Part of a value that exists in the dictionary's values.
        case_sensitive : bool
            Whether case matters (for strings).

        Returns
        -------
        list of int
            Multiple indexes where the key or value provided was found in a dictionary's key or value.

        Raises
        ------
        ValueError
            If no keys or values had the provided key or value in them (thus, the list is empty).
        """

        indexes = []
        for i, kv in enumerate(self.items()):
            k, v = kv
            if not case_sensitive:
                if key:
                    if key.lower() in k.lower():
                        indexes.append(i)
                        continue
                if val:
                    if val.lower() in v.lower():
                        indexes.append(i)
                        continue

            try:
                if key in k:
                    indexes.append(i)
                    continue
            except TypeError:
                if key == k:
                    indexes.append(i)
                    continue
            try:
                if val in v:
                    indexes.append(i)
                    continue
            except TypeError:
                if val == v:
                    indexes.append(i)

        if not indexes:
            raise ValueError("No keys or values were found to have the key or value in them.")
        return indexes

    def key_with(self, val, case_sensitive: bool=True):
        """
        Returns the key of a given value if that key's value matches exactly.

        Parameters
        ----------
        val : object
            The value that matches to a key's value.
        case_sensitive : bool
            Whether case matters (for strings).

        Returns
        -------
        object
            The first key that has the exact corresponding value.

        Raises
        ------
        ValueError
            If no keys were found to have the exact value provided.
        """

        for k, v in self.items():
            if not case_sensitive:
                if val.lower() == v.lower():
                    return k
            if val == v:
                return k
        return ValueError("No key was found to have the name or associated value.")

    def keys_with(self, *, name=None, val=None, case_sensitive: bool=True):
        """
        Returns the keys that have the given name in the key or the given value in their corresponding value.

        Parameters
        ----------
        name : object
            The name of the key that may be in the dictionary's keys.
        val : object
            The name of the value that may be in the dictionary's values.
        case_sensitive : bool
            Whether case matters (for strings).

        Returns
        -------
        list of object
            List of all of the keys that had the name or the value provided in them.

        Raises
        ------
        ValueError
            If no keys were found to have part of the name provided or no values have part of the value provided.
        """

        keys = []
        for k, v in self.items():
            if not case_sensitive:
                if name:
                    if name.lower() in k.lower():
                        keys.append(k)
                        continue
                if val:
                    if val.lower() in v.lower():
                        keys.append(k)
                        continue
            try:
                if name in k:
                    keys.append(k)
                    continue
            except TypeError:
                if name == k:
                    keys.append(k)
                    continue
            try:
                if val in v:
                    keys.append(k)
                    continue
            except TypeError:
                if val == v:
                    keys.append(k)
        if not keys:
            raise ValueError("No keys were found that had the name or value in them.")
        return keys

    def val_with(self, key, case_sensitive: bool=True):
        """
        Returns the value of a given key if that value's key matches exactly.

        Parameters
        ----------
        key : object
            The key that matches to a value's key exactly.
        case_sensitive : bool
            Whether case matters (for strings).

        Returns
        -------
        object
            The first value that has the exact corresponding key.

        Raises
        ------
        ValueError
            If no values were found to have the exact key provided.
        """

        for k, v in self.items():
            if not case_sensitive:
                if key.lower() == k.lower():
                    return v

            if key == k:
                return v
        raise ValueError("No values were found to have the name or associated key.")

    def vals_with(self, *, key=None, name=None, case_sensitive: bool=True):
        """
        Returns the values that have the given name in the value or the given key in their corresponding key.

        Parameters
        ----------
        key : object
            The name of the key that may correspond to the dictionary's values.
        name : object
            The name of the value that may be in the dictionary's values.
        case_sensitive : bool
            Whether case matters (for strings).

        Returns
        -------
        list of object
            List of all of the values that had the name provided in them or the key name in their corresponding key.

        Raises
        ------
        ValueError
            If no values were found to have part of the name provided or no keys have part of the key provided.
        """

        vals = []
        for k, v in self.items():
            if not case_sensitive:
                if key:
                    if key.lower() in k.lower():
                        vals.append(v)
                        continue
                if name:
                    if name.lower() in v.lower():
                        vals.append(v)
                        continue
            try:
                if key in k:
                    vals.append(v)
                    continue
            except TypeError:
                if key == k:
                    vals.append(v)
                    continue
            try:
                if name in v:
                    vals.append(v)
                    continue
            except TypeError:
                if name == v:
                    vals.append(v)
        if not vals:
            raise ValueError("No values were found to have the name or associated key in them.")
        return vals
