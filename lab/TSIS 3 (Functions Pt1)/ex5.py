from itertools import permutations

def print_permutations():
    string = input("Введите строку: ")
    perms = [''.join(p) for p in permutations(string)]
    for perm in perms:
        print(perm)

print_permutations()