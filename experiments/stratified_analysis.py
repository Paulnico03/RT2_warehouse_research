from pathlib import Path

import pandas as pd


RESULTS_FILE = Path(
    "data/final/final_results.csv"
)


def main():

    df = pd.read_csv(RESULTS_FILE)

    print("=" * 80)
    print("STRATIFIED FINAL ANALYSIS")
    print("=" * 80)

    df["solved_bool"] = (
        df["status"] == "solved"
    )

    # -----------------------------------------------------
    # SUCCESS RATE BY CONDITION
    # -----------------------------------------------------

    success = (
        df.groupby(
            [
                "num_packages",
                "deadline_mode",
                "layout_mode",
                "capacity",
            ]
        )
        ["solved_bool"]
        .agg(
            trials="count",
            solved="sum",
            success_rate="mean",
        )
        .reset_index()
    )

    success["success_rate_percent"] = (
        success["success_rate"] * 100
    )

    print()
    print("SUCCESS RATE BY CONDITION")
    print("-" * 80)

    print(
        success[
            [
                "num_packages",
                "deadline_mode",
                "layout_mode",
                "capacity",
                "trials",
                "solved",
                "success_rate_percent",
            ]
        ].to_string(index=False)
    )

    # -----------------------------------------------------
    # SOLVED BY BOTH
    # -----------------------------------------------------

    status = df.pivot(
        index="scenario_id",
        columns="capacity",
        values="status",
    )

    solved_ids = status.index[
        (status[1] == "solved")
        & (status[2] == "solved")
    ]

    both = df[
        df["scenario_id"].isin(
            solved_ids
        )
    ].copy()

    # -----------------------------------------------------
    # MEAN METRICS BY CONDITION
    # -----------------------------------------------------

    metrics = [
        "makespan",
        "plan_length",
        "expanded_nodes",
        "states_evaluated",
        "planning_time_ms",
    ]

    summary = (
        both.groupby(
            [
                "num_packages",
                "deadline_mode",
                "layout_mode",
                "capacity",
            ]
        )[metrics]
        .mean()
        .round(2)
        .reset_index()
    )

    print()
    print("MEAN METRICS FOR SCENARIOS SOLVED BY BOTH")
    print("-" * 80)

    print(
        summary.to_string(
            index=False
        )
    )

    # -----------------------------------------------------
    # CAPACITY 1 VS 2 DIFFERENCES
    # -----------------------------------------------------

    print()
    print("PAIRED MEAN DIFFERENCES BY CONDITION")
    print("-" * 80)

    condition_columns = [
        "num_packages",
        "deadline_mode",
        "layout_mode",
    ]

    cap1 = (
        both[both["capacity"] == 1]
        .set_index("scenario_id")
    )

    cap2 = (
        both[both["capacity"] == 2]
        .set_index("scenario_id")
    )

    rows = []

    for scenario_id in solved_ids:

        row1 = cap1.loc[scenario_id]
        row2 = cap2.loc[scenario_id]

        row = {
            "scenario_id": scenario_id,
            "num_packages": row1[
                "num_packages"
            ],
            "deadline_mode": row1[
                "deadline_mode"
            ],
            "layout_mode": row1[
                "layout_mode"
            ],
        }

        for metric in metrics:
            row[f"{metric}_diff"] = (
                row1[metric]
                - row2[metric]
            )

        rows.append(row)

    differences = pd.DataFrame(rows)

    diff_metrics = [
        f"{metric}_diff"
        for metric in metrics
    ]

    diff_summary = (
        differences.groupby(
            condition_columns
        )[diff_metrics]
        .agg(
            ["count", "mean", "median"]
        )
        .round(2)
    )

    print(diff_summary)


if __name__ == "__main__":
    main()
