import unittest
import sys 
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.trashPandasdf.froude_scale import getFroudeCoeff
import sys
import os
from src.trashPandasdf.froude_scale import getFroudeCoeff

class TestFroude(unittest.TestCase):
    def test_getFroudeCoeff(self):
        """
        Test the getFroudeCoeff function
        """
        unit1 = 'm/s'
        unit2 = 'kg^2'
        unit3 = 'm-N'
        self.assertEqual(getFroudeCoeff(unit1),0.5)
        self.assertEqual(getFroudeCoeff(unit2),6)
        self.assertEqual(getFroudeCoeff(unit3),4)

if __name__ == '__main__':  
    unittest.main()
