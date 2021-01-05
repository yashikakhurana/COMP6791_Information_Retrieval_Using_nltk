# This file contains the sub-project 3
import json  # importing the json module to generate the json file

import nltk # importing the nltk module
from bs4 import BeautifulSoup # importing the bs4 for BeautifulSoup
from texttable import Texttable # importing the texttable to generate the table
from nltk.stem import PorterStemmer # importing the stemmer to stem (Porter Stemmer)
content_first30 = [] # global variable to store the list of 30 stop words
content_first150 = [] # global variable to store the list of 150 stop words

def subproject3(inverted_index, sorted_document_tokens, document_list): # subproject3() method to build the lossy dictionary compression techniques of Table 5.1

    #------------------------------------------------------------------------------------------------
    # REMOVING NUMBERS
    #------------------------------------------------------------------------------------------------


    total_token_count = len(inverted_index)  # getting the total no of tokens generated i.e. unfiltered tokens

    non_positional_positing = sum(len(v) for v in inverted_index.values()) # getting the value of the non positional postings

    remove_numbers = []  # list to store the tokens after removing the no.
    for j in sorted_document_tokens:
        if not(j[0].isnumeric()): # if the token is not numeric
            token_tple = (j[0], j[1])
            remove_numbers.append(token_tple) # append the tokens to the list

    inverted_index_without_no = {}  #building the inverted index
    for rm in remove_numbers:

        if rm[0] in inverted_index_without_no: # if the term exist in the index
            temp_posting_list = inverted_index_without_no[rm[0]]
            temp_posting_list.append(rm[1]) # append the id to the postings list
        else:
            posting_list = list() # if it is encountering the term first time
            posting_list.append(rm[1])  # create a list and id
            inverted_index_without_no[rm[0]] = posting_list # create the key and assign the doc id


    total_token_without_no = len(inverted_index_without_no) # calculating the distinct tokens
    non_positional_positing_without_no = sum(len(v) for v in inverted_index_without_no.values()) # calculating the non positinal index value


    # ------------------------------------------------------------------------------------------------
    # CASE FOLDING
    # ------------------------------------------------------------------------------------------------

    document_dicts = [] # creating the document list

    # iterating over the input
    for i in document_list:
        # setting the html.parse
        soup = BeautifulSoup(i, 'html.parser')
        # finding the text tag
        text_tag = soup.find('text')

        # checking the type of text to get only meaningful documents
        if (text_tag.get('type') != 'BRIEF') and (text_tag.get('type') != 'UNPROC'):
            reuters = soup.find('reuters')
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

            # print(temp_text)
            punctuations = '''!()[]{};:'"\,<>./?#$%^|&*_+~\u0005\u0005\u0005'''

            for char in temp_text: # removing the punctuation from the text
                if char in punctuations:
                    temp_text = temp_text.replace(char, " ")

            text = nltk.word_tokenize(temp_text) # case folding the terms
            text = [i.lower() for i in text]

            for j in text:
                if j != '\x03' and j != '\u0005\u0005\u0005' and j != '' and not(j.isdigit()): # removing the no. and unicode
                    token_tuple = (j, id)
                    document_dicts.append(token_tuple)






    sorted_document_tokens_case_folding = list(set(document_dicts)) # getting the list of unique tokens

    sorted_document_tokens_case_folding = sorted(set(sorted_document_tokens_case_folding)) # getting the sorted list of tokens



    inverted_index_cf = {} # building the indexer
    for sorted_tokens_cf in sorted_document_tokens_case_folding: # iterating the tokens

        if sorted_tokens_cf[0] in inverted_index_cf: # if the key(term) exist
            temp_posting_list = inverted_index_cf[sorted_tokens_cf[0]]
            temp_posting_list.append(sorted_tokens_cf[1]) # assig the doc id to the exisitng posting list
        else:
            posting_list = list() # if the term doesn't exist
            posting_list.append(sorted_tokens_cf[1]) # creating a list and assigning the doc id
            inverted_index_cf[sorted_tokens_cf[0]] = posting_list # creating the dictionary key and assigning the list


    total_token_case_folding = len(inverted_index_cf) # calculating the distinct tokens
    non_positional_positing_case_folding = sum(len(v) for v in inverted_index_cf.values()) # calculating the non positional index values




    # ------------------------------------------------------------------------------------------------
    # REMOVAL OF 30 STOP WORDS
    # ------------------------------------------------------------------------------------------------

    with open("first30.txt") as f: # reading the 30 stop words and storing in the list
        global content_first30
        content_first30 = f.read().splitlines()

    stop_words30 = []  # list to store the tokens after removing the 30 stop words
    for i in sorted_document_tokens_case_folding:
        if i[0] not in content_first30:  # making a check if the term is not stop words, then generate the token
            token_stop_words_30_tuple = (i[0], i[1]) # generating the token tuple
            stop_words30.append(token_stop_words_30_tuple)
    inverted_index_stop_words_30 = {} # dictionary to build the index
    for sw30 in stop_words30:
        if sw30[0] in inverted_index_stop_words_30: # if the term key exist in the posting list
            temp_posting_list = inverted_index_stop_words_30[sw30[0]]
            temp_posting_list.append(sw30[1]) # append the doc id to the posting list
        else:
            posting_list = list() # if the key-term is encountered first time, create the list
            posting_list.append(sw30[1]) # append the doc id to the new list
            inverted_index_stop_words_30[sw30[0]] = posting_list # create the key term and assign the posting list


    total_token_stop_words_30 = len(inverted_index_stop_words_30) # calculating the count of distinct tokens
    non_positional_positing_stop_words_30 = sum(len(v) for v in inverted_index_stop_words_30.values()) # calculating the count of non positional index values


    # ------------------------------------------------------------------------------------------------
    # REMOVAL OF 150 STOP WORDS
    # ------------------------------------------------------------------------------------------------

    with open("first150.txt") as f: # reading the list of 150 stop words
        global content_first150
        content_first150 = f.read().splitlines() # storing the list of 150 stop words into the list

    stop_words150 = []
    for i in sorted_document_tokens_case_folding:
        if i[0] not in content_first150:  # removing the 150 stop words from the list
            token_stop_words_150_tuple = (i[0], i[1]) # generating the tuples
            stop_words150.append(token_stop_words_150_tuple)
    inverted_index_stop_words_150 = {} # building the index
    for sw150 in stop_words150:
        if sw150[0] in inverted_index_stop_words_150: # check if the term exist in the index
            temp_posting_list = inverted_index_stop_words_150[sw150[0]]
            temp_posting_list.append(sw150[1]) # append the doc id to the posting list
        else:
            posting_list = list() # if the key doesn't exist, create an empty list
            posting_list.append(sw150[1])
            inverted_index_stop_words_150[sw150[0]] = posting_list # assign the key-term to the dictionary and docid

    #print(len(inverted_index_stop_words_150))
    total_token_stop_words_150 = len(inverted_index_stop_words_150) # calculating the distinct tokens
    non_positional_positing_stop_words_150 = sum(len(v) for v in inverted_index_stop_words_150.values()) # calculating the non positional index values
    #print(non_positional_positing_stop_words_150)

    # ------------------------------------------------------------------------------------------------
    # PORTER STEMMER
    # ------------------------------------------------------------------------------------------------


    document_dicts_ps = [] # list to store the tokens

    # iterating over the input
    for i in document_list:
        # setting the html.parse
        soup = BeautifulSoup(i, 'html.parser')
        # finding the text tag
        text_tag = soup.find('text')

        # checking the type of text to get only meaningful documents
        if (text_tag.get('type') != 'BRIEF') and (text_tag.get('type') != 'UNPROC'):
            reuters = soup.find('reuters')
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

            # print(temp_text)
            punctuations = '''!()[]{};:'"\,<>./?#$%^|&*_+~\u0005\u0005\u0005'''

            for char in temp_text:  # removing the punctuation from the text
                if char in punctuations:
                    temp_text = temp_text.replace(char, " ")

            text = nltk.word_tokenize(temp_text)
            text = [i.lower() for i in text] # case folding of the text

            ps = PorterStemmer()  # Porter Stemmer to stem the tokens

            for j in text:
                if j != '\x03' and j != '\u0005\u0005\u0005' and j != '' and not (j.isdigit()) and j not in content_first30 and j not in content_first150:
                    token_tuple = (ps.stem(j), id) # stemmings, removing stop words, no
                    document_dicts_ps.append(token_tuple)

    sorted_document_tokens_ps = list(set(document_dicts_ps)) # generating the unique tokens

    sorted_document_tokens_ps= sorted(set(sorted_document_tokens_ps)) # sorting the unique tokens

    inverted_index_ps = {} # building the indexer
    for sorted_tokens_ps in sorted_document_tokens_ps:

        if sorted_tokens_ps[0] in inverted_index_ps: # if the token exist in the indexer
            temp_posting_list = inverted_index_ps[sorted_tokens_ps[0]] # get the postings list
            temp_posting_list.append(sorted_tokens_ps[1]) # assign the doc id to the psoting list
        else:
            posting_list = list() # if the key doesn't exist in the indexer, create new list
            posting_list.append(sorted_tokens_ps[1]) # append the doc id
            inverted_index_ps[sorted_tokens_ps[0]] = posting_list # create a key in the dictionary and assign the newly created posting list

    total_token_porter_stemmer = len(inverted_index_ps) # calculate the distinct tokens
    non_positional_positing_porter_stemmer = sum(len(v) for v in inverted_index_ps.values()) # calculating the non positional indexer values

    t = Texttable() # building the Table 5.1
    main_row = [['', 'Distinct terms', '', '', '', 'Non positional postings', '']]

    row = ['', 'number', '\u0394%', 'T%', 'number', '\u0394%', 'T%']
    main_row.append(row)

    row = ['unfiltered', total_token_count, '', '', non_positional_positing, '', '']

    main_row.append(row)
    cumulative_cost = 0
    cumulative_cost_np = 0
    temp = 100 * (total_token_count - total_token_without_no) / total_token_count
    #print(temp, "%")
    cumulative_cost += temp
    np = 100 * (non_positional_positing - non_positional_positing_without_no) / non_positional_positing
    cumulative_cost_np += np
    row = ['no numbers', total_token_without_no, -temp, -cumulative_cost, non_positional_positing_without_no, -np,
           -cumulative_cost_np]
    main_row.append(row)
    #print("Cumulative", cumulative_cost)
    temp = 100 * (total_token_without_no - total_token_case_folding) / total_token_without_no
    #print(temp, "%")
    cumulative_cost += temp
    np = 100 * (
                non_positional_positing_without_no - non_positional_positing_case_folding) / non_positional_positing_without_no
    cumulative_cost_np += np
    row = ['case folding', total_token_case_folding, -temp, -cumulative_cost, non_positional_positing_case_folding, -np,
           -cumulative_cost_np]
    main_row.append(row)
    #print("Cumulative", cumulative_cost)
    temp = 100 * (total_token_case_folding - total_token_stop_words_30) / total_token_case_folding
    #print(temp, "%")
    cumulative_cost += temp
    np = 100 * (
                non_positional_positing_case_folding - non_positional_positing_stop_words_30) / non_positional_positing_case_folding
    cumulative_cost_np += np
    row = ['30 stop words', total_token_stop_words_30, -temp, -cumulative_cost, non_positional_positing_stop_words_30,
           -np, -cumulative_cost_np]
    main_row.append(row)
    #print("Cumulative", cumulative_cost)
    temp = 100 * (total_token_stop_words_30 - total_token_stop_words_150) / total_token_stop_words_30
    #print(temp, "%")
    cumulative_cost += temp
    np = 100 * (
                non_positional_positing_stop_words_30 - non_positional_positing_stop_words_150) / non_positional_positing_stop_words_30
    cumulative_cost_np += np
    row = ['150 stop words', total_token_stop_words_150, -temp, -cumulative_cost,
           non_positional_positing_stop_words_150, -np, -cumulative_cost_np]
    main_row.append(row)
    #print("Cumulative", cumulative_cost)
    temp = 100 * (total_token_stop_words_150 - total_token_porter_stemmer) / total_token_stop_words_150
    #print(temp, "%")
    cumulative_cost += temp
    np = 100 * (
                non_positional_positing_stop_words_150 - non_positional_positing_porter_stemmer) / non_positional_positing_stop_words_150
    cumulative_cost_np += np
    row = ['stemming', total_token_porter_stemmer, -temp, -cumulative_cost, non_positional_positing_porter_stemmer, -np,
           -cumulative_cost_np]
    main_row.append(row)
    #print("Cumulative", cumulative_cost)
    t.add_rows(main_row)
    print(t.draw()) # printing the talbe
    f = open("Table.txt", "w") # storing the output of the table
    f.write("".join(str(item) for item in t.draw()))
    f.close()
    json.dump(inverted_index_ps, open("invertedIndex_subproject3.json", "w", encoding="utf−8")) # storing the newly create index into invertedIndex_subproject3.json
    return inverted_index_ps