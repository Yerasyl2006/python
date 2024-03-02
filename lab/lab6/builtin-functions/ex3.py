def function(string):
    restring=string.lower()[::-1]
    return restring==string.lower()

s=input()
print(function(s))