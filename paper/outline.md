# Evaluating the Impact of Robot Carrying Capacity on Deadline-Constrained Warehouse Planning

## Abstract

- Problem: warehouse robot planning under delivery deadlines.
- Compare carrying capacity 1 vs carrying capacity 2.
- Controlled factorial experiment with:
  - 2 or 3 packages
  - relaxed or tight deadlines
  - clustered or distributed layouts
  - 20 seeds per condition
- 160 paired scenarios, 320 planner runs.
- Main findings:
  - success rate: 72.50% -> 93.75%
  - +21.25 percentage points
  - exact McNemar p ≈ 1.16e-10
  - paired solved scenarios show lower makespan, plan length, search effort.
- Main interpretation:
  extra capacity is useful when package placement allows concurrent transport.

## I. Introduction

### Context
- Autonomous warehouse robots must transport packages efficiently.
- Planning becomes harder when deadlines and routing constraints are present.
- Carrying capacity affects both execution efficiency and the planning search space.

### Problem
- Many simplified warehouse planning models assume a robot carries one package at a time.
- It is not obvious whether increasing carrying capacity always improves performance.

### Research question
How does increasing robot carrying capacity from one to two packages affect
solvability, mission makespan, plan length, and planning complexity under
different package distributions and deadline constraints?

### Hypotheses
H1:
Capacity 2 increases the probability of finding a deadline-feasible plan.

H2:
For scenarios solved by both capacities, capacity 2 reduces mission makespan
and plan length.

H3:
The benefit of additional capacity depends on the package layout.

### Contributions
- Generalized PDDL+ warehouse model with numeric carrying capacity.
- Controlled paired experiment.
- Automated ENHSP execution and result extraction.
- Statistical comparison of feasibility and efficiency.
- ROS2 + Jupyter interface for interactive experiment execution.

## II. Related Work

### Automated planning in robotics
- Classical planning and temporal/numeric planning.
- PDDL and PDDL+.

### Warehouse robotic planning
- Pickup/delivery tasks.
- Routing and scheduling.
- Deadline-constrained delivery.

### Planner
- ENHSP.
- Numeric/temporal planning.
- opt-hrmax configuration.

### Research gap
- Focus on how carrying capacity interacts with deadlines and spatial package distribution.

NOTE:
This section requires literature references and should not be written only from our own experiment.

## III. Methodology

### A. Warehouse model

Locations:
- dock
- aisle-A
- aisle-B
- shipping

Robot:
- continuous movement between connected locations.

Packages:
- initial location
- target location
- remaining deadline time.

### B. Original capacity-one model

Original representation:
- hand-empty predicate
- robot holds at most one package.

### C. Generalized carrying-capacity model

Numeric fluents:
- current-load(robot)
- max-capacity(robot)

Pickup allowed when:

current-load < max-capacity

Pickup:
- increases current-load by 1.

Drop/delivery:
- decreases current-load by 1.

This allows the same domain to represent both capacity 1 and capacity 2.

### D. Deadline model

- time-remaining decreases continuously.
- deadline-breach event occurs when time reaches zero.
- package cannot be successfully delivered after deadline breach.

## IV. Experimental Setup

### A. Experimental factors

Factor 1: carrying capacity
- 1
- 2

Factor 2: number of packages
- 2
- 3

Factor 3: deadline mode
- relaxed
- tight

Factor 4: package layout
- clustered
- distributed

Seeds:
- 20 per condition.

Total scenario conditions:

2 package counts
x 2 deadline modes
x 2 layouts
x 20 seeds
= 160 scenarios

Each scenario evaluated with two capacities:

160 x 2 = 320 planner runs.

### B. Controlled pairing

For a given scenario:
- same package count
- same deadlines
- same warehouse geometry
- same package placement
- same planner

Only robot carrying capacity changes.

### C. Planner

ENHSP

Planner configuration:
- opt-hrmax

Timeout:
- 120 seconds

### D. Metrics

Feasibility:
- solved / unsolvable

Mission efficiency:
- makespan
- plan length

Search complexity:
- expanded nodes
- states evaluated

Runtime:
- planning time

### E. Statistical analysis

Solvability:
- exact McNemar test
- paired scenarios

Continuous metrics:
- Wilcoxon signed-rank test
- only scenarios solved by both capacities

Planning-time anomaly:
- three ENHSP runs reported invalid negative planning times.
- negative timing measurements were treated as missing.
- only two affected the both-solved runtime comparison.
- planning-time paired n = 114.

## V. Results

### A. Solvability

Capacity 1:
116 / 160 solved
72.50%

Capacity 2:
150 / 160 solved
93.75%

Difference:
+21.25 percentage points

Paired outcomes:
- both solved: 116
- capacity 1 only: 0
- capacity 2 only: 34
- neither solved: 10

Exact McNemar:
p ≈ 1.16e-10

### B. Paired efficiency results

Among 116 scenarios solved by both capacities:

Makespan:
- capacity 1 mean = 11.983
- capacity 2 mean = 8.500
- mean paired reduction = 28.54%
- Wilcoxon p ≈ 4.89e-17

Plan length:
- capacity 1 mean = 26.931
- capacity 2 mean = 20.483
- reduction = 23.34%
- p ≈ 4.89e-17

Expanded nodes:
- capacity 1 mean = 12395.6
- capacity 2 mean = 2544.4
- reduction = 61.93%
- p ≈ 2.41e-20

States evaluated:
- capacity 1 mean = 21328.6
- capacity 2 mean = 5401.4
- reduction = 57.80%
- p ≈ 2.93e-20

Planning time:
- valid paired n = 114
- capacity 1 mean = 602.9 ms
- capacity 2 mean = 258.9 ms
- reduction = 44.27%
- p ≈ 1.75e-18

### C. Effect of experimental conditions

Relaxed deadlines:
- all conditions solved by both capacities.

2 packages, tight, clustered:
- capacity 1: 45%
- capacity 2: 100%

2 packages, tight, distributed:
- capacity 1: 50%
- capacity 2: 50%

3 packages, tight, clustered:
- capacity 1: 50%
- capacity 2: 100%

3 packages, tight, distributed:
- capacity 1: 35%
- capacity 2: 100%

### D. Spatial-layout interaction

Important observation:

For 2 distributed packages:
- capacity 2 cannot transport both packages together.
- makespan often remains identical to capacity 1.

For clustered packages:
- capacity 2 can collect multiple packages on the same visit.
- large makespan and plan-length reductions occur.

For 3 distributed packages:
- two packages still share an aisle.
- capacity 2 can still exploit multi-package transport.

## VI. Discussion

### Main interpretation

Extra carrying capacity is not universally beneficial simply because the robot
can hold more packages.

The advantage depends on whether the spatial structure of the problem allows
the additional capacity to be exploited.

### Feasibility

Capacity 2 rescued 34 scenarios that capacity 1 could not solve.

No scenario was solved exclusively by capacity 1.

### Search complexity

Capacity 2 generally reduced:
- expanded nodes
- evaluated states

This indicates that increased physical capability can also simplify the
planning problem in this domain.

### Negative-control-like condition

Two-package distributed scenarios are important because increased carrying
capacity often provides no route-level advantage.

This demonstrates that observed improvements are not simply caused by changing
a numeric parameter.

### Limitations

- Small warehouse topology.
- Only one robot.
- Maximum tested main-experiment package count = 3.
- Capacity comparison limited to 1 vs 2.
- Fixed planner and heuristic.
- Runtime affected by system noise.
- Three anomalous negative ENHSP timing values.
- Generated scenarios rather than real warehouse traces.

## VII. Conclusion

- Capacity 2 significantly increased solvability.
- It reduced makespan, plan length, and search effort for jointly solvable cases.
- The effect depends strongly on package layout and deadline tightness.
- Carrying capacity should therefore be considered jointly with spatial task
  structure when designing warehouse planning systems.

### Future work

- larger warehouse graphs
- more packages
- multiple robots
- additional carrying capacities
- alternative planners/heuristics
- real warehouse task distributions
- repeated runtime measurements

## References

To be completed after literature review.
