import json
from furtheredge.abstracted_packages import furtheredge_pandas as pd


def npv(merged_df, values_to_project):
    """
    Calculate the Net Present Value (NPV) of projected values.

    Args:
        merged_df (pandas.DataFrame): DataFrame containing merged data, including
            columns necessary for NPV calculation.
        values_to_project (str): Column name containing the values to project.

    Returns:
        pandas.Series: Series containing the calculated NPV for each row in the DataFrame.
    """
    annual_interest_rt = merged_df["interest_rt"]
    monthly_interest_rt = (1 + annual_interest_rt) ** (1 / 12) - 1
    discount_factor = 1 / (1 + monthly_interest_rt) ** (
        merged_df["proj_m"] + 1
    )

    npv = merged_df[values_to_project] * discount_factor
    npv_df = pd.DataFrame(
        {
            "NPV": npv,
            "mp_id": merged_df["mp_id"],
        }
    )

    npv_df = npv_df.iloc[::-1]
    grouped_data = npv_df.groupby("mp_id")
    npv_df["van"] = grouped_data["NPV"].cumsum()
    npv_df = npv_df.iloc[::-1]

    return npv_df["van"] / discount_factor


def load_json_to_dict(file_json_path):
    """
    Loads a JSON file and returns its contents as a dictionary.

    :param file_json_path: The path to the JSON file
    :return: A dictionary containing the contents of the JSON file
    """
    try:
        with open(file_json_path, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File not found: {file_json_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_json_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
