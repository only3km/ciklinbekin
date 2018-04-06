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

# DFDRadicals.txt

with open('../DFDRadicals.txt', 'w', encoding='utf8') as outfile:
    count = 0
    for row in radicals:
        if (row.type == EntryType.RADICAL_STROKE_NUMBER):
            outfile.write('+Stroke='+str(row.number)+'\n')
        elif (row.type == EntryType.RADICAL):
            outfile.write((','.join([c.render_new_format() for c in row.characters])+'\t' \
                         +','.join([b.get_new_format() for b in row.r10n])+'\t\t' \
                         +row.radical_name_chi+'\t' \
                         +'-'.join([b.get_new_format() for b in row.radical_name_buc])).strip()+'\n')
