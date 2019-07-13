from dfd.parser import process_dfd_characters, process_dfd_radicals
from dfd.models.entry import EntryType, DFDStrokeNumber, DFDRadicalNumber
from jinja2 import Template

DFDCharacters = open("../DFDCharacters.txt", "r", encoding='utf8').readlines()
DFDRadicals = open("../DFDRadicals.txt", "r", encoding='utf8').readlines()

entries = process_dfd_characters(DFDCharacters)
radicals = process_dfd_radicals(DFDRadicals)

entries_new = []
for i in range(len(entries)):
    if i ==0 or entries[i].stroke_no != entries[i-1].stroke_no:
        entries_new.append(DFDRadicalNumber(entries[i].stroke_no))
    entries_new.append(entries[i])

radicals_new = []
for i in range(len(radicals)):
    if i ==0 or radicals[i].stroke_no != radicals[i-1].stroke_no:
        radicals_new.append(DFDStrokeNumber(radicals[i].stroke_no))
    radicals_new.append(radicals[i])

# DFD.html
f = open('./template/dfd.html.jinja2','r',encoding='utf-8')
t = Template(f.read())
f.close()
output = t.render(chars = entries_new, radicals = radicals_new)
f2 = open('../build/DFD.html',"w", encoding='utf8')
f2.write(output)
f2.close()
