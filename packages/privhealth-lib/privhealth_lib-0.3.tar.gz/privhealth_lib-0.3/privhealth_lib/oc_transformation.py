import os
from openclean.data.load import dataset
from openclean.operator.transform.select import select
from openclean.operator.transform.insert import inscol
from openclean.function.eval.base import Const
from openclean.operator.transform.insert import insrow
from openclean.operator.transform.update import update
from openclean.operator.transform.filter import filter
from openclean.function.eval.base import Col
from openclean.operator.transform.move import movecols
from openclean.operator.transform.move import move_rows
from openclean.operator.transform.sort import order_by

def selecionar_colunas(caminho, *args, is_data_full=False):
    """
    Seleciona colunas específicas de um conjunto de dados.

    Args:
        caminho (str): O caminho para o arquivo de dados.
        *args (str): Os nomes das colunas a serem selecionadas.
        is_data_full (bool, optional): Indica se deve retornar o conjunto de dados completo ou apenas as primeiras linhas. O padrão é False.

    Returns:
        openclean.data.DataFrame: O conjunto de dados com as colunas selecionadas.
    """
    path_to_file = os.path.join(os.getcwd(), 'source', 'data')
    ds = dataset(os.path.join(path_to_file, caminho))
    colunas = []
    for i in args:
        colunas.append(i)
    selected = select(ds, columns = colunas)
    if is_data_full == True:
        return selected
    else:
        return selected.head()

def inserir_coluna(caminho, coluna, posicao, valor, is_data_full=False):
    """
    Insere uma nova coluna em um conjunto de dados.

    Args:
        caminho (str): O caminho para o arquivo de dados.
        coluna (str): O nome da nova coluna a ser inserida.
        posicao (int): A posição em que a nova coluna deve ser inserida.
        valor (Any): O valor constante a ser atribuído a todas as linhas da nova coluna.
        is_data_full (bool, optional): Indica se deve retornar o conjunto de dados completo ou apenas as primeiras linhas. O padrão é False.

    Returns:
        openclean.data.DataFrame: O conjunto de dados com a nova coluna inserida.
    """
    path_to_file = os.path.join(os.getcwd(), 'source', 'data')
    ds = dataset(os.path.join(path_to_file, caminho))
    new_col = inscol(ds, names = [coluna], pos=posicao, values= Const(valor))
    if is_data_full == True:
        return new_col
    else:
        return new_col.head()

def inserir_linhas(caminho, posicao,*args, is_data_full=False):
    """
    Insere novas linhas em um conjunto de dados.

    Args:
        caminho (str): O caminho para o arquivo de dados.
        posicao (int): A posição em que as novas linhas devem ser inseridas.
        *args (list): Os valores das novas linhas a serem inseridas.
        is_data_full (bool, optional): Indica se deve retornar o conjunto de dados completo ou apenas as primeiras linhas. O padrão é False.

    Returns:
        openclean.data.DataFrame: O conjunto de dados com as novas linhas inseridas.
    """
    path_to_file = os.path.join(os.getcwd(), 'source', 'data')
    ds = dataset(os.path.join(path_to_file, caminho))
    valoresLinha = []
    for i in args:
        valoresLinha.append(i)
    new_row = insrow(ds, pos=posicao, values = valoresLinha)
    if is_data_full == True:
        return new_row
    else:
        return new_row.head()

def atualizar_nome_coluna(caminho, coluna, is_data_full=False):
    """
    Atualiza o nome de uma coluna em um conjunto de dados.

    Args:
        caminho (str): O caminho para o arquivo de dados.
        coluna (str): O nome da coluna a ser atualizada.
        is_data_full (bool, optional): Indica se deve retornar o conjunto de dados completo ou apenas as primeiras linhas. O padrão é False.

    Returns:
        openclean.data.DataFrame: O conjunto de dados com o nome da coluna atualizado.
    """
    path_to_file = os.path.join(os.getcwd(), 'source', 'data')
    ds = dataset(os.path.join(path_to_file, caminho))
    title_case = update(ds, columns = coluna, func = str.title)
    if is_data_full == True:
        return title_case
    else:
        return title_case.head()

def filtrar_valor_por_coluna(caminho, coluna, valor, is_data_full=False):
    """
    Filtra um conjunto de dados com base em um valor específico em uma coluna.

    Args:
        caminho (str): O caminho para o arquivo de dados.
        coluna (str): O nome da coluna a ser filtrada.
        valor (Any): O valor a ser filtrado.
        is_data_full (bool, optional): Indica se deve retornar o conjunto de dados completo ou apenas as primeiras linhas. O padrão é False.

    Returns:
        openclean.data.DataFrame: O conjunto de dados filtrado.
    """
    path_to_file = os.path.join(os.getcwd(), 'source', 'data')
    ds = dataset(os.path.join(path_to_file, caminho))
    filtered = filter(ds, predicate = Col(coluna)==valor)
    if is_data_full == True:
        return filtered
    else:
        return filtered.head()

def mover_coluna(caminho, coluna, posicao, is_data_full=False):
    """
    Move uma coluna para uma nova posição em um conjunto de dados.

    Args:
        caminho (str): O caminho para o arquivo de dados.
        coluna (str): O nome da coluna a ser movida.
        posicao (int): A nova posição da coluna.
        is_data_full (bool, optional): Indica se deve retornar o conjunto de dados completo ou apenas as primeiras linhas. O padrão é False.

    Returns:
        openclean.data.DataFrame: O conjunto de dados com a coluna movida.
    """
    path_to_file = os.path.join(os.getcwd(), 'source', 'data')
    ds = dataset(os.path.join(path_to_file,caminho))
    moved_col = movecols(ds, coluna,posicao)
    if is_data_full == True:
        return moved_col
    else:
        return moved_col.head()

def mover_linha(caminho, pos_linha, nova_posicao, is_data_full=False):
    """
    Move uma linha para uma nova posição em um conjunto de dados.

    Args:
        caminho (str): O caminho para o arquivo de dados.
        pos_linha (int): A posição da linha a ser movida.
        nova_posicao (int): A nova posição da linha.
        is_data_full (bool, optional): Indica se deve retornar o conjunto de dados completo ou apenas as primeiras linhas. O padrão é False.

    Returns:
        openclean.data.DataFrame: O conjunto de dados com a linha movida.
    """
    path_to_file = os.path.join(os.getcwd(), 'source', 'data')
    ds = dataset(os.path.join(path_to_file,caminho))
    moved_row = move_rows(ds, pos_linha, nova_posicao)
    if is_data_full == True:
        return moved_row
    else:
        return moved_row.head()

def ordenar_valor_descendente_coluna(caminho, coluna, is_data_full=False):
    """
    Ordena um conjunto de dados em ordem descendente com base em uma coluna.

    Args:
        caminho (str): O caminho para o arquivo de dados.
        coluna (str): O nome da coluna a ser ordenada.
        is_data_full (bool, optional): Indica se deve retornar o conjunto de dados completo ou apenas as primeiras linhas. O padrão é False.

    Returns:
        openclean.data.DataFrame: O conjunto de dados ordenado em ordem descendente.
    """
    path_to_file = os.path.join(os.getcwd(), 'source', 'data')
    ds = dataset(os.path.join(path_to_file,caminho))
    sorted = order_by(ds, columns = coluna, reversed=True)
    if is_data_full == True:
        return sorted
    else:
        return sorted.head()