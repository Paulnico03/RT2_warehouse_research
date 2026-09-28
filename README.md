# RT2 Warehouse Research

## Evaluating the Impact of Robot Carrying Capacity on Deadline-Constrained Warehouse Planning

**Author:** Paolo Nicolini  
**Course:** Research Track II  
**University:** University of Genoa  
**Branch used during development:** `research-track-2`

---

## Overview

This repository contains the final Research Track II project investigating how the carrying capacity of a warehouse robot affects deadline-constrained automated planning.

The warehouse is modeled using **PDDL+** and solved with the **ENHSP** numeric planner. The original warehouse model allowed the robot to carry only one package at a time. This project generalizes the model by replacing the Boolean single-package representation with numeric fluents describing:

- the robot's current load;
- the robot's maximum carrying capacity.

The generalized domain allows the same warehouse scenario to be evaluated with either:

- **capacity 1**, or
- **capacity 2**.

The project includes the planning models, automatic scenario generation, batch experiments, statistical analysis, figures, an interactive Jupyter notebook, a ROS2 interface, and the final IEEE-style research paper.

---

## Research Question

> **How does increasing robot carrying capacity from one to two packages affect solvability, mission makespan, plan length, and planning complexity under different package distributions and deadline constraints?**

The experiment evaluates both mission-level and computational effects of carrying capacity.

---

## Hypotheses

The study investigates three main hypotheses:

- **H1:** increasing robot capacity from one to two packages improves the probability of finding a deadline-feasible plan;
- **H2:** for scenarios solved under both capacities, capacity two reduces mission makespan and plan length;
- **H3:** the benefit of additional carrying capacity depends on the spatial distribution of packages.

Search-complexity metrics are also analyzed to determine how robot capability affects planner behavior.

---

## Experimental Design

The final experiment varies four factors.

| Factor | Values |
|---|---|
| Robot capacity | 1, 2 |
| Number of packages | 2, 3 |
| Deadline mode | relaxed, tight |
| Package layout | clustered, distributed |

For every combination of:

- 2 package-count conditions;
- 2 deadline conditions;
- 2 layout conditions;

**20 reproducible seeds** are generated.

Therefore:

```text
2 × 2 × 2 × 20 = 160 warehouse scenarios
```

Each scenario is evaluated with both robot capacities:

```text
160 × 2 = 320 planner executions
```

The design is paired: the capacity-one and capacity-two versions of each scenario have identical package positions, deadlines, warehouse topology, and random seed.

Only the robot carrying capacity changes.

---

## Package Layouts

### Clustered

Packages are located in the same aisle.

This gives a capacity-two robot the opportunity to collect multiple packages during the same visit.

### Distributed

For two-package scenarios:

```text
Aisle A: 1 package
Aisle B: 1 package
```

For three-package scenarios:

```text
Aisle A: 2 packages
Aisle B: 1 package
```

or the symmetric configuration.

The two-package distributed condition is particularly important because additional capacity does not automatically reduce travel: the robot must still visit both aisles.

---

## Deadline Generation

Deadlines are generated reproducibly from the scenario seed.

| Packages | Relaxed | Tight |
|---|---:|---:|
| 2 | 20–30 | 7–12 |
| 3 | 25–40 | 11–16 |

Separate random streams are used for layout generation and deadline generation so that changing the package layout does not unintentionally regenerate deadline values.

---

## Warehouse Model

The simplified warehouse contains four principal locations:

```text
dock
aisle-A
aisle-B
shipping
```

Travel times are fixed:

```text
dock -> aisle-A       = 2
dock -> aisle-B       = 3
aisle-A -> shipping   = 2
aisle-B -> shipping   = 3
```

Reverse movements use the corresponding symmetric distances.

Robot motion is represented using:

```text
start-move
robot-transit
end-move
```

Package manipulation uses:

```text
pick
drop-intermediate
deliver-package
```

Package deadlines are represented through a continuously decreasing numeric fluent:

```text
time-remaining(package)
```

An autonomous deadline event prevents successful delivery after the deadline has expired.

---

## Carrying-Capacity Generalization

The original model used:

```text
hand-empty(robot)
```

which enforced a maximum carrying capacity of one package.

The generalized domain replaces it with:

```text
current-load(robot)
max-capacity(robot)
```

A package can be picked up when:

```text
current-load < max-capacity
```

Pickup increments the current load, while dropping or delivering a package decrements it.

The same PDDL+ domain can therefore represent different robot capacities simply by changing the initial value of:

```text
max-capacity
```

---

## Planner

The final experiments use **ENHSP** with:

```text
opt-hrmax
```

Each planning run has a maximum execution time of:

```text
120 seconds
```

Final experiment outcome:

```text
Solved runs:      266
Unsolvable runs:   54
Timeouts:           0
Unknown/parser:     0
```

---

## Main Results

### Solvability

| Capacity | Solved | Total | Success rate |
|---|---:|---:|---:|
| 1 | 116 | 160 | 72.50% |
| 2 | 150 | 160 | 93.75% |

Increase in success rate:

```text
+21.25 percentage points
```

Paired scenario outcomes:

| Outcome | Scenarios |
|---|---:|
| Both solved | 116 |
| Capacity 1 only | 0 |
| Capacity 2 only | 34 |
| Neither solved | 10 |

Exact McNemar test:

```text
p = 1.16415321827 × 10^-10
```

---

## Success Rate by Condition

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

The largest feasibility differences appear under tight deadlines.

The two-package tight distributed condition remains at **50% for both capacities**, demonstrating that increased carrying capacity is not universally beneficial when the spatial layout prevents packages from sharing the same route.

---

## Paired Performance Results

The following metrics use the **116 scenarios solved under both capacities**.

| Metric | Capacity 1 | Capacity 2 | Mean paired reduction |
|---|---:|---:|---:|
| Makespan | 11.983 | 8.500 | 28.54% |
| Plan length | 26.931 | 20.483 | 23.34% |
| Expanded nodes | 12,395.595 | 2,544.371 | 61.93% |
| States evaluated | 21,328.578 | 5,401.440 | 57.80% |

Planning time uses **114 valid paired measurements**:

| Metric | Capacity 1 | Capacity 2 | Mean paired reduction |
|---|---:|---:|---:|
| Planning time | 602.904 ms | 258.921 ms | 44.27% |

Three anomalous negative planning-time values were reported by ENHSP and treated as missing rather than corrected or estimated.

---

## Statistical Results

Wilcoxon signed-rank tests for jointly solved scenarios:

```text
Makespan:
p = 4.89418 × 10^-17

Plan length:
p = 4.89418 × 10^-17

Expanded nodes:
p = 2.40612 × 10^-20

States evaluated:
p = 2.93061 × 10^-20

Planning time:
p = 1.75050 × 10^-18
```

Pairwise behavior:

```text
Makespan:
Capacity 2 better: 86
Ties:              30
Capacity 2 worse:   0

Plan length:
Capacity 2 better: 86
Ties:              30
Capacity 2 worse:   0

Expanded nodes:
Capacity 2 better: 108
Capacity 2 worse:    8

States evaluated:
Capacity 2 better: 108
Capacity 2 worse:    8

Planning time:
Capacity 2 better: 100
Ties:                1
Capacity 2 worse:   13
```

---

## Main Interpretation

The experiments show that additional carrying capacity can affect three different aspects of planning:

1. **Feasibility**  
   Capacity two can make deadline-constrained scenarios solvable that are infeasible with capacity one.

2. **Mission efficiency**  
   When multiple packages can share part of the same route, capacity two reduces repeated travel, mission makespan, and plan length.

3. **Planning complexity**  
   In most jointly solved scenarios, capacity two also reduces the amount of search performed by ENHSP.

The benefit is strongly dependent on spatial structure.

When packages are clustered, a capacity-two robot can exploit the additional load capability directly.

When two packages are placed in different aisles, the robot still has to visit both locations, so additional capacity provides little or no route-level advantage.

---

## Repository Structure

```text
RT2_warehouse_research/
│
├── data/
│   ├── final/
│   │   ├── final_results.csv
│   │   ├── final_scenario_metadata.csv
│   │   ├── final_run_console.log
│   │   └── batch_runs/
│   │
│   ├── processed/
│   │   └── figures/
│   │
│   ├── pilot/
│   └── raw/
│
├── docs/
│
├── experiments/
│   ├── generate_problems.py
│   ├── run_experiments.py
│   ├── analyze_results.py
│   ├── statistical_analysis.py
│   ├── stratified_analysis.py
│   └── generate_figures.py
│
├── notebooks/
│   └── warehouse_experiment.ipynb
│
├── paper/
│   ├── main.tex
│   ├── main.pdf
│   └── figures/
│
├── planning/
│   ├── baseline/
│   ├── multi_capacity/
│   ├── generated_problems/
│   ├── pilot_problems/
│   └── pilot_factorial/
│
├── ros2_ws/
│   └── src/
│       └── warehouse_experiment/
│
├── .gitignore
└── README.md
```

---

## Main Planning Domain

The generalized capacity-aware domain is located at:

```text
planning/multi_capacity/domain-warehouse-capacity.pddl
```

Generated paired experimental problems are stored under:

```text
planning/generated_problems/
```

---

## Experiment Scripts

### Generate scenarios

```bash
cd ~/RT2_warehouse_research
source .venv/bin/activate

python3 experiments/generate_problems.py
```

### Run experiments

```bash
python3 experiments/run_experiments.py
```

### Analyze results

```bash
python3 experiments/analyze_results.py
```

### Statistical analysis

```bash
python3 experiments/statistical_analysis.py
```

### Stratified analysis

```bash
python3 experiments/stratified_analysis.py
```

### Generate figures

```bash
python3 experiments/generate_figures.py
```

---

## Software Environment

The project was developed and verified with:

```text
Ubuntu 24.04
ROS2 Jazzy
Python 3.12
Java 21
Git 2.43
```

Main Python packages include:

```text
pandas
numpy
scipy
matplotlib
jupyter
ipykernel
ipywidgets
```

ENHSP must be installed separately and accessible through the experiment configuration.

---

## Python Environment

The project uses a virtual environment created with access to the system ROS2 Python packages.

Example:

```bash
cd ~/RT2_warehouse_research

python3 -m venv --system-site-packages .venv
source .venv/bin/activate
```

Install any missing Python dependencies as required.

---

## ROS2 Package

The ROS2 package is located at:

```text
ros2_ws/src/warehouse_experiment
```

Build it with:

```bash
cd ~/RT2_warehouse_research

source .venv/bin/activate
source /opt/ros/jazzy/setup.bash

cd ros2_ws

colcon build \
    --packages-select warehouse_experiment \
    --symlink-install
```

Then:

```bash
source install/setup.bash
```

---

## ROS2 Experiment Node

Start the experiment node:

```bash
cd ~/RT2_warehouse_research

source .venv/bin/activate
source /opt/ros/jazzy/setup.bash
source ros2_ws/install/setup.bash

ros2 run warehouse_experiment experiment_node
```

The node listens on:

```text
/warehouse_experiment/request
```

and publishes results on:

```text
/warehouse_experiment/result
```

Request format:

```json
{
  "scenario_id": 1000,
  "capacity": 2
}
```

Example result for scenario `1000`, capacity `2`:

```text
status: solved
plan_length: 12
makespan: 4
expanded_nodes: 50
states_evaluated: 117
```

Planning time may vary slightly between executions.

---

## ROS2 Result Listener

In another terminal:

```bash
cd ~/RT2_warehouse_research

source .venv/bin/activate
source /opt/ros/jazzy/setup.bash
source ros2_ws/install/setup.bash

ros2 topic echo \
/warehouse_experiment/result \
--full-length
```

---

## Jupyter Notebook

The main notebook is:

```text
notebooks/warehouse_experiment.ipynb
```

Start Jupyter with:

```bash
cd ~/RT2_warehouse_research

source .venv/bin/activate
source /opt/ros/jazzy/setup.bash
source ros2_ws/install/setup.bash

jupyter notebook
```

The notebook provides:

- loading of the final experimental dataset;
- solvability analysis;
- paired statistical analysis;
- visualization of the main results;
- scenario and capacity selection;
- interactive ROS2 experiment execution.

The registered kernel is:

```text
RT2 Warehouse
```

---

## ROS2 Integration Validation

The complete interactive path was verified as:

```text
Jupyter
   ↓
ROS2 request
   ↓
warehouse_experiment node
   ↓
ENHSP
   ↓
ROS2 result
   ↓
Jupyter
```

Scenario `1000` was used as an end-to-end consistency check.

Capacity one produced:

```text
plan length:       20
makespan:           8
expanded nodes:   661
states evaluated: 1180
```

Capacity two produced:

```text
plan length:       12
makespan:           4
expanded nodes:    50
states evaluated: 117
```

This ROS2 execution is a software-integration validation and is not counted as an additional statistical trial.

---

## Figures

Generated figures are available in:

```text
data/processed/figures/
```

and the figures used in the final paper are stored in:

```text
paper/figures/
```

Principal figures include:

```text
success_rate_by_condition.png
makespan_by_condition.png
expanded_nodes_boxplot.png
paired_makespan_reduction.png
```

---

## Research Paper

The final IEEE-style paper is available at:

```text
paper/main.pdf
```

The LaTeX source is:

```text
paper/main.tex
```

Paper title:

> **Evaluating the Impact of Robot Carrying Capacity on Deadline-Constrained Warehouse Planning**

The final paper contains:

```text
Abstract
I.    Introduction
II.   Related Work
III.  Methodology
IV.   Experimental Setup
V.    Results
VI.   Discussion
VII.  Validity, Limitations, and Future Work
VIII. Conclusion
References
```

The final manuscript is five IEEE-style pages and includes 13 academic references.

---

## Reproducibility

The experiment is designed to be reproducible.

The repository includes:

- deterministic scenario generation;
- explicit random seeds;
- paired capacity-one and capacity-two problems;
- raw planner outputs;
- scenario metadata;
- processed CSV results;
- statistical-analysis scripts;
- generated figures;
- executed Jupyter notebook;
- ROS2 planner interface;
- final research paper.

The final experiment contains:

```text
160 paired scenarios
320 planner executions
```

with no unresolved runs.

---

## Limitations

The experiment intentionally uses a controlled simplified environment.

Current limitations include:

- one robot;
- two warehouse aisles;
- two or three packages in the final factorial experiment;
- synthetic package distributions;
- synthetic deadlines;
- capacities limited to one and two packages;
- one ENHSP planner configuration;
- individual rather than repeated wall-clock runtime measurements.

These choices make it possible to isolate the effect of carrying capacity, but the results should not be interpreted as direct performance estimates for a full industrial warehouse.

---

## Future Work

Possible extensions include:

- larger warehouse topologies;
- more package quantities;
- carrying capacities greater than two;
- multi-robot systems;
- congestion and collision avoidance;
- task allocation;
- alternative ENHSP heuristics;
- comparison with other numeric planners;
- repeated runtime measurements;
- real or realistic warehouse workload traces.

---

## Final Verified Version

The final project version was checked for consistency across:

```text
PDDL+ model
scenario generator
320-run dataset
statistical analysis
figures
ROS2 interface
Jupyter notebook
IEEE paper
```

The verified Git tag is:

```text
rt2-final
```

The final GitHub repository is:

```text
Paulnico03/RT2_warehouse_research
```

---

## Author

**Paolo Nicolini**  
University of Genoa  
Research Track II