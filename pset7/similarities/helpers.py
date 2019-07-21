from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""
    
    a_lines = a.split("\n")
    b_lines = b.split("\n")
    
    return compare_list(a_lines, b_lines)


def sentences(a, b):
    """Return sentences in both a and b"""
    a_sentence = sent_tokenize(a)
    b_sentence = sent_tokenize(b)
    
    return compare_list(a_sentence, b_sentence)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    substrings_of_a = find_substrings(a, n)
    substrings_of_b = find_substrings(b, n)
    
    return compare_list(substrings_of_a, substrings_of_b)


def compare_list(a, b):
    """"compares two lists and returns intersection"""
    
    # converts lists to set and creates intersection set
    compare_set = set(a).intersection(set(b))
    
    # converts new set to list and returns
    return list(compare_set)
    
    
def find_substrings(a, n):  
    """"creates substrings of a given n length from given string a"""""
    
    # finds final possible position of substring (ex: if length of a was 7 and n was 3, i better stop at the 5th position/letter to ensure there is enough letters)
    j = len(a) - n + 1
    
    substrings = []
    
    # finds all substrings of given length n for the string a
    for i in range(j):
        substrings.append(a[i:n + i])
    
    return substrings    