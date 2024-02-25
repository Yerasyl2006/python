import re
text = 'Yerasyl have stronger, than Ramazan.'
print(re.sub("[ ,.]", ":", text))
