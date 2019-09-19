# Table of Contents
* [NoteUtil Rules](#noteutil-rules)
    * [Typing Notes](#typing-notes)
        * [Headings](#headings)
        * [Categories](#categories)
        * [Extensions](#extensions)
        * [Pairs](#pairs)
    * [Order of Conversation](#order-of-conversion)
    * [Editing Notes](#editing-notes)
* [Configuration Setup](#configuration-setup)
    * [Configuration Parameters](#configuration-parameters)
    * [Configuration Example](#configuration-example)
* [Quiz Rules](#quiz-rules)
    * [Usage of Terms and Definitions in Quiz](#usage-of-terms-and-definitions-in-quiz)
    * [Usage of Headings in Quiz](#usage-of-headings-in-quiz)
    * [Quiz Options](#quiz-options)
    * [Saving, Loading, and Refreshing in Quiz](#saving-loading-and-refreshing-in-quiz)
* [Leitner Rules](#leitner-rules)
    * [Usage of Terms and Definitions in Leitner](#usage-of-terms-and-definitions-in-leitner)
    * [Boxes](#boxes)
    * [Saving, Loading, and Refreshing in Leitner](#saving-loading-and-refreshing-in-leitner)
    

# NoteUtil Rules:

## Typing Notes:
When typing your notes, it is essential that you follow these guidelines so that NoteUtil can comprehend your notes
    with as few bugs as possible. 
The following rules dictate a few requirements for your notes:

1. Each intended note must be separated by a newline (what you get by pressing enter), unless it is a block.
2. Create blocks by surrounding the note by the "block" string designated in the config file.
3. If you want a note to be ignored, you must start the line with whatever you put for "comments" in the config file.

Your notes are read from the beginning of the file to the end, so order will matter, especially if you use headings.

### Headings:
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
4. Heading names (content) must be unique.
5. Do not use the heading character within the first n characters of your notes when starting a new line, with n being the number of headings.
6. Headings are considered notes too, and thus must also comply with the note rules.

### Categories:
When you want to group together specific notes, but they don't appear in chronological order, you can use Categories to 
include all of them into the same "heading-like" way. These are prefixed the similarly to Headings, except that you definitely
should use a different character and category characters do not repeat. 

Example:
```
# Let $ denote Category 1's prefix
# Let ! denote Category 2's prefix
# In order to assign both Category 1 and 2 to the Note:
$!The quick brown fox jumps over the lazy dog
```

Rules for using Categories:
1. Category prefixes should go before the content of the Note, after any heading characters.
2. In order to assign one Note more than one Category, place the prefixes **in the order you type them** in the config file.
3. If Category prefixes are not in the order shown in the config file, then they will not be recognized.
4. The Categories themselves aren't Notes, but they reference to a group of Notes similar to Headings.

### Extensions:
Extensions are an additional piece of text that you want to separate from either the main content of the *Note*. 
They are created by surrounding your notes with a specific string (bounds) and are useful for adding information to a *Note* that's not required.

Example (The note is spread through multiple lines for convenience):
```
The Bosnian Crisis (1908): This occurred when Austria-Hungary said that they're officially going to annex Bosnia 
(already under the Habsburgs influence, but Bosnia is independent, technically). {Serbia wanted to create a unified 
slavic kingdom under the Serbian monarchy (super Balkan state), but Austria tried to derail Serbian aspirations to unify
the area.} Following this, Serbia said to Russia that they're going to go to war against Austria, and asked them for help. 
Russia agreed to back them up, but Wilhelm told Nicholas that he doesn't want that because then Germany will back 
Austria-Hungary. Nicholas decided he couldn't afford a war since his people weren't behind him, leading to Russia 
backing out, swearing that they would never bow to Austria again.
```
Notice that there is a little bit of historical context bounded in between the `{` and `}` characters. This part of the note would
be taken out of the regular content of the *note* and placed in the extensions dictionary under the name "Historical Context".


Rules for using extensions:
1. Extensions must have a name, left bound string, and right bound string.
2. If your note is a pair, that does not affect how your extension is made, but you should be careful for conflicts between the separators and the extension's bounds.
3. Extensions are an addition to a *note*, so it must be included in the content of a *note*. Otherwise it just becomes a note.

### Pairs:
Pairs are notes that are separated into two parts by a separator; the left part is called the term, and the right part
is called the definition. Pairs are essential to NoteUtil because of their usage in Quiz and Leitner as the basis of
questions and answers. 

Example:
```
Scalars ~ These are elements of fields (F). It is a fancy word for "number," and is often used when we want to emphasize that an object is a number, as opposed to a vector. 
```
In this case, the separator is the tilde (~), and the term is everything before the separator ("Scalar"), 
while the definition is everything after the separator. 

Rules for using pairs:
1. A pair may only have one separator.
2. Pairs must have content after the separator (no empty definitions).
3. Terms may not be duplicated.

## Order of Conversion:
The order of conversion is the order in which NoteUtil creates its notes. Here is the order:

1. Headings
2. Categories
3. Extensions
4. Pairs
5. Content

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

Numbers 2 and 3 have not been implemented yet.

# Configuration Setup:

# Quiz Module Rules:

# Quiz Rules:
## Usage of Terms and Definitions in Quiz:

The quiz revolves around notes that are pairs - those who have a separator that distinguish between term and definition.
Any notes that are not pairs have no use in the quiz module, aside from headings. With your terms and definitions, 
you can tell the quiz to generate them in some order to cycle through all of your pairs.
Once the quiz gives you the pair, you can mark the term as correct or incorrect, which you can later review.

A standard procedure of quizzing is to cycle through all of the terms, marking each one of them correct or incorrect 
as you answer them, and then reviewing all of the ones you got incorrect until you memorize them. 

## Usage of Headings in Quiz:

Headings help you decide which group of notes you want to study. If you only want to study a single chapter out of many,
then you can simply select that chapter (heading) to quiz yourself on without worrying about the other notes. 

In this case, Notes that you marked as correct or incorrect are kind of like their own heading - if you want to quiz 
only on the terms that you marked as incorrect, you can select that "heading."
WARNING: You should not have a heading with the name "correct" or "incorrect" because those are used to determine whether
to only use notes that you marked as correct or incorrect. This name is case sensitive, however, so you can have a heading
named "Correct" or "Incorrect" without any issues.

## Quiz Options:

Several options are available to help you customize your quizzing session. Among them include:

* Randomization or chronological order
* Selecting specific headings to study from
* Tracking of correct and incorrect answers
* Selecting terms that you haven't marked as correct or incorrect

## Saving, Loading, and Refreshing in Quiz:

Once you are done quizzing, you can save the terms that you marked as correct and incorrect in a .qz file. 
However, be aware that if you decide to change your notes and then try to load your save progress, the quiz will only
keep the terms that have not changed at all. If there is any difference, it will not be loaded. This was done to avoid
any problems between old and new notes. 

An alternative to saving and loading while using the program is to refresh the quiz. If you have updated your notes
and have another NoteUtil, you can update the quiz with your new notes. Again, the quiz will discard any old notes that
do not match exactly with any of the new notes.

# Leitner Rules:

## Usage of Terms and Definitions in Leitner:

The Leitner uses notes that are pairs - those who have a separator that distinguish between term and definition.
Any notes that are not pairs will have no use in the Leitner module. With your terms and definitions, you will go
through all of them, marking them as correct or incorrect. When you have gone through all of them, that concludes one
review "session." The next review session will always include all of the terms that you previously got wrong, but
after a few sessions the terms that you got right will start appearing less and less frequently. Thus, you will review
the terms that you marked incorrect more often than the ones that you marked correct.

## Boxes
The Leitner system is a method of spaced repetition where cards are reviewed at increasing intervals. This program
uses seven boxes, or groups of terms for spaced repetition. By default, cards in Box 1 (default) will be reviewed every
other session because these are the ones that are new or marked incorrect. Card boxes will appear in the following
periods:

1. Box 1: 1 session
2. Box 2: 2 sessions
3. Box 3: 3 sessions
4. Box 4: 5 sessions
5. Box 5: 11 sessions
6. Box 6: 19 sessions
7. Box 7: 29 sessions

You can change the periods of review for each box or limit the number of boxes.

## Saving, Loading, and Refreshing in Leitner:

Once you are done reviewing, you can save the terms that are in your boxes into a .lt file.
However, be aware that if you decide to change your notes and then try to load your save progress, the Leitner will only
keep the terms that have not changed at all. If there is any difference, it will not be loaded. This was done to avoid
any problems between old and new notes. 

An alternative to saving and loading while using the program is to refresh the Leitner. If you have updated your notes
and have another NoteUtil, you can update the quiz with your new notes. Again, the quiz will discard any old notes that
do not match exactly with any of the new notes.
 


