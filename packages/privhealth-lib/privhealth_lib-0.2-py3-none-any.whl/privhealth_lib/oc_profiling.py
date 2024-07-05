import os
from openclean.data.load import dataset
from openclean.profiling.dataset import dataset_profile


def dataset_statistics(caminho):
    """
    Calculates and returns the statistical summary of a dataset.

    Args:
        caminho (str): The path to the dataset file.

    Returns:
        dict: A dictionary containing the statistical summary of the dataset.
    """
    path_to_file = os.path.join(os.getcwd(), 'source', 'data')
    ds = dataset(os.path.join(path_to_file, caminho))
    profiles = dataset_profile(ds)
    print(profiles.stats())
    return profiles.stats()


def max_min_coluna(caminho, coluna):
    """
    Returns the minimum and maximum values of a specific column in a dataset.

    Args:
        caminho (str): The path to the dataset file.
        coluna (str): The name of the column.

    Returns:
        tuple: A tuple containing the minimum and maximum values of the column.
    """
    path_to_file = os.path.join(os.getcwd(), 'source', 'data')
    ds = dataset(os.path.join(path_to_file, caminho))
    profiles = dataset_profile(ds)
    return profiles.minmax(coluna)


def data_types(caminho):
    """
    Returns the data types of each column in a dataset.

    Args:
        caminho (str): The path to the dataset file.

    Returns:
        dict: A dictionary mapping column names to their respective data types.
    """
    path_to_file = os.path.join(os.getcwd(), 'source', 'data')
    ds = dataset(os.path.join(path_to_file, caminho))
    profiles = dataset_profile(ds)
    return profiles.types()
