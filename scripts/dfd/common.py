# -*- coding: utf-8 -*-
import re
from jinja2 import Template
import unicodedata
import datetime

ranges = [
  {"from": ord(u"\u3300"), "to": ord(u"\u33ff")},         # compatibility ideographs
  {"from": ord(u"\ufe30"), "to": ord(u"\ufe4f")},         # compatibility ideographs
  {"from": ord(u"\uf900"), "to": ord(u"\ufaff")},         # compatibility ideographs
  {"from": ord(u"\U0002F800"), "to": ord(u"\U0002fa1f")}, # compatibility ideographs
  {"from": ord(u"\u30a0"), "to": ord(u"\u30ff")},         # Japanese Kana
  {"from": ord(u"\u3000"), "to": ord(u"\u303f")},         # puntuations
  {"from": ord(u"\u2e80"), "to": ord(u"\u2eff")},         # cjk radicals supplement
  {"from": ord(u"\u4e00"), "to": ord(u"\u9fff")},
  {"from": ord(u"\u3400"), "to": ord(u"\u4dbf")},
  {"from": ord(u"\U00020000"), "to": ord(u"\U0002a6df")},
  {"from": ord(u"\U0002a700"), "to": ord(u"\U0002b73f")},
  {"from": ord(u"\U0002b740"), "to": ord(u"\U0002b81f")},
  {"from": ord(u"\U0002b820"), "to": ord(u"\U0002ceaf")}  # included as of Unicode 8.0
]

def is_cjk(char):
  return any([range["from"] <= ord(char) <= range["to"] for range in ranges])

def is_ids(c):
    for x in c:
        if '\u2ff0' <= x <='\u2ffb':
            return True
    return False

def is_r10n(s):
    if (len(s)==0):
        return False
    for x in s:
        if not ('a'<=x<='z' or '0'<=x<='z'):
            return False
    return True

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


def denormalise_buc(s):
    return unicodedata.normalize('NFKD',s)

