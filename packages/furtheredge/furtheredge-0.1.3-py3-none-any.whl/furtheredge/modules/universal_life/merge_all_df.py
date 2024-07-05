from furtheredge.abstracted_packages import furtheredge_pandas as pd
from furtheredge.abstracted_packages import furtheredge_numpy as np


def lowercase_string_columns(df):
    """
    Transform all string columns in a DataFrame to lowercase.

    Args:
    - df (DataFrame): Input DataFrame.

    Returns:
    - DataFrame: DataFrame with string columns transformed to lowercase.
    """
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.lower()

    return df


def initialize_output_dataframe(
    model_points,
    duration_month,
    starting_projection_date,
):
    """
    Initialize an output DataFrame for projections based on model points and projection parameters.

    This function creates an output DataFrame for projections based on the given model points,
    duration in months, and starting projection date.

    Parameters:
    - model_points (pd.DataFrame): DataFrame containing model points with 'mp_id' column.
    - duration_month (int): Duration of the projection period in months.
    - starting_projection_date (str or datetime): Starting date of the projection period.

    Returns:
    - pd.DataFrame: Initialized DataFrame with columns 'mp_id', 'proj_m' (projection month index),
                    and 'proj_date' (projection date).
    """

    dfs = []
    proj_date = pd.date_range(
        start=starting_projection_date, periods=duration_month, freq="MS"
    )
    for mp_id in list(model_points["mp_id"]):
        df = pd.DataFrame(
            {
                "mp_id": mp_id,
                "proj_m": range(duration_month),
                "proj_date": proj_date,
            }
        )
        dfs.append(df)
    result_df = pd.concat(dfs, ignore_index=True)
    return result_df[["mp_id", "proj_m", "proj_date"]]


def merge_all_dfs_police(
    model_points,
    ri_rates,
    wop_rates,
    tech_assumptions,
    product,
    projection_date,
    projection_points,
):
    """
    Merge various dataframes to create a comprehensive output dataframe for insurance policy projections.

    This function merges multiple dataframes including model points, rates, assumptions, and product details
    to create an output dataframe suitable for projecting insurance policies.

    Parameters:
    - model_points (pd.DataFrame): DataFrame containing model points for insurance policies.
    - ri_rates (pd.DataFrame): DataFrame containing reinsurance rates.
    - wop_rates (pd.DataFrame): DataFrame containing waiver of premium rates.
    - tech_assumptions (pd.DataFrame): DataFrame containing technical assumptions.
    - product (pd.DataFrame): DataFrame containing product details.
    - projection_date (str or datetime): Starting date of the projection.
    - projection_points (int): Number of projection points (months).

    Returns:
    - pd.DataFrame: Merged dataframe containing all necessary columns for insurance policy projections.
    """

    output = initialize_output_dataframe(
        model_points, projection_points, projection_date
    )
    output = pd.merge(output, model_points, on="mp_id", how="left")

    output = pd.merge(
        output,
        product,
        on=["product_type", "plan_code"],
        how="left",
    )

    output["projection_yr_11"] = np.ceil(
        (output["duration_init_m"] + output["proj_m"]) / 12
    ).clip(upper=11)

    output = pd.merge(
        output,
        tech_assumptions,
        left_on=["tech_assumption_id", "projection_yr_11"],
        right_on=["tech_assumption_id", "projection_yr"],
    )

    output.drop(["projection_yr_11"], axis=1, inplace=True)

    output["age_y"] = output["age_init_y"] + (
        (output["duration_init_m"] + output["proj_m"] - 1) // 12
    )

    output["age_y_80"] = output["age_y"].clip(upper=79)

    output = pd.merge(
        output,
        wop_rates,
        left_on=["wop_rates_id", "age_y_80", "projection_yr"],
        right_on=["wop_rates_id", "age_y_80", "PROJ_YR"],
    )

    ri_rates_pivot = ri_rates.pivot(
        index=["ri_rates_id", "age_y_80"],
        columns="Variable_Name",
        values="ri_rate",
    )

    output = pd.merge(
        output,
        ri_rates_pivot,
        left_on=["ri_rates_id", "age_y_80"],
        right_index=True,
        how="left",
    )

    output.rename(
        columns={col: f"{col}" for col in ri_rates_pivot.columns},
        inplace=True,
    )

    output.drop(["age_y_80"], axis=1, inplace=True)

    return output
