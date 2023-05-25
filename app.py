import taipy as tp
from taipy.gui import Gui, notify
from taipy.config import Config

import numpy as np
import pandas as pd


BUSINESS_PATH = "data/yelp_business.csv"

# Load the business data using pandas
business_df = pd.read_csv(BUSINESS_PATH)

# Remove quotation marks from the name
business_df.name = business_df.name.str[1:-1]

# Taipy Core
Config.load("config/config.toml")

Config.configure_data_node(id="review_data", read_fct_params=("data/yelp_review.csv",))

scenario_object = Config.scenarios["scenario"]
business_name = business_df.name[0]
reviews = None


def on_selection(state):
    """
    Re-runs the scenario when the user selects a business.

    Args:
        - state: state of the app
    """
    notify(state, "info", "Running query...")
    scenario = tp.create_scenario(scenario_object)
    scenario.business_name.write(state.business_name)
    tp.submit(scenario)
    state.reviews = scenario.parsed_reviews.read()
    notify(state, "success", "Query finished")


page = """

# Querying **Big Data**{: .color-primary} with Taipy and Dask

## Select a **business**{: .color-primary}

<|{business_name}|selector|lov={list(business_df.name)}|dropdown|on_change=on_selection|>



## Average **stars**{: .color-primary} for that business: <|{"⭐"*int(np.mean(reviews.stars))}|text|raw|>

<|{round(np.mean(reviews.stars),2)}|indicator|value={np.mean(reviews.stars)}|min=1|max=5|width=30%|>

## **Reviews**{: .color-primary} for that business:

<|{reviews}|table|width=100%|>
"""


def on_init(state):
    scenario = tp.create_scenario(scenario_object)
    tp.submit(scenario)
    state.reviews = scenario.parsed_reviews.read()


if __name__ == "__main__":
    tp.Core().run()
    Gui(page).run()
