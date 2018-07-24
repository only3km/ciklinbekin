from ..common import is_r10n, r10n_to_buc

class Syllable():
    def __init__(self, r10n, r10n_corrected = None, is_deleted= False):
        self.r10n = r10n
        self.r10n_corrected = r10n_corrected
        self.is_deleted = is_deleted
        self.buc = r10n_to_buc(r10n)
        self.buc_corrected = r10n_to_buc(r10n_corrected) if r10n_corrected is not None else ''

    def __str__(self):
        if (self.buc_corrected == ''):
            return self.buc
        elif (self.r10n_corrected == ' '):
            return "<s>%s</s>" % self.buc
        else:
            return "<s>%s</s> %s" % (self.buc, self.buc_corrected)

    def get_buc_corrected(self):
        if (self.buc_corrected != ''):
            return self.buc_corrected
        else:
            return self.buc

    def get_buc_original(self):
        return self.buc
    
    @classmethod
    def try_parse(cls, s):
        if s.startswith('~~') and s.endswith('~~'):
            # try , locations
            i = s.find(',')
            while i!=-1 and i < len(s):
                old = s[2:i]
                new = s[i+1:-2]
                if (is_r10n(old) and is_r10n(new)):
                    return True, cls(old, new)
                i = s.find(',', i+1)
            
            if (is_r10n(s[2:-2])):
                return True, cls(s[2:-2], is_deleted= True)
            return False, None
        else:
            if is_r10n(s):
                return True, cls(s)
            else:
                return False, None
