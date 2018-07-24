from ..common import is_cjk, is_ids

class Character():
    """代表一個字符
    """

    def __init__(self, c, sub=None):
        """        
        Arguments:
            c {str} -- 此字符（可以是IDS）
            sub {str} -- 替代字符
        """
        if (is_ids(c)):
            self.ids = c
            if (sub is not None):
                self.char = sub
            self.is_ids = True
        else:
            self.char = c
            if sub is not None:
                raise Exception("非IDS不可有替代字符")
            self.is_ids = False

    @classmethod
    def try_parse(cls, s):
        """字符	= 單個Unicode字符 | "{" , IDS , "," , 替代Unicode字符 , "}" | "{" , IDS , "}" 
        """

        if len(s) == 1:
            if is_cjk(s):
                return True, cls(s)
            else:
                return False, None
        else:
            if s.startswith('{') and s.endswith('}'):
                tokens = s[1:-1].split(',')
                if len(tokens) == 1 and is_ids(tokens[0].strip()):
                    return True, cls(tokens[0].strip())
                elif len(tokens) == 2 and is_ids(tokens[0].strip()) and is_cjk(tokens[1].strip()):
                    return True, cls(tokens[0].strip(), tokens[1].strip())
                else:
                    return False, None
            else:
                return False, None
