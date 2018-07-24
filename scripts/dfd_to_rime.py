from jinja2 import Template
import datetime
from dfd.parser import process_dfd_characters, process_dfd_radicals


DFDCharacters = open("../DFDCharacters.txt", "r", encoding='utf8').readlines()
DFDRadicals = open("../DFDRadicals.txt", "r", encoding='utf8').readlines()

entries = process_dfd_characters(DFDCharacters)
radicals = process_dfd_radicals(DFDRadicals)

dict_entries = {}
dict_order = []
for r in radicals + entries:
    for x in r.spit_rime():
        if (x[0] not in dict_entries):
            dict_order.append(x[0])
            dict_entries[x[0]] = []
        if (x[1] not in dict_entries[x[0]]):
            dict_entries[x[0]].append(x[1])

rime_entries = []
for c in dict_order:
    for p in dict_entries[c]:
        rime_entries.append(c+"\t"+p)

# dfd.dict.yaml
f = open('./template/dfd.dict.jinja2','r',encoding='utf-8')
t = Template(f.read())
f.close()
output = t.render(entries = rime_entries, datetime=datetime.datetime.now().strftime('%a %b %d %H:%M:%S %Y'))
f2 = open('../Rime schema/dfd.dict.yaml',"w", encoding='utf8')
f2.write(output)
f2.close()

