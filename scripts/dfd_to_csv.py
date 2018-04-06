from dfd_common import process_lines, EntryType
from jinja2 import Template

tsv_file = open("../DFD.tsv", "r", encoding='utf8')
tsv_content = tsv_file.readlines()
entries = process_lines(tsv_content[306:])
radicals = process_lines(tsv_content[:305],True)
dict_entries = {}
dict_order = []
for r in radicals + entries:
    if (r.type in [EntryType.RADICAL, EntryType.NORMAL_CHARACTER]):
        for x in r.spit_rime():
            if (x[0] not in dict_entries):
                dict_order.append(x[0])
                dict_entries[x[0]] = []
            if (x[1] not in dict_entries[x[0]]):
                dict_entries[x[0]].append(x[1])

# DFD.characters.csv
import csv
with open('../output.csv', 'w', newline='', encoding='utf8') as csvfile:
    writer = csv.writer(csvfile, dialect='excel')
    writer.writerow(["#","漢字","羅馬字","漢字更正","羅馬字更正","註釋"])
    count = 0
    for i in range(0, len(entries)):
        if (entries[i].type == EntryType.NORMAL_CHARACTER):
            writer.writerow([i, ','.join([c.get_original() for c in entries[i].characters]), ','.join(entries[i].buc),'','',''])
