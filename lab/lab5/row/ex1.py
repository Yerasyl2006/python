import re
import csv

f = open('row.txt', 'r', encoding='utf8')
text = f.read()

pattern = r"\n(?P<реті>[0-9]+)\.\n(?P<аты>.+)\n(?P<саны>.+)x(?P<бағасы>.+)\n(?P<құны>.+)"

res = re.finditer(pattern, text)

with open('data.csv', 'w', newline='',encoding="utf8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['реті', 'аты', 'саны', 'бағасы', 'құны'])
    for x in res:
        writer.writerow([
            x.group('реті'), 
            x.group('аты'),
            float(x.group('саны').strip().replace(',','.')),
            float(x.group('бағасы').strip().replace(',','.').replace(' ','')),
            float(x.group('құны').strip().replace(',','.').replace(' ',''))
        ])