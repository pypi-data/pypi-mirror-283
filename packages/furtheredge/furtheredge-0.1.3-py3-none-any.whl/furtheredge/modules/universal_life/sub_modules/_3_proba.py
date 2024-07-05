from furtheredge.abstracted_packages import furtheredge_pandas as pd
from furtheredge.abstracted_packages import furtheredge_numpy as np


def proba_calculation(merged_df):
    """
    Perform probability calculations for the given DataFrame by applying various
    calculation functions and adding new columns with the results.

    Args:
        merged_df (pandas.DataFrame): Input DataFrame containing policy and financial data.

    Returns:
        pandas.DataFrame: DataFrame with additional columns calculated based on input data.
    """

    print("Proba calculation")

    merged_df["annual_mortality_death_rt"] = annual_mortality_rate_death(
        merged_df
    )

    merged_df["annual_mortality_or_rt"] = annual_mortality_rate_or(merged_df)

    merged_df["annual_mortality_adb_rt"] = annual_mortality_rate_adb(merged_df)

    merged_df["monthly_survival_death_rt"] = monthly_survival_death_rate(
        merged_df
    )

    merged_df["monthly_survival_or_rt"] = monthly_survival_or_rate(merged_df)

    merged_df["monthly_survival_adb_rt"] = monthly_survival_adb_rate(merged_df)

    merged_df["monthly_stay_rt"] = monthly_stay_rate(merged_df)

    merged_df["incremental_survival_rt"] = incremental_survival_rate(merged_df)

    merged_df["cumulative_survival_rt"] = cumulative_survival_rate(merged_df)

    return merged_df


def annual_mortality_rate_death(merged_df):
    """
    Calculate the annual mortality rate due to death for each row in the DataFrame.

    Args:
        merged_df (pandas.DataFrame): Input DataFrame containing policy data.

    Returns:
        pandas.Series: Series containing mortality rates due to death for each row.
    """
    cover_death_rate = merged_df["qx_death_rt"]

    return (
        merged_df["emf"]
        * (cover_death_rate / 1000)
        * merged_df["inforce_ind"]
        * (1 + merged_df["death_xprem_pc"])
    )


def annual_mortality_rate_or(merged_df):
    """
    Calculate the annual OR (Other Riders) mortality rate for each row in the DataFrame by summing up
    various other rates.

    Args:
        merged_df (pandas.DataFrame): Input DataFrame containing policy data.

    Returns:
        pandas.Series: Series containing overall mortality rates for each row.
    """
    return (
        merged_df["adjusted_qx_ptd_acc_rt"]
        + merged_df["adjusted_qx_ptd_add_rt"]
        + merged_df["adjusted_qx_ci_add_rt"]
        + merged_df["adjusted_qx_ppd_rt"]
        + merged_df["adjusted_qx_wop_rt"]
        + merged_df["adjusted_qx_ci_acc_rt"]
    ) * 12


def annual_mortality_rate_adb(merged_df):
    """
    Calculate the annual mortality rate due to accidental death benefit (ADB) for each row in the DataFrame.

    Args:
        merged_df (pandas.DataFrame): Input DataFrame containing policy data.

    Returns:
        pandas.Series: Series containing mortality rates due to ADB for each row.
    """
    cover_adb_rate = merged_df["qx_adb_rt"]

    sa_adb_amt = merged_df["sa_adb_amt"]

    return (
        (cover_adb_rate / 1000) * merged_df["inforce_ind"] * (sa_adb_amt != 0)
    )


def monthly_survival_death_rate(merged_df):
    """
    Calculate the monthly survival rate based on annual mortality death rate.

    This function computes the monthly survival rate using the annual mortality death rate
    from the input DataFrame. The formula used assumes a constant monthly survival rate
    derived from the annual rate.

    Parameters:
    - merged_df (pd.DataFrame): DataFrame containing 'annual_mortality_death_rt' column.

    Returns:
    - float: Monthly survival rate.
    """

    annual_mortality_death_rate = merged_df["annual_mortality_death_rt"]

    return (1 - annual_mortality_death_rate) ** (1 / 12)


def monthly_survival_or_rate(merged_df):
    """
    Calculate the monthly survival rate based on annual mortality for other riders rate.

    This function computes the monthly survival rate using the annual mortality for other riders rate
    from the input DataFrame. The formula used assumes a constant monthly survival rate
    derived from the annual rate.

    Parameters:
    - merged_df (pd.DataFrame): DataFrame containing 'annual_mortality_or_rt' column.

    Returns:
    - float: Monthly survival rate.
    """

    annual_mortality_or_rate = merged_df["annual_mortality_or_rt"]

    return (1 - annual_mortality_or_rate) ** (1 / 12)


def monthly_survival_adb_rate(merged_df):
    """
    Calculate the monthly survival rate based on annual mortality for accelerated death benefits (ADB) rate.

    This function computes the monthly survival rate using the annual mortality for accelerated death benefits (ADB) rate
    from the input DataFrame. The formula used assumes a constant monthly survival rate
    derived from the annual rate.

    Parameters:
    - merged_df (pd.DataFrame): DataFrame containing 'annual_mortality_adb_rt' column.

    Returns:
    - float: Monthly survival rate.
    """

    annual_mortality_adb_rate = merged_df["annual_mortality_adb_rt"]

    return (1 - annual_mortality_adb_rate) ** (1 / 12)


def monthly_stay_rate(merged_df):
    """
    Calculate the monthly stay (or lapse) rate based on annual lapse rate.

    This function computes the monthly stay (or lapse) rate using the annual lapse rate
    from the input DataFrame. The formula used assumes a constant monthly stay rate
    derived from the annual rate.

    Parameters:
    - merged_df (pd.DataFrame): DataFrame containing 'annual_lapse_rt' column.

    Returns:
    - float: Monthly stay (or lapse) rate.
    """

    annual_lapse_rate = merged_df["annual_lapse_rt"]

    return (1 - annual_lapse_rate) ** (1 / 12)


def incremental_survival_rate(merged_df):
    """
    Calculate the incremental survival rate based on monthly survival rates and stay rate.

    This function computes the incremental survival rate using the monthly survival rates
    for death, other riders, accelerated death benefits (ADB), and the monthly stay rate
    from the input DataFrame. The formula used assumes multiplication of these rates to
    compute the overall incremental survival rate.

    Parameters:
    - merged_df (pd.DataFrame): DataFrame containing columns 'monthly_survival_death_rt',
                                'monthly_survival_or_rt', 'monthly_survival_adb_rt',
                                and 'monthly_stay_rt'.

    Returns:
    - float: Incremental survival rate.
    """
    monthly_survival_death_rate = merged_df["monthly_survival_death_rt"]
    monthly_survival_or_rate = merged_df["monthly_survival_or_rt"]
    monthly_survival_adb_rate = merged_df["monthly_survival_adb_rt"]
    monthly_stay_rate = merged_df["monthly_stay_rt"]

    return (
        monthly_survival_death_rate
        * monthly_survival_or_rate
        * monthly_survival_adb_rate
        * monthly_stay_rate
    )


def cumulative_survival_rate(merged_df):
    """
    Calculate the cumulative survival rate based on incremental survival rates.

    This function computes the cumulative survival rate using the incremental survival rates
    calculated for each policy (mp_id) in the input DataFrame. The cumulative survival rate
    is the cumulative product of incremental survival rates starting from the first month.

    Parameters:
    - merged_df (pd.DataFrame): DataFrame containing 'incremental_survival_rt' column and
                                a grouping column 'mp_id' to identify policies.

    Returns:
    - pd.Series: Series containing cumulative survival rates for each row in the DataFrame.
    """

    merged_df["incremental_survival_prod"] = (
        merged_df.groupby("mp_id")["incremental_survival_rt"]
        .cumprod()
        .shift(1)
        .fillna(1)
    )

    merged_df["cumulative_survival_rt"] = 1
    first_indices = merged_df.groupby("mp_id").head(1).index

    merged_df.loc[first_indices, "cumulative_survival_rt"] = 1

    merged_df["cumulative_survival_rt"] = (
        merged_df.groupby("mp_id")["cumulative_survival_rt"].transform(
            "cumprod"
        )
        * merged_df["incremental_survival_prod"]
    )

    first_indices = merged_df.groupby("mp_id").head(1).index

    merged_df.loc[first_indices, "cumulative_survival_rt"] = 1

    return merged_df["cumulative_survival_rt"]
