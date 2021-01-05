# This file contains the sub-project 1

import json   # importing the json module
from functools import reduce

import nltk   # importing the nltk module

path ="./reuters21578"  # path of the reuters corpus 21578

import os   # importing the os module

import re  # imprting re module
import math

from bs4 import BeautifulSoup  # using BeautifulSoup to do data scrapping
import time   # importing the time module
temp_token = []
final_block = {}
doc_length = {}
def subproject1(): # subproject1() method which will generate the naive indexer and also the result will be store in the invertedIndex.json


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


    document_dict = {}      # list to store all the reuter documents

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
            document_dict[id]=temp_text
    document_dict = dict(sorted(document_dict.items()))
    f = open("tokens.json", "w")  # stroing the list of tokens in the token.txt

    for i in document_dict:
        temp_text = document_dict[i]
        text = nltk.word_tokenize(temp_text)   # nltk word_tokenize to get the tokens of the text
        doc_length[i]= len(text)
        for j in text:
            if j != '\x03' and j!='\u0005\u0005\u0005' and j!='':  # removing the unicode characters from the text
                token_tuple = (j, i)   # generated tuple of tokens and id (document id)
                f.write(str(token_tuple)+'\n')
                temp_token.append(token_tuple)  # appending the token tuple to the list


    #f.write("\n".join(str(item) for item in temp_token))
    f.close()


def generate_block():
    # Using readlines()
    file1 = open('tokens.json', 'r')  # reading file of tokens, id pairs
    Lines = file1.readlines() # reading file line by line
    counter = 0  # counter which will help to count the no. of blocks
    block_counter = 10000 # parameter to count no. of tokens per block

    temp_block = {}  # temporary block which will be used to store individual blocks generated temporarily
    block_cal=0 # count no of blocks
    for line in Lines: # iterate the file line by line
        line = eval(line) # retrieve as tuples

        counter+=1   # increment the counter

        if counter == block_counter or line == Lines[-1]: # if counter is equal to the parameter or the current line is equal to end of the file generate the block
            block_cal+=1  # incrementing block no.
            str_block = str(block_cal) # converting block no. to string
            block_name = "block" + str_block # generating the unique block+id
            temp_block = dict(sorted(temp_block.items())) # sort the temp block before appending the final block
            final_block[block_name] = temp_block # allocating the key  as block+id and value as temp block to that particular block
            temp_block = {} # flushing all the data of the temp_block to create next temp block
            counter = 0 # re-set counter to 0 to again prepare for next block

        else:      # else counter is not yet 10000 tokens
            if line[0] in temp_block:  # check if the key is present in temp block
                tmp_list = temp_block[line[0]]  # key is present in the temp block
                check_doc_id = any(line[1] in d for d in tmp_list) # check if the doc id is present in the temporary list
                if check_doc_id:  # if it its true then iterate the list
                    for temp_list in tmp_list: # iterating the existing postings list
                         if line[1] in temp_list: # if the doc id is already present
                             temp_tf = temp_list[line[1]] # get the tf of that doc id
                             temp_tf += 1 # increment by one if the doc id is already present i.e term frequency
                             temp_list[line[1]] = temp_tf # update with the new
                else:
                    tmp_list.append({line[1]: 1}) # term is already present in the block but not the doc id

            else:   #new term
                temp_block[line[0]]= [{line[1]:1}] # term is not in block, create new hash key
merged_index = {}  # merge index for the spimi index to be build
def merge_block():  # merge block function to merge the blocks created
    while len(final_block)!=0:  # run while all the elements of all the blocks are in the spimi index

        #print("Merge block started")
        lowest_term = next(iter(final_block[next(iter(final_block))])) # taking the first block first element is the smallest element
        #print(lowest_term)

        for blck in list(final_block): # comparing with all the blocks to get the lowest token present in all block
            if next(iter(final_block[blck])) < lowest_term: # if the current block element is less then the lowest token taken
                lowest_term = next(iter(final_block[blck])) # then update the lowest term
        #print(lowest_term)
        merged_index[lowest_term] = []  # creating a dictionary for the lowest term found in all the blocks
        for blcks in list(final_block): # run the loop through all the blocks
            if lowest_term in final_block[blcks]: # if the lowest term is present in current block

                block_posting_list = final_block[blcks][lowest_term]  # get the corresponding posting list of the lowest term
                temp_posting_list = merged_index[lowest_term] # get the postings list of the merged index i.e. of spimi
                for single_doc_id in block_posting_list: # iterate the postings list which is not yet covered in the spimi

                    if any((next(iter(single_doc_id))) in d for d in temp_posting_list): # if the key is present in the dictionary
                        for i in temp_posting_list:
                            if next(iter(i)) == next(iter(single_doc_id)):  # if that doc id is already present in the spimi
                                #print("hello")
                                i[next(iter(i))] = i[next(iter(i))] + single_doc_id[next(iter(single_doc_id))] # add the value of the tf of the same doc id

                    else:
                        temp_posting_list.append(single_doc_id)  # if that doc id is not present, append the doc id, tf pair
                if lowest_term in final_block[blcks]: # delete the lowest term from the block once it is processed
                    del final_block[blcks][lowest_term]  # deleting the particular key from the block
        for blc in list(final_block):  # check if the block gets empty i.e. no more terms are left
            check_empty = final_block[blc]
            if len(check_empty)==0: # if the lenght is 0
                del final_block[blc] # delete the block

def cal_l_avg():  # function to calculate the average length of the documents present in the reuters
    total_length =0 # to calculate the sum of all the lenght intialised as 0
    for i in doc_length: # iterate through the all the docs
        total_length+=doc_length[i] # add the lenght of the docs
    return total_length/len(doc_length) # return the average lenght by dividing the no. of documents

def cal_no_of_documents(): # function to calculate the no. of documents
    return len(doc_length) # return len of documents

def cal_doc_l(doc_id): # calculate lenght of document by given id
    return doc_length[doc_id] # return the lenght of document by given id

def get_posting_list(token): # function to get the postings list of the given query on spimi
    return merged_index[token]

def bm25calculator(query_term ,k,b):  # function to calculate the ranked by the formula bm25
    posting_list = get_posting_list(query_term) # get the psoting list of the query term
    ranking_doc_id = {} # to store the "docid": rsv value
    doc_freq = len(posting_list) # get the document frequency
    for signle_doc_id in posting_list: # iterate over the postings list

        doc_id = next(iter(signle_doc_id)) # get the ket
        doc_tf = signle_doc_id[doc_id] # get the value
        N = cal_no_of_documents() # get no. of documents present in the reuters
        L_doc = cal_doc_l(doc_id) # get the lenght of current document
        L_avg = cal_l_avg() # get the average of the documents
        lg = math.log10(N/doc_freq)
        uppr = (k+1)*doc_tf
        lwr = k*((1-b)+b*(L_doc/L_avg))+doc_tf
        cal_rsv = lg*uppr/lwr # bm25 formula
        ranking_doc_id[doc_id] = cal_rsv # update in the dictionary
    #ranking_doc_id = dict(sorted(ranking_doc_id))
    ranking_doc_id= sorted(ranking_doc_id.items(), key=lambda x: x[1], reverse=True)
    return ranking_doc_id # return the dictionary


def spimi_index(query): # function to query on spimi index
    if query in merged_index: # check if the key is present in the spimi
        return merged_index[query] # return the postings list
    else: # if it is not present
        return "query not present" # return message key is not present

def or_spimi(query):  # function to run or spimi queries

    or_docs_id = []   # list to store the results of the individual query
    for single_term in query: # iterate the list of query
        if single_term in merged_index: # if the key is present in the spimi index
           # tmp = set([i for s in [d.keys() for d in merged_index[single_term]] for i in s])

            or_docs_id.append(merged_index[single_term]) # append the result

    temp_dic = {}

    for j in or_docs_id:
        for k in j:

            if next(iter(k)) in temp_dic:
                temp_dic[next(iter(k))] += 1
            else:
                temp_dic[next(iter(k))] = 1

    temp_dic = sorted(temp_dic.items(), key=lambda x: x[1], reverse=True)



   # or_docs_id = list(set(or_docs_id)) # generate the unique postings list present
    #print(or_docs_id)
    return temp_dic # return postings list



def and_spimi(query): # function to run the and queries on spimi

    and_doc_id = []
    for single_term in query: # iterate the list of query
        if single_term in merged_index: # if the key is present in the spimi index

            and_doc_id.append(merged_index[single_term])  # append the result

    temp_list = []
    for i in and_doc_id:
        tmp_list2 = []
        for x in i:

            tmp_list2.append(next(iter(x)))
        temp_list.append(tmp_list2)
    res = list(reduce(lambda i, j: i & j, (set(x) for x in temp_list)))
    return res

def bm25_several_queries(queries): # function to run bm25 on several queries
    several_query_results = {}
    for t in queries:
        res = bm25calculator(t, 1, 0.5)
        several_query_results[t] = res
    several_query_result = {}
    for t in several_query_results:
        posting_list = several_query_results[t]
        for i in posting_list:
            if i[0] in several_query_result:
                several_query_result[i[0]] += i[1]
            else:
                several_query_result[i[0]] = i[1]   # sorting the value in descending order by rsv value
    several_query_result = sorted(several_query_result.items(), key=lambda x: x[1], reverse=True)
    return several_query_result

#-------------------start timer-----------------------
start_time = time.time()   # to get the start time before building the naive indexer
#-------------------load corpus-----------------------
print("---------------Loading Corpus-----------")
subproject1()
print("---------------Blocks generation started-----------")
#-------------------generate blocks-----------------------
generate_block()
# print(len(final_block))
# block1 = final_block["block1"]
# json.dump(block1, open("block1.json", "w", encoding="utf−8"))
# blocklast = final_block["block5829"]
# json.dump(blocklast, open("blocklast.json", "w", encoding="utf−8"))

#-------------------stop_timer-----------------------
print("---------------Block generation completed-----------")
print("Total time taken by spimi blocks  to build is--- %s seconds ---" % (time.time() - start_time)) # getting the current time now to evaluate the total time taken by the naive indexer to build

print("---------------Blocks Merging started-----------")
#-------------------Merger-blocks-----------------------
merge_block()
print("---------------Indexer built-----------")
json.dump(merged_index, open("invertedIndex.json", "w", encoding="utf−8"),indent=1)
#-------------------BM25formula k and b values comparsion-----------------------
bm25_comparison_1 = bm25calculator("Brierley",1,0.5)
json.dump(bm25_comparison_1, open("bm25_comparison_1.json", "w", encoding="utf−8"),indent=3)
bm25_comparison_2 = bm25calculator("Brierley",1,0.2)
json.dump(bm25_comparison_2, open("bm25_comparison_2.json", "w", encoding="utf−8"),indent=3)
bm25_comparison_3 = bm25calculator("Brierley",1,0.8)
json.dump(bm25_comparison_3, open("bm25_comparison_3.json", "w", encoding="utf−8"),indent=3)
bm25_comparison_4 = bm25calculator("Brierley",2,0.8)
json.dump(bm25_comparison_4, open("bm25_comparison_4.json", "w", encoding="utf−8"),indent=3)
spimi = spimi_index("Brierley")
json.dump(spimi, open("spimi_comparison.json", "w", encoding="utf−8"),indent=3)
#-------------------------Test-queries----------------------

#-------------------Test-query1-----------------------
single_word_query = ["logic", "belt", "obtain", "Empire"]  # sample queries list
single_query_result = {}
for t in single_word_query:
    res = bm25calculator(t,1,0.5)
    single_query_result[t]= res
json.dump(single_query_result, open("single_term_queries.json", "w", encoding="utf−8"),indent=3)
#-------------------Test-query2-----------------------
bm25_several_querie = ["investors","stock","Ottawa"]  #Ottawa present in 008 -8029 and rest 004-4001
several_query_result = bm25_several_queries(bm25_several_querie)
json.dump(several_query_result, open("single_term_queries.json", "w", encoding="utf−8"),indent=3)

#-------------------Test-query3-----------------------
and_queries_unranked = ["earth","minerals","titanium"] #doc011 ,id 11999
and_queries_unranked = and_spimi(and_queries_unranked)
json.dump(and_queries_unranked, open("and_queries_unranked.json", "w", encoding="utf−8"),indent=3)

#-------------------Test-query4-----------------------
or_queries_unranked = ["earth","minerals","titanium"]
or_queries_unranked = or_spimi(or_queries_unranked)
json.dump(or_queries_unranked, open("or_queries_unranked.json", "w", encoding="utf−8"),indent=3)

#-----------------------------information need queries-----------------------
# using bm25
#-------------------query1-----------------------
query1 = "Democrats' welfare and healthcare reform policies"
# remvong punctuation
punctuations =  '''!()[]{};:'"\,<>./?#$%^|&*_+~\u0005\u0005\u0005'''   # punctuation to be removed

for char in query1:    # removing the punctuation from the text
    if char in punctuations:
        query1 = query1.replace(char, " ")  # replacing the punctuation to empty
# run "or" for "Democrats Welfare" "and" "or" for "healthcare reform policies"
query1 = ["Democrats","welfare","healthcare","reform","policies"]

information_need_query_a_bm25 = bm25_several_queries(query1)
json.dump(information_need_query_a_bm25, open("information_need_query_a_bm25.json", "w", encoding="utf−8"),indent=3)

#-------------------query2-----------------------

query2 = ["Drug","company","bankruptcies"]
# rbm25

information_need_query_b_bm25 = bm25_several_queries(query2)
json.dump(information_need_query_b_bm25, open("information_need_query_b_bm25.json", "w", encoding="utf−8"),indent=3)

#-------------------query3-----------------------
query3 = ["George","Bush"]
# bm25
information_need_query_c_bm25 = bm25_several_queries(query3)
json.dump(information_need_query_c_bm25, open("information_need_query_c_bm25.json", "w", encoding="utf−8"),indent=3)







