# 将八音字表转为一行一字的csv以及rime dict

from jinja2 import Template
import datetime

outputs = []

def is_ids(c):
    for x in c:
        if '\u2ff0' <= x <='\u2ffb':
            return True
    return False

def outputChar(s,initial,final,tone):
    #print(s,' ',initial,' ',final, ' ',tone)
    #字形 #等價 #異形 #initial #final #tone #shown
    outputs.append([s,'','',initial,final,tone, True])

with open('../CikLinBekIn.md','r',encoding="utf8") as f:
    lines = f.readlines()
    lines = lines[7:] # 忽略首 6 行
    final = ''
    initial = ''
    tone = ''
    for i in range(0,len(lines)):
        currentLine = lines[i].strip()
        
        if (len(currentLine)==0):
            continue
        if (currentLine.find("##")!=-1 and (currentLine.find('###')==-1)):
            # e.g. ##春公
            final = currentLine[2:]
        elif (currentLine.find("###")!=-1):
            # e.g. ###柳
            initial = currentLine[3:]
        elif (currentLine[0] in ['0','1','2','3','4','5','6','7','8','9']):
            tone = currentLine[0]
            inQuote = False
            quoteString = ''
            for j in range(0,len(currentLine)):
                if inQuote:
                    if currentLine[j]=='`':
                        inQuote = False
                        outputChar(quoteString,initial,final,tone)
                        quoteString = ''
                    else:
                        quoteString = quoteString + currentLine[j]
                else:
                    if currentLine[j] in ['0','1','2','3','4','5','6','7','8','9','.',' ']:
                        continue
                    elif currentLine[j]=='`':
                        inQuote = True
                    else:
                        outputChar(currentLine[j],initial,final,tone)



for i in range(0,len(outputs)):
    if outputs[i][-1] == False:
        continue
    if outputs[i][0][0]==':':
        #觱`:⿵咸角`
        outputs[i-1][-1] = False
        outputs[i][0] = outputs[i][0][1:] #去掉冒號
        outputs[i][1] = outputs[i-1][0] #將冒號前字設爲IDS的等價
    elif outputs[i][0][-1]==':':
        #`⿰⿱亠䜌欠:`㱍
        outputs[i+1][-1] = False
        outputs[i][0] = outputs[i][0][:-1] #去掉冒號
        outputs[i][2] = outputs[i+1][0] #將冒號後字設爲IDS的異形
    elif len(outputs[i][0])>1 and outputs[i][0][1]==':':
        # `牆:⿰爿夾⿱回`
        splits = outputs[i][0].split(':')
        outputs[i][0] = splits[1] #將IDS設爲本字
        outputs[i][1] = splits[0] #將引號內冒號前的字設爲IDS的等價

            
import csv
with open('../build/CikLinBekIn.csv', 'w',newline='',encoding='utf8') as csvfile:
    writer = csv.writer(csvfile, dialect='excel')
    writer.writerow(["#","漢字","等價","異形","聲母","韻母","調"])
    count = 0
    for i in range(0,len(outputs)):
        if (outputs[i][-1] == True):
            count = count +1
            writer.writerow([count]+outputs[i][:-1])

# ciklinbekin.dict.yaml
f = open('./template/ciklinbekin.dict.jinja2','r',encoding='utf-8')
t = Template(f.read())
f.close()
# Character to Romanization mappings
convert = {}
with open('../convert.tsv') as tsvfile:
  reader = csv.reader(tsvfile, delimiter='\t')
  for row in reader:
    convert[row[0]] = row[1]
dict_entries = []
for x in outputs:
    if (is_ids(x[0])):
        continue
    initial = convert[x[3][0]]
    tone = x[5]
    final = (convert[x[4]].replace('ng','k') if ("ng" in convert[x[4]]) else convert[x[4]]+'h') if tone in ['4','8'] else convert[x[4]]
    dict_entries.append(x[0] + "\t" + initial+final+tone)
output = t.render(entries = dict_entries, datetime=datetime.datetime.now().strftime('%a %b %d %H:%M:%S %Y'))
f2 = open('../build/Rime schema/ciklinbekin.dict.yaml',"w", encoding='utf8')
f2.write(output)
f2.close()
