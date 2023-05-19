import pandas as pd
import dask.dataframe as dd


def get_id_from_name(name: str, business_dict: dict):
    """
    Returns the business_id from the name of the business.

    Args:
        - name: name of the business
        - business_dict: dict with the name as key and the business_id as value

    Returns:
        - business_id: id of the business
    """
    business_id = business_dict[name]
    return business_id


def parse_business_data(data: dd.DataFrame):
    """
    Parses the reviews of a business.

    Args:
        - data: dask dataframe with the reviews of a business

    Returns:
        - data: dask dataframe with the parsed reviews
    """
    # Sort data by useful
    data = data.sort_values(by="useful", ascending=False)
    # Keep only the stars, date and text columns
    data = data[["stars", "date", "text"]]
    return data

def get_business_data(business_id: str, data: dd.DataFrame):
    """
    Returns a dask dataframe with the reviews of a business.

    Args:
        - business_id: id of the business
        - data: dask dataframe with the reviews

    Returns:
        - df_business: dask dataframe with the reviews of the business
    """
    df_business = data[(data.business_id == business_id)].compute()
    return df_business


def create_business_dict(business_df: pd.DataFrame):
    """
    Creates a dict with the name as key and the business_id as value.

    Args:
        - business_df: pandas dataframe with the business data

    Returns:
        - business_dict: dict with the name as key and the business_id as value
    """
    business_dict = dict(zip(business_df.name, business_df.business_id))
    return business_dict



