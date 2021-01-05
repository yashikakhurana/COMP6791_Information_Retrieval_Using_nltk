import json
import math
import os

import nltk
from bs4 import BeautifulSoup  # using BeautifulSoup to do data scrapping
from nltk.corpus import stopwords
from functools import reduce
import ast

# using stopwords.words('english') provided by nltk

path ="./"
tokens_list = []  # list to store tokens
final_block = {}
doc_length = {}
url_list = []
def loadpages():

    documents_dict = {}
    for i in os.listdir(path):
        # if it ends with .sgm then only do further processing
        if i.endswith('.html'):
            # used different encoding, due to mac environment
            with open(os.path.join(path, i), errors="ignore") as filename:
                # reading the file content
                reuters_file_content = filename.read()  # reading the file

                soup = BeautifulSoup(reuters_file_content, 'html.parser')  # using BeautifulSoup to extract the tags data
                # finding the text tag
                #print(soup)
                text_tag = soup.find('body')
                title= ""
                if soup.find(title) is not None:
                    title = soup.find('title').string
                #title = title.string
                temp_text = " "
                if soup.find('body') is not None:
                   temp_text = text_tag.get_text(separator=' ', strip=True)
                # print(temp_text)

                # extract title, search for more tags
                #temp_text = ' '.join(text_tag.text.split())
                #print(temp_text)
                #print(title)
                final_text = title+" "+temp_text
                #print(final_text)
                punctuations = '''!()[]{};:'"\©,<>./?#$%^|&*_+~-'''  # punctuation to be removed

                for char in final_text:  # removing the punctuation from the text
                    if char in punctuations:
                        final_text = final_text.replace(char, " ")  # replacing the punctuation to empty
               # print(final_text)
                t = i.split(".")
                documents_dict[t[0]]=final_text
    #print(documents_dict)
    documents_dict = dict(sorted(documents_dict.items()))
    #print(documents_dict)

    for key in documents_dict:
        #print(documents_dict[key])
        final_text = documents_dict[key]
        text = nltk.word_tokenize(final_text)
        #print(text)
        text = [i.lower() for i in text]  # case folding of the text
        #print(text)

        stop_words = set(stopwords.words('english'))
        removed_stop_words_text = []
        for j in text:
            if j not in stop_words:
                removed_stop_words_text.append(j)
        ps = nltk.PorterStemmer()  # Porter Stemmer to stem the tokens
        #print(removed_stop_words_text)
        stemming_text = [ps.stem(i) for i in removed_stop_words_text]
        #print(stemming_text)
        # print(reuters_file_content)
        #print(i)
        doc_length[key] = len(stemming_text)
        for k in stemming_text:

            temp_tuple = (k, key)
            tokens_list.append(temp_tuple)
    #print(tokens_list)






def generate_block():
    # Using readlines()
    # file1 = open('tokens.json', 'r')  # reading file of tokens, id pairs
    # Lines = file1.readlines() # reading file line by line
    counter = 0  # counter which will help to count the no. of blocks
    block_counter = 10000 # parameter to count no. of tokens per block

    temp_block = {}  # temporary block which will be used to store individual blocks generated temporarily
    block_cal=0 # count no of blocks
    for line in tokens_list: # iterate the file line by line
        # line = eval(line) # retrieve as tuples

        counter+=1   # increment the counter

        if counter == block_counter or line == tokens_list[-1]: # if counter is equal to the parameter or the current line is equal to end of the file generate the block
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
        merged_index[lowest_term] = [{'df': 0}]  # creating a dictionary for the lowest term found in all the blocks
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
                        temp_posting_list[0]['df']+=1

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
    if token in merged_index:
        return merged_index[token][1:len(merged_index[token])]
    else:
        return ""


def bm25calculator(query_term ,k,b):  # function to calculate the ranked by the formula bm25
    posting_list = get_posting_list(query_term) # get the psoting list of the query term
    ranking_doc_id = {} # to store the "docid": rsv value
    doc_freq = 0
    if query_term in merged_index:
        doc_freq =  merged_index[query_term][0]['df']# get the document frequency
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
        return get_posting_list(query) # return the postings list
    else: # if it is not present
        return "query not present" # return message key is not present

def or_spimi(query):  # function to run or spimi queries

    or_docs_id = []   # list to store the results of the individual query
    for single_term in query: # iterate the list of query
        if single_term in merged_index: # if the key is present in the spimi index
           # tmp = set([i for s in [d.keys() for d in merged_index[single_term]] for i in s])

            or_docs_id.append(get_posting_list(single_term)) # append the result
    temp_dic = {}

    for j in or_docs_id:
        for k in j:

            if next(iter(k)) in temp_dic:
                temp_dic[next(iter(k))] += 1
            else:
                temp_dic[next(iter(k))] = 1

    temp_dic = sorted(temp_dic.items(), key=lambda x: x[1], reverse=True)
    return temp_dic # return postings list

def and_spimi(query): # function to run the and queries on spimi

    and_doc_id = []
    for single_term in query: # iterate the list of query
        if single_term in merged_index: # if the key is present in the spimi index

            and_doc_id.append(get_posting_list(single_term))  # append the result

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


def tfidfcalculator(query_term):  # function to calculate the ranked by the formula bm25
    posting_list = get_posting_list(query_term) # get the psoting list of the query term
    ranking_doc_id = {} # to store the "docid": rsv value
    doc_freq = 0
    if query_term in merged_index:
        doc_freq = merged_index[query_term][0]['df']  # get the document frequency
    for signle_doc_id in posting_list: # iterate over the postings list

        doc_id = next(iter(signle_doc_id)) # get the ket
        doc_tf = signle_doc_id[doc_id] # get the value
        N = cal_no_of_documents() # get no. of documents present in the reuters

        tf = 1+math.log10(doc_tf)
        idf = math.log10(N/doc_freq)
        tf_idf = tf*idf
        ranking_doc_id[doc_id] = tf_idf # update in the dictionary
    #ranking_doc_id = dict(sorted(ranking_doc_id))
    ranking_doc_id= sorted(ranking_doc_id.items(), key=lambda x: x[1], reverse=True)
    return ranking_doc_id # return the dictionary


def tfidf_several_queries(queries): # function to run bm25 on several queries
    several_query_results = {}
    for t in queries:
        res = tfidfcalculator(t)
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

def pre_process_query(query_terms):

    # remove punctuation
    punctuations = '''!()[]{};:'"\©,<>./?#$%^|&*_+~-'''  # punctuation to be removed

    for char in query_terms:  # removing the punctuation from the text
        if char in punctuations:
            query_terms = query_terms.replace(char, " ")  # replacing the punctuation to empty
    # work tokenise
    text = nltk.word_tokenize(query_terms)
    # lower case
    text = [i.lower() for i in text]  # case folding of the text
    # removal of stop words
    stop_words = set(stopwords.words('english'))
    removed_stop_words_text = []
    for j in text:
        if j not in stop_words:
            removed_stop_words_text.append(j)
    # porter stemmer
    ps = nltk.PorterStemmer()  # Porter Stemmer to stem the tokens
    # print(removed_stop_words_text)
    stemming_text = [ps.stem(i) for i in removed_stop_words_text]
    # print(stemming_text)
    # print(reuters_file_content)
    return stemming_text

def load_url(): # load url
    with open('temp_list.json', 'r') as f:
        global url_list
        url_list = ast.literal_eval(f.read())
    return url_list

def get_url(results): # get url
    # print(results)
    results_list = []
    for i in results:
        # print(url_list)
        # print(int(i[0]))
        tmp = url_list[int(i[0])-1]
        # print(tmp)
        tmp_tuple = (tmp,i[1])
        results_list.append(tmp_tuple)
    return results_list[0:16]




loadpages()
generate_block()
print(len(final_block))

merge_block()
json.dump(merged_index, open("final_index.json", "w", encoding="utf−8"))

print(len(merged_index))
#merged_index['ymca'][0]['df']+=1
# print(merged_index['ymca'][0]['df'])
# print(get_posting_list('within'))
load_url()

# #-------------------Test-query1 bm25-----------------------
bm25_several_quer = "which researchers at Concordia worked on COVID 19-related research"
bm25_pre_process_query = pre_process_query(bm25_several_quer)
several_query_result = bm25_several_queries(bm25_pre_process_query)
several_query_result = get_url(several_query_result)
json.dump(several_query_result, open("Test_Query1_bm25.json", "w", encoding="utf−8"),indent=3)

# #-------------------Test-query1 tf-idf-----------------------
tf_idf_several_query = "which researchers at Concordia worked on COVID 19-related research"
tf_idf_pre_process_query = pre_process_query(tf_idf_several_query)
several_query_result = tfidf_several_queries(tf_idf_pre_process_query)
several_query_result = get_url(several_query_result)
json.dump(several_query_result, open("Test_Query1_tf-idf.json", "w", encoding="utf−8"),indent=3)

# #-------------------Test-query1 different measure-----------------------
spimi_several_queries = "which researchers at Concordia worked on COVID 19-related research"
spimi_pre_process_query = pre_process_query(spimi_several_queries)
several_query_result = or_spimi(spimi_pre_process_query)
several_query_result = get_url(several_query_result)
json.dump(several_query_result, open("Test_Query1_diffmeasure.json", "w", encoding="utf−8"),indent=3)


# #-------------------Test-query1 variation bm25-----------------------
bm25_several_quer = "researchers Concordia COVID 19"
bm25_pre_process_query = pre_process_query(bm25_several_quer)
several_query_result = bm25_several_queries(bm25_pre_process_query)
several_query_result = get_url(several_query_result)
json.dump(several_query_result, open("Test_Query1_variationbm25.json", "w", encoding="utf−8"),indent=3)

# #-------------------Test-query1 variation tf-idf-----------------------
tf_idf_several_query = "researchers Concordia COVID 19"
tf_idf_pre_process_query = pre_process_query(tf_idf_several_query)
several_query_result = tfidf_several_queries(tf_idf_pre_process_query)
several_query_result = get_url(several_query_result)
json.dump(several_query_result, open("Test_Query1_variationtf-idf.json", "w", encoding="utf−8"),indent=3)

# #-------------------Test-query1 variation different measure-----------------------
spimi_several_queries = "researchers Concordia COVID 19"
spimi_pre_process_query = pre_process_query(spimi_several_queries)
several_query_result = or_spimi(spimi_pre_process_query)
several_query_result = get_url(several_query_result)
json.dump(several_query_result, open("Test_Query1_variationdiffmeasure.json", "w", encoding="utf−8"),indent=3)



# #-------------------Test-query2 bm25-----------------------
bm25_several_quer = "which departments at Concordia have research in environmental issues, sustainability, energy and water"
bm25_pre_process_query = pre_process_query(bm25_several_quer)
several_query_result = bm25_several_queries(bm25_pre_process_query)
several_query_result = get_url(several_query_result)
json.dump(several_query_result, open("Test_Query2_bm25.json", "w", encoding="utf−8"),indent=3)

# #-------------------Test-query2 tf-idf-----------------------
tf_idf_several_query =  "which departments at Concordia have research in environmental issues, sustainability, energy and water "
tf_idf_pre_process_query = pre_process_query(tf_idf_several_query)
several_query_result = tfidf_several_queries(tf_idf_pre_process_query)
several_query_result = get_url(several_query_result)
json.dump(several_query_result, open("Test_Query2_tf-idf.json", "w", encoding="utf−8"),indent=3)

# #-------------------Test-query2 different measure-----------------------
spimi_several_queries =  "which departments at Concordia have research in environmental issues, sustainability, energy and water"
spimi_pre_process_query = pre_process_query(spimi_several_queries)
several_query_result = or_spimi(spimi_pre_process_query)
several_query_result = get_url(several_query_result)
json.dump(several_query_result, open("Test_Query2_diffmeasure.json", "w", encoding="utf−8"),indent=3)


# #-------------------Test-query2 variation bm25-----------------------
bm25_several_quer = "departments Concordia research environmental issues sustainability energy water"
bm25_pre_process_query = pre_process_query(bm25_several_quer)
several_query_result = bm25_several_queries(bm25_pre_process_query)
several_query_result = get_url(several_query_result)
json.dump(several_query_result, open("Test_Query2_variationbm25.json", "w", encoding="utf−8"),indent=3)

# #-------------------Test-query2  variation tf-idf-----------------------
tf_idf_several_query =  "departments Concordia research environmental issues sustainability energy water"
tf_idf_pre_process_query = pre_process_query(tf_idf_several_query)
several_query_result = tfidf_several_queries(tf_idf_pre_process_query)
several_query_result = get_url(several_query_result)
json.dump(several_query_result, open("Test_Query2_variationtf-idf.json", "w", encoding="utf−8"),indent=3)

# #-------------------Test-query2 variation different measure-----------------------
spimi_several_queries =  "departments Concordia research environmental issues sustainability energy water"
spimi_pre_process_query = pre_process_query(spimi_several_queries)
several_query_result = or_spimi(spimi_pre_process_query)
several_query_result = get_url(several_query_result)
json.dump(several_query_result, open("Test_Query2_variationdiffmeasure.json", "w", encoding="utf−8"),indent=3)

# #-------------------Challenge-query1 bm25-----------------------
bm25_several_quer = "water management sustainability Concordia"
bm25_pre_process_query = pre_process_query(bm25_several_quer)
several_query_result = bm25_several_queries(bm25_pre_process_query)
several_query_result = get_url(several_query_result)
json.dump(several_query_result, open("Challenge_Query1_bm25.json", "w", encoding="utf−8"),indent=3)

# #-------------------Challenge-query1 tf-idf-----------------------
tf_idf_several_query = "water management sustainability Concordia"
tf_idf_pre_process_query = pre_process_query(tf_idf_several_query)
several_query_result = tfidf_several_queries(tf_idf_pre_process_query)
several_query_result = get_url(several_query_result)
json.dump(several_query_result, open("Challenge_Query1_tf-idf.json", "w", encoding="utf−8"),indent=3)

# #-------------------Challenge-query1 different measure-----------------------
spimi_several_queries = "water management sustainability Concordia"
spimi_pre_process_query = pre_process_query(spimi_several_queries)
several_query_result = or_spimi(spimi_pre_process_query)
several_query_result = get_url(several_query_result)
json.dump(several_query_result, open("Challenge_Query1_diffmeasure.json", "w", encoding="utf−8"),indent=3)


# #-------------------Challenge-query2 bm25-----------------------
bm25_several_quer = "Concordia COVID-19 faculty"
bm25_pre_process_query = pre_process_query(bm25_several_quer)
several_query_result = bm25_several_queries(bm25_pre_process_query)
several_query_result = get_url(several_query_result)
json.dump(several_query_result, open("Challenge_Query2_bm25.json", "w", encoding="utf−8"),indent=3)

# #-------------------Challenge-query2 tf-idf-----------------------
tf_idf_several_query = "Concordia COVID-19 faculty"
tf_idf_pre_process_query = pre_process_query(tf_idf_several_query)
several_query_result = tfidf_several_queries(tf_idf_pre_process_query)
several_query_result = get_url(several_query_result)
json.dump(several_query_result, open("Challenge_Query2_tf-idf.json", "w", encoding="utf−8"),indent=3)

# #-------------------Challenge-query2 different measure-----------------------
spimi_several_queries = "Concordia COVID-19 faculty"
spimi_pre_process_query = pre_process_query(spimi_several_queries)
several_query_result = or_spimi(spimi_pre_process_query)
several_query_result = get_url(several_query_result)
json.dump(several_query_result, open("Challenge_Query2_diffmeasure.json", "w", encoding="utf−8"),indent=3)


# #-------------------Challenge-query3 bm25-----------------------
bm25_several_quer = "SARS-CoV Concordia faculty"
bm25_pre_process_query = pre_process_query(bm25_several_quer)
several_query_result = bm25_several_queries(bm25_pre_process_query)
several_query_result = get_url(several_query_result)
json.dump(several_query_result, open("Challenge_Query3_bm25.json", "w", encoding="utf−8"),indent=3)

# #-------------------Challenge-query3 tf-idf-----------------------
tf_idf_several_query = "SARS-CoV Concordia faculty"
tf_idf_pre_process_query = pre_process_query(tf_idf_several_query)
several_query_result = tfidf_several_queries(tf_idf_pre_process_query)
several_query_result = get_url(several_query_result)
json.dump(several_query_result, open("Challenge_Query3_tf-idf.json", "w", encoding="utf−8"),indent=3)

# #-------------------Challenge-query3 different measure-----------------------
spimi_several_queries = "SARS-CoV Concordia faculty"
spimi_pre_process_query = pre_process_query(spimi_several_queries)
several_query_result = or_spimi(spimi_pre_process_query)
several_query_result = get_url(several_query_result)
json.dump(several_query_result, open("Challenge_Query3_diffmeasure.json", "w", encoding="utf−8"),indent=3)