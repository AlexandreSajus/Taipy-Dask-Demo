import dask.dataframe as dd


def get_data(path_to_csv: str, optional: str = None):
    """
    Loads a csv file into a dask dataframe.
    Converts the date column to datetime.

    Args:
        - path_to_csv: path to the csv file
        - optional: optional argument (currently necessary to fix Core bug with generic data nodes)

    Returns:
        - dataset: dask dataframe
    """
    dataset = dd.read_csv(path_to_csv)
    dataset["date"] = dd.to_datetime(dataset["date"])
    return dataset


def write_function():
    """
    Useless function to fix Core bug with generic data nodes.
    """
    return None