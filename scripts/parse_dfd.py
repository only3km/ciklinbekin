# -*- coding: utf-8 -*-
import re
from enum import Enum
from jinja2 import Template
import unicodedata

def r10n_to_buc(r):
    """將擬音code 轉換爲平話字"""
    initials_mapping = {'b':'b', 'p':'p', 'm':'m', 'd':'d', 't':'t', 'n':'n', 'l':'l', 'g':'g', 'k':'k', 'ng':'ng', 'h':'h', 'z':'c', 'c':'ch', 's':'s'}
    initials = initials_mapping.keys()
    finals_mapping = {
        'ung':  ['ŭng',  'ūng', 'óng',  'ók',  'ùng',  'ông',  'ŭk'],  # 春
        'ua':   ['uă',   'uā',  'uá',   'uáh', 'uà',   'uâ',   'uăh'], # 花
        'iong': ['iŏng', 'iōng','ióng', 'iók', 'iòng', 'iông', 'iŏk'], # 香 
        'iu':   ['iŭ',   'iū',  'éu',   'éuh', 'iù',   'êu',   None],  # 秋
        'ang':  ['ăng',  'āng', 'áng',  'ák',  'àng',  'âng',  'ăk'],  # 山
        'ai':   ['ăi',   'āi',  'ái',   'áih', 'ài',   'âi',   'ăih'], # 開
        'a':    ['ă',    'ā',   'á',    'áh',  'à',    'â',    'ăh'],  # 嘉 
        'ing':  ['ĭng',  'īng', 'éng',  'ék',  'ìng',  'êng',  'ĭk'],  # 賓
        'uang': ['uăng', 'uāng','uáng', 'uák', 'uàng', 'uâng', 'uăk'], # 歡
        'o' :   ['ŏ̤',    'ō̤',   'ó̤',    'ó̤h',  'ò̤',    'ô̤',    'ŏ̤h'],  # 歌
        'y':    ['ṳ̆',    'ṳ̄',   'é̤ṳ',   'é̤ṳh', 'ṳ̀',    'ê̤ṳ',   'ṳ̆h'],  # 須
        'uoi':  ['uŏi',  'uōi', 'uói',  'uóih','uòi',  'uôi',  None],  # 杯
        'u':    ['ŭ',    'ū',   'ó',    'óh',  'ù',    'ô',    'ŭh'],  # 孤
        'eng':  ['ĕng',  'ēng', 'áing', 'áik', 'èng',  'âing', 'ĕk'],  # 燈
        'uong': ['uŏng', 'uōng','uóng', 'uók', 'uòng', 'uông', 'uŏk'], # 光
        'ui':   ['ŭi',   'ūi',  'ói',   'óih', 'ùi',   'ôi',   'ŭih'], # 輝
        'ieu':  ['iĕu',  'iēu', 'iéu',  'iéuh','ièu',  'iêu',  None],  # 燒
        'yng':  ['ṳ̆ng',  'ṳ̄ng', 'é̤ṳng', 'é̤ṳk', 'ṳ̀ng',  'ê̤ṳng', 'ṳ̆k'],  # 銀
        'ong':  ['ŏng',  'ōng', 'áung', 'áuk', 'òng',  'âung', 'ŏk'],  # 缸
        'i':    ['ĭ',    'ī',   'é',    'éh',  'ì',    'ê',    'ĭh'],  # 之
        'oeng': ['ĕ̤ng',  'ē̤ng', 'áe̤ng', 'áe̤k', 'è̤ng',  'âe̤ng', 'ĕ̤k'],  # 東
        'au':   ['ău',   'āu',  'áu',   'áuh' ,'àu',   'âu',   'ăuh'], # 郊
        'uo':   ['uŏ',   'uō',  'uó',   'uóh', 'uò',   'uô',   'uŏh'], # 過
        'e':    ['ă̤',    'ā̤',   'á̤',    'á̤h',  'à̤',    'â̤',    'ă̤h'],  # 西
        'io':   ['iŏ',   'iō',  'ió',   'ióh', 'iò',   'iô',   'iŏh'], # 橋
        'ie':   ['iĕ',   'iē',  'ié',   'iéh', 'iè',   'iê',   'iĕh'], # 鷄
        'iang': ['iăng', 'iāng','iáng', 'iák', 'iàng', 'iâng', 'iăk'], # 聲
        'oi':   ['ŏi',   'ōi',  'ó̤i',   'ó̤ih', 'òi',   'ô̤i',   'ŏih'], # 催
        'oe':   ['ĕ̤',    'ē̤',   'áe̤',   'áe̤h', 'è̤',    'âe̤',   'ĕ̤h'],  # 初
        'ieng': ['iĕng', 'iēng','iéng', 'iék', 'ièng', 'iêng', 'iĕk'], # 天
        'ia':   ['iă',   'iā',  'iá',   'iáh', 'ià',   'iâ',   'iăh'], # 奇
        'uai':  ['uăi',  'uāi', 'uái',  'uáih','uài',  'uâi',  'uăih'],# 歪  
        'eu':   ['ĕu',   'ēu',  'áiu',  'áiuh','èu',   'âiu',  'ĕuh']  # 溝  
    }
    finals = finals_mapping.keys()
    tone_mappings = [1,2,3,4,5,2,6,7]

    if (r == ' '):
        return ' '

    def convert_once(r):
        if (r =='ng'):
            return 'ng'
        result = ''
        # Get the initial
        found_initial = False
        for i in initials:
            if r.startswith(i):
                result += initials_mapping[i]
                r = r[len(i):]

        # Get the tone
        try:
            tone = int(r[-1])
            r = r[:-1]
        except:
            raise ValueError("Malformed r18n: " + r)
        # Get the rime
        if r.endswith('k'):
            r = r[:-1] + 'ng'
        elif r.endswith('h'):
            r = r[:-1]
        result += finals_mapping[r][tone_mappings[tone-1]-1]
        return result
    result = []
    for x in r.split(' '):
        result.append(convert_once(x))
    return "-".join(result)

class Syllable():
    def __init__(self, r10n, r10n_corrected = ''):
        self.r10n = r10n
        self.r10n_corrected = r10n_corrected
        self.buc = r10n_to_buc(r10n)
        self.buc_corrected = r10n_to_buc(r10n_corrected) if r10n_corrected != '' else ''

    def __str__(self):
        if (self.buc_corrected == ''):
            return self.buc
        else:
            return "<s>%s</s> %s" % (self.buc, self.buc_corrected)


class EntryType(Enum):
    RADICAL = 1
    RADICAL_STROKE_NUMBER = 2
    RADICAL_NUMBER = 3
    NORMAL_CHARACTER = 4

class DFDEntry():
    def get_str_type(self):
        return str(self.type)

    str_type = property(get_str_type, None)

class DFDStrokeNumber(DFDEntry):
    def __init__(self):
        self.type = EntryType.RADICAL_STROKE_NUMBER

class DFDRadicalNumber(DFDEntry):
    def __init__(self):
        self.type = EntryType.RADICAL_NUMBER

class DFDCharacterEntry(DFDEntry):

    def __init__(self):
        self.type = EntryType.NORMAL_CHARACTER
        self.characters = []
        self.character_types = []
        self.characters_corrected = []
        self.buc = []
        self.buc_corrected = []
        self.r10n = []
        self.r10n_corrected = []

    def __is_ids(self,c):
        for x in c:
            if '\u2ff0' <= x <='\u2ffb':
                return True
        return False

    def add_char(self,c, c_corrected = ''):
        if (c not in self.characters):
            self.characters.append(c)
            self.character_types.append(self.__is_ids(c))
            self.characters_corrected.append(c_corrected)

    def add_r10n(self,r,r_corrected=''):
        if (r not in self.r10n)  and (r not in self.r10n_corrected) :
            self.r10n.append(r)
            self.r10n_corrected.append(r_corrected)
            self.buc.append(r10n_to_buc(r))
            self.buc_corrected.append(r10n_to_buc(r_corrected) if r_corrected != '' else '')

    def spit_rime(self):
        result = []
        for i, c in enumerate(self.characters):
            if self.character_types[i] == False:
                for j, p in enumerate(self.r10n):
                    result.append(c+"\t"+(p if self.r10n_corrected[j] =='' else self.r10n_corrected[j]))
        return result

    def spit_html(self):
        buc = ""
        char = ""
        for i, c in enumerate(self.characters):
            if self.character_types[i] == True:
                char += '<code>%s</code>' % c
            else:
                if (self.characters_corrected[i]!=''):
                    char += '<s>%s</s>%s' % (c, self.characters_corrected[i])
                else:
                    char += c
        tmp = [] 
        for i, p in enumerate(self.buc):
            if self.buc_corrected[i] != "":
                if (self.buc_corrected[i] == ' '):
                    tmp.append("<s>%s</s>" % p)
                else:
                    tmp.append("<s>%s</s> %s" % (p,self.buc_corrected[i]))
            else:
                tmp.append(p)
        buc = ", ".join(tmp)
        return (char, buc)
    
    def get_html_char(self):
        return self.spit_html()[0]
    
    def get_html_buc(self):
        return unicodedata.normalize('NFKD',self.spit_html()[1])

    html_char = property(get_html_char, None)
    html_buc = property(get_html_buc, None)

class DFDRadicalEntry(DFDCharacterEntry):
    def __init__(self):
        super().__init__()
        self.type = EntryType.RADICAL
        self.radical_name_chi = ''
        self.radical_name_buc = ''
    
    def add_radical_name(self, chi, buc, uoio = False):
        self.radical_name_chi = chi
        if uoio:
            self.radical_name_buc = [(Syllable(b.replace('uo','io'),b) if b.replace('uo','io')!=b else Syllable(b) )for b in buc.split(' ')]
        else:    
            self.radical_name_buc = [Syllable(b) for b in buc.split(' ')]


    def get_html_buc_radical(self):
        return unicodedata.normalize('NFKD',self.spit_html()[1] + (' (%s)'%'-'.join([str(b) for b in self.radical_name_buc]) if len(self.radical_name_buc)>0 else ''))

    html_buc_radical = property(get_html_buc_radical, None)

def process_lines(lines, radical_mode = False):
    reMDCross1 = r'^.*~~([a-z0-9]+)~~.*$'
    reMDCross1_hanzi = r'^.*~~([^a-z0-9~]+)~~.*$'
    entries = []
    lastChar = None
    current_entry = None

    def commit():
        nonlocal entries, lastChar, current_entry
        if (current_entry!=None):
            entries.append(current_entry)
            current_entry = None
            lastChar = None

    for line in lines:
        line = line.strip()
        segments = line.split('\t')
        is_uoioerror = '漳泉亂' in line
        if re.compile(reMDCross1).match(line) != None:
            corrected_r10n = re.compile(reMDCross1).match(line).group(1)
        else:
            corrected_r10n = None

        if re.compile(reMDCross1_hanzi).match(line) != None:
            corrected_char = re.compile(reMDCross1_hanzi).match(line).group(1)
        else:
            corrected_char = None
        if (len(line) > 0):
            #print(line)
            if (not line.startswith('#')):
                char = segments[0]
                syllable = segments[1]
                if (not radical_mode):
                    # 是有字符行 (NORMAL_CHARACTER)
                    if ((lastChar == None or char != lastChar) and ('=v' not in line)):
                        # 同前一行不同
                        commit()
                        current_entry = DFDCharacterEntry()
                    else:
                        # 同前一行是同一個條目
                        pass
                    current_entry.add_char(char)
                    if (is_uoioerror):
                        if 'uo' in syllable:
                            current_entry.add_r10n(syllable.replace('uo','io'), syllable)
                        else:
                            current_entry.add_r10n(syllable, ' ')  
                    elif (corrected_r10n != None):
                        current_entry.add_r10n(corrected_r10n, syllable)
                    else:
                        current_entry.add_r10n(syllable)
                else:
                    # RADICAL
                    if (lastChar == None or char != lastChar) \
                        and ('=v' not in line) \
                        and (not len(char)>1):
                        # RADICAL
                        commit()
                        current_entry = DFDRadicalEntry()
                        if (corrected_char == None):
                            current_entry.add_char(char)
                        else:
                            current_entry.add_char(corrected_char,char)
                        if (is_uoioerror):
                            if 'uo' in syllable:
                                current_entry.add_r10n(syllable.replace('uo','io'), syllable)
                        elif (corrected_r10n != None):
                            current_entry.add_r10n(corrected_r10n, syllable)
                        else:
                            current_entry.add_r10n(syllable)
                    elif (len(char)>1):
                        current_entry.add_radical_name(char, syllable, is_uoioerror)
                    else:
                        if (corrected_char == None):
                            current_entry.add_char(char)
                        else:
                            current_entry.add_char(corrected_char,char)
                    
                        if (is_uoioerror):
                            if 'uo' in syllable:
                                current_entry.add_r10n(syllable.replace('uo','io'), syllable)
                        elif (corrected_r10n != None):
                            current_entry.add_r10n(corrected_r10n, syllable)
                        else:
                            current_entry.add_r10n(syllable)
                lastChar = char
            elif re.compile(r'^### (\d+) ###$').match(line) != None:
                radical_num = re.compile(r'^### (\d+) ###$').match(line).group(1)
                commit()
                current_entry = DFDRadicalNumber()
                current_entry.number = radical_num
                commit()
            elif  re.compile(r'^### (\d+) STROKES? ###$').match(line) != None:
                stroke_num = re.compile(r'^### (\d+) STROKES? ###$').match(line).group(1)
                commit()
                current_entry = DFDStrokeNumber()
                current_entry.number = int(stroke_num)
                commit()
    
    commit()
    return entries
    
tsv_file = open("../DFD.tsv", "r", encoding='utf8')
tsv_content = tsv_file.readlines()
entries = process_lines(tsv_content[306:])
radicals = process_lines(tsv_content[:305],True)

f = open('./template/dfd.html.jinja2','r',encoding='utf-8')

t = Template(f.read())

output = t.render(chars = entries, radicals = radicals)

f2 = open('../DFD.html',"w", encoding='utf8')

f2.write(output)
f2.close()