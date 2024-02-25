import re
def text_match(text):
        patterns = 'ab{2,3}'
        if re.search(patterns,  text):
                return 'Found a match!'
        else:
                return('Not matched!')
print(text_match("abmdmmdsn,s,s,abbb"))
print(text_match("aabbbbbc"))
print(text_match("ab"))
