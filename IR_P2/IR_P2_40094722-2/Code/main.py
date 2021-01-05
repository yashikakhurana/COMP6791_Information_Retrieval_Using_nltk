#importing all the files for subproject1, subproject2 and subproject3
from SubProject_1 import subproject1
from SubProject_2 import subproject2
from SubProject_3 import subproject3

#building the inverted index by calling the subproject1() which will return the inverted index and sorted tokens
inverted_index, sorted_document_tokens, document_list= subproject1()
#building the table 5.1 and returning the invered index after applying Porter Stemmer
inverted_index_porter_stemmer=subproject3(inverted_index,sorted_document_tokens, document_list)
#running the sample queries and challenge queries
subproject2(inverted_index,inverted_index_porter_stemmer)

