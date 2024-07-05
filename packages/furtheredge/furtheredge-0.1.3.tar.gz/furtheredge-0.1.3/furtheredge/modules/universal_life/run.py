from furtheredge.modules.universal_life.sub_modules._1_duration import (
    duration_calculation,
)
from furtheredge.modules.universal_life.sub_modules._2_reserve import (
    reserve_calculation_apply,
)
from furtheredge.modules.universal_life.sub_modules._3_proba import (
    proba_calculation,
)
from furtheredge.modules.universal_life.sub_modules._4_prospective import (
    prospective_calculation,
)
from furtheredge.modules.universal_life.required_data_calculation import (
    required_columns_duration,
    required_columns_proba,
    required_columns_prospective,
    required_columns_reserve,
)
from furtheredge.modules.validator_dfs import check_columns_existence
import time

dict_functions_mapping = {
    "duration": duration_calculation,
    "reserve": reserve_calculation_apply,
    "proba": proba_calculation,
    "prospective": prospective_calculation,
}


def sub_module_process(
    merged_df,
    required_columns,
    not_found_columns,
    sub_module_name,
):
    """
    Process a specific submodule operation on a DataFrame based on its name, if it exists in the function mapping.

    This function checks for the existence of required columns in the merged DataFrame, then applies the
    corresponding submodule function if it exists in the function mapping. Updates the not_found_columns list
    with any missing columns information.

    Parameters:
    - merged_df (pd.DataFrame): The DataFrame to process.
    - required_columns (list): List of columns required by the submodule function.
    - not_found_columns (list): List to append missing column information.
    - sub_module_name (str): Name of the submodule function to apply.

    Returns:
    - tuple: Updated not_found_columns list and the processed DataFrame (merged_df).
    """
    validator, not_found_columns_process = check_columns_existence(
        merged_df, required_columns
    )

    if sub_module_name in dict_functions_mapping:
        if validator:
            merged_df = dict_functions_mapping[sub_module_name](merged_df)
            not_found_columns.append(
                {
                    "process_name": sub_module_name,
                    "columns_not_found": not_found_columns_process,
                }
            )
        else:
            not_found_columns.append(
                {
                    "process_name": sub_module_name,
                    "columns_not_found": not_found_columns_process,
                }
            )
    return not_found_columns, merged_df


def universal_life_module(output, show_excecution_time=True):
    """
    Orchestrates the execution of several submodule processes on the output DataFrame.

    Processes include duration, reserve, proba, and prospective, each checking for required columns
    and appending any missing column information to not_found_columns.

    Parameters:
    - output (pd.DataFrame): DataFrame to process.

    Returns:
    - tuple: Processed output DataFrame and not_found_columns list.
    """

    not_found_columns = []
    start_time = time.time()
    not_found_columns, output = sub_module_process(
        output,
        required_columns_duration,
        not_found_columns,
        "duration",
    )
    end_time = time.time()
    execution_time = end_time - start_time
    if show_excecution_time:
        print("Execution time duration:", execution_time, "seconds")

    start_time = time.time()

    not_found_columns, output = sub_module_process(
        output,
        required_columns_reserve,
        not_found_columns,
        "reserve",
    )

    end_time = time.time()
    execution_time = end_time - start_time
    if show_excecution_time:
        print("Execution time reserve:", execution_time, "seconds")

    start_time = time.time()
    not_found_columns, output = sub_module_process(
        output,
        required_columns_proba,
        not_found_columns,
        "proba",
    )

    end_time = time.time()
    execution_time = end_time - start_time
    if show_excecution_time:
        print("Execution time proba:", execution_time, "seconds")

    start_time = time.time()
    not_found_columns, output = sub_module_process(
        output,
        required_columns_prospective,
        not_found_columns,
        "prospective",
    )
    end_time = time.time()
    execution_time = end_time - start_time
    if show_excecution_time:
        print("Execution time prospective:", execution_time, "seconds")

    return output, not_found_columns
