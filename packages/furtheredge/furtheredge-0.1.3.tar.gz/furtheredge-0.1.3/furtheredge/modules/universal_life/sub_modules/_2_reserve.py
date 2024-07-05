from furtheredge.abstracted_packages import furtheredge_numpy as np
from furtheredge.abstracted_packages import furtheredge_pandas as pd
import gc
import time


def reserve_calculation_apply(merged_df, show_excecution_time=True):
    """
    Perform reserve calculations on the merged_df DataFrame.

    Args:
        merged_df (pandas.DataFrame): DataFrame containing merged data,
            including columns necessary for reserve calculations.

    Returns:
        pandas.DataFrame: DataFrame with additional columns for reserve calculations.
    """
    print("Reserve calculation")

    merged_df["premium_alloc_amt"] = premium_allocation_amount_res(merged_df)

    merged_df = process_sar_death_sar_adb_fund_value_av_fund_value(merged_df)

    merged_df["fund1_interest_amt"] = fund1_interest_amount(merged_df)

    return merged_df


def premium_allocation_amount_res(merged_df):
    """
    Calculate the premium allocation amount for reserves.

    Args:
        merged_df (pandas.DataFrame): DataFrame containing merged data.

    Returns:
        pandas.Series: Series containing the premium allocation amount for reserves.
    """
    return merged_df["net_paid_premium_amt"]


def _sar_death_education(merged_df_origin):
    merged_df = merged_df_origin.copy()
    merged_df["monthly_interest_rt"] = (1 + merged_df["interest_rt"]) ** (
        1 / 12
    ) - 1
    merged_df["discount_factor"] = 1 / (
        (1 + merged_df["monthly_interest_rt"]) ** (merged_df["proj_m"])
    )
    merged_df["product_value"] = (
        merged_df["paid_premium_amt"] * merged_df["discount_factor"]
    )

    merged_df = merged_df.iloc[::-1]
    grouped_data = merged_df.groupby("mp_id")
    merged_df["van"] = grouped_data["product_value"].cumsum()
    merged_df = merged_df.iloc[::-1]

    output_temp = pd.DataFrame()
    output_temp["shifted_col"] = (
        merged_df.groupby(["mp_id"])["van"].shift(-1).fillna(0)
    )
    gc.collect()
    return (
        output_temp["shifted_col"]
        * merged_df["inforce_ind"]
        / merged_df["discount_factor"]
    )


# def _sar_death_other(group, previous_av_fund):
#     sa_cov1_amt = group["sa_death_amt"].values
#     return (
#         np.maximum(
#             0,
#             sa_cov1_amt - previous_av_fund - group["premium_alloc_amt"].values,
#         )
#         * group["inforce_ind"].values
#     )


def _sar_death_other(row, previous_av_fund):
    """
    Calculate the Sum at Risk (SAR) for other types of death benefits.

    This function calculates the SAR for other death benefits by subtracting the
    previous account value fund and premium allocation amount from the sum assured
    for death. The result is then multiplied by the inforce indicator.

    Parameters:
    - row (pd.Series): A row from a DataFrame containing necessary columns like
                       'sa_death_amt', 'premium_alloc_amt', and 'inforce_ind'.
    - previous_av_fund (float): The previous account value fund.

    Returns:
    - float: The calculated SAR for other death benefits.
    """
    sa_cov1_amt = row["sa_death_amt"]
    return (
        max(0, sa_cov1_amt - previous_av_fund - row["premium_alloc_amt"])
        * row["inforce_ind"]
    )


def _sar_adb_education(merged_df):
    """
    Retrieve the Sum at Risk (SAR) for Accidental Death Benefit (ADB) education.

    This function returns the SAR for ADB education directly from the 'sar_death_amt' column
    of the provided DataFrame.

    Parameters:
    - merged_df (pd.DataFrame): DataFrame containing the 'sar_death_amt' column.

    Returns:
    - pd.Series: Series containing the SAR for ADB education.
    """
    return merged_df["sar_death_amt"].values


# def _sar_adb_other(group, previous_av_fund):
#     sa_adb_amt = group["sa_adb_amt"].values
#     return (
#         np.maximum(
#             0,
#             sa_adb_amt - previous_av_fund - group["premium_alloc_amt"].values,
#         )
#         * group["inforce_ind"].values
#     )


def _sar_adb_other(row, previous_av_fund):
    """
    Calculate the Sum at Risk (SAR) for other types of Accidental Death Benefit (ADB).

    This function calculates the SAR for other ADB benefits by subtracting the
    previous account value fund and premium allocation amount from the sum assured
    for ADB. The result is then multiplied by the inforce indicator.

    Parameters:
    - row (pd.Series): A row from a DataFrame containing necessary columns like
                       'sa_adb_amt', 'premium_alloc_amt', and 'inforce_ind'.
    - previous_av_fund (float): The previous account value fund.

    Returns:
    - float: The calculated SAR for other ADB benefits.
    """
    sa_adb_amt = row["sa_adb_amt"]
    return (
        max(0, sa_adb_amt - previous_av_fund - row["premium_alloc_amt"])
        * row["inforce_ind"]
    )


def _coi_death(merged_df):
    """
    Calculate Cost of Insurance (COI) for death.

    Args:
        merged_df (pandas.DataFrame): DataFrame containing merged data.

    Returns:
        pandas.Series: Series containing COI for death.
    """
    return (
        merged_df["sar_death_amt"].values
        * merged_df["adjusted_qx_death_rt"].values
    )


def _coi_other_riders(merged_df):
    """
    Calculate Cost of Insurance (COI) for other riders.

    Args:
        merged_df (pandas.DataFrame): DataFrame containing merged data.

    Returns:
        pandas.Series: Series containing COI for other riders.
    """
    return merged_df["sar_death_amt"].values * (
        merged_df["adjusted_qx_ptd_acc_rt"].values
        + merged_df["adjusted_qx_ptd_add_rt"].values
        + merged_df["adjusted_qx_ci_add_rt"].values
        + merged_df["adjusted_qx_ppd_rt"].values
        + merged_df["adjusted_qx_wop_rt"].values
        + merged_df["adjusted_qx_ci_acc_rt"].values
    )


def _coi_adb(merged_df):
    """
    Calculate Cost of Insurance (COI) for ADB.

    Args:
        merged_df (pandas.DataFrame): DataFrame containing merged data.

    Returns:
        pandas.Series: Series containing COI for ADB.
    """
    return (
        merged_df["sar_adb_amt"].values
        * merged_df["adjusted_qx_abd_rt"].values
    )


# def process_education_case(group):

#     fund_values = np.zeros(len(group))
#     av_fund = np.zeros(len(group))
#     fmf_amt = np.zeros(len(group))
#     prev_av_fund = np.zeros(len(group))

#     prev_av_fund_value = 0

#     mask = group["proj_m"] == 0
#     fund_values[mask] = group.loc[mask, "initial_fund1_av_amt"]
#     prev_av_fund_value = fund_values[mask]
#     fund_values[mask] = (
#         group.loc[mask, "premium_alloc_amt"]
#         - group.loc[mask, "coi_death_amt"]
#         - group.loc[mask, "coi_or_amt"]
#         - group.loc[mask, "coi_adb_amt"]
#         + prev_av_fund_value
#     ) * group.loc[mask, "inforce_ind"]
#     fmf_amt[mask] = (group.loc[mask, "fmf_pc"] * fund_values[mask]) / 12
#     av_fund[mask] = (fund_values[mask] - fmf_amt[mask]) * (
#         1 + group.loc[mask, "guaranteed_interest_rt"]
#     ) ** (1 / 12)

#     mask = group["proj_m"] != 0
#     fund_values[mask] = (
#         group.loc[mask, "premium_alloc_amt"]
#         - group.loc[mask, "coi_death_amt"]
#         - group.loc[mask, "coi_or_amt"]
#         - group.loc[mask, "coi_adb_amt"]
#         + prev_av_fund_value
#     ) * group.loc[mask, "inforce_ind"]
#     fmf_amt[mask] = (group.loc[mask, "fmf_pc"] * fund_values[mask]) / 12
#     av_fund[mask] = (fund_values[mask] - fmf_amt[mask]) * (
#         1 + group.loc[mask, "guaranteed_interest_rt"]
#     ) ** (1 / 12)

#     prev_av_fund[1:] = av_fund[:-1]
#     prev_av_fund[0] = group.iloc[0]["initial_fund1_av_amt"]

#     group["fund1_value_amt"] = fund_values
#     group["fund1_av_amt"] = av_fund
#     group["fmf_amt"] = fmf_amt
#     group["prev_fund1_av_amt"] = prev_av_fund
#     return group


def process_education_case(group):
    """
    Process education case data for calculating fund values, account values, and related amounts.

    This function iterates over each row in the provided group DataFrame to calculate
    fund values, account values, fund management fee amounts, and previous account values
    based on the given calculations.

    Parameters:
    - group (pd.DataFrame): A group DataFrame containing necessary columns like
                            'proj_m', 'initial_fund1_av_amt', 'premium_alloc_amt',
                            'coi_death_amt', 'coi_or_amt', 'coi_adb_amt', 'inforce_ind',
                            'fmf_pc', 'guaranteed_interest_rt'.

    Returns:
    - pd.DataFrame: DataFrame with added columns 'fund1_value_amt', 'fund1_av_amt',
                    'fmf_amt', 'prev_fund1_av_amt' containing calculated values for each row.
    """
    fund_values = []
    av_fund = []
    fmf_amt = []
    prev_av_fund = []
    prev_av_fund_value = 0

    for index, row in group.iterrows():
        if row["proj_m"] == 0:
            fund_value = row["initial_fund1_av_amt"]
            prev_av_fund_value = fund_value
            fund_value = (
                row["premium_alloc_amt"]
                - row["coi_death_amt"]
                - row["coi_or_amt"]
                - row["coi_adb_amt"]
                + prev_av_fund_value
            ) * row["inforce_ind"]
            fmf_amt_value = (row["fmf_pc"] * fund_value) / 12

            av_fund_value = (fund_value - fmf_amt_value) * (
                1 + row["guaranteed_interest_rt"]
            ) ** (1 / 12)
        else:

            fund_value = (
                row["premium_alloc_amt"]
                - row["coi_death_amt"]
                - row["coi_or_amt"]
                - row["coi_adb_amt"]
                + prev_av_fund_value
            ) * row["inforce_ind"]
            fmf_amt_value = (row["fmf_pc"] * fund_value) / 12

            av_fund_value = (fund_value - fmf_amt_value) * (
                1 + row["guaranteed_interest_rt"]
            ) ** (1 / 12)

        fund_values.append(fund_value)
        av_fund.append(av_fund_value)
        fmf_amt.append(fmf_amt_value)
        prev_av_fund.append(prev_av_fund_value)
        prev_av_fund_value = av_fund_value

    group["fund1_value_amt"] = fund_values
    group["fund1_av_amt"] = av_fund
    group["fmf_amt"] = fmf_amt
    group["prev_fund1_av_amt"] = prev_av_fund
    return group


# def process_other_case(group):
#     num_rows = len(group)
#     fund_values = np.zeros(num_rows)
#     av_fund = np.zeros(num_rows)
#     sar_death_other = np.zeros(num_rows)
#     sar_or_amt = np.zeros(num_rows)
#     sar_adb_other = np.zeros(num_rows)
#     coi_death_amt = np.zeros(num_rows)
#     coi_or_amt = np.zeros(num_rows)
#     coi_adb_amt = np.zeros(num_rows)
#     fmf_amt = np.zeros(num_rows)
#     prev_av_fund = np.zeros(num_rows)

#     prev_av_fund_value = group["initial_fund1_av_amt"].values

#     sar_death_value = _sar_death_other(group, prev_av_fund_value)
#     sar_or_amt_value = sar_death_value
#     sar_adb_value = _sar_adb_other(group, prev_av_fund_value)
#     coi_death_amt_value = (
#         sar_death_value * group["adjusted_qx_death_rt"].values
#     )
#     coi_or_amt_value = sar_or_amt_value * (
#         group["adjusted_qx_ptd_acc_rt"].values
#         + group["adjusted_qx_ptd_add_rt"].values
#         + group["adjusted_qx_ci_add_rt"].values
#         + group["adjusted_qx_ppd_rt"].values
#         + group["adjusted_qx_wop_rt"].values
#         + group["adjusted_qx_ci_acc_rt"].values
#     )
#     coi_adb_amt_value = sar_adb_value * group["adjusted_qx_abd_rt"].values

#     fund_value = (
#         group["premium_alloc_amt"].values
#         - coi_death_amt_value
#         - coi_or_amt_value
#         - coi_adb_amt_value
#         + prev_av_fund_value
#     ) * group["inforce_ind"].values
#     fmf_amt_value = (group["fmf_pc"].values * fund_value) / 12
#     av_fund_value = (fund_value - fmf_amt_value) * (
#         1 + group["guaranteed_interest_rt"].values
#     ) ** (1 / 12)

#     fund_values = fund_value
#     av_fund = av_fund_value
#     sar_death_other = sar_death_value
#     sar_or_amt = sar_or_amt_value
#     sar_adb_other = sar_adb_value
#     coi_death_amt = coi_death_amt_value
#     coi_or_amt = coi_or_amt_value
#     coi_adb_amt = coi_adb_amt_value
#     fmf_amt = fmf_amt_value
#     prev_av_fund = prev_av_fund_value

#     group["fund1_value_amt"] = fund_values
#     group["fund1_av_amt"] = av_fund
#     group["sar_death_amt"] = sar_death_other
#     group["sar_or_amt"] = sar_or_amt
#     group["sar_adb_amt"] = sar_adb_other
#     group["coi_death_amt"] = coi_death_amt
#     group["coi_or_amt"] = coi_or_amt
#     group["coi_adb_amt"] = coi_adb_amt
#     group["fmf_amt"] = fmf_amt
#     group["prev_fund1_av_amt"] = prev_av_fund

#     return group


def process_other_case(group):
    """
    Process other case data for calculating fund values, account values, and related amounts.

    This function iterates over each row in the provided group DataFrame to calculate
    fund values, account values, Sum at Risk (SAR) for death, other amounts like cost of
    insurance (COI), and fund management fee (FMF) amounts based on the given calculations.

    Parameters:
    - group (pd.DataFrame): A group DataFrame containing necessary columns like
                            'proj_m', 'initial_fund1_av_amt', 'premium_alloc_amt',
                            'coi_death_amt', 'coi_or_amt', 'coi_adb_amt', 'inforce_ind',
                            'fmf_pc', 'guaranteed_interest_rt', 'adjusted_qx_death_rt',
                            'adjusted_qx_ptd_acc_rt', 'adjusted_qx_ptd_add_rt',
                            'adjusted_qx_ci_add_rt', 'adjusted_qx_ppd_rt',
                            'adjusted_qx_wop_rt', 'adjusted_qx_ci_acc_rt', 'adjusted_qx_abd_rt'.

    Returns:
    - pd.DataFrame: DataFrame with added columns 'fund1_value_amt', 'fund1_av_amt',
                    'sar_death_amt', 'sar_or_amt', 'sar_adb_amt', 'coi_death_amt',
                    'coi_or_amt', 'coi_adb_amt', 'fmf_amt', 'prev_fund1_av_amt'
                    containing calculated values for each row.
    """
    fund_values = []
    av_fund = []
    sar_death_other = []
    sar_or_amt = []
    sar_adb_other = []
    coi_death_amt = []
    coi_or_amt = []
    coi_adb_amt = []
    fmf_amt = []
    prev_av_fund = []
    prev_av_fund_value = 0
    av_fund_value = 0
    sar_death_value = 0
    sar_or_amt_value = 0
    sar_adb_value = 0
    coi_death_amt_value = 0
    coi_or_amt_value = 0
    coi_adb_amt_value = 0
    fmf_amt_value = 0
    for index, row in group.iterrows():
        if row["proj_m"] == 0:
            fund_value = row["initial_fund1_av_amt"]
            prev_av_fund_value = fund_value
            sar_death_value = _sar_death_other(row, prev_av_fund_value)
            sar_or_amt_value = sar_death_value
            sar_adb_value = _sar_adb_other(row, prev_av_fund_value)
            coi_death_amt_value = sar_death_value * row["adjusted_qx_death_rt"]
            coi_or_amt_value = sar_or_amt_value * (
                row["adjusted_qx_ptd_acc_rt"]
                + row["adjusted_qx_ptd_add_rt"]
                + row["adjusted_qx_ci_add_rt"]
                + row["adjusted_qx_ppd_rt"]
                + row["adjusted_qx_wop_rt"]
                + row["adjusted_qx_ci_acc_rt"]
            )
            coi_adb_amt_value = sar_adb_value * row["adjusted_qx_abd_rt"]
            fund_value = (
                row["premium_alloc_amt"]
                - coi_death_amt_value
                - coi_or_amt_value
                - coi_adb_amt_value
                + prev_av_fund_value
            ) * row["inforce_ind"]
            fmf_amt_value = (row["fmf_pc"] * fund_value) / 12
            av_fund_value = (fund_value - fmf_amt_value) * (
                1 + row["guaranteed_interest_rt"]
            ) ** (1 / 12)

        else:
            sar_death_value = _sar_death_other(row, prev_av_fund_value)
            sar_or_amt_value = sar_death_value
            sar_adb_value = _sar_adb_other(row, prev_av_fund_value)
            coi_death_amt_value = sar_death_value * row["adjusted_qx_death_rt"]
            coi_or_amt_value = sar_or_amt_value * (
                row["adjusted_qx_ptd_acc_rt"]
                + row["adjusted_qx_ptd_add_rt"]
                + row["adjusted_qx_ci_add_rt"]
                + row["adjusted_qx_ppd_rt"]
                + row["adjusted_qx_wop_rt"]
                + row["adjusted_qx_ci_acc_rt"]
            )
            coi_adb_amt_value = sar_adb_value * row["adjusted_qx_abd_rt"]
            fund_value = (
                row["premium_alloc_amt"]
                - coi_death_amt_value
                - coi_or_amt_value
                - coi_adb_amt_value
                + prev_av_fund_value
            ) * row["inforce_ind"]
            fmf_amt_value = (row["fmf_pc"] * fund_value) / 12
            av_fund_value = (fund_value - fmf_amt_value) * (
                1 + row["guaranteed_interest_rt"]
            ) ** (1 / 12)

        fund_values.append(fund_value)
        av_fund.append(av_fund_value)
        sar_death_other.append(sar_death_value)
        sar_or_amt.append(sar_or_amt_value)
        sar_adb_other.append(sar_adb_value)
        coi_death_amt.append(coi_death_amt_value)
        coi_or_amt.append(coi_or_amt_value)
        coi_adb_amt.append(coi_adb_amt_value)
        fmf_amt.append(fmf_amt_value)
        prev_av_fund.append(prev_av_fund_value)

        prev_av_fund_value = av_fund_value

    group["fund1_value_amt"] = fund_values
    group["fund1_av_amt"] = av_fund
    group["sar_death_amt"] = sar_death_other
    group["sar_or_amt"] = sar_or_amt
    group["sar_adb_amt"] = sar_adb_other
    group["coi_death_amt"] = coi_death_amt
    group["coi_or_amt"] = coi_or_amt
    group["coi_adb_amt"] = coi_adb_amt
    group["fmf_amt"] = fmf_amt
    group["prev_fund1_av_amt"] = prev_av_fund

    return group


def process_sar_death_sar_adb_fund_value_av_fund_value(merged_df):
    """
    Process SAR (Sum at Risk) for death, SAR for ADB (Accelerated Death Benefit),
    fund value, and account value calculations based on product type (Education or Other).

    This function separates the input DataFrame into 'Education' and 'Other' product types,
    computes SAR for death and ADB, COI (Cost of Insurance) amounts, and then applies
    appropriate processing functions ('process_education_case' for Education and
    'process_other_case' for Other) to calculate fund values and account values.

    Parameters:
    - merged_df (pd.DataFrame): Merged DataFrame containing data for both Education and Other product types.

    Returns:
    - pd.DataFrame: DataFrame with added columns 'sar_death_amt', 'sar_or_amt', 'sar_adb_amt',
                    'coi_death_amt', 'coi_or_amt', 'coi_adb_amt', 'fund1_value_amt', 'fund1_av_amt',
                    'fmf_amt', 'prev_fund1_av_amt' containing calculated values for each row.
    """
    df_education = merged_df[
        merged_df["product_type"] == "Education"
    ].reset_index(drop=True)
    df_other = merged_df[merged_df["product_type"] != "Education"].reset_index(
        drop=True
    )

    output_result_education = pd.DataFrame()
    output_result_other = pd.DataFrame()

    start_time = time.time()

    if not df_education.empty:
        df_education["sar_death_amt"] = _sar_death_education(df_education)
        df_education["sar_or_amt"] = df_education["sar_death_amt"]
        df_education["sar_adb_amt"] = _sar_adb_education(df_education)

        df_education["coi_death_amt"] = _coi_death(df_education)
        df_education["coi_or_amt"] = _coi_other_riders(df_education)
        df_education["coi_adb_amt"] = _coi_adb(df_education)
        output_result_education = (
            df_education.groupby("mp_id")
            .apply(process_education_case)
            .reset_index(drop=True)
        )
    end_time = time.time()
    execution_time = end_time - start_time
    # print("Execution time reserve education:", execution_time, "seconds")
    start_time = time.time()
    if not df_other.empty:
        output_result_other = (
            df_other.groupby("mp_id")
            .apply(process_other_case)
            .reset_index(drop=True)
        )
    end_time = time.time()
    execution_time = end_time - start_time
    # print("Execution time reserve other:", execution_time, "seconds")
    final_result = pd.concat(
        [output_result_education, output_result_other]
    ).reset_index(drop=True)
    return final_result


def fund1_interest_amount(merged_df):
    """
    Calculate interest.

    Args:
        merged_df (pandas.DataFrame): DataFrame containing merged data.

    Returns:
        pandas.Series: Series containing interest values.
    """
    return (
        merged_df["fund1_av_amt"].values - merged_df["fund1_value_amt"].values
    )
