from pathlib import Path
import pandas as pd


RESULTS_FILE = Path(
    "data/final/final_results.csv"
)


def main():

    df = pd.read_csv(RESULTS_FILE)

    print("=" * 70)
    print("FINAL DATASET VALIDATION")
    print("=" * 70)

    print()
    print(f"Total runs: {len(df)}")
    print(f"Unique scenarios: {df['scenario_id'].nunique()}")

    print()
    print("Runs by capacity:")
    print(
        df["capacity"]
        .value_counts()
        .sort_index()
    )

    runs_per_scenario = (
        df.groupby("scenario_id")["capacity"]
        .nunique()
    )

    bad_pairs = runs_per_scenario[
        runs_per_scenario != 2
    ]

    print()
    print(
        "Scenarios without both capacities:",
        len(bad_pairs)
    )

    print()
    print("Overall status:")
    print(
        df["status"].value_counts()
    )

    print()
    print("Status by capacity:")
    print(
        pd.crosstab(
            df["capacity"],
            df["status"],
        )
    )

    df["solved"] = (
        df["status"] == "solved"
    )

    success = (
        df.groupby(
            [
                "num_packages",
                "deadline_mode",
                "layout_mode",
                "capacity",
            ]
        )
        ["solved"]
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
    print("=" * 70)
    print("SUCCESS RATE BY CONDITION")
    print("=" * 70)

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

    solved_df = df[
        df["status"] == "solved"
    ].copy()

    metrics = [
        "makespan",
        "plan_length",
        "planning_time_ms",
        "expanded_nodes",
        "states_evaluated",
    ]

    print()
    print("=" * 70)
    print("SOLVED-RUN METRICS BY CAPACITY")
    print("=" * 70)

    summary = (
        solved_df
        .groupby("capacity")[metrics]
        .agg(
            [
                "count",
                "mean",
                "std",
                "median",
            ]
        )
    )

    print(summary)

    print()
    print("=" * 70)
    print("MISSING VALUES")
    print("=" * 70)

    print(
        df[metrics]
        .isna()
        .sum()
    )


if __name__ == "__main__":
    main()
