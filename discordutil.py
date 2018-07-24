"""
This module has several methods to modify a message into a discord format.
"""


import pyautogui


def bold(message: str):
    """
    Emphasize whole message.

    Parameters
    ----------
    message : str
        The message intended to be sent

    Returns
    -------
    str
        Modified message
    """

    return "**" + message + "**"


def italic(message: str):
    """
    Italicize whole message.

    Parameters
    ----------
    message : str
        The message intended to be sent

    Returns
    -------
    str
        Modified message
    """
    return "*" + message + "*"


def underline(message: str):
    """
    Underline whole message.

    Parameters
    ----------
    message : str
        The message intended to be sent

    Returns
    -------
    str
        Modified message
    """
    return "__" + message + "__"


def strikeout(message: str):
    """
    Strikeout whole message.

    Parameters
    ----------
    message : str
        The message intended to be sent

    Returns
    -------
    str
        Modified message
    """
    return "~~" + message + "~~"


def bold_words(message: str, *words: str):
    """
    Emphasizes specific words.

    Parameters
    ----------
    message : str
        The message you want to send
    words : str
        Words that you want to be bolded

    Returns
    -------
    str
        Modified message

    Notes
    -----
    Implementation
        0. Look at the first word
        1. Start at index 0
        2. Use the in keyword to determine if the word is in the message
            2a. Also use .lower() on both strings for case-insensitivity
        3. Add ** to before and after the word.
        4. Add the length of the word to the index
        5. Add 4 to the index because ** surrounding the word is 4 characters
        6. Reset index and look at the next word
    """
    index = 0
    for word in words:
        while word.lower() in message[index:].lower():
            index = message.lower().index(word.lower(), index)
            message = message[:index] + "**" + message[index: index + len(word)] + "**" + message[index + len(word):]
            index += len(word) + 4
        index = 0

    return message


def italic_words(message: str, *words: str):
    """
    Italicizes specific words.

    Parameters
    ----------
    message : str
        The message you want to send
    words : str
        Words that you want to be bolded

    Returns
    -------
    str
        Modified message

    Notes
    -----
    Implementation
        0. Look at the first word
        1. Start at index 0
        2. Use the in keyword to determine if the word is in the message
            2a. Also use .lower() on both strings for case-insensitivity
        3. Add * to before and after the word.
        4. Add the length of the word to the index
        5. Add 2 to the index because * surrounding the word is 2 characters
        6. Reset index and look at the next word
    """
    index = 0
    for word in words:
        while word.lower() in message[index:].lower():
            index = message.lower().index(word.lower(), index)
            message = message[:index] + "*" + message[index: index + len(word)] + "*" + message[index + len(word):]
            index += len(word) + 2
        index = 0

    return message


def underline_words(message: str, *words: str):
    """
    Underlines specific words.

    Parameters
    ----------
    message : str
        The message you want to send
    words : str
        Words that you want to be bolded

    Returns
    -------
    str
        Modified message

    Notes
    -----
    Implementation
        0. Look at the first word
        1. Start at index 0
        2. Use the in keyword to determine if the word is in the message
            2a. Also use .lower() on both strings for case-insensitivity
        3. Add __ to before and after the word.
        4. Add the length of the word to the index
        5. Add 4 to the index because __ surrounding the word is 4 characters
        6. Reset index and look at the next word
    """
    index = 0
    for word in words:
        while word.lower() in message[index:].lower():
            index = message.lower().index(word.lower(), index)
            message = message[:index] + "__" + message[index: index + len(word)] + "__" + message[index + len(word):]
            index += len(word) + 4
        index = 0

    return message


def strikeout_words(message: str, *words: str):
    """
    Strikeout specific words.

    Parameters
    ----------
    message : str
        The message you want to send
    words : str
        Words that you want to be bolded

    Returns
    -------
    str
        Modified message

    Notes
    -----
    Implementation
        0. Look at the first word
        1. Start at index 0
        2. Use the in keyword to determine if the word is in the message
            2a. Also use .lower() on both strings for case-insensitivity
        3. Add ~~ to before and after the word.
        4. Add the length of the word to the index
        5. Add 4 to the index because ~~ surrounding the word is 4 characters
        6. Reset index and look at the next word
    """
    index = 0
    for word in words:
        while word.lower() in message[index:].lower():
            index = message.lower().index(word.lower(), index)
            message = message[:index] + "~~" + message[index: index + len(word)] + "~~" + message[index + len(word):]
            index += len(word) + 4
        index = 0

    return message


def println(message: str):
    """
    Types the message and then presses enter

    Parameters
    ----------
    message : str
        The message to be typed

    Returns
    -------
    None

    """
    pyautogui.typewrite(message)
    pyautogui.press("enter")


def split_message(message: str, embedded: bool=False, language: str=""):
    """
    Splits a message into more messages of size less than 2000 characters.

    This is to bypass the Discord 2000 character limit.

    Parameters
    ----------
    message : str
        A long message to split up.
    embedded : bool
        Whether to embed the message in code format (surrounded by ```)
    language : str
        Name of the language of the code.

    Returns
    -------
    list of str
        All messages to send.
    """

    lines = message.split("\n")
    curr_message = ""
    messages = []

    if embedded:
        curr_message += "```" + language + "\n"
        for line in lines:
            if len(line) + len(curr_message) + 5 > 2000:
                messages.append(curr_message + "```")
                curr_message = "```" + language + line + "\n"
            else:
                curr_message += line + "\n"
        messages.append(curr_message + "```")

    else:
        for line in lines:
            if len(line) + len(curr_message) + 2 > 2000:
                messages.append(curr_message)
                curr_message = line + "\n"
            else:
                curr_message += line + "\n"
        messages.append(curr_message)
    return messages
