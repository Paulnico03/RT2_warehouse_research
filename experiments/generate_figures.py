from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


RESULTS_FILE = Path(
    "data/final/final_results.csv"
)

OUTPUT_DIR = Path(
    "data/processed/figures"
)


def condition_label(row):
    return (
        f"{int(row['num_packages'])} pkg\n"
        f"{row['deadline_mode']}\n"
        f"{row['layout_mode']}"
    )


def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = pd.read_csv(RESULTS_FILE)

    df["solved_bool"] = (
        df["status"] == "solved"
    )

    # =====================================================
    # FIGURE 1: SUCCESS RATE
    # =====================================================

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
        .mean()
        .mul(100)
        .reset_index(
            name="success_rate"
        )
    )

    conditions = (
        success[
            [
                "num_packages",
                "deadline_mode",
                "layout_mode",
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    labels = [
        condition_label(row)
        for _, row in conditions.iterrows()
    ]

    cap1_values = []
    cap2_values = []

    for _, condition in conditions.iterrows():

        subset = success[
            (
                success["num_packages"]
                == condition["num_packages"]
            )
            & (
                success["deadline_mode"]
                == condition["deadline_mode"]
            )
            & (
                success["layout_mode"]
                == condition["layout_mode"]
            )
        ]

        cap1_values.append(
            subset[
                subset["capacity"] == 1
            ]["success_rate"].iloc[0]
        )

        cap2_values.append(
            subset[
                subset["capacity"] == 2
            ]["success_rate"].iloc[0]
        )

    x = np.arange(len(labels))
    width = 0.36

    plt.figure(
        figsize=(12, 6)
    )

    plt.bar(
        x - width / 2,
        cap1_values,
        width,
        label="Capacity 1",
    )

    plt.bar(
        x + width / 2,
        cap2_values,
        width,
        label="Capacity 2",
    )

    plt.ylabel("Success rate (%)")
    plt.xlabel("Experimental condition")
    plt.title(
        "Planning Success Rate by "
        "Experimental Condition"
    )

    plt.xticks(
        x,
        labels,
        rotation=0,
    )

    plt.ylim(0, 110)
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR
        / "success_rate_by_condition.png",
        dpi=300,
    )

    plt.close()

    # =====================================================
    # SELECT SCENARIOS SOLVED BY BOTH CAPACITIES
    # =====================================================

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

    # =====================================================
    # FIGURE 2: MEAN MAKESPAN
    # =====================================================

    makespan = (
        both.groupby(
            [
                "num_packages",
                "deadline_mode",
                "layout_mode",
                "capacity",
            ]
        )
        ["makespan"]
        .mean()
        .reset_index()
    )

    cap1_values = []
    cap2_values = []

    for _, condition in conditions.iterrows():

        subset = makespan[
            (
                makespan["num_packages"]
                == condition["num_packages"]
            )
            & (
                makespan["deadline_mode"]
                == condition["deadline_mode"]
            )
            & (
                makespan["layout_mode"]
                == condition["layout_mode"]
            )
        ]

        cap1_values.append(
            subset[
                subset["capacity"] == 1
            ]["makespan"].iloc[0]
        )

        cap2_values.append(
            subset[
                subset["capacity"] == 2
            ]["makespan"].iloc[0]
        )

    plt.figure(
        figsize=(12, 6)
    )

    plt.bar(
        x - width / 2,
        cap1_values,
        width,
        label="Capacity 1",
    )

    plt.bar(
        x + width / 2,
        cap2_values,
        width,
        label="Capacity 2",
    )

    plt.ylabel("Mean makespan")
    plt.xlabel("Experimental condition")
    plt.title(
        "Mean Makespan for Scenarios "
        "Solved by Both Capacities"
    )

    plt.xticks(
        x,
        labels,
        rotation=0,
    )

    plt.legend()
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR
        / "makespan_by_condition.png",
        dpi=300,
    )

    plt.close()

    # =====================================================
    # FIGURE 3: EXPANDED NODES
    # ALL 160 PAIRED SCENARIOS
    # =====================================================

    node_data = []

    labels_box = []

    for capacity in [1, 2]:

        values = df[
            df["capacity"] == capacity
        ]["expanded_nodes"]

        node_data.append(values)

        labels_box.append(
            f"Capacity {capacity}"
        )

    plt.figure(
        figsize=(7, 6)
    )

    plt.boxplot(
        node_data,
        labels=labels_box,
        showfliers=False,
    )

    plt.yscale("log")

    plt.ylabel(
        "Expanded nodes (log scale)"
    )

    plt.title(
        "Search Effort Across All Scenarios"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR
        / "expanded_nodes_boxplot.png",
        dpi=300,
    )

    plt.close()

    # =====================================================
    # FIGURE 4: PAIRED MAKESPAN DIFFERENCE
    # =====================================================

    cap1 = (
        both[both["capacity"] == 1]
        .set_index("scenario_id")
    )

    cap2 = (
        both[both["capacity"] == 2]
        .set_index("scenario_id")
    )

    diff = pd.DataFrame(
        index=solved_ids
    )

    diff["difference"] = (
        cap1["makespan"]
        - cap2["makespan"]
    )

    plt.figure(
        figsize=(8, 5)
    )

    counts = (
        diff["difference"]
        .value_counts()
        .sort_index()
    )

    plt.bar(
        counts.index.astype(str),
        counts.values,
    )

    plt.xlabel(
        "Makespan reduction "
        "(capacity 1 - capacity 2)"
    )

    plt.ylabel(
        "Number of paired scenarios"
    )

    plt.title(
        "Distribution of Paired "
        "Makespan Improvements"
    )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR
        / "paired_makespan_reduction.png",
        dpi=300,
    )

    plt.close()

    print(
        "Figures saved to:",
        OUTPUT_DIR,
    )

    for path in sorted(
        OUTPUT_DIR.glob("*.png")
    ):
        print(" -", path)


if __name__ == "__main__":
    main()
