from datetime import datetime
from furtheredge.abstracted_packages import furtheredge_pandas as pd
from furtheredge.abstracted_packages import furtheredge_numpy as np
from dateutil.relativedelta import relativedelta


def load_rename_policies_columns(policies, run_settings):
    """
    Load and rename columns in the policies DataFrame based on run settings.

    This function renames the columns in the policies DataFrame according to the
    mapping provided in the run settings, calculates additional date-related columns,
    and adjusts payment end dates based on the payment mode.

    Parameters:
    - policies (pd.DataFrame): DataFrame containing policy data.
    - run_settings (dict): Dictionary containing run settings, including column mappings and projection date.

    Returns:
    - pd.DataFrame: DataFrame with renamed columns and additional calculated columns.
    """

    mapping_dict = run_settings["mapping_columns_names_policies"]

    policies_renamed_df = rename_columns(policies, mapping_dict)

    policies_renamed_df["projection_date"] = datetime.strptime(
        run_settings["projection_date"], "%d/%m/%Y"
    )

    policies_renamed_df["inception_year"] = policies_renamed_df[
        "inception_date"
    ].dt.year

    policies_renamed_df["duration_init_m"] = policies_renamed_df.apply(
        lambda row: calculate_months_difference(
            row["projection_date"], row["inception_date"]
        ),
        axis=1,
    )

    policies_renamed_df["maturity_init_m"] = policies_renamed_df.apply(
        lambda row: calculate_months_difference(
            row["maturity_date"], row["inception_date"]
        ),
        axis=1,
    )
    policies_renamed_df["inception_date"] = pd.to_datetime(
        policies_renamed_df["inception_date"]
    )

    inception_date_vector = policies_renamed_df["inception_date"]
    years_timedelta = pd.to_timedelta(
        policies_renamed_df["payment_duration_y"] * 365, unit="D"
    )

    temp_date_4 = (
        inception_date_vector + years_timedelta - pd.DateOffset(months=3)
    )
    temp_date_12 = (
        inception_date_vector + years_timedelta - pd.DateOffset(months=1)
    )
    temp_date_2 = (
        inception_date_vector + years_timedelta - pd.DateOffset(months=6)
    )
    temp_date_1 = (
        inception_date_vector + years_timedelta - pd.DateOffset(months=12)
    )

    policies_renamed_df["end_payment_date"] = inception_date_vector

    conditions = [
        policies_renamed_df["payment_mode"] == 4,
        policies_renamed_df["payment_mode"] == 12,
        policies_renamed_df["payment_mode"] == 2,
        policies_renamed_df["payment_mode"] == 1,
    ]
    choices = [temp_date_4, temp_date_12, temp_date_2, temp_date_1]

    policies_renamed_df["end_payment_date"] = np.select(
        conditions, choices, default=inception_date_vector
    )
    policies_renamed_df.drop(["projection_date"], axis=1, inplace=True)

    return policies_renamed_df


def rename_columns(dataframe, mapping_dict):
    """
    Rename columns in a DataFrame based on a provided mapping dictionary.

    This function renames the columns of the given DataFrame according to the
    key-value pairs in the mapping dictionary.

    Parameters:
    - dataframe (pd.DataFrame): The DataFrame whose columns are to be renamed.
    - mapping_dict (dict): Dictionary containing the column name mappings,
                           where the keys are the new names and the values are the old names.

    Returns:
    - pd.DataFrame: DataFrame with renamed columns.
    """
    renamed_columns = {v: k for k, v in mapping_dict.items()}
    dataframe_renamed = dataframe.rename(columns=renamed_columns)

    return dataframe_renamed


def calculate_months_difference(end_date, start_date):
    """
    Calculate the difference in months between two dates.

    This function computes the total number of months between the start date and the end date.
    If there are remaining days after the full months, it adds an additional month to the total.

    Parameters:
    - end_date (datetime): The end date.
    - start_date (datetime): The start date.

    Returns:
    - int: The total number of months difference between the two dates.
    """
    delta = relativedelta(end_date, start_date)
    total_months_difference = delta.years * 12 + delta.months
    if delta.days > 0:
        total_months_difference += 1
    return total_months_difference
