from library import *
from address import *
import unittest


class LibraryTestCase(unittest.TestCase):
    
    def test_valid_add_customer(self):
        Library()
        library = Library.load_from_pickle()
        library.add_customer(6, "Daniel", "Shchetinin", Address("Israel", "Ashdod", "Kineret", 116), "d117596@gmail.com", 2002)
        self.assertRaises(library.add_customer(6, "Daniel", "Shchetinin", Address("Israel", "Ashdod", "Kineret", 116), "d117596@gmail.com", 2002))

if __name__ == "__main__":
    unittest.main()