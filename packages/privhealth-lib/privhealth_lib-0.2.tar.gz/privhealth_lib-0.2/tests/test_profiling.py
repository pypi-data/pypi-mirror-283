# tests/test_profiling.py

import unittest
import os
from privhealth_lib.oc_profiling import dataset_statistics, max_min_coluna, data_types

class TestProfiling(unittest.TestCase):
    def set_up(self):
        self.caminho = 'test_data.csv'
        # Crie um DataFrame de teste e salve como CSV para uso nos testes
        import pandas as pd
        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35]
        })
        os.makedirs(os.path.join(os.getcwd(), 'source', 'data'), exist_ok=True)
        df.to_csv(os.path.join(os.getcwd(), 'source', 'data', self.caminho), index=False)

    def test_dataset_statistics(self):
        stats = dataset_statistics(self.caminho)
        self.assertIsNotNone(stats)

    def test_max_min_coluna(self):
        minmax = max_min_coluna(self.caminho, 'age')
        self.assertEqual(minmax['min'], 25)
        self.assertEqual(minmax['max'], 35)

    def test_data_types(self):
        types = data_types(self.caminho)
        self.assertIn('age', types)
        self.assertEqual(types['age'], 'int')

    def tear_down(self):
        os.remove(os.path.join(os.getcwd(), 'source', 'data', self.caminho))

if __name__ == "__main__":
    unittest.main()
