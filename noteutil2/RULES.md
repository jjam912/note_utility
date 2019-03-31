# NoteUtil Rules:

## Typing Notes:
When typing your notes, it is essential that you follow these guidelines so that NoteUtil can comprehend your notes
    with as few bugs as possible. 
The following rules dictate a few requirements for your notes:

1. Each intended *note* and *pair* must be separated by a newline (what you get by pressing enter).
2. If you intend for a *note* to become a *pair*, it must have only one *separator*.
3. If you want a *note* to be ignored, you must start the line with whatever you put for *Comments* in the Config file.

Your notes are read from the beginning of the file to the end, so order will matter, especially if you use headings.

## Headings:
When you want to structure your notes into a hierarchy, you use *headings*. In Markdown, one "#" indicates the highest 
level heading, while six "#"s indicate the lowest level heading. You must construct your notes in this way too, 
repeating one character at the start of a line, if you want to use headings in your notes.

Example:
```
# Chapter 1
## Unit 1
### Section 1
Here you would write your regular notes: Without the heading character prefix.
```

If you use Google Docs, a fantastic add-on is [Docs to Markdown](https://chrome.google.com/webstore/detail/docs-to-markdown/igffnbdfnodiaphfmfaiiaegmoljbghf?hl=en-US),
which will convert your notes into a Markdown file, adding on the headings you used automatically. 
You may notice that underlining doesn't convert directly, but the program detects whenever an underline was converted 
and will surround it with __. If you do use Markdown, make sure that none of your other settings interfere with Markdown syntax.

However, it is up to you if you want to prefix your headings with other characters.

Rules for using headings:
1. Headings must use the same single character, only using count to dictate the heading hierarchy (1 being the highest).
2. Your notes must begin with the highest level heading and go down by increments of 1. 
    You cannot go from a level 1 heading to a level 3 heading.
3. Going back up a level of heading (level 3 to 2) to the previous heading is not allowed. 
    Either type the notes that are intended for the 2nd level heading immediately after it, or create a new 2nd level heading.
4. Do not use the heading character within the first n characters of your notes, with n being the number of headings.
5. Headings are considered notes too, and thus must also comply with the note rules.

## Custom Comparisons:

## Order of Conversion:
The order of conversion is the order in which NoteUtil creates its notes. Here is the order:

1. Headings
2. Pairs
3. Content

This means that anything lower in the creation hierarchy should not interfere with anything higher in the creation hierarchy.
