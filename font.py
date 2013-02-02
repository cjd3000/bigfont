from __future__ import print_function
from __future__ import division

import copy
import functools
import os
import re
import logging
import base
import operator
import pickle
import inspect

from zipfile import ZipFile, BadZipfile # or BadZipFile in 3.x
from base import BaseObject
from letter import BigLetter
from decorators import trace

def bigprint(text,font=None):
    """Print text in big font.

    Uses given BigFont if specified, otherwise a default font."""
    print(render(text,font))

_default_font = 'standard.flf'
def render(text,font=None):
    """Render text in big font and return as a string.

    Uses given BigFont if specified, otherwise a default font."""
    if font is None:
        if not _builtin_fonts.has_key(_default_font):
            _get_builtins()
            font = _builtin_fonts[_default_font]

    return font.render(text)

_builtin_fonts = {}
def _get_builtins():
    """Retrieve any fonts from bigfont/fonts."""
    global _builtin_fonts
    mypath = os.path.dirname(inspect.getfile(inspect.currentframe()))
    fontpath = os.path.join(mypath,'fonts')
    logging.info("importing all fonts from %s" % fontpath)
    for fn in os.listdir(fontpath):
        try:
            _builtin_fonts[fn] = font_from_file(os.path.join(fontpath,fn))
        except:
            logging.warn("import font failed (%s)" % fn)
        

def font_from_file(filename):
    """Extract font info from zipfile or plain textfile."""
    data = None
    while 1:
        try: # zipped?
            with ZipFile(filename,'r') as fh:
                data = fh.read(os.path.basename(filename))
            break
        except BadZipfile as e:
            logging.info("%s does not appear to be a zipfile" % filename)

        with open(filename,'r') as fh:
            data = fh.readlines()
        break
                  
    return BigFont(data,name=filename)

def font_from_pickle(fontname,pklfile='fontcache.pkl'):
    with open(pklfile,'r') as fh:
        pklfonts = pickle.load(fh)
        return pklfonts[fontname]

class BigFont(BaseObject):
    """Stores all characters from a font as a list of BigLetters."""
    def __init__(self,data=None,name=None,nonprintable=32,eol="\n",**kwargs):
        super(BigFont,self).__init__(**kwargs)
        self.nonprintable = nonprintable
        self.letters = self._extract_letters(data)
        #self.renderfcn = kern
        self.eol = eol
        self.name = name
        self.smooshrules = None # make rules from header line
        self.raise_missing = True

    def _extract_letters(self,data):
        """Extract list of BigLetters from flf file data"""
        if data is None:
            return None
        elif isinstance(data,str):
            lines = re.split("\r?\n",data)
        else:
            lines = [line.rstrip() for line in data]
            
        header = lines[0]
        logging.info("ignoring header (FIXME)")
        endchar = '@'
        logging.info("endchar is hardcoded to %s (FIXME)" % endchar)
        buf = []
        letters = [[]]*self.nonprintable
        for line in lines:
            if len(line) > 1 and line[-2:] == (endchar*2):
                buf.append(line[:-2])
                letters.append(BigLetter(buf))
                buf = []
            elif len(line) > 0 and line[-1] == endchar:
                buf.append(line[:-1])
        return letters

    @trace
    def __call__(self,s):
        """Shortcut to render()."""
        return self.render(s)
    
    @trace
    def __getitem__(self,key):
        """Access a BigLetter from the character representation."""
        try:
            return self.letters[ord(key)]
        except IndexError as e:
            if self.raise_missing:
                raise KeyError("%s is not present in font")
            else:
                return self.letters[ord('?')] # fixme, return an empty Bigletter?

    @trace
    def render(self,s):
        """Return string rendered in the font, suitable for printing."""
        return functools.reduce(operator.add, [self[c] for c in s])

    def bigprint(self,s):
        """Render and print multi-line string."""
        lines = s.split(self.eol)
        for line in lines:
            print(self.render(line))





