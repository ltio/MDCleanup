# Miscellaneous operating system interfaces
import os, glob, re

# Step 1 (Optional) : Iterate through each file in the folder and open merge each file with one another till you get a full text file

# Step 2 : Read each line and re-write it to a new file. There is no edit

combined_file = open('OUTFILE', 'r+', encoding = "utf8")
output_file = open('finish','w+')

# HTML Tags. Note that you need the newlines (\n) here because if tags are next to one another, it won't be reflected on the site
open_article = '<article>\n\n'
close_article = '</article>\n\n'
open_chapter = '<chapter>\n\n'
close_chapter = '</chapter>\n\n'

# You will need a ARTICLE & CHAPTER open/closed status to know when to put in the tags above
chapter_open = False
article_open = False

# Step 3 : Look for keywords and make changes to each sentence
for sentence in combined_file:

    edit_sentence = sentence

    # 3.1 Converting headers
    
    # Header 1
    if 'CHAPTER' in edit_sentence:
        
        # Before editing the CHAPTER's tag, insert open and close chapter
        
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
            edit_sentence = '#' + edit_sentence.replace('#','')
    
    article_header_one = 'ARTICLE'
    article_header_two = 'Article'
    article_header_three = 'article'
    
    # Header 2 , check for variants
    if article_header_one or article_header_two or article_header_three in edit_sentence:
        
        # Check if it is a HTML tag, just add a new line to ensure that tag is invoked
        if (re.match('<article>', edit_sentence)):
            edit_sentence = edit_sentence + '\n'
            article_open = True
        else:
            # If article tag not declared, declare one
            if ((re.match(article_header_two, edit_sentence) or re.search(article_header_one, edit_sentence)) and article_open):
                output_file.write(close_article)
                article_open = False
                output_file.write(open_article)
                
                # Check if header is correct, header 2
                if edit_sentence.count('#') == 0:
                    edit_sentence = '## ' + edit_sentence
                
                if edit_sentence.count('#') != 2:
                    edit_sentence = '##' + edit_sentence.replace('#','')
            
            elif (re.search(article_header_one, edit_sentence)):
                output_file.write(open_article)
                article_open = True
                
        # This is to ensure that the correct MD format 
        try:
            if (re.match('Article', edit_sentence) or re.match(' Article', edit_sentence)):
                if (edit_sentence.split()[2][0].isupper()):
                    edit_sentence = '## ' + edit_sentence
        except IndexError:
            edit_sentence = '## ' + edit_sentence
            
    # 3.2 If the current sentence has header tags but is not a header
    if ('#' in edit_sentence):
        if not (article_header_one in edit_sentence or 'CHAPTER' in edit_sentence or article_header_two in edit_sentence or ' Article' in edit_sentence):
            edit_sentence = edit_sentence.replace('#','')
        
    # 3.3 End/Footnotes
    if (re.search("\d-\d", edit_sentence) != None):

        # If there is, then find the no. of the end/footnote
        end_footnote_one = re.search("\d-\d", edit_sentence).group()
        
        # If does not match, means its a endnote not a footnote
        if (re.match("\d[ -]\d", edit_sentence)) == None :
            edit_sentence = edit_sentence.replace(end_footnote_one, '[^' + end_footnote_one + ']')
        else:
            edit_sentence = edit_sentence.replace(end_footnote_one, '[^' + end_footnote_one + ']:')
    
    # This will allow (E.G. (^1) / ^1) from anywhere if the page to be rectified into [^1]
    if (re.search('\^\d', edit_sentence) != None):
        
        if (re.search('\(\^\d\)', edit_sentence) != None):
            wrong_note = re.search('\(\^\d\)', edit_sentence).group()
            note_number = re.search('\^\d', edit_sentence).group()
            edit_sentence = edit_sentence.replace(wrong_note, '[' + note_number + ']')
        # This checks for ^1, but [^1] and [^1]: also fits the bill so we need to prevent them from adding []
        elif (re.search('[^\d]', edit_sentence) == None and re.search('[^\d]:', edit_sentence) == None):
            end_footnote_two = re.search('\^\d', edit_sentence).group()
            edit_sentence = edit_sentence.replace(end_footnote_two, '[' + end_footnote_two + ']')
        
    # This will retify those footnotes missing the ':'
    if (re.match('\[\^\d\]', edit_sentence) != None):
    
        end_footnote_three = re.search('\[\^\d\]', edit_sentence).group()
        edit_sentence = edit_sentence.replace(end_footnote_three, end_footnote_three + ':')
    
    output_file.write(edit_sentence)

# Best practice to close, if there are too many files left unopened it will consume resources on your local PC 
combined_file.close()
output_file.close()

