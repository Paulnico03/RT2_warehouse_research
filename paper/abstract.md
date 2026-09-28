# Abstract

Robot carrying capacity can influence both the physical execution of warehouse
tasks and the computational difficulty of planning them. This work evaluates
the effect of increasing a warehouse robot's carrying capacity from one to two
packages in a deadline-constrained PDDL+ planning domain.

The original single-package model was generalized using numeric fluents for
current load and maximum capacity. A controlled factorial experiment was then
performed by varying package count, deadline tightness, and package
distribution while evaluating both capacity configurations on identical
warehouse scenarios. Twenty reproducible seeds were generated for each
condition, producing 160 paired scenarios and 320 ENHSP planner executions.

Capacity one solved 72.50% of the scenarios, compared with 93.75% for capacity
two, an increase of 21.25 percentage points. An exact McNemar test confirmed a
significant difference in paired solvability (p = 1.16 × 10^-10). Among the 116
scenarios solved by both capacities, capacity two reduced mean makespan by
28.54%, plan length by 23.34%, expanded nodes by 61.93%, and evaluated states
by 57.80%.

The results also show that the benefit of additional capacity depends on
package layout. Large improvements occur when multiple packages can share part
of the same route, whereas two-package distributed scenarios show little or no
mission-level benefit. These findings indicate that robot carrying capacity
should be evaluated jointly with spatial task structure and deadline
constraints when designing warehouse planning systems.
