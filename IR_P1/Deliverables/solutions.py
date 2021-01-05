"""
Write your reusable code here.
Main method stubs corresponding to each block is initialized here. Do not modify the signature of the functions already
created for you. But if necessary you can implement any number of additional functions that you might think useful to you
within this script.

Delete "Delete this block first" code stub after writing solutions to each function.

Write you code within the "WRITE YOUR CODE HERE vvvvvvvvvvvvvvvv" code stub. Variable created within this stub are just
for example to show what is expected to be returned. You CAN modify them according to your preference.
"""



def block_reader(path):
    #importing the os module
    import os
    #Getting the path directory
    for i in os.listdir(path):
        #if it ends with .sgm then only do further processing
        if i.endswith('.sgm'):
            #used different encoding, due to mac environment
            with open(os.path.join(path,i),encoding="ISO-8859-1") as filename:
                #reading the file content
                reuters_file_content= filename.read()
                yield reuters_file_content


def block_document_segmenter(INPUT_STRUCTURE):
    #imprting re module
    import re
    #splitting the document form <!DOCTYPE to separate 22 .sgm files
    document = [re.split('<!DOCTYPE lewis SYSTEM "lewis.dtd">', i)[1] for i in INPUT_STRUCTURE]
    #iterating the document to get the <REUTERS pair to get the news document
    for j in document:
        i=j
        while len(i)!=0:
            if '</REUTERS>' in i:
                #getting the index of pair of reuters tag
                document_text = i[i.index('<REUTERS'):i.index('</REUTERS>')+10]
                #updating the i to get the next reuters pair
                i = i[i.index('</REUTERS>')+10:]
                yield document_text
            else: break



def block_extractor(INPUT_STRUCTURE):
    #using BeautifulSoup to do data scrapping
    from bs4 import BeautifulSoup
   #iterating over the input
    for i in INPUT_STRUCTURE:
        #setting the html.parse
        soup = BeautifulSoup(i, 'html.parser')
        #finding the text tag
        text_tag = soup.find('text')

        #checking the type of text to get only meaningful documents
        if (text_tag.get('type') !='BRIEF') and (text_tag.get('type') !='UNPROC'):
            reuters= soup.find('reuters')
            #getting the id of the news document
            ids = reuters.get('newid')
            #parsing the id into int
            id = int(ids)
            #getting the date of the document
            date = soup.find('date').string
            #getting the title of the document
            title = soup.find('title').string
            #getting the body of the document
            body = soup.find('body')
            #building a string of useful data
            temp_text = date+' '+title+' '+body.get_text()
            #print(temp_text)
            content_dict = {"ID": id, "TEXT": temp_text}
            yield content_dict

    # WRITE YOUR CODE HERE ^^^^^^^^^^^^^^^^


def block_tokenizer(INPUT_STRUCTURE):
    import nltk
    for i in INPUT_STRUCTURE:
        #first removing the punctuation
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        no_punct = ""

        for char in i['TEXT']:
            if char not in punctuations:
                no_punct = no_punct + char

        i['TEXT']= no_punct
        #using the word_tokenize to get the words tokens
        text = nltk.word_tokenize(i['TEXT'])
        for j in text:
            token_tuple = (i['ID'], j)
            yield token_tuple


def block_stemmer(INPUT_STRUCTURE):
    #using the Porter Stemming
    from nltk.stem import PorterStemmer
    ps = PorterStemmer()
    for i in INPUT_STRUCTURE:
        #first lower casing the tokens
        i[1]=i[1].lower()
        #applying the Porter stemming
        token_tuple = (i[0], ps.stem(i[1]))
        yield token_tuple



def block_stopwords_removal(INPUT_STRUCTURE, stopwords):
    #removing the stop words from the tokens generated in the previous block
    from nltk.corpus import stopwords
    #using stopwords.words('english') provided by nltk
    stop_words = set(stopwords.words('english'))
    for i in INPUT_STRUCTURE:
        if i[1] not in stop_words:
            #generating the new tuples
            token_tuple = (i[0], i[1])  # Sample id, token tuple structure of output
            yield token_tuple

