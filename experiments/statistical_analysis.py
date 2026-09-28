from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binomtest, wilcoxon


RESULTS_FILE = Path(
    "data/final/final_results.csv"
)


def print_metric_analysis(
    paired,
    metric,
    label,
):
    cap1 = paired[f"{metric}_cap1"]
    cap2 = paired[f"{metric}_cap2"]

    valid = (
        cap1.notna()
        & cap2.notna()
    )

    x = cap1[valid]
    y = cap2[valid]

    differences = x - y

    print()
    print("-" * 70)
    print(label)
    print("-" * 70)

    print(f"Valid paired observations: {len(x)}")

    print()
    print("Capacity 1:")
    print(f"  mean   = {x.mean():.3f}")
    print(f"  median = {x.median():.3f}")
    print(f"  std    = {x.std():.3f}")

    print()
    print("Capacity 2:")
    print(f"  mean   = {y.mean():.3f}")
    print(f"  median = {y.median():.3f}")
    print(f"  std    = {y.std():.3f}")

    print()
    print("Paired difference (cap1 - cap2):")
    print(
        f"  mean difference   = "
        f"{differences.mean():.3f}"
    )
    print(
        f"  median difference = "
        f"{differences.median():.3f}"
    )

    percentage_reduction = (
        (x - y) / x * 100
    )

    print(
        f"  mean % reduction  = "
        f"{percentage_reduction.mean():.2f}%"
    )

    wins = (y < x).sum()
    ties = (y == x).sum()
    losses = (y > x).sum()

    print()
    print("Pairwise comparison:")
    print(
        f"  capacity 2 lower/better = {wins}"
    )
    print(f"  ties                    = {ties}")
    print(
        f"  capacity 2 higher/worse = {losses}"
    )

    if np.allclose(
        differences.to_numpy(),
        0,
    ):
        print()
        print(
            "Wilcoxon test not applicable: "
            "all paired differences are zero."
        )
        return

    test = wilcoxon(
        x,
        y,
        alternative="two-sided",
        zero_method="wilcox",
    )

    print()
    print("Wilcoxon signed-rank test:")
    print(
        f"  statistic = "
        f"{test.statistic:.3f}"
    )
    print(f"  p-value   = {test.pvalue:.6g}")


def main():

    df = pd.read_csv(RESULTS_FILE)

    print("=" * 70)
    print("PAIRED STATISTICAL ANALYSIS")
    print("=" * 70)

    # =====================================================
    # SOLVABILITY
    # =====================================================

    status = df.pivot(
        index="scenario_id",
        columns="capacity",
        values="status",
    )

    cap1_solved = (
        status[1] == "solved"
    )

    cap2_solved = (
        status[2] == "solved"
    )

    both_solved = (
        cap1_solved
        & cap2_solved
    ).sum()

    cap1_only = (
        cap1_solved
        & ~cap2_solved
    ).sum()

    cap2_only = (
        ~cap1_solved
        & cap2_solved
    ).sum()

    neither = (
        ~cap1_solved
        & ~cap2_solved
    ).sum()

    print()
    print("SOLVABILITY")
    print("-" * 70)

    print(
        f"Both solved:          {both_solved}"
    )
    print(
        f"Capacity 1 only:      {cap1_only}"
    )
    print(
        f"Capacity 2 only:      {cap2_only}"
    )
    print(
        f"Neither solved:       {neither}"
    )

    success_cap1 = cap1_solved.mean()
    success_cap2 = cap2_solved.mean()

    print()
    print(
        f"Capacity 1 success: "
        f"{success_cap1 * 100:.2f}%"
    )
    print(
        f"Capacity 2 success: "
        f"{success_cap2 * 100:.2f}%"
    )

    print(
        f"Difference: "
        f"{(success_cap2 - success_cap1) * 100:.2f} "
        f"percentage points"
    )

    discordant = (
        cap1_only + cap2_only
    )

    mcnemar = binomtest(
        min(cap1_only, cap2_only),
        n=discordant,
        p=0.5,
        alternative="two-sided",
    )

    print()
    print("Exact McNemar test:")
    print(
        f"  discordant pairs = {discordant}"
    )
    print(
        f"  p-value = "
        f"{mcnemar.pvalue:.12g}"
    )

    # =====================================================
    # KEEP ONLY SCENARIOS SOLVED BY BOTH
    # =====================================================

    solved_ids = status.index[
        (status[1] == "solved")
        & (status[2] == "solved")
    ]

    both = df[
        df["scenario_id"].isin(
            solved_ids
        )
    ].copy()

    metrics = [
        "makespan",
        "plan_length",
        "planning_time_ms",
        "expanded_nodes",
        "states_evaluated",
    ]

    cap1 = (
        both[both["capacity"] == 1]
        .set_index("scenario_id")
    )

    cap2 = (
        both[both["capacity"] == 2]
        .set_index("scenario_id")
    )

    paired = pd.DataFrame(
        index=solved_ids
    )

    for metric in metrics:
        paired[f"{metric}_cap1"] = (
            cap1[metric]
        )
        paired[f"{metric}_cap2"] = (
            cap2[metric]
        )

    print()
    print(
        f"Scenarios solved by both capacities: "
        f"{len(paired)}"
    )

    # =====================================================
    # PAIRED METRIC TESTS
    # =====================================================

    print_metric_analysis(
        paired,
        "makespan",
        "MISSION MAKESPAN",
    )

    print_metric_analysis(
        paired,
        "plan_length",
        "PLAN LENGTH",
    )

    print_metric_analysis(
        paired,
        "expanded_nodes",
        "EXPANDED NODES",
    )

    print_metric_analysis(
        paired,
        "states_evaluated",
        "STATES EVALUATED",
    )

    print_metric_analysis(
        paired,
        "planning_time_ms",
        "PLANNING TIME",
    )


if __name__ == "__main__":
    main()
