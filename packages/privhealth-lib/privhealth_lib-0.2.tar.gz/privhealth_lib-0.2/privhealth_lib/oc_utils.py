import numpy as np

def search_resolved(resolved, search_columns, search_values):
    """
    Searches a Pandas DataFrame for rows matching multiple columns with specific values.

    Args:
        resolved (pd.DataFrame): The DataFrame to search.
        search_columns (list): List of column names to search.
        search_values (list): List of values to search for, corresponding to search_columns.

    Returns:
        pd.DataFrame: A DataFrame containing rows that match all search criteria.
    """

    # Ensure valid input lengths
    if len(search_columns) != len(search_values):
        raise ValueError("Lengths of search_columns and search_values must be equal.")

    # Create a boolean mask for efficient filtering
    mask = np.ones(len(resolved), dtype=bool)
    for col, value in zip(search_columns, search_values):
        mask &= resolved[col] == value  # Add conditions to the mask

    return resolved[mask]
