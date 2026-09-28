# VI. Discussion

## A. Effect of Carrying Capacity on Feasibility

The results show that increasing robot carrying capacity from one to two
packages can substantially improve the feasibility of deadline-constrained
warehouse planning problems.

Across the 160 paired scenarios, capacity two solved 34 instances that were
unsolvable under capacity one, while no scenario showed the opposite behavior.
This asymmetry indicates that the additional carrying capability enlarged the
set of warehouse instances for which a valid deadline-respecting plan could be
found.

The effect is particularly visible under tight deadlines. Under relaxed
deadlines, both capacities solved all scenarios, meaning that carrying capacity
had little influence on basic feasibility when sufficient time was available.
Under tighter temporal constraints, however, repeated travel became more
important and the ability to transport multiple packages during the same route
could determine whether the mission was completed before a deadline.

This distinction is important because it shows that robot capability should not
be evaluated independently of task difficulty. A larger carrying capacity may
provide little benefit when deadlines are loose, but become decisive as temporal
constraints become more restrictive.

## B. Interaction Between Capacity and Spatial Layout

The package-layout factor provides one of the clearest interpretations of the
experimental results.

For two-package clustered scenarios, both packages are located in the same
aisle. A capacity-two robot can therefore collect both packages during one
visit and transport them together for part of the route. This produces a direct
reduction in repeated movement.

The corresponding reduction in makespan and plan length is consistent with
this route-level explanation.

The two-package distributed condition provides an important contrasting case.
Because one package is located in each aisle, the robot must visit both aisles
regardless of whether it can carry one or two packages. In these scenarios,
increased carrying capacity does not automatically create an opportunity for
shared transport.

This explains why the two-package distributed scenarios show identical mean
makespan and plan length across capacities in the jointly solved cases, and why
the tight distributed condition does not show an improvement in solvability.

The three-package distributed scenarios behave differently. Although packages
are distributed between both aisles, two packages remain colocated in one
aisle. The capacity-two robot can therefore exploit its additional carrying
capability for part of the mission.

The results consequently show that carrying capacity should not be treated as
an isolated performance parameter. Its practical value depends on the spatial
structure of the transportation requests.

## C. Mission Efficiency

For scenarios solved under both capacities, capacity two reduced both mission
makespan and plan length.

The average makespan reduction of 28.54% indicates that the additional
carrying capability frequently allows the robot to complete the mission using
less elapsed time.

The 23.34% mean reduction in plan length provides complementary evidence.
Because the plan contains fewer actions, the improvement is not only temporal:
the capacity-two robot often requires fewer discrete planning steps to complete
the same delivery task.

The pairwise results strengthen this interpretation. Capacity two produced a
lower makespan and shorter plan in 86 of the 116 jointly solved scenarios, while
the remaining 30 scenarios were ties. No jointly solved scenario produced a
worse makespan or longer plan under capacity two.

However, the presence of 30 ties also confirms that additional capacity is not
universally useful. These ties are largely consistent with situations in which
the spatial arrangement does not permit multiple packages to share a useful
portion of the route.

## D. Effect on Planning Search Complexity

One of the more interesting findings is that increased physical capability
also reduced planner search effort in most jointly solved scenarios.

Capacity two reduced the mean number of expanded nodes by 61.93% and the mean
number of evaluated states by 57.80%.

At first sight, a larger carrying capacity might be expected to increase search
complexity because the planner has access to more possible package-handling
combinations. A capacity-two robot can represent states in which multiple
packages are carried simultaneously, potentially increasing branching.

In the tested domain, however, this increase in available actions is outweighed
by the existence of shorter and more direct solution strategies.

When multiple packages can be transported together, the planner can reach the
goal without repeatedly returning to pickup locations. The corresponding
solution paths are shorter, and the heuristic search frequently reaches them
after exploring substantially fewer states.

This effect is not universal. Capacity two expanded more nodes and evaluated
more states in eight of the 116 jointly solved scenarios. Therefore, the
results should not be interpreted as a general theoretical claim that larger
carrying capacity always reduces planning complexity.

Instead, the experiment shows that, for the warehouse topology, heuristic,
and scenario distributions considered here, the additional capability usually
simplifies the search by enabling more efficient goal-achieving routes.

## E. Planning Time and Computational Measures

Planning time follows the same overall trend as the search-complexity metrics,
with a mean paired reduction of 44.27%.

However, wall-clock runtime is inherently more sensitive to operating-system
scheduling, background processes, Java runtime behavior, and temporary machine
load.

For this reason, expanded nodes and evaluated states are treated as the more
reliable indicators of changes in planning effort.

The experiment also exposed three anomalous ENHSP outputs in which negative
planning-time values were reported. Because negative execution time has no
physical interpretation, these measurements were treated as missing values
rather than having their sign changed or being replaced by estimated values.

This conservative treatment avoids introducing artificial measurements into
the statistical analysis.

## F. Implications for Warehouse Planning

The results suggest that robot capability and task structure should be
considered jointly when designing warehouse planning systems.

Increasing carrying capacity can provide three distinct advantages:

1. it can make previously infeasible deadline-constrained tasks solvable;
2. it can reduce mission duration and the number of required actions;
3. it can reduce the amount of planner search needed to find a solution.

However, these benefits depend on whether the layout and package distribution
allow multiple items to be transported together.

From a system-design perspective, this means that the usefulness of additional
carrying capacity should be evaluated against the expected structure of
warehouse requests.

For environments where packages are frequently colocated or share substantial
route segments, additional capacity may provide significant benefits. In
contrast, if tasks are usually spatially separated, the same increase in
capacity may provide much smaller improvements.

## G. Limitations

Several limitations should be considered when interpreting the results.

First, the warehouse topology is intentionally small. The environment contains
only a dock, two aisles, and a shipping location. This simplified topology
makes the effect of carrying capacity easier to isolate, but it does not capture
the routing complexity of a large industrial warehouse.

Second, only a single robot is considered. Real robotic warehouse systems may
contain many robots, introducing congestion, collision avoidance, task
allocation, and coordination problems.

Third, the main factorial experiment contains only two and three packages.
Preliminary testing with four packages showed that capacity-one planning could
become substantially more computationally expensive, so larger scenarios were
excluded in order to keep the complete experiment tractable.

Fourth, only two carrying capacities are evaluated. The results therefore
describe the transition from capacity one to capacity two and should not be
assumed to scale linearly to larger capacities.

Fifth, the experiment uses one planner and one planner configuration,
`opt-hrmax`. Different heuristics or planning systems could produce different
search-complexity behavior.

Sixth, the generated scenarios are synthetic rather than derived from real
warehouse operational traces. The experiment therefore provides a controlled
study of causal factors rather than an estimate of performance in a specific
industrial warehouse.

Finally, planning-time measurements were collected from individual executions
rather than repeated runtime trials for every identical problem. Runtime
results should therefore be interpreted together with the more stable node and
state metrics.

## H. Future Extensions

Several extensions could build on this work.

The warehouse topology could be expanded to include additional aisles,
alternative routes, and asymmetric travel costs.

Larger package sets could be investigated using longer timeouts or more
efficient experimental infrastructure.

Multi-robot planning would allow carrying capacity to be studied together with
task allocation and robot coordination.

Additional carrying capacities could be tested to determine whether the
observed improvements continue beyond capacity two or exhibit diminishing
returns.

The experiment could also be repeated with alternative ENHSP heuristics or
other numeric planners to determine how strongly the observed search-complexity
effects depend on the planning algorithm.

Finally, real or realistic warehouse order distributions could replace the
synthetic scenario generator, allowing the practical value of carrying
capacity to be studied under workload distributions closer to industrial
operations.
