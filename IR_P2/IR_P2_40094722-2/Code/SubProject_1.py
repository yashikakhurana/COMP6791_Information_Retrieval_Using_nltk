# This file contains the sub-project 1

import json   # importing the json module

import nltk   # importing the nltk module

path ="./reuters21578"  # path of the reuters corpus 21578

import os   # importing the os module

import re  # imprting re module

from bs4 import BeautifulSoup  # using BeautifulSoup to do data scrapping
import time   # importing the time module
def subproject1(): # subproject1() method which will generate the naive indexer and also the result will be store in the invertedIndex.json

    start_time = time.time()   # to get the start time before building the naive indexer
    # Getting the path directory
    documents_list = []      # list to store the 22 sgm files
    for i in os.listdir(path):
        # if it ends with .sgm then only do further processing
        if i.endswith('.sgm'):
            # used different encoding, due to mac environment
            with open(os.path.join(path, i), errors="ignore") as filename:
                # reading the file content
                reuters_file_content = filename.read()  #reading the file

                # splitting the document form <!DOCTYPE to separate 22 .sgm files
                document = [re.split('<!DOCTYPE lewis SYSTEM "lewis.dtd">', reuters_file_content)[1]]
                # iterating the document to get the <REUTERS pair to get the news document
                for j in document:
                    i = j
                    while len(i) != 0:    #extracting the reuters tag from the documents
                        if '</REUTERS>' in i:
                            # getting the index of pair of reuters tag
                            document_text = i[i.index('<REUTERS'):i.index('</REUTERS>') + 10]
                            # updating the i to get the next reuters pair
                            i = i[i.index('</REUTERS>') + 10:]
                            documents_list.append(document_text)
                        else:
                            break




    document_dict = []      # list to store all the reuter documents
    # iterating over the input
    for i in documents_list:   # iterating the 22 sgm files data
        # setting the html.parse
        soup = BeautifulSoup(i, 'html.parser')  # using BeautifulSoup to extract the tags data
        # finding the text tag
        text_tag = soup.find('text')

        # checking the type of text to get only meaningful documents
        if (text_tag.get('type') != 'BRIEF') and (text_tag.get('type') != 'UNPROC'):
            reuters = soup.find('reuters')    # finding the reuters tag
            # getting the id of the news document
            ids = reuters.get('newid')
            # parsing the id into int
            id = int(ids)
            # getting the date of the document
            date = soup.find('date').string
            # getting the title of the document
            title = soup.find('title').string
            # getting the body of the document
            body = soup.find('body')
            # building a string of useful data
            temp_text = date + ' ' + title + ' ' + body.get_text()


            punctuations =  '''!()[]{};:'"\,<>./?#$%^|&*_+~\u0005\u0005\u0005'''   # punctuation to be removed


            for char in temp_text:    # removing the punctuation from the text
                if char in punctuations:
                    temp_text = temp_text.replace(char, " ")  # replacing the punctuation to empty


            text = nltk.word_tokenize(temp_text)   # nltk word_tokenize to get the tokens of the text



            for j in text:
                if j != '\x03' and j!='\u0005\u0005\u0005' and j!='':  # removing the unicode characters from the text
                    token_tuple = (j, id)   # generated tuple of tokens and id (document id)
                    document_dict.append(token_tuple)  # appending the token tuple to the list

    f = open("tokens.txt", "w")  # stroing the list of tokens in the token.txt
    f.write("\n".join(str(item) for item in document_dict))
    f.close()

    sorted_document_tokens = sorted(set(document_dict))  # sorting the tuple of tokens

    sorted_document_tokens = list(set(sorted_document_tokens)) # generating the unique tuple of tokens

    sorted_document_tokens = sorted(set(sorted_document_tokens)) # sorting the unique tuple of tokens

    f = open("sortedTokens.txt", "w") # storing the unique and sorted tokens into the sortedTokens.txt
    f.write("\n".join(str(item) for item in sorted_document_tokens))
    f.close()

    inverted_index = {}   # building the naive indexer storing the term as a key and postings list as a list()
    for sorted_tokens in sorted_document_tokens:

        if sorted_tokens[0] in inverted_index:  # if the key i.e. terms already exist in the index, append the id in posting list
            temp_posting_list = inverted_index[sorted_tokens[0]]
            temp_posting_list.append(sorted_tokens[1])
        else:
            posting_list = list()   # if the kay don't exist in the dictionary, create the list and assign the key and list in the dictionary
            posting_list.append(sorted_tokens[1])
            inverted_index[sorted_tokens[0]] = posting_list


    print("Total time taken by naive indexer to build is--- %s seconds ---" % (time.time() - start_time)) # getting the current time now to evaluate the total time taken by the naive indexer to build
    json.dump(inverted_index, open("invertedIndex.json", "w", encoding="utf−8")) # storing the generated inverted index in invertedIndex.json file
    return inverted_index, sorted_document_tokens, documents_list





