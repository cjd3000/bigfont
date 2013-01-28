import unittest
import os
import copy

from letter import BigLetter

class BasicBigLetterTests(unittest.TestCase):
    def setUp(self):
        d = ["|-\\","| |","| /"]
        e = ("----","--  ","____")
        self.letterD = BigLetter(d)
        self.letterD2 = BigLetter(d)
        self.letterE = BigLetter(e)

    def test_add(self):
        dc = copy.copy(self.letterD)
        de = self.letterD + self.letterE
        de2 = self.letterD2
        de2 += self.letterE
        self.assertEqual(de, de2)
        self.assertEqual(dc + self.letterD, self.letterD + dc)

    def test_equality(self):
        self.assertNotEqual(self.letterD,self.letterE)
        self.assertEqual(self.letterD,self.letterD)
        self.assertEqual(self.letterD,self.letterD2)
        self.assertEqual(self.letterD,copy.copy(self.letterD))


from font import BigFont, font_from_file

class BasicBigFontTests(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_file_load(self):
        standard = font_from_file(os.path.join('fonts','standard.flf'))
        self.assertEqual(1,1)

    def test_call(self):
        standard = font_from_file(os.path.join('fonts','standard.flf'))
        self.assertEqual(standard['a'],standard['a'])


suites = []
suites.append(unittest.TestLoader().loadTestsFromTestCase(BasicBigLetterTests))
suites.append(unittest.TestLoader().loadTestsFromTestCase(BasicBigFontTests))
alltests = unittest.TestSuite(suites)
unittest.TextTestRunner(verbosity=2).run(alltests)

if os.name == 'nt':
    raw_input("Press enter to exit.")
