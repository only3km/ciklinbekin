# Python 3
# coding=utf-8
# 戚林八音字表

import re
import csv

reMDHasSimilarCode1 = r'`([^`]*:[^`]*)`'
reMDHasSimilarCode2 = r'`([^`]*:[^`]*)`'
reMDHasSimilarCodeHTML = r'<!--code>\1</code-->'
reMDCode = r'`([^`]*)`'
reMDCodeHTML = r'<code>\1</code>'
reMDA = r'\[([^\[\]\(\)]*)\]\(([^\[\]\(\)]*)\)'
reMDAHTML = r'<a href="\2">\1</a>'
reMDCross = r'~~([^~]*)~~'
reMDCrossHTML = r'<s>\1</s>'

import time

infile = open("../convert.tsv", "r")

yamls = ['# Rime dictionary', '# encoding: utf-8', '# 戚林八音校注 2001', '', '---', 'name: ciklinbekin', 'version: '+time.asctime( time.localtime(time.time()) ), 'use_preset_vocabulary: true', '...', '', '# 使 融•嵐 不變韻地區讀音 標記韻母', '# 聲母']

romanConsonants = []
hanConsonants = []
romanVowels = []
hanVowels = []
corv = -1

# Character to Romanization mappings
convert = {}
with open('../convert.tsv') as tsvfile:
  reader = csv.reader(tsvfile, delimiter='\t')
  for row in reader:
    convert[row[0]] = row[1]

yamls.append('')

infile = open("../CikLinBekIn.md", "r")

chars = []
char2Sound = {}
linesWOTone = []

isListing = False
htmls = ['<!doctype html>', '<html>', '<head>', '<meta charset="utf-8">', '<meta name="viewport" content="width=device-width, initial-scale=1">', '<title>戚林八音字表</title>', '<link rel="icon" href="img/icon.png" type="image/png">', '<link rel="stylesheet" href="css/ciklinbekin.css">', '<link rel="stylesheet" href="css/Hei.css">','</head>', '<body>']

vowel = vstop = consonant = tone = syllable = ''
isDesc = isSimilar = False
group = []

for line in infile.readlines():
	# for Typora auto generation \u200b
	line = re.sub( r'[\n\r\u200B]', '', line )
	if len(line) > 0:
		if line.startswith('###'):
			### 声母
			consonant = line[3]
			consonant = convert[consonant]
			# h3
			htmls.append('<h3><a name="'+ consonant+vowel +'"></a>'+line[3:]+'</h3>')
		elif line.startswith('##'):
			if len(line) == 2:
				break
			## 韵母
			vowel = line[2:]
			vowel = convert[vowel]
			if vowel.endswith('ng'):
				vstop = vowel.replace('ng', 'k')
			else:
				vstop = vowel + 'h'
			# h2
			htmls.append('<h2><a name="'+ vowel +'"></a>'+line[2:]+'</h2>')
		elif line[0] in '12345678' and len(line) > 2:
			# 調
			tone = line[0]
			# 字條
			string = line[3:]
			# ol li
			if tone == '1':
				htmls.append('<ol>')
			string2html = re.sub( reMDHasSimilarCode1, reMDHasSimilarCodeHTML, string )
			string2html = re.sub( reMDHasSimilarCode2, reMDHasSimilarCodeHTML, string2html )
			string2html = re.sub( reMDCross, reMDCrossHTML, string2html )
			string2html = re.sub( reMDCode, reMDCodeHTML, string2html )
			htmls.append('<li>'+string2html+'</li>')
			if tone == '8':
				htmls.append('</ol>')
			# check Tone 6
			if tone == '6':
				if len(string) > 0:
					print('⚠️', consonant, vowel, '6️⃣', string)
			#
			string = re.sub( reMDCross, ' ', string )
			string = re.sub( reMDCode, '', string )
			string = re.sub( r'[\? ]', '', string)
			for c in string:
				# 收
				if tone in '48':
					syllable = consonant + vstop + tone
				else:
					syllable = consonant + vowel + tone
				l = c + '\t' + syllable
				if l not in yamls:
					yamls.append(l)
					if l[:len(l)-1] not in linesWOTone:
						linesWOTone.append(l[:len(l)-1])
				else:
					print(l, ' is already recorded!')
				if c not in chars:
					chars.append(c)
					char2Sound[c] = []
				char2Sound[c].append(syllable)
				if c < '\U0002F800':
					if c > '\uF900' and c < '\uFAFF' and c not in ['\uFA11', '\uFA13', '\uFA14', '\uFA0E', '\uFA0F', '\uFA1F', '\uFA21', '\uFA23', '\uFA24', '\uFA27', '\uFA28', '\uFA29']:
						print(c, 'CJK Compatibility Ideographs')
				elif c < '\U0002FA1F':
					print(c, 'CJK Compatibility Ideographs Supplement')
				# if c not in sharedHans:
				# 	noneSharedHans.append(c)
					#print(c, 'not supported')
		elif line.startswith('#'):
			# h1
			htmls.append('<h1><a name="top"></a>'+line[1:]+'</h1>')
		elif line.startswith('- '):
			# ul li
			if not isListing:
				isListing = True
				htmls.append('<ul>')
			string = line[2:]
			string2html = re.sub( reMDCross, reMDCrossHTML, string )
			string2html = re.sub(reMDCode, reMDCodeHTML, string)
			string2html = re.sub(reMDA, reMDAHTML, string2html)
			htmls.append('<li>'+string2html+'</li>')
	elif isListing:
		isListing = False
		htmls.append('</ul>')

htmls.append('</body>')
htmls.append('</html>')

outfile = open("../build/CikLinBekIn.html", "w")
outfile.write('\n'.join(htmls))
outfile.close()

#outfile = open("ciklinbekin.dict.yaml", "w")
#outfile.write('\n'.join(yamls))
#outfile.close()

i = 0
basic = 0
for c in chars:
	i = i + len(char2Sound[c])
	if c <= '\uffff':
		basic = basic + 1
print(len(chars), 'Characters')
print(basic, 'Basic Characters')
print(i, 'Records')
