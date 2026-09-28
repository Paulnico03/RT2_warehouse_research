# VII. Conclusion

This work investigated how increasing the carrying capacity of a warehouse
robot from one to two packages affects deadline-constrained automated planning.

A generalized PDDL+ warehouse model was developed by replacing the original
Boolean single-package representation with numeric fluents describing the
robot's current load and maximum capacity. This allowed the same planning
domain to be evaluated under two robot-capacity configurations while keeping
the remaining warehouse model unchanged.

A controlled paired experiment was then performed using combinations of two
and three packages, relaxed and tight deadlines, clustered and distributed
package layouts, and 20 reproducible seeds per condition. The resulting
dataset contained 160 paired scenarios and 320 ENHSP planner executions.

The results show that increased carrying capacity can affect both task
feasibility and planning efficiency. Capacity one solved 72.50% of the tested
scenarios, while capacity two solved 93.75%. Thirty-four scenarios that were
unsolvable with capacity one became solvable with capacity two, while no
scenario showed the opposite outcome.

For the 116 scenarios solved under both capacities, capacity two reduced mean
mission makespan by 28.54% and mean plan length by 23.34%. It also reduced
search effort substantially, with mean reductions of 61.93% in expanded nodes
and 57.80% in evaluated states.

The experiment also demonstrates that the usefulness of additional carrying
capacity depends strongly on task structure. When packages are clustered,
capacity two can combine multiple pickups and reduce repeated travel. When two
packages are located in different aisles, the additional capacity may provide
little or no route-level advantage because both locations must still be
visited.

Therefore, carrying capacity should not be considered in isolation when
designing robotic warehouse systems. Its benefit depends on the interaction
between robot capability, package distribution, and temporal constraints.

Future work could extend the experiment to larger warehouse topologies,
additional package quantities and robot capacities, multi-robot systems,
alternative planning heuristics, and realistic warehouse workloads. Such
extensions would help determine how the effects observed in this controlled
study scale to more complex robotic logistics environments.
