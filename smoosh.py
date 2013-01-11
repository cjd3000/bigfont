from base import BaseObject

class Smoosher(BaseObject):
    """Uses various rules to combine characters into a single character."""
    def __init__(self,
                 universal=False,
                 equal_char=False,
                 underscore=False,
                 hierarchy=False,
                 opposite_pair=False,
                 big_x=False,
                 hardblank=False,
                 vertical_equal_char=False,
                 vertical_underscore=False,
                 vertical_hierarchy=False,
                 horizontal_line=False,
                 vertical_line=False,
                 **kwargs):
        super(Smoosher,self).__init__(**kwargs)
        self.universal=universal
        self.equal_char=equal_char
        self.underscore=underscore
        self.hierarchy=hierarchy
        self.opposite_pair=opposite_pair
        self.big_x=big_x
        self.hardblank=hardblank
        self.vertical_equal_char=equal_char
        self.vertical_underscore=underscore
        self.vertical_hierarchy=hierarchy
        self.horizontal_line=horizontal_line
        self.vertical_line=vertical_line

    def smoosh(a,b):
        """Smoosh single characters according to smooshing rules."""
        if a == ' ':
            return b
        if self.universal or b == ' ' or a == b:
            return a
        return '?'
