from furtheredge.abstracted_packages import furtheredge_numpy as np
from furtheredge.abstracted_packages import furtheredge_pandas as pd
from furtheredge.modules.model_point_generator.policies_refinement import (
    load_rename_policies_columns,
)


def generate_model_points(policies, run_settings):
    """
    Generate model points from a given policies DataFrame and run settings.

    This function processes the policies DataFrame based on the provided run settings,
    constructs a pivot table, and generates model points.

    Parameters:
    - policies (pd.DataFrame): DataFrame containing policy data.
    - run_settings (dict): Dictionary containing run settings, including pivot configuration.

    Returns:
    - pd.DataFrame: DataFrame containing the generated model points with an additional 'mp_id' column.

    """

    index_list = []
    values_dict = {}
    modelpoints = pd.DataFrame()
    pivot_config = run_settings["pivot_config"]

    policies = load_rename_policies_columns(policies, run_settings)

    for col, agg_func in pivot_config.items():
        if (col not in policies.columns) and (agg_func != "NOT_USED"):
            print(
                f"Warning: '{col}' is not present in the Policies DataFrame."
            )
            continue

        if agg_func.startswith("USED_DIRECT"):
            index_list.append(col)
        elif agg_func.startswith("USED_AGG"):
            agg_type = agg_func.split("_")[2]
            values_dict[col] = agg_type.lower()

    if len(index_list) > 0:
        modelpoints = policies.pivot_table(
            index=index_list,
            values=list(values_dict.keys()),
            aggfunc=values_dict,
        ).reset_index()
    else:
        print("No valid columns found to create a pivot table.")

    modelpoints.insert(0, "mp_id", np.arange(1, len(modelpoints) + 1))

    return modelpoints
