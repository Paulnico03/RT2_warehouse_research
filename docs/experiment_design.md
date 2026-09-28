# Experimental Design

## Research Question

Does increasing the carrying capacity of a warehouse robot from
one package to two packages improve performance in
deadline-constrained PDDL+ delivery tasks?

## Hypotheses

### H1 - Mission performance

A robot with capacity 2 will achieve lower mission makespan than
a robot with capacity 1.

### H2 - Planning complexity

Changing the robot capacity may affect the computational
complexity of the planner, measured through planning time,
expanded nodes, and evaluated states.

## Independent Variable

Robot maximum carrying capacity:

- Capacity 1
- Capacity 2

## Dependent Variables

- Problem solved / unsolved
- Mission makespan
- Plan length
- Planning time
- Expanded nodes
- States evaluated

## Controlled Variables

For every paired comparison, the following must remain identical:

- Warehouse topology
- Distances
- Robot starting location
- Package starting locations
- Package destination
- Package deadlines
- ENHSP planner configuration
- ENHSP version
- Hardware and operating system

Only max-capacity changes.

## Pilot Experiment

The first controlled experiment used three packages:

- pkg1: aisle-A -> shipping
- pkg2: aisle-A -> shipping
- pkg3: aisle-B -> shipping

Results:

### Capacity 1

- Solved
- Makespan: 14.0
- Plan length: 32
- Planning time: 1398 ms
- Expanded nodes: 23719
- States evaluated: 41470

### Capacity 2

- Solved
- Makespan: 10.0
- Plan length: 24
- Planning time: 663 ms
- Expanded nodes: 4092
- States evaluated: 8768

The pilot confirms that the capacity-2 model can carry multiple
packages simultaneously and motivates a larger controlled study.
