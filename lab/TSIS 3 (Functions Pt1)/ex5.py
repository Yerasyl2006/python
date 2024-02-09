from itertools import permutations
"""import a function permutations
from the itertools module.
permutations generates
all possible permutations of elements"""
def print_permutations():
    s = input("String : ")
    perms = permutations(s) #here perms is iterator
    # and "permutations" is the function
    
    print("All permutations : ")
    for perm in perms:
        print(''.join(perm))
        #takes each element (character)
        #from the perm tuple and concatenates them 
        #into one string, using the empty string '' as the delimiter.

print_permutations()