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
Here you would write your regular notes without the heading character prefix.
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

## Order of Conversion:
The order of conversion is the order in which NoteUtil creates its notes. Here is the order:

1. Headings
2. Pairs
3. Content

This means that anything lower in the creation hierarchy should not interfere with anything higher in the creation hierarchy.

## Editing Notes:
You can edit your notes directly through NoteUtil, without needing to touch your original note file.
All changes to notes will be saved in the file of the same name as your notes, but with a .nu extension, leaving your
    original note file unchanged. 
    
You are able to:

1. Change the content of your notes.
    * This will directly affect several other parts of your notes, such as whether your note is a pair.
2. ~~Add and remove notes.~~
    * ~~If you remove a heading, it will also delete every other note and  headings that were under that heading.~~
3. ~~Append notes by parsing new content.~~

Too hard to implement; just copy your .nu file to your original note file, and then add/remove what you need.

# Quiz Rules:

## Terms and Definitions:

The quiz revolves around notes that are pairs - those who have a separator that distinguish between term and definition.
Any notes that are not pairs have no use in the quiz module, aside from headings. With your terms and definitions, 
you can tell the quiz to either ask you to define the term, or to guess the term given its definition.
Once the quiz gives you the answer (definition or term), you can mark the term as correct or incorrect, which you can later review.

A standard procedure of quizzing is to cycle through all of the terms, marking each one of them correct or incorrect 
as you answer them, and then reviewing all of the ones you got incorrect until you memorize them. 

## Use of Headings in Quiz:

Headings help you decide which group of notes you want to study. If you only want to study a single chapter out of many,
then you can simply select that chapter (heading) to quiz yourself on without worrying about the other notes. 

In this case, Notes that you marked as correct or incorrect are kind of like their own heading - if you want to quiz 
only on the terms that you marked as incorrect, you can select that "heading."

## Options:

Several options are available to help you customize your quizzing session. Among them include:

* Randomization or chronological order
* Selecting specific headings to study from
* Tracking of correct and incorrect answers
* Selecting terms that you haven't marked as correct or incorrect

## Saving, Loading, and Refreshing:

Once you are done quizzing, you can save the terms that you marked as correct and incorrect in a .qz file. 
However, be aware that if you decide to change your notes and then try to load your save progress, the quiz will only
keep the terms that have not changed at all. If there is any difference, it will not be loaded. This was done to avoid
any problems between old and new notes. 

An alternative to saving and loading while using the program is to refresh the quiz. If you have updated your notes
and have another NoteUtil, you can update the quiz with your new notes. Again, the quiz will discard any old notes that
do not match exactly with any of the new notes.