from dfd.models.entry import EntryType, DFDCharacterEntry
from jinja2 import Template
import datetime

def process_lines(lines):
    page = 1
    col = 1
    stroke = 1
    row = 1
    output = []
    for line in lines:
        line = line.strip()
        # remove comment
        percent_sign = line.find('%')
        if percent_sign != -1:
            line = line[:percent_sign].strip()
        if len(line) == 0:
            continue
        if line.startswith('+'):
            # control
            if line.startswith('+Page'):
                if line.startswith('+Page='):
                    page = int(line[len('+Page='):])
                    col=1
                    row=1
                else:
                    page += 1
                    col=1
                    row=1
            elif line.startswith('+Column'):
                if line.startswith('+Column='):
                    col = int(line[len('+Column='):])
                    row = 1
                else:
                    col+=1
                    row=1
            elif line.startswith('+Stroke'):
                if line.startswith('+Stroke='):
                    stroke = int(line[len('+Stroke='):])
            else:
                print('Unknown command', line)
        else:
            success, entry = DFDCharacterEntry.parse_line(line,page, col, row, stroke)
            if success:
                output.append(entry)
                row+=1
            else:
                print('parse line failed: ', line)
    return output

DFDCharacters = open("../DFDCharacters.txt", "r", encoding='utf8')
txt_content = DFDCharacters.readlines()
entries = process_lines(txt_content)


dict_entries = {}
dict_order = []
for r in entries:
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

