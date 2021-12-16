import re
import string
import pickle
import json
from random import randrange
import unicodedata


# https://stackoverflow.com/questions/43593428/splitting-a-sentence-by-ending-characters/43596240
def get_sentences(text):
    sentences = re.split(r'[.?!]\s*', text)
    if sentences[-1]:
        return sentences
    else:
        return sentences[:-1]


def strip_punc(s):
    res = s.translate(str.maketrans('', '', string.punctuation))
    return res.replace("\n", " ")


def get_author_abbrev(full_name):
    name_parts = full_name.split(" ")
    author_abbrev = "".join(map(lambda x: x[0].lower(), name_parts[:-1]))
    author_abbrev += name_parts[-1].lower()

    return author_abbrev


def read_pickle_file(data_file):
    with open(data_file, 'rb') as f:
        data = pickle.load(f)

    return data


def write_pickle_data(data, out_file):
    with open(out_file, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

def write_json_data(data, out_file):
    with open(out_file, 'w') as f:
        json.dump(data, f)

def read_json_file(data_file):
    with open(data_file, 'rb') as f:
        data = json.load(f)

    return data




def concat_paper_info(paper_title, paper_abstract):
    return paper_title + '. ' + paper_abstract



# Quickselect algorithm from
# https://pythonandr.com/2016/07/18/randomized-selection-algorithm-quickselect-python-code/
def partition(x, key, pivot_index = 0):
    i = 0
    if pivot_index != 0:
        x[0], x[pivot_index] = x[pivot_index], x[0]

    for j in range(len(x)-1):
        if key(x[j+1]) < key(x[0]):
            x[j+1],x[i+1] = x[i+1],x[j+1]
            i += 1

    x[0],x[i] = x[i],x[0]
    return x,i


def RSelect(x, k, key=lambda t: t):
    if len(x) == 1:
        return x[0]
    else:
        xpart = partition(x, key, randrange(len(x)))
        x = xpart[0] # partitioned array
        j = xpart[1] # pivot index
        if j == k:
            return x[j]
        elif j > k:
            return RSelect(x[:j], k, key)
        else:
            k = k - j - 1
            return RSelect(x[(j+1):], k, key)


def get_top_k(data, k, key=lambda t: t):
    thresh_elem_idx = len(data) - k
    thresh_elem = RSelect(data, thresh_elem_idx, key)

    return sorted(filter(lambda t: key(t) >= key(thresh_elem), data), key=key, reverse=True)




def standardize_non_ascii(s):
    def NFD(s):
        return unicodedata.normalize('NFD', s)

    return NFD(NFD(s).casefold())


def drop_table(cur, table_name):
    drop_table_sql = "DROP TABLE IF EXISTS " + table_name
    cur.execute(drop_table_sql)

def get_search_pattern(query):
    return "%" + query + "%"

def return_print_err(msg):
    print(msg)
    return msg

def gen_sql_in_tup(num_vals):
    if num_vals == 0:
        return "(FALSE)"
    return "(" + ",".join(["%s"] * num_vals) + ")"


if __name__ == '__main__':
    str1 = 'naïve bayes'
    str2 = 'naive bayes'

    print(standardize_non_ascii(str1))
    print(standardize_non_ascii(str2))
    print(standardize_non_ascii(str1) == standardize_non_ascii(str2))
