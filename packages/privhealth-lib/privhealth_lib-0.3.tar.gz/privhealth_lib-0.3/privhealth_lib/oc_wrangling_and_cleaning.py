import os
from openclean.data.load import dataset
from openclean.operator.map.violations import fd_violations
from openclean.operator.collector.count import distinct
from openclean.operator.collector.repair import Shortest, Vote, conflict_repair
from openclean.operator.transform.update import update
from openclean.operator.transform.filter import filter
from openclean.function.value.null import is_empty
from openclean.function.eval.null import IsNotEmpty
from .oc_utils import search_resolved

def corrigir_violacao_depend(caminho, post_fixed_column, pre_fixed_columns, comparison_values):
    """
    Corrige as violações de dependência funcional em um conjunto de dados.
    
    Parâmetros:
    - caminho: O caminho para o arquivo de dados.
    - post_fixed_column: A coluna que será corrigida.
    - pre_fixed_columns: As colunas que são dependentes da coluna corrigida.
    - comparison_values: Os valores de comparação para encontrar as violações corrigidas.
    """
    path_to_file = os.path.join(os.getcwd())
    ds = dataset(os.path.join(path_to_file, caminho))
    df_selected = ds
    colunas = []
    for i in pre_fixed_columns:
        colunas.append(i)
     
    fd1_violations = fd_violations(ds, colunas, [post_fixed_column])
     
    strategy = {post_fixed_column: Vote()}
    
    resolved = conflict_repair(conflicts=fd1_violations, strategy=strategy, in_order=False)
     
    violation_group = search_resolved(resolved=resolved, search_columns = pre_fixed_columns,search_values = comparison_values)
    
    fd2_violations = fd_violations(resolved, pre_fixed_columns, [post_fixed_column])

    print('# of violations for selected columns before is {}\n'.format(len(fd1_violations)))
    print('# of violations for selected columns) is {}\n'.format(len(fd2_violations)))
    print(violation_group)

def dados_faltantes_lambda_func(caminho, coluna):
    """
    Atualiza os valores faltantes em uma coluna usando uma função lambda.
    
    Parâmetros:
    - caminho: O caminho para o arquivo de dados.
    - coluna: A coluna que será atualizada.
    
    Retorna:
    - Um objeto que contém a contagem dos valores atualizados na coluna.
    """
    path_to_file = os.path.join(os.getcwd(), 'source', 'data')
    ds = dataset(os.path.join(path_to_file, caminho))
    updated_misspelled = update (ds, coluna, lambda x: 'Unknow' if is_empty(x) else(x))
    return updated_misspelled[coluna].value_counts()

def retirar_dados_faltantes(caminho, coluna):
    """
    Remove os dados faltantes de uma coluna.
    
    Parâmetros:
    - caminho: O caminho para o arquivo de dados.
    - coluna: A coluna que terá os dados faltantes removidos.
    
    Retorna:
    - Um objeto que contém a contagem dos valores na coluna após a remoção dos dados faltantes.
    """
    path_to_file = os.path.join(os.getcwd(), 'source', 'data')
    ds = dataset(os.path.join(path_to_file, caminho))
    ds = filter(ds, predicate = IsNotEmpty(coluna))
    return ds[coluna].value_counts()