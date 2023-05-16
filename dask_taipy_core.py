import taipy as tp
from taipy import Gui, Config

import numpy as np
import pandas as pd
import dask.dataframe as dd

BUSINESS_PATH = "data/yelp_business.csv"
REVIEW_PATH = "data/yelp_review_repaired.csv"

# Load the business data using pandas
business_df = pd.read_csv(BUSINESS_PATH)

# Create a list of the business names
selection_names = list(business_df.name[:20])


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


# Taipy Core
Config.load("config.toml")

Config.configure_data_node(
    id="review_data", read_fct_params=("data/yelp_review_repaired_large.csv",)
)

Config.export("configured")

scenario_object = Config.scenarios["scenario"]

tp.Core().run()
scenario = tp.create_scenario(scenario_object)
tp.submit(scenario)

business_name = '"Dental by Design"'
reviews = scenario.parsed_reviews.read()


def on_selection(state):
    """
    Re-runs the scenario when the user selects a business.

    Args:
        - state: state of the app
    """
    print("Running query...")
    scenario = tp.create_scenario(scenario_object)
    scenario.business_name.write(state.business_name)
    tp.submit(scenario)
    state.reviews = scenario.parsed_reviews.read()
    print("Query finished")


page = """
# Querying Big Data with Taipy and Dask

## Select a business

<|{business_name}|selector|lov={selection_names}|dropdown|on_change=on_selection|>

## Average stars for that business:

<|{round(np.mean(reviews.stars),2)}|indicator|value={np.mean(reviews.stars)}|min=1|max=5|width=30%|>

## Reviews for that business:

<|{reviews}|table|>
"""

Gui(page).run()
