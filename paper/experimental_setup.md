# IV. Experimental Setup

## A. Experimental Factors

The experiment was designed to isolate the effect of robot carrying capacity
while also investigating whether its impact changes under different warehouse
conditions.

Four experimental factors were considered.

### 1. Robot Carrying Capacity

Two robot configurations were evaluated:

- capacity 1;
- capacity 2.

The carrying capacity is represented through the PDDL+ numeric fluent
`max-capacity`. All other domain properties remain unchanged between the two
capacity conditions.

### 2. Number of Packages

Two problem sizes were included in the main experiment:

- 2 packages;
- 3 packages.

A four-package configuration was investigated during preliminary feasibility
testing but was not included in the main factorial experiment because the
capacity-one condition produced substantially larger search effort and
execution time. Restricting the main experiment to two and three packages made
it possible to perform a larger number of controlled repetitions while keeping
the complete experiment computationally manageable.

### 3. Deadline Mode

Two deadline conditions were defined:

- relaxed;
- tight.

Relaxed deadlines were selected so that both robot capacities would generally
have sufficient time to complete the deliveries.

Tight deadlines were designed to create more demanding planning instances in
which route efficiency and carrying capacity could influence whether a valid
plan existed.

The exact deadline values were generated reproducibly from the scenario seed.

### 4. Package Layout

Two spatial package distributions were considered:

- clustered;
- distributed.

In clustered scenarios, packages are placed in the same warehouse aisle.
This creates an opportunity for a capacity-two robot to collect multiple
packages during the same visit.

In distributed two-package scenarios, one package is placed in each aisle.
In this configuration, increasing carrying capacity does not necessarily
reduce travel because the robot must still visit both locations.

For three-package distributed scenarios, two packages are located in one aisle
and the remaining package in the other aisle. Capacity two can therefore still
be exploited for part of the transportation task.

## B. Warehouse Topology

All scenarios use the same warehouse topology.

The model contains the following principal locations:

- `dock`;
- `aisle-A`;
- `aisle-B`;
- `shipping`.

The robot starts at the dock and packages must ultimately be delivered to the
shipping location.

The travel distances are fixed across all experiments. The relevant
connections are:

- dock to aisle-A: 2 time units;
- dock to aisle-B: 3 time units;
- aisle-A to shipping: 2 time units;
- aisle-B to shipping: 3 time units.

Reverse connections use the corresponding symmetric distance.

Keeping the warehouse graph and movement speed fixed ensures that changes in
planner behavior are caused by the experimental factors rather than by changes
in the environment geometry.

## C. Scenario Generation

Scenarios are generated automatically by a Python script.

Each scenario is identified by:

- a scenario ID;
- a random seed;
- number of packages;
- deadline mode;
- layout mode.

The generator produces two PDDL+ problem files for every scenario:

- one with `max-capacity = 1`;
- one with `max-capacity = 2`.

Within each pair, package positions, deadlines, warehouse geometry, and all
other initial conditions are identical.

Separate pseudo-random generators are used for package-layout decisions and
deadline generation. This prevents changes in package placement from
unintentionally changing the deadline values.

As a result, scenarios with the same seed, package count, and deadline mode
can be compared across layout conditions while preserving identical deadline
values.

## D. Factorial Design and Number of Runs

For each combination of:

- 2 package-count conditions;
- 2 deadline modes;
- 2 layout modes;

20 reproducible seeds were generated.

The number of distinct warehouse scenarios is therefore

\[
2 \times 2 \times 2 \times 20 = 160.
\]

Each scenario is evaluated with both carrying capacities:

\[
160 \times 2 = 320
\]

planner executions in the final experiment.

This paired factorial structure allows the capacity conditions to be compared
using exactly the same underlying warehouse instances.

## E. Planner Configuration

All planning problems are solved using ENHSP.

The same planner configuration is used for every run:

`opt-hrmax`

The planner is executed through Java using the same PDDL+ domain file for all
capacity conditions.

A timeout of 120 seconds is applied to every planner execution.

No final experimental run reached the timeout.

The planner output is stored as raw text and subsequently parsed
automatically.

## F. Collected Metrics

The experiment records both feasibility and performance metrics.

### Feasibility

Each run is classified as:

- solved;
- unsolvable;
- timeout.

No final run was classified as timeout or unknown.

### Mission-Level Metrics

For solved problems, the following quantities are extracted:

- plan length;
- mission makespan.

Plan length represents the number of discrete actions in the generated plan.

Makespan represents the temporal duration required to complete the warehouse
mission.

### Search-Complexity Metrics

The following planner statistics are also collected:

- expanded nodes;
- states evaluated.

These metrics provide a machine-independent indication of the amount of search
performed by the planner and are therefore particularly useful for comparing
planning complexity between capacity conditions.

### Runtime

Planning time in milliseconds is also recorded.

Runtime is treated more cautiously than node-based metrics because it can vary
with system load and execution conditions.

During the final experiment, ENHSP produced three anomalous negative planning
time values. These values were treated as invalid measurements and stored as
missing rather than being transformed or estimated.

Two of those anomalous measurements occurred in scenarios otherwise solved by
both capacity configurations, so the paired planning-time analysis contains
114 valid pairs instead of 116.

## G. Automated Experiment Pipeline

The complete experiment is automated through Python scripts.

The pipeline performs the following sequence:

1. generate reproducible PDDL+ problem files;
2. execute ENHSP for each capacity condition;
3. enforce the 120-second timeout;
4. save the complete raw planner output;
5. parse relevant planner metrics;
6. associate each result with scenario metadata;
7. write the processed results to CSV files.

The automation reduces the risk of manual transcription errors and allows the
full experiment to be reproduced from the project repository.

## H. Statistical Analysis

Because both robot capacities are evaluated on the same warehouse scenarios,
the observations are paired.

### Solvability

The binary solved/unsolvable outcomes are compared using an exact McNemar test.

This test evaluates the discordant scenario pairs:

- scenarios solved only by capacity one;
- scenarios solved only by capacity two.

### Quantitative Metrics

Makespan, plan length, expanded nodes, states evaluated, and planning time are
compared using the Wilcoxon signed-rank test.

For mission metrics such as makespan and plan length, only scenarios solved
under both capacity configurations are included because an unsolved planning
problem does not produce a valid mission plan.

The same paired subset is used for the main search-complexity comparison so
that both capacities are evaluated on identical successfully solved problem
instances.

The Wilcoxon signed-rank test is used instead of relying on a parametric paired
t-test because several planner metrics exhibit highly skewed distributions and
large differences in scale.

## I. Reproducibility and Interactive Interface

In addition to the batch experiment scripts, the project provides a ROS2 node
that exposes individual planning experiments through two topics:

- `/warehouse_experiment/request`;
- `/warehouse_experiment/result`.

A Jupyter notebook acts as an interactive ROS2 client. The user can select a
scenario ID and robot capacity, submit a planning request, and inspect the
resulting ENHSP metrics.

The notebook also loads the final experimental dataset, reproduces the main
statistical analysis, and visualizes the results.

This interface provides an additional reproducibility layer by linking the
experimental data analysis directly to the planning software used to generate
the results.
