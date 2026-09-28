# V. Results

## A. Overall Solvability

The final experiment contained 160 paired warehouse scenarios and 320 planner
executions.

Capacity one solved 116 of the 160 scenarios, corresponding to a success rate
of 72.50%.

Capacity two solved 150 of the 160 scenarios, corresponding to a success rate
of 93.75%.

The observed increase in solvability was therefore

\[
93.75\% - 72.50\% = 21.25
\]

percentage points.

The paired outcomes are summarized in Table I.

| Capacity 1 | Capacity 2 | Number of scenarios |
|---|---|---:|
| solved | solved | 116 |
| solved | unsolvable | 0 |
| unsolvable | solved | 34 |
| unsolvable | unsolvable | 10 |

The 34 discordant scenarios all favored capacity two: no scenario was solved
only by capacity one.

An exact McNemar test on the paired binary outcomes produced

\[
p = 1.16 \times 10^{-10}.
\]

The null hypothesis of equal paired solvability is therefore rejected at
conventional significance levels.

## B. Solvability by Experimental Condition

The effect of carrying capacity depends strongly on the scenario conditions.

The success rates for the eight combinations of package count, deadline mode,
and layout are shown below.

| Packages | Deadline | Layout | Capacity 1 | Capacity 2 |
|---:|---|---|---:|---:|
| 2 | relaxed | clustered | 100% | 100% |
| 2 | relaxed | distributed | 100% | 100% |
| 2 | tight | clustered | 45% | 100% |
| 2 | tight | distributed | 50% | 50% |
| 3 | relaxed | clustered | 100% | 100% |
| 3 | relaxed | distributed | 100% | 100% |
| 3 | tight | clustered | 50% | 100% |
| 3 | tight | distributed | 35% | 100% |

Under relaxed deadlines, both capacities solved every scenario.

The differences emerge under tight deadlines. For two clustered packages,
capacity two increased the success rate from 45% to 100%. For three clustered
packages, the success rate increased from 50% to 100%. For three distributed
packages, the increase was from 35% to 100%.

The two-package tight distributed condition behaves differently: both
capacities solved 50% of the scenarios. In this layout, the two packages are
located in different aisles, so a larger carrying capacity does not allow them
to be collected during the same aisle visit.

Figure 1 reports the complete condition-level success-rate comparison.

**Fig. 1.** Planning success rate by experimental condition.

File:
`figures/success_rate_by_condition.png`

## C. Mission Makespan

Mission-level comparisons were performed only on the 116 scenarios solved by
both robot capacities.

For these paired scenarios, the mean makespan was:

- capacity one: 11.983 time units;
- capacity two: 8.500 time units.

The mean paired reduction was 28.54%.

Capacity two produced a lower makespan in 86 of the 116 paired scenarios,
while 30 pairs had equal makespan and no pair produced a larger makespan under
capacity two.

The Wilcoxon signed-rank test produced

\[
p = 4.89 \times 10^{-17}.
\]

The paired mean makespan by experimental condition is shown in Figure 2.

**Fig. 2.** Mean makespan for scenarios solved by both capacities.

File:
`figures/makespan_by_condition.png`

The condition-level means provide additional information about when the extra
capacity is useful.

For two-package clustered scenarios, the mean makespan changed from 10 to 5
under relaxed deadlines and from 8 to 4 among the jointly solved tight
scenarios.

For two-package distributed scenarios, the mean makespan remained 10 for both
capacities under both relaxed and jointly solved tight conditions.

For three-package scenarios, capacity two reduced the mean makespan in every
condition. Under relaxed deadlines the mean decreased from 15 to 10, while
under tight conditions it decreased from 12 to 8 for clustered layouts and
from 14 to 10 for distributed layouts.

These results indicate that the mission-level benefit of increased carrying
capacity depends on whether multiple packages can share part of the same route.

## D. Plan Length

For the same 116 jointly solved scenarios, the mean plan length was:

- capacity one: 26.931 actions;
- capacity two: 20.483 actions.

The mean paired reduction was 23.34%.

Capacity two produced a shorter plan in 86 scenarios and an equal-length plan
in 30 scenarios. No jointly solved scenario produced a longer plan under
capacity two.

The Wilcoxon signed-rank test produced

\[
p = 4.89 \times 10^{-17}.
\]

The similarity between the plan-length and makespan pairwise patterns is
consistent with the route-level explanation: when the robot can collect
multiple packages during the same visit, repeated travel and associated
pickup/delivery sequences are reduced.

## E. Search Complexity

The planner search statistics show a substantial difference between the two
capacity conditions for the 116 scenarios solved by both configurations.

### Expanded Nodes

The mean number of expanded nodes was:

- capacity one: 12,395.6;
- capacity two: 2,544.4.

The mean paired reduction was 61.93%.

Capacity two expanded fewer nodes in 108 of the 116 paired scenarios, while
capacity one expanded fewer nodes in eight scenarios.

The Wilcoxon signed-rank test produced

\[
p = 2.41 \times 10^{-20}.
\]

### States Evaluated

The mean number of evaluated states was:

- capacity one: 21,328.6;
- capacity two: 5,401.4.

The mean paired reduction was 57.80%.

Capacity two evaluated fewer states in 108 paired scenarios and more states in
eight.

The Wilcoxon signed-rank test produced

\[
p = 2.93 \times 10^{-20}.
\]

Figure 3 illustrates the difference in expanded-node distributions across the
complete experiment.

**Fig. 3.** Expanded nodes for the two robot-capacity configurations.

File:
`figures/expanded_nodes_boxplot.png`

The node-based metrics are particularly useful because they reflect planner
search effort more directly than wall-clock time and are less sensitive to
temporary system load.

## F. Planning Time

Planning time was also lower on average under capacity two.

For the valid paired measurements:

- capacity one mean planning time: 602.9 ms;
- capacity two mean planning time: 258.9 ms.

The mean paired reduction was 44.27%.

Capacity two had lower planning time in 100 pairs, equal time in one pair, and
higher time in 13 pairs.

The Wilcoxon signed-rank test produced

\[
p = 1.75 \times 10^{-18}.
\]

The planning-time comparison contains 114 valid pairs rather than 116 because
two jointly solved runs contained anomalous negative timing values reported by
ENHSP. These measurements were treated as missing rather than corrected or
estimated.

Because execution time can also be influenced by operating-system scheduling
and transient machine load, the expanded-node and evaluated-state results are
treated as the more robust indicators of planning complexity.

## G. Spatial Interaction with Carrying Capacity

The strongest qualitative result is the interaction between carrying capacity
and package placement.

When two packages are clustered in the same aisle, a capacity-two robot can
collect both during one visit. This reduces repeated motion and produces large
reductions in makespan and plan length.

When two packages are distributed across different aisles, the robot must
visit both aisles regardless of carrying capacity. Consequently, the
additional capacity produces little or no mission-level advantage in that
condition.

Three-package distributed scenarios behave differently because the generator
places two packages in one aisle and one in the other. The capacity-two robot
can therefore still combine two pickups during part of the mission, producing
a measurable advantage.

This interaction is also visible in the feasibility results. Under tight
deadlines, additional capacity rescues many clustered and three-package
distributed scenarios, while it does not improve the success rate for the
two-package distributed condition.

Figure 4 shows the distribution of paired makespan reductions across the
jointly solved scenarios.

**Fig. 4.** Distribution of paired makespan reduction, defined as capacity-one
makespan minus capacity-two makespan.

File:
`figures/paired_makespan_reduction.png`

Overall, the results show that carrying capacity influences not only mission
duration but also the existence of feasible deadline-respecting plans and the
amount of search required by the planner.
