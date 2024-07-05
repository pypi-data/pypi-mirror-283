from furtheredge.abstracted_packages import furtheredge_numpy as np
from furtheredge.abstracted_packages import furtheredge_pandas as pd


def duration_calculation(merged_df, persistency_rate=1):
    """
    Perform duration calculation for the given DataFrame by applying various
    calculation functions and adding new columns with the results.

    Args:
        merged_df (pandas.DataFrame): Input DataFrame containing policy and financial data.
        persistency_rate (float, optional): Rate of persistency to be applied. Default is 1.

    Returns:
        pandas.DataFrame: DataFrame with additional columns calculated based on input data.
    """

    print("Duration calculation")

    merged_df["persistency_rt"] = 1

    merged_df["fundav_ind"] = 1

    merged_df["proj_init_m"] = projected_months_from_inception(merged_df)

    merged_df["proj_init_y"] = projection_years_from_inception(merged_df)

    merged_df["payment_ind"] = payment_indicator(merged_df)

    merged_df["inforce_ind"] = indicator_policy_inforce(merged_df)

    merged_df["paid_premium_amt"] = paid_premium_amount(
        merged_df, persistency_rate
    )

    merged_df["fee_amt"] = fees_amount(merged_df)

    merged_df["acq_loading_amt"] = acquisition_loading_amount(merged_df)

    merged_df["net_paid_premium_amt"] = net_paid_premium_amount(merged_df)

    merged_df["adjusted_qx_death_rt"] = adjusted_qx_death(merged_df)

    merged_df["adjusted_qx_ptd_acc_rt"] = adjusted_qx_ptd(merged_df)

    merged_df["adjusted_qx_ptd_add_rt"] = adjusted_qx_ptd_additional(merged_df)

    merged_df["adjusted_qx_ci_add_rt"] = (
        adjusted_qx_critical_illness_additional(merged_df)
    )

    merged_df["adjusted_qx_ppd_rt"] = adjusted_qx_ppd(merged_df)

    merged_df["adjusted_qx_abd_rt"] = adjusted_qx_adb(merged_df)

    merged_df["adjusted_qx_wop_rt"] = adjusted_qx_wop(merged_df)

    merged_df["adjusted_qx_ci_acc_rt"] = (
        adjusted_qx_critical_illness_accelerated(merged_df)
    )

    return merged_df


def projected_months_from_inception(merged_df):
    """
    Calculate the projected months from inception.

    This function computes the projected months from inception by adding the
    'proj_m' column values to the 'duration_init_m' column values.

    Parameters:
    - merged_df (pd.DataFrame): DataFrame containing the 'proj_m' and 'duration_init_m' columns.

    Returns:
    - pd.Series: Series containing the calculated projected months from inception.
    """

    proj_m = merged_df["proj_m"]
    duration_init_m = merged_df["duration_init_m"]

    return proj_m + duration_init_m


def projection_years_from_inception(merged_df):
    """
    Calculate projection years from inception.

    This function computes the projection years from inception by dividing
    the 'proj_init_m' column values by 12 and rounding up to the nearest whole number.

    Parameters:
    - merged_df (pd.DataFrame): DataFrame containing the 'proj_init_m' column.

    Returns:
    - pd.Series: Series containing the calculated projection years from inception.
    """

    proj_init_y = np.ceil(merged_df["proj_init_m"] / 12)

    return proj_init_y


def payment_indicator(merged_df):
    """
    Calculate the payment indicator for each row in the DataFrame based on payment months.

    Args:
        merged_df (pandas.DataFrame): Input DataFrame containing policy data.

    Returns:
        pandas.Series: Series containing payment indicators for each row.
    """

    proj_month = merged_df["proj_date"].dt.month

    inception_month = merged_df["inception_date"].dt.month

    payment_mode = merged_df["payment_mode"]

    before_end_payment_date = (
        merged_df["proj_date"] < merged_df["end_payment_date"]
    )

    payment_indicator = np.where(
        ((proj_month - inception_month) * payment_mode / 12) % 1 == 0, 1, 0
    ) * np.where(before_end_payment_date, 1, 0)

    return payment_indicator


def indicator_policy_inforce(merged_df):
    """
    Calculate the policy in-force indicator for each row in the DataFrame.

    Args:
        merged_df (pandas.DataFrame): Input DataFrame containing policy data.

    Returns:
        pandas.Series: Series containing in-force indicators for each row.
    """

    before_maturity_date = merged_df["proj_date"] <= merged_df["maturity_date"]

    indicator = np.where(before_maturity_date, 1, 0)

    return indicator


def paid_premium_amount(merged_df, persistency_rate=1):
    """
    Calculate the paid premium amount for each modelpoint in the DataFrame.

    Args:
        merged_df (pandas.DataFrame): Input DataFrame containing policy data.
        persistency_rate (float, optional): Rate of persistency to be applied. Default is 1.

    Returns:
        pandas.Series: Series containing premium durations for each row.
    """

    return (
        merged_df["modal_premium_amt"]
        * merged_df["payment_ind"]
        * merged_df["inforce_ind"]
        * persistency_rate
    )


def fees_amount(merged_df):
    """
    Calculate the fees amount for each row in the DataFrame.

    Args:
        merged_df (pandas.DataFrame): Input DataFrame containing policy data.

    Returns:
        pandas.Series: Series containing fees amounts for each row.
    """

    sa_death = merged_df["sa_death_amt"]
    sa_loading_pm = merged_df["sa_loading_pm"]

    return sa_death * merged_df["inforce_ind"] * ((sa_loading_pm / 1000) / 12)


def acquisition_loading_amount(merged_df):
    """
    Calculate the acquisition loading for each row in the DataFrame.

    Args:
        merged_df (pandas.DataFrame): Input DataFrame containing policy data.

    Returns:
        pandas.Series: Series containing acquisition loadings for each row.
    """

    return (
        merged_df["modal_premium_amt"]
        * merged_df["prem_loading_pc"]
        * merged_df["payment_ind"]
    )


def net_paid_premium_amount(output):
    """
    Calculate the premium allocation amount duration for each row in the DataFrame.

    Args:
        merged_df (pandas.DataFrame): Input DataFrame containing policy data.

    Returns:
        pandas.Series: Series containing premium allocation amounts for each row.
    """

    return (
        output["paid_premium_amt"]
        - output["fee_amt"]
        - output["acq_loading_amt"]
    )


def adjusted_qx_death(merged_df):
    """
    Calculate the probability of death for each row in the DataFrame.

    Args:
        merged_df (pandas.DataFrame): Input DataFrame containing policy data.

    Returns:
        pandas.Series: Series containing probabilities of death for each row.
    """
    return (
        merged_df["coi_pc"]
        * ((merged_df["qx_death_rt"] / 1000) / 12)
        * merged_df["inforce_ind"]
        * (1 + merged_df["death_xprem_pc"])
    )


def adjusted_qx_ptd(merged_df):
    """
    Calculate the probability of total and permanent disability (TPD) for each row in the DataFrame.

    Args:
        merged_df (pandas.DataFrame): Input DataFrame containing policy data.

    Returns:
        pandas.Series: Series containing probabilities of TPD for each row.
    """
    cover_tpd_rate = merged_df["qx_ptd_acc_rt"]
    coi_pc = merged_df["coi_pc"]
    sa_cov2_amt = merged_df["sa_tpd_amt"]
    sa_cov2_pc = sa_cov2_amt != 0

    return (
        coi_pc
        * ((cover_tpd_rate / 1000) / 12)
        * merged_df["inforce_ind"]
        * sa_cov2_pc
    )


def adjusted_qx_ptd_additional(merged_df):
    """
    Calculate the probability of additional total and permanent disability (TPD) for each row in the DataFrame.

    Args:
        merged_df (pandas.DataFrame): Input DataFrame containing policy data.

    Returns:
        pandas.Series: Series containing probabilities of additional TPD for each row.
    """

    cover_tpd_add_rate = merged_df["qx_ptd_add_rt"]
    coi_pc = merged_df["coi_pc"]
    sa_cov3_amt = merged_df["sa_tpd_add_amt"]
    sa_cov3_pc = sa_cov3_amt != 0

    return (
        coi_pc
        * ((cover_tpd_add_rate / 1000) / 12)
        * merged_df["inforce_ind"]
        * sa_cov3_pc
    )


def adjusted_qx_critical_illness_additional(merged_df):
    """
    Calculate the probability of additional critical illness for each row in the DataFrame.

    Args:
        merged_df (pandas.DataFrame): Input DataFrame containing policy data.

    Returns:
        pandas.Series: Series containing probabilities of additional critical illness for each row.
    """

    cover_critical_illness_add_rate = merged_df["qx_ci_add_rt"]

    coi_pc = merged_df["coi_pc"]
    sa_cov4_pc = merged_df["sa_ci_add_amt"] != 0

    return (
        coi_pc
        * ((cover_critical_illness_add_rate / 1000) / 12)
        * merged_df["inforce_ind"]
        * sa_cov4_pc
    )


def adjusted_qx_ppd(merged_df):
    """
    Calculate the probability of partial and permanent disability (PPD) for each row in the DataFrame.

    Args:
        merged_df (pandas.DataFrame): Input DataFrame containing policy data.

    Returns:
        pandas.Series: Series containing probabilities of PPD for each row.
    """

    cover_ppd_rate = merged_df["qx_ppd_rt"]
    coi_pc = merged_df["coi_pc"]
    sa_cov6_pc = merged_df["sa_ppd_amt"] != 0

    return (
        coi_pc
        * ((cover_ppd_rate / 1000) / 12)
        * merged_df["inforce_ind"]
        * sa_cov6_pc
    )


def adjusted_qx_adb(merged_df):
    """
    Calculate the probability of accidental death benefit (ADB) for each row
    in the output DataFrame based on model points.

    Returns:
        pandas.Series: Series containing the probability of accidental death benefit (ADB)
        for each row in the output DataFrame.
    """

    cover_adb_rate = merged_df["qx_adb_rt"]
    coi_pc = merged_df["coi_pc"]
    sa_cov7_pc = merged_df["sa_adb_amt"] != 0

    return (
        coi_pc
        * ((cover_adb_rate / 1000) / 12)
        * merged_df["inforce_ind"]
        * sa_cov7_pc
    )


def adjusted_qx_wop(merged_df):
    """
    Calculate the probability of waiver of premium (WOP) for each row
    in the output DataFrame based on model points.

    Returns:
        pandas.Series: Series containing the probability of waiver of premium (WOP)
        for each row in the output DataFrame.
    """

    wop_rate = merged_df["qx_wop_rt"]
    coi_pc = merged_df["coi_pc"]
    sa_wop_amt = merged_df["sa_wop_amt"] != 0

    return (
        coi_pc
        * ((wop_rate / 1000) / 12)
        * merged_df["inforce_ind"]
        * sa_wop_amt
    )


def adjusted_qx_critical_illness_accelerated(merged_df):
    """
    Calculate the probability of accelerated critical illness for each row
    in the output DataFrame based on model points.

    Returns:
        pandas.Series: Series containing the probability of accelerated critical illness
        for each row in the output DataFrame.
    """

    cover_critical_illness_acc_rate = merged_df["qx_ci_acc_rt"]
    coi_pc = merged_df["coi_pc"]
    sa_cov10_pc = merged_df["sa_ci_acc_amt"] != 0

    return (
        coi_pc
        * ((cover_critical_illness_acc_rate / 1000) / 12)
        * merged_df["inforce_ind"]
        * sa_cov10_pc
    )
