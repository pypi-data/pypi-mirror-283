from datetime import datetime
from collections import OrderedDict
from furtheredge.abstracted_packages import furtheredge_pandas as pd
from furtheredge.modules.universal_life.run import universal_life_module
from furtheredge.modules.universal_life.merge_all_df import (
    merge_all_dfs_police,
)
from furtheredge.modules.model_point_generator.model_point_generator import (
    generate_model_points,
)
from furtheredge.modules.universal_life.required_data_calculation import (
    required_columns_duration,
    required_columns_reserve,
    required_columns_proba,
    required_columns_prospective,
)


def universal_life(
    policies,
    ri_rates,
    wop_rates,
    tech_assumptions,
    product,
    save_model_points,
    model_points_path,
    proj_columns,
    non_proj_columns,
    run_settings,
    chuck_size=-100,
    projection_points=700,
    show_excecution_time=True,
):
    """
    Perform calculations for a universal life insurance module.

    Parameters:
    - policies (pd.DataFrame): Dataframe containing policies data.
    - ri_rates (pd.DataFrame): Dataframe containing reinsurance rates.
    - wop_rates (pd.DataFrame): Dataframe containing waiver of premium rates.
    - tech_assumptions (pd.DataFrame): Dataframe containing technical assumptions.
    - product (pd.DataFrame): Dataframe containing product information.
    - save_model_points (Boolean): If you want to save model_points file or not.
    - model_points_path (str): Path to save model points CSV file.
    - proj_columns (list): List of columns to include in projected results.
    - non_proj_columns (list): List of columns to include in non-projected results.
    - run_settings (dict): Dictionary containing run settings, including 'projection_date'.
    - chuck_size (int, optional): Size of chunks for processing model points. Defaults to -100.
    - projection_points (int, optional): Number of projection points. Defaults to 700.
    - show_execution_time (bool, optional): Flag indicating whether to display execution times of each submodule. Defaults to True.

    Returns:
    - tuple: Projected results DataFrame, Non-projected results DataFrame, List of not found columns.
    """

    model_points = generate_model_points(policies, run_settings)
    if save_model_points:
        model_points.to_csv(model_points_path, index=False)

    # ----------------------- sample 5 policy per "inception_year" ----------------------------

    # model_points = (
    #     model_points.groupby(
    #         by=["product_type", "payment_mode"], group_keys=False
    #     )
    #     .apply(lambda df: df.sample(5, random_state=42))
    #     .reset_index(drop=True)
    # )

    # -------------------------------------------------------------------------------------

    projection_date = datetime.strptime(
        run_settings["projection_date"], "%d/%m/%Y"
    )

    if chuck_size <= 0:
        output = merge_all_dfs_police(
            model_points,
            ri_rates,
            wop_rates,
            tech_assumptions,
            product,
            projection_date,
            projection_points,
        )

        required_proj_calculation = list(
            OrderedDict.fromkeys(
                required_columns_duration
                + required_columns_reserve
                + required_columns_proba
                + required_columns_prospective
            )
        )

        output = output[required_proj_calculation]

        result_universal_life, not_found_columns = universal_life_module(
            output, show_excecution_time
        )
        not_found_columns_proj = [
            item
            for item in proj_columns
            if item not in result_universal_life.columns
        ]

        not_found_columns_non_proj = [
            item
            for item in non_proj_columns
            if item not in result_universal_life.columns
        ]
        for not_found_col in not_found_columns_proj:
            # result_universal_life[not_found_col] = np.nan
            proj_columns.remove(not_found_col)

        for not_found_col in not_found_columns_non_proj:
            # result_universal_life[not_found_col] = np.nan
            non_proj_columns.remove(not_found_col)

        proj_result, non_proj_result = (
            result_universal_life[proj_columns],
            result_universal_life[non_proj_columns],
        )
        non_proj_result = non_proj_result.drop_duplicates(ignore_index=True)
        return proj_result, non_proj_result, not_found_columns
    else:
        all_result_universal_life = pd.DataFrame()

        for chunk_start in range(0, len(model_points), chuck_size):
            chunk_end = min(chunk_start + chuck_size, len(model_points))
            chunk_model_points = model_points[chunk_start:chunk_end]
            output = merge_all_dfs_police(
                chunk_model_points,
                ri_rates,
                wop_rates,
                tech_assumptions,
                product,
                projection_date,
                projection_points,
            )

            required_proj_calculation = list(
                OrderedDict.fromkeys(
                    required_columns_duration + required_columns_reserve
                )
            )

            output = output[required_proj_calculation]

            result_universal_life, not_found_columns = universal_life_module(
                output, show_excecution_time
            )

            all_result_universal_life = pd.concat(
                [all_result_universal_life, result_universal_life],
                ignore_index=True,
            )

        not_found_columns_proj = [
            item
            for item in proj_columns
            if item not in all_result_universal_life.columns
        ]

        not_found_columns_non_proj = [
            item
            for item in non_proj_columns
            if item not in all_result_universal_life.columns
        ]

        for not_found_col in not_found_columns_proj:
            # all_result_universal_life[not_found_col] = np.nan
            proj_columns.remove(not_found_col)
        for not_found_col in not_found_columns_non_proj:
            # all_result_universal_life[not_found_col] = np.nan
            non_proj_columns.remove(not_found_col)

        proj_result, non_proj_result = (
            all_result_universal_life[proj_columns],
            all_result_universal_life[non_proj_columns],
        )
        non_proj_result.drop_duplicates(inplace=True, ignore_index=True)
        return proj_result, non_proj_result, not_found_columns
