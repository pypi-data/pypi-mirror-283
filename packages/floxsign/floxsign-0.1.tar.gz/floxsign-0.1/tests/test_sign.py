# tests/test_sign.py
import unittest
from sign import get_symbol_name

class TestSymbolMapper(unittest.TestCase):
    def test_get_name(self):
        self.assertEqual(get_symbol_name('%'), 'percent')
        self.assertEqual(get_symbol_name('$'), 'dollar')
        self.assertEqual(get_symbol_name('^'), 'unknown symbol')

if __name__ == '__main__':
    unittest.main()