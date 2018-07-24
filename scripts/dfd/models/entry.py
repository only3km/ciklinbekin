from .kanji import Kanji
from .syllable import Syllable
from enum import Enum


class EntryType(Enum):
    RADICAL = 1
    NORMAL_CHARACTER = 4

class DFDEntry():
    pass

class DFDCharacterEntry(DFDEntry):
    """正常條目
    """

    def __init__(self, chars, r10ns, page_no=0, col_no=0, row_no=0, stroke_no=0):
        self.type = EntryType.NORMAL_CHARACTER
        self.characters = chars
        self.r10n = r10ns
        self.page_no = page_no
        self.col_no = col_no
        self.row_no = row_no
        self.stroke_no =stroke_no

    def spit_rime(self):
        """[summary]
        """

        result = []
        for i, c in enumerate(self.characters):
            if c.is_corrected_ids() == False:
                for j, p in enumerate(self.r10n):
                    result.append((c.get_corrected().char, (p.r10n if p.r10n_corrected is None else p.r10n_corrected)))
        return result

    def spit_html(self):
        buc = ""
        char = ""
        for i, c in enumerate(self.characters):
            char += c.render_all()
        tmp = [] 
        for i, p in enumerate(self.r10n):
            tmp.append(str(p))
        buc = ", ".join(tmp)
        return (char, buc)
    
    def get_html_char(self):
        return self.spit_html()[0]
    
    def get_html_buc(self):
        return denormalise_buc(self.spit_html()[1])

    html_char = property(get_html_char, None)
    html_buc = property(get_html_buc, None)

    @classmethod
    def parse_line(cls,s,page_no, col_no, row_no,stroke_no):
        #條目	= 漢字列表 , "\t" , 讀音列表
        tokens = s.strip().split('\t')
        if (len(tokens)!=2):
            return False, None
        chars_str = tokens[0].strip()
        r10n_str = tokens[1].strip()
        chars_list = []
        r10n_list = []

        while len(chars_str) > 0:
            #print(chars_str)
            i = chars_str.find(',')
            while i<len(chars_str) and i!=-1:
                tmp_str = chars_str[:i]
                success, kanji = Kanji.try_parse(tmp_str)
                if success:
                    chars_list.append(kanji)
                    chars_str = chars_str[len(tmp_str)+1:]
                    break
                else:
                    i = chars_str.find(',',i+1)
            success, kanji = Kanji.try_parse(chars_str)
            if success:
                chars_list.append(kanji)
                chars_str = ''
        assert chars_str == ''

        while len(r10n_str) > 0:
            #print(r10n_str)
            i = r10n_str.find(',')
            while i<len(r10n_str) and i!=-1:
                tmp_str = r10n_str[:i]
                success, syll = Syllable.try_parse(tmp_str)
                if success:
                    r10n_list.append(syll)
                    r10n_str = r10n_str[len(tmp_str)+1:]
                    break
                else:
                    i = r10n_str.find(',',i+1)
                    
            success, syll = Syllable.try_parse(r10n_str)
            if success:
                r10n_list.append(syll)
                r10n_str = ''
        assert r10n_str == ''

        return True, cls(chars_list, r10n_list, page_no, col_no,row_no,stroke_no)

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
        return denormalise_buc(self.spit_html()[1] + (' (%s)'%'-'.join([str(b) for b in self.radical_name_buc]) if len(self.radical_name_buc)>0 else ''))

    html_buc_radical = property(get_html_buc_radical, None)

