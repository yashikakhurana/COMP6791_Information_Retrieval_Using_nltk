# This file contains the sub-project 2
import json  # importing the json module for the output files
from SubProject_3 import content_first30,content_first150
from nltk.stem import PorterStemmer # importing the Porter Stemmer to stem the text
def subproject2(inverted_index, inverted_index_porter_stemmer): # subproject2() method to run the sample queries and challenge queries on both the index
    sample_queries = ["logic", "belt", "obtain", "Empire"]  # sample queries list
    q = {}
    for i in sample_queries: # iterating over the sample queries list
        if i in inverted_index: # checking if the query exist in the inverted index
            postings_list = inverted_index[i]
            #print(postings_list)
            q[i] = postings_list # assigning the postings list of the query to the dictionary value

        else:
           # print("Term not found!")
            q[i] = ["Term not found!"]  # if the sample query not found give the result "Term not found"

    json.dump(q, open("sampleQueries.json", "w", encoding="utf−8"), indent=3) # store the queries result into samppleQueries.json

    q = {}   # pre-processing of the term to run on the sub project 3 index
    sample_queries = [i for i in sample_queries if not(i.isdigit())] # removing the number
    sample_queries = [i.lower() for i in sample_queries] # case folding the sample queries
    sample_queries = [i for i in sample_queries if i not in content_first30 ] # removing the stop words-30
    sample_queries = [i for i in sample_queries if i not in content_first150] # removing the stop words-15-
    ps = PorterStemmer() # PorterStemmer to stem the sample queries
    sample_queries = [ ps.stem(i) for i in sample_queries] # applying the Porter Stemmer to the sample queries



    for i in sample_queries:  # iterating the processed sample queries
        if i in inverted_index_porter_stemmer:
            postings_list = inverted_index_porter_stemmer[i]
            # print(postings_list)
            q[i] = postings_list # if the term exist then assign the result

        else:
            # print("Term not found!")
            q[i] = ["Term not found!"] # if the term is not found give the results "Term not found"

    json.dump(q, open("sampleQueries_subproject3.json", "w", encoding="utf−8"), indent=3) # store the results in sampleQueries_subproject3.json

    sample_queries = ["pineapple", "Phillippines", "Brierley", "Chrysler", "Philippines"]  # challenge queries given in the project

    q = {}
    for i in sample_queries: # iterating the challenge queries to check if the indx exist in the naive indexer
        if i in inverted_index: # if the term exist
            postings_list = inverted_index[i]
            #print(postings_list)
            q[i] = postings_list # assign the posting list of the term found to the result

        else:
            #print("Term not found!")
            q[i] = ["Term not found!"] # if the key not found return the result "Term not found"

    json.dump(q, open("challengeQueries.json", "w", encoding="utf−8"), indent=3) # store the results into the challengeQueries.json

    q = {}  # running the challenge queries and doing the pre-processing of the terms to run before on the final index created by the subproject 3
    sample_queries = [i for i in sample_queries if not (i.isdigit())] # checking if the term is digit
    sample_queries = [i.lower() for i in sample_queries] # doing the case folding of the term
    sample_queries = [i for i in sample_queries if i not in content_first30] # removing the stop words 30
    sample_queries = [i for i in sample_queries if i not in content_first150] # removing the stop words 150
    ps = PorterStemmer() # Porter Stemmer to stem the challenge queries
    sample_queries = [ps.stem(i) for i in sample_queries] # stemming all the challenge queries
    for i in sample_queries: # iterating the challenge queries
        if i in inverted_index_porter_stemmer: # if the pre-processed term is present in the index created by the final sub project 3
            postings_list = inverted_index_porter_stemmer[i]
            # print(postings_list)
            q[i] = postings_list  # assigning the result to the term

        else:
            # print("Term not found!")
            q[i] = ["Term not found!"] # if the pre-processed term is not found return "Term not found"

    json.dump(q, open("challengeQueries_subproject3.json", "w", encoding="utf−8"), indent=3) # generating the challengeQueries_subproject3.json
