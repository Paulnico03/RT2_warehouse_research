# III. Methodology

## A. Warehouse Planning Model

The warehouse task is represented as a PDDL+ planning domain. PDDL+ is used
because the problem combines discrete robot actions with continuously evolving
quantities and autonomous events [1].

The domain contains three principal object types:

- `robot`
- `package`
- `location`

The warehouse topology is represented through the predicate

`connected(location_1, location_2)`

and numerical distances between connected locations. The robot state includes
its current location and whether it is currently moving. Each package has an
initial location, a target location, a remaining delivery time, and a delivery
status.

Robot motion is represented using two discrete actions and one continuous
process. The `start-move` action removes the robot from its current location,
records the destination, and initializes the remaining travel distance. While
the robot is moving, the `robot-transit` process continuously decreases the
remaining distance at unit rate. Once the remaining distance reaches zero, the
`end-move` action places the robot at its destination.

This separation between discrete actions and continuous processes makes it
possible to represent travel duration explicitly while retaining a symbolic
planning formulation.

## B. Deadline Representation

Each package is associated with a numeric fluent

`time-remaining(package)`

which represents the amount of time available before its delivery deadline.

For every undelivered package, the autonomous process `package-aging`
continuously decreases this value according to

\[
\frac{d}{dt}\text{time-remaining}(p) = -1.
\]

When the remaining time reaches zero, the autonomous
`deadline-breach` event marks the package as having missed its deadline.

A package can be successfully delivered only if:

1. the robot is located at the package target location;
2. the robot is currently carrying that package; and
3. the deadline has not been missed.

The planner must therefore account simultaneously for routing decisions,
pickup and delivery actions, and the continuous passage of time.

## C. Original Single-Capacity Representation

The original warehouse model represented robot carrying capability through
the Boolean predicate

`hand-empty(robot)`.

A package could be picked up only when this predicate was true. After a pickup,
`hand-empty` became false and the robot could not collect another package
until the currently held package was dropped or delivered.

This representation therefore enforced a maximum carrying capacity of exactly
one package.

Although suitable for a single-capacity robot, the Boolean representation
does not generalize naturally to robots capable of transporting more than one
package.

## D. Generalized Numeric Carrying Capacity

To support multiple robot capacities within the same planning domain, the
Boolean `hand-empty` representation was replaced by two numeric fluents:

`current-load(robot)`

and

`max-capacity(robot)`.

The pickup precondition becomes

\[
\text{current-load}(r) < \text{max-capacity}(r).
\]

When a package is picked up, the current load is increased by one:

\[
\text{current-load}(r)
\leftarrow
\text{current-load}(r) + 1.
\]

When a package is dropped or successfully delivered, the current load is
decreased by one:

\[
\text{current-load}(r)
\leftarrow
\text{current-load}(r) - 1.
\]

The resulting formulation allows the same PDDL+ domain to represent different
robot carrying capabilities by changing only the initial value of
`max-capacity`.

In the experiments performed in this work, two configurations are compared:

- capacity 1: `max-capacity = 1`;
- capacity 2: `max-capacity = 2`.

This design is important for experimental control because the domain,
warehouse geometry, package positions, deadlines, actions, and planner remain
unchanged between the two conditions. The only manipulated robot capability
is its maximum load.

## E. Package Handling Actions

Three actions control package manipulation:

- `pick`
- `drop-intermediate`
- `deliver-package`

The `pick` action removes a package from its current warehouse location, marks
it as being carried by the robot, and increments the robot load.

The `drop-intermediate` action allows the robot to place a carried package at
its current location without completing the delivery. This action decrements
the robot load and makes the package available at the new location.

The `deliver-package` action completes the transportation task when the robot
is carrying a package at its assigned target location and its deadline has not
been violated. The package is marked as delivered and the robot load is
decremented.

For capacity two, the robot may satisfy the pickup precondition for a second
package while already carrying one package. This allows multiple packages to
share part of the same route when their spatial distribution permits it.

## F. Planning Objective and Planner

The generated planning problems are solved with ENHSP, a heuristic
forward-search planner designed for numeric and expressive planning domains
[2]–[4].

All experiments use the same planner configuration:

`opt-hrmax`

so that planner behavior remains controlled across capacity conditions.

The planning goal is to reach a state in which every package in the scenario
has been successfully delivered.

The planner output is parsed automatically to obtain:

- problem status;
- plan length;
- mission makespan;
- planning time;
- expanded search nodes;
- evaluated states.

These quantities are subsequently used to evaluate both task feasibility and
planning efficiency.

## G. Experimental Logic

The methodological comparison is paired. Every generated warehouse scenario is
solved twice:

1. once with robot capacity 1;
2. once with robot capacity 2.

All other scenario properties remain identical within the pair.

This design isolates carrying capacity as the independent variable and avoids
comparing performance across different warehouse instances.

The analysis distinguishes two types of outcome.

**Feasibility** evaluates whether a valid deadline-respecting plan exists.

**Efficiency** evaluates the quality and computational cost of planning for
scenarios that can be solved under both robot capacities.

This distinction is necessary because a scenario that is solvable only under
capacity two has no meaningful capacity-one makespan or plan length with which
to perform a paired numerical comparison.
