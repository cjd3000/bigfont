from __future__ import print_function
from __future__ import division

import copy
import functools
import os
import re
import logging
import base
import unittest
import operator
import pickle

from zipfile import ZipFile, BadZipfile # or BadZipFile in 3.x
from base import BaseObject
from letter import BigLetter
from decorators import trace

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

    def print(self,s):
        """Render and print multi-line string."""
        lines = s.split(self.eol)
        for line in lines:
            print(self.render(line))


class BasicBigFontTests(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_file_load(self):
        standard = font_from_file('standard.flf')
        self.assertEqual(1,1)

    def test_call(self):
        standard = font_from_file('standard.flf')
        self.assertEqual(standard['a'],standard['a'])


if __name__ == "__main__":
    unittest.main(exit=False)



