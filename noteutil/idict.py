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
            If index >= len(self.items).
        """

        return list(self.keys())[index], list(self.values())[index]

    def items_at(self, indexes: list):
        """
        Returns a list of (key, value) tuples at the provided indexes.

        Parameters
        ----------
        indexes : list of int
            All indexes of items that are wanted.

        Returns
        -------
        list of tuple(object, object)
            All items in the (key, value) pairing.

        Raises
        ------
        IndexError
            If one of the indexes in the list is >= len(self.items).
        """

        indexed_items = []
        for i in indexes:
            indexed_items.append(self.item_at(i))
        return indexed_items

    def index_with(self, *, key=None, val=None, func=None):
        """
        Returns the first index where the key or value matches exactly as the given key or value.

        Parameters
        ----------
        key : object, optional if value is provided.
            Specific key to look for in the dictionary's keys.
        val : object, optional if key is provided.
            Specific value to look for in the dictionary's values.
        func : function, optional
            Function to apply to dictionary's key or value before comparison of equality.
            Does not affect the provided key or value.

        Returns
        -------
        int
            The first index where the specific key or value was found.

        Raises
        ------
        IndexError
            If the key or value doesn't exist in the dictionary.
        """

        for i, kv in enumerate(self.items()):
            k, v = kv
            if func is not None:
                if key == func(k):
                    return i
                if val == func(v):
                    return i
            elif key == k or val == v:
                return i
        raise IndexError("Equivalent key or value not found in items.")

    def indexes_with(self, *, key=None, val=None, func=None):
        """
        Returns multiple indexes where the provided key or value is "in" a key or value of the dictionary.

        If the "in" operator does not work, the TypeError will be caught and == will be used instead.

        Parameters
        ----------
        key : object, optional if value is provided.
            Part of a key that exists in the dictionary's keys.
        val : object, optional if key is provided.
            Part of a value that exists in the dictionary's values.
        func : function, optional
            Function to apply to dictionary's key or value before comparison of equality.
            Does not affect the provided key or value.

        Returns
        -------
        list of int
            Multiple indexes where the key or value provided was found in a dictionary's key or value.

        Raises
        ------
        IndexError
            If no keys or values had the provided key or value in them (thus, the list is empty).
        """

        indexes = []
        for i, kv in enumerate(self.items()):
            k, v = kv
            if func is not None:
                try:
                    if key in func(k):
                        indexes.append(i)
                        continue
                except TypeError:
                    if key == func(k):
                        indexes.append(i)
                        continue
                try:
                    if val in func(v):
                        indexes.append(i)
                        continue
                except TypeError:
                    if val == func(v):
                        indexes.append(i)
                        continue
            else:
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
                        continue

        if not indexes:
            raise IndexError("No keys or values were found to have the provided key or value in them.")
        return indexes

    def key_with(self, *, index=None, name=None, val=None, func=None):
        """
        Returns the key of a given value if that key's value matches exactly with a key in the dictionary.

        Parameters
        ----------
        index : int, optional if val is provided.
            The index of the key
        name : object
            The name of the key that may equal the key after func is applied.
        val : object, optional if index is provided.
            The value that matches to a dictionary key's value.
        func : function, optional
            Function to apply to the dictionary's value before comparison of equality.
            Does not affect the provided value.

        Returns
        -------
        object
            The first key that has the exact corresponding value.

        Raises
        ------
        KeyError
            If no keys were found to have the exact value provided.
        """
        i = 0
        for k, v in self.items():
            if func is not None:
                if name == func(k) or val == func(v) or index == i:
                    return k
            elif val == v or name == k or index == i:
                return k
            i += 1
        raise KeyError("No key was found to have the provided name or value.")

    def keys_with(self, *, indexes: list=None, name=None, val=None, func=None):
        """
        Returns the keys that have the given name in the key or the given value in their corresponding value.

        If the "in" operator does not work, the TypeError will be caught and == will be used instead.

        Parameters
        ----------
        indexes: list of int, optional if name or value is provided.
            Indexes of keys.
        name : object, optional if indexes or value is provided.
            The name of the key that are part of the dictionary's keys.
        val : object, optional if name is provided.
            The name of the value that are part of the dictionary's values.
        func : function, optional
            Function to apply to the dictionary's keys and values before comparison of "in" or equality.
            Does not affect the provided name or value.

        Returns
        -------
        list of object
            List of all of the keys that had the name or the value provided in them.

        Raises
        ------
        KeyError
            If no keys were found to have part of the name provided or no values have part of the value provided.
        """

        keys = []
        for i, kv in enumerate(self.items()):
            k, v = kv

            if indexes is not None:
                if i in indexes:
                    keys.append(k)
                    continue

            if func is not None:
                try:
                    if name in func(k):
                        keys.append(k)
                        continue
                except TypeError:
                    if name == func(k):
                        keys.append(k)
                        continue
                try:
                    if val in func(v):
                        keys.append(k)
                        continue
                except TypeError:
                    if val == func(v):
                        keys.append(k)
                        continue
            else:
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
                        continue
        if not keys:
            raise KeyError("No keys were found to have the provided name or value in them.")
        return keys

    def val_with(self, *, index=None, key=None, name=None, func=None):
        """
        Returns the value of a given key if that value's key matches exactly with the dictionary's key.

        If the "in" operator does not work, the TypeError will be caught and == will be used instead.

        Parameters
        ----------
        index : int, optional if key is provided.
            Index of a key.
        key : object
            The key that matches to a value's key exactly.
        name : object
            The name of the value that may equal the val after func is applied.
        func : function, optional
            Function to apply to the dictionary's key before comparison of equality.
            Does not affect the provided key.

        Returns
        -------
        object
            The first value that has the exact corresponding key.

        Raises
        ------
        ValueError
            If no values were found to have the exact key provided.
        """

        i = 0
        for k, v in self.items():
            if func is not None:
                if key == func(k) or name == func(v) or index == i:
                    return v
            elif key == k or name == v or index == i:
                return v
            i += 1
        raise ValueError("No values were found to have the provided name or key.")

    def vals_with(self, *, indexes: list=None, key=None, name=None, func=None):
        """
        Returns the values that have the given name in the value or the given key in their corresponding key.

        Parameters
        ----------
        indexes : list of int
            Indexes of values that are wanted.
        key : object, optional if name is provided.
            The name of the key that is part of the dictionary's keys.
        name : object, optional if key is provided.
            The name of the value that is part of the dictionary's values.
        func : function, optional
            Function to apply to the dictionary's key and value before comparison of "in" or equality.
            Does not affect the provided key or name.

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
        for i, kv in enumerate(self.items()):
            k, v = kv

            if indexes is not None:
                if i in indexes:
                    vals.append(v)
                    continue

            if func is not None:
                try:
                    if key in func(k):
                        vals.append(v)
                        continue
                except TypeError:
                    if key == func(k):
                        vals.append(v)
                        continue
                try:
                    if name in func(v):
                        vals.append(v)
                        continue
                except TypeError:
                    if name == func(v):
                        vals.append(v)
                        continue
            else:
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
                        continue
        if not vals:
            raise ValueError("No values were found to have the provided name or key in them.")
        return vals
