import unittest
from trashPandas import trashPandas
import pandas as pd

class TestTrashPandas(unittest.TestCase):
    def test_init_with_dataframe(self):
        """
        Test initializing trashPandas with a simple dataframe
        """
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        tp = trashPandas(df)
        
        self.assertEqual(tp.shape, (3, 2))
        self.assertListEqual(list(tp.columns), ['A', 'B'])
        self.assertListEqual(list(tp['A']), [1, 2, 3])
        self.assertListEqual(list(tp['B']), [4, 5, 6])

if __name__ == '__main__':
    unittest.main()