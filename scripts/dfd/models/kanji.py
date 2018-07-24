from .character import Character

class Kanji():
    """漢字，可以被刪除或更正
    """

    def __init__(self, c, c_corrected = None, is_deleted = False):
        """
        Arguments:
            c {Character} -- 原本的漢字
        
        Keyword Arguments:
            c_corrected {Character} -- 更正的漢字 (default: {None})
            is_deleted {bool} -- 是否刪去 (default: {False})
        """

        self.char = c
        self.char_corrected = c_corrected
        self.is_deleted = is_deleted
        if is_deleted and (c_corrected is not None):
            raise Exception('刪除的漢字不能有更正')

    def get_corrected(self):
        """得到正確的漢字
        """
        if self.char_corrected != None:
            return self.char_corrected
        else:
            return self.char

    def is_corrected_ids(self):
        return self.get_corrected().is_ids

    def get_original(self):
        return self.char
    
    def is_original_ids(self):
        return self.get_original().is_ids

    def __str__(self):
        return self.get_corrected()

    def has_correction(self):
        return self.char_corrected is not None

    def _render_html(self, c: Character):
        if (c.is_ids):
            return '<code>%s</code>' % c.ids
        else:
            return c.char

    def render_corrected(self):
        return self._render_html(self.get_corrected())
    
    def render_original(self):
        return self._render_html(self.get_original())

    def render_all(self):
        if (self.has_correction()):
            return "<s>%s</s>%s" % (self.render_original(), self.render_corrected())
        elif self.is_deleted:
            return '<s>%s</s>' % self.render_original()
        else:
            return self.render_corrected()

    @classmethod
    def try_parse(cls, s):
        #漢字	= 字符 | "~~" , 字符 , "~~" | "~~" , 字符 , "," , 字符 , "~~"
        if s.startswith('~~') and s.endswith('~~'):
            # try different , locations
            i = s.find(',')
            while i != -1 and i < len(s):
                old_char = s[2:i]
                new_char = s[i+1:-2]
                success1, old_character = Character.try_parse(old_char)
                success2, new_character = Character.try_parse(new_char)
                if (success1 and success2):
                    return True, cls(old_character, new_character)
                s.find(',',i+1)
            # try deleted
            success, deleted_character = Character.try_parse(s[2:-2])
            if success:
                return True, cls(deleted_character, is_deleted = True)
            else:
                return False, None
        else:
            is_success, char = Character.try_parse(s)
            if (is_success):
                return True, cls(char)
            else:
                return False, None
