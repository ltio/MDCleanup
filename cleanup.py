# Miscellaneous operating system interfaces
import os, glob, re

# Step 1 (Optional) : Iterate through each file in the folder and open merge each file with one another till you get a full text file

    # Mdmerge

# Step 2 : Read each line and re-write it to a new file
combined_file = open('OUTFILE', 'r+', encoding = "utf8")
output_file = open('finish','w+', encoding = "utf8")

# HTML Tags. Note that you need the newlines (\n) here because if tags are next to one another, it won't be reflected on the site
open_article = '<article>\n\n'
close_article = '</article>\n\n'
open_chapter = '<chapter>\n\n'
close_chapter = '</chapter>\n\n'

# You will need a ARTICLE & CHAPTER open/closed status to know when to put in the tags above
chapter_open = False
article_open = False

# Step 3 : Scan through each edit_sentence
for sentence in combined_file:

    edit_sentence = sentence

    # Remove redunant header/text
    edit_sentence = edit_sentence.replace('#', '')
    edit_sentence = edit_sentence.replace('&nbsp', ' ')

    # 3.1 Converting headers

    chapter_header_one = 'CHAPTER'
    # Need a solution for this 'Chapter' header
    # chapter_header_two = 'Chapter'

    # Header 1, check for variants
    if chapter_header_one in edit_sentence:

        # If chapter is currently opened, check if article is closed
        if (chapter_open):
            # If article is not closed (open), close article then chapter and then open chapter again
            if (article_open):
                output_file.write(close_article)
                output_file.write(close_chapter)
                output_file.write(open_chapter)
                # Redundant but for visualisation
                chapter_open = True
                article_open = False
            else:
                output_file.write(close_chapter)
                output_file.write(open_chapter)
                # Redundant but for visualisation
                chapter_open = True
        else:
            output_file.write(open_chapter)
            chapter_open = True

        # Check if header is correct, header 1
        if edit_sentence.count('#') != 1:
            edit_sentence = '#' + edit_sentence.replace('# ','')

    article_header_one = ' ARTICLE'
    article_header_two = ' Article'
    article_header_three = 'article'

    # Header 2, check for variants
    if article_header_one or article_header_two or article_header_three in edit_sentence:

        # Check if it is a HTML tag, just add a new line to ensure that tag is invoked
        if (re.search('<article>', edit_sentence)):
            edit_sentence = edit_sentence + '\n'
            article_open = True
        else:
            # If article is opened
            if ((re.match(article_header_one, edit_sentence) or re.match(article_header_two, edit_sentence)) and article_open):
                output_file.write(close_article)
                output_file.write(open_article)

                # Check if header is correct, header 2
                if edit_sentence.count('#') == 0:
                    edit_sentence = '## ' + edit_sentence

                # Redundant but as fail safe
                if edit_sentence.count('#') != 2:
                    edit_sentence = '##' + edit_sentence.replace('#','')
            # If article is closed
            elif ((re.match(article_header_one, edit_sentence) or re.match(article_header_two, edit_sentence)) and not article_open):
                output_file.write(open_article)
                article_open = True

                # Check if header is correct, header 2
                if edit_sentence.count('#') == 0:
                    edit_sentence = '## ' + edit_sentence

                # Redundant but as fail safe
                if edit_sentence.count('#') != 2:
                    edit_sentence = '##' + edit_sentence.replace('#','')

        # This is to ensure that the correct MD format
        # try:
            # if (re.match('Article', edit_sentence) or re.match(' Article', edit_sentence)):
                # if (edit_sentence.split()[2][0].isupper()):
                    # edit_sentence = '## ' + edit_sentence
        # except IndexError:
            # edit_sentence = '## ' + edit_sentence

    # 3.2 End/Footnotes
    # If footnote is found
    if (re.match('[\(\[]*\^\d{1,2}[-\s]*\d{0,2}[\)\]]*:*' ,edit_sentence)):

        # Save note for checking
        note = re.match('[\(\[]*\^\d{1,2}[-\s]*\d{0,2}[\)\]]*:*' ,edit_sentence).group()
        new_note = note

        # Check if square bracket exist instead of rounded
        if (re.search('\(', new_note) or re.search('\)', new_note)):
            new_note = new_note.replace('(', '[')
            new_note = new_note.replace(')', ']')

        # Check if square bracket is implemented, if not add it in
        if not (re.search('\[', new_note) and re.search('\]', new_note)):
            # This is to remove any case where only one of the bracket is implement
            new_note = new_note.replace('[', '')
            new_note = new_note.replace(']', '')
            new_note = '[' + new_note + ']'

        # This will not work for endnote as it will affect (E.G. 2. word)
        # if not (re.search('\^', new_note)):
            # new_note = new_note.replace('[', '[^')

        if not (re.search(':', new_note)):
            new_note += ':'

        # Check if note contains space and replace space with -
        if not (re.search('\s\d{1,2}', new_note)):
            new_note = new_note.replace(' ', '')

        if (re.search('\s\d{1,2}', new_note)):
            new_note = new_note.replace(' ', '-')

        edit_sentence = edit_sentence.replace(note, new_note)
    # If endnote is found
    elif (re.search('[\(\[]*\^\d{1,2}[-\s]*\d{0,2}[\)\]]*:*' ,edit_sentence)):
        # Save note for checking
        note = re.search('[\(\[]*\^\d{1,2}[-\s]*\d{0,2}[\)\]]*:*' ,edit_sentence).group()
        new_note = note

        # Check if square bracket exist instead of rounded
        if (re.search('\(', new_note) or re.search('\)', new_note)):
            print ('b')
            new_note = new_note.replace('(', '[')
            new_note = new_note.replace(')', ']')

        # Check if square bracket is implemented, if not add it in
        if not (re.search('\[', new_note) and re.search('\]', new_note)):
            # This is to remove any case where only one of the bracket is implement
            new_note = new_note.replace('[', '')
            new_note = new_note.replace(']', '')
            new_note = '[' + new_note + ']'

        # This will not work for endnote as it will affect (E.G. word 2.1 word)
        # if not (re.search('\^', new_note)):
            # new_note = new_note.replace('[', '[^')

        if (re.search(':', new_note)):
            new_note = new_note.replace(':', '')

        # Check if note contains space and replace space with -
        if not (re.search('\s\d{1,2}', new_note)):
            new_note = new_note.replace(' ', '')

        if (re.search('\s\d{1,2}', new_note)):
            new_note = new_note.replace(' ', '-')

        edit_sentence = edit_sentence.replace(note, new_note)

    output_file.write(edit_sentence)

# Best practice to close, if there are too many files left unopened it will consume resources on your local PC
combined_file.close()
output_file.close()
