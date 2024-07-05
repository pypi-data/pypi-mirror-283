import unittest
import os
from privhealth_lib.oc_wrangling_and_cleaning import (corrigir_violacao_depend, dados_faltantes_lambda_func,
retirar_dados_faltantes)

class TestWranglingAndCleaning(unittest.TestCase):
    """
    Uma classe de casos de teste para testar as funções no módulo WranglingAndCleaning.
    """

    def set_up(self):
        """
        Configuração inicial para os testes.
        Cria um DataFrame de teste e salva como CSV para uso nos testes.
        """
        self.caminho = 'test_data.csv'
        import pandas as pd
        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'age': [25, 30, 35, None, 40],
            'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', None]
        })
        os.makedirs(os.path.join(os.getcwd(), 'source', 'data'), exist_ok=True)
        df.to_csv(os.path.join(os.getcwd(), 'source', 'data', self.caminho), index=False)

    def test_corrigir_violacao_depend(self):
        """
        Testa a função corrigir_violacao_depend.
        Verifica se a função corrige a violação de dependência entre as colunas corretamente.
        """
        corrigir_violacao_depend(self.caminho, 'city', ['name'], ['David'])
        # Esta função imprime os resultados e não retorna, então o teste é visual

    def test_dados_faltantes_lambda_func(self):
        """
        Testa a função dados_faltantes_lambda_func.
        Verifica se a função retorna corretamente a contagem de dados faltantes na coluna especificada.
        """
        counts = dados_faltantes_lambda_func(self.caminho, 'city')
        self.assertEqual(counts['Unknown'], 1)

    def test_retirar_dados_faltantes(self):
        """
        Testa a função retirar_dados_faltantes.
        Verifica se a função remove corretamente os dados faltantes na coluna especificada.
        """
        counts = retirar_dados_faltantes(self.caminho, 'age')
        self.assertNotIn(None, counts.index)

    def tear_down(self):
        """
        Limpeza após os testes.
        Remove o arquivo CSV de teste criado durante a configuração inicial.
        """
        os.remove(os.path.join(os.getcwd(), 'source', 'data', self.caminho))

if __name__ == "__main__":
    unittest.main()
