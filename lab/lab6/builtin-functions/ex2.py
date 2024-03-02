def letters(string):
    n=0
    m=0
    for i in string:
        if i.isupper():
            n=n+1
        if i.islower():
            m=m+1
    return n,m
    

a=input()
upper,lower=letters(a)
print("Numbers of upper:",upper)
print("Numbers of lower",lower)


