import unittest
import os
from privhealth_lib.oc_transformation import (selecionar_colunas, inserir_coluna, inserir_linhas,
atualizar_nome_coluna, filtrar_valor_por_coluna, mover_coluna, mover_linha, ordenar_valor_descendente_coluna)


class TestTransformation(unittest.TestCase):
    def set_up(self):
        self.caminho = 'test_data.csv'
        # Crie um DataFrame de teste e salve como CSV para uso nos testes
        import pandas as pd
        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'city': ['New York', 'Los Angeles', 'Chicago']
        })
        os.makedirs(os.path.join(os.getcwd(), 'source', 'data'), exist_ok=True)
        df.to_csv(os.path.join(os.getcwd(), 'source', 'data', self.caminho), index=False)

    def test_selecionar_colunas(self):
        """
        Testa a função selecionar_colunas.
        """
        selected = selecionar_colunas(self.caminho, 'name', 'age')
        self.assertEqual(list(selected.columns), ['name', 'age'])

    def test_inserir_coluna(self):
        """
        Testa a função inserir_coluna.
        """
        new_col = inserir_coluna(self.caminho, 'salary', 3, 50000)
        self.assertIn('salary', new_col.columns)

    def test_inserir_linhas(self):
        """
        Testa a função inserir_linhas.
        """
        new_row = inserir_linhas(self.caminho, 1, 'David', 40, 'Houston')
        self.assertEqual(new_row.iloc[1]['name'], 'David')

    def test_atualizar_nome_coluna(self):
        """
        Testa a função atualizar_nome_coluna.
        """
        updated = atualizar_nome_coluna(self.caminho, 'name')
        self.assertEqual(updated.iloc[0]['name'], 'Alice')

    def test_filtrar_valor_por_coluna(self):
        """
        Testa a função filtrar_valor_por_coluna.
        """
        filtered = filtrar_valor_por_coluna(self.caminho, 'city', 'New York')
        self.assertEqual(filtered.iloc[0]['city'], 'New York')

    def test_mover_coluna(self):
        """
        Testa a função mover_coluna.
        """
        moved_col = mover_coluna(self.caminho, 'city', 0)
        self.assertEqual(moved_col.columns[0], 'city')

    def test_mover_linha(self):
        """
        Testa a função mover_linha.
        """
        moved_row = mover_linha(self.caminho, 0, 2)
        self.assertEqual(moved_row.iloc[2]['name'], 'Alice')

    def test_ordenar_valor_descendente_coluna(self):
        """
        Testa a função ordenar_valor_descendente_coluna.
        """
        sorted_df = ordenar_valor_descendente_coluna(self.caminho, 'age')
        self.assertEqual(sorted_df.iloc[0]['age'], 35)

    def tear_down(self):
        os.remove(os.path.join(os.getcwd(), 'source', 'data', self.caminho))

if __name__ == "__main__":
    unittest.main()
