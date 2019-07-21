   
def find_substring(a, n):  
    size_of_a = len(a) - n + 1
    substrings_of_a = []
    for i in range(size_of_a):
        substrings_of_a.append(a[i:n + i])
    return substrings_of_a
    
print (find_substring("meow", 3))