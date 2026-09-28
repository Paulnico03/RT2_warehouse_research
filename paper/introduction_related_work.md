# I. Introduction

Automated and robotized warehouse systems have become an important area of
research because mobile robots can support flexible material-handling and
order-fulfillment operations. Modern robotic warehouse systems introduce
planning and control problems involving routing, task allocation, storage,
order picking, and the coordination of autonomous vehicles [5], [6].
Consequently, the capabilities assigned to each robot can influence not only
the physical execution of warehouse tasks, but also the structure and
difficulty of the associated planning problem.

One capability of particular interest is the number of packages that a robot
can transport simultaneously. A robot restricted to carrying one package at a
time may need to revisit the same warehouse area several times, whereas a robot
with a larger carrying capacity may collect multiple packages during a single
visit. However, additional capacity does not necessarily imply an advantage in
every situation. If packages are located in different parts of the warehouse,
the robot may be unable to exploit its additional capacity. Similarly, when
delivery deadlines are restrictive, carrying capacity may determine whether a
feasible plan exists at all.

These characteristics connect warehouse planning with the broader class of
pickup-and-delivery problems. Classical work on pickup-and-delivery routing
considers the transportation of loads between origins and destinations subject
to operational constraints [8]. The pickup-and-delivery problem with time
windows further combines routing decisions with vehicle-capacity, precedence,
and temporal constraints [7]. Such formulations provide an important
operations-research foundation for studying transportation capacity and
deadlines. In the present work, however, the problem is studied from an
automated-planning perspective using an explicit symbolic and numeric model of
the robot, the packages, continuous time, and deadline events.

PDDL+ provides a suitable representation for this purpose because it extends
planning-domain modelling with autonomous processes and events, allowing
mixed discrete-continuous behavior and time-dependent effects to be expressed
within the planning model [1]. Numeric heuristic-search methods have further
extended the range of numeric planning problems that can be addressed
efficiently [2]–[4]. In this project, the warehouse domain is solved using the
ENHSP numeric planner, with the `opt-hrmax` configuration.

The starting warehouse model allowed the robot to carry only one package at a
time. This work generalizes that representation by replacing the binary
hand-empty condition with numeric fluents representing the robot's current
load and maximum carrying capacity. The same planning domain can therefore be
instantiated with a carrying capacity of either one or two packages without
changing the remaining problem definition.

The central research question is:

**How does increasing robot carrying capacity from one to two packages affect
solvability, mission makespan, plan length, and planning complexity under
different package distributions and deadline constraints?**

To answer this question, a controlled factorial experiment was constructed.
The experiment varies the number of packages, deadline tightness, and spatial
package distribution while evaluating each generated scenario twice: once
with robot capacity one and once with capacity two. Twenty reproducible random
seeds are used for every combination of conditions, producing 160 paired
scenarios and 320 planner executions.

The study evaluates two complementary aspects of performance. First,
*feasibility* is measured by whether the planner can produce a valid
deadline-respecting plan. Second, for scenarios solved under both capacities,
*efficiency* is evaluated through mission makespan, plan length, expanded
search nodes, evaluated states, and planning time. Because the two capacity
conditions use the same underlying scenarios, paired statistical tests can be
used to distinguish systematic effects of carrying capacity from differences
between problem instances.

The main contribution of this work is therefore not only a generalized
capacity-aware PDDL+ warehouse model, but also a reproducible experimental
method for evaluating how a physical robot capability interacts with spatial
task structure, temporal constraints, and planner search complexity.
Additionally, a ROS2 interface and an interactive Jupyter notebook are
provided to execute individual planning experiments and inspect the resulting
metrics.

# II. Related Work

## A. PDDL+ and Numeric Automated Planning

The Planning Domain Definition Language family provides a standard formalism
for expressing automated-planning problems. Fox and Long introduced PDDL+ to
model domains containing both discrete actions and continuous autonomous
behavior [1]. In PDDL+, processes can represent continuously evolving state
variables while events model instantaneous transitions triggered by changing
conditions. This is particularly appropriate for the warehouse model used in
this work: robot motion and the passage of package deadline time can evolve
autonomously, while a deadline violation can be represented as an event.

Efficient search in numeric planning requires heuristics that reason about
numeric as well as propositional state variables. Scala, Haslum, and Thiébaux
extended the subgoaling principle underlying classical planning heuristics to
numeric planning, including an admissible variant suitable for optimal numeric
planning [2]. Scala et al. also developed interval-based relaxation techniques
for general numeric planning, including problems containing non-linear
expressions, cyclic numeric dependencies, and autonomous processes [3].
Subsequent work further developed subgoaling techniques for both satisficing
and optimal numeric planning and demonstrated their use within forward
state-space heuristic search [4].

These developments provide the methodological basis for using heuristic
numeric planning in the present experiment. Rather than implementing a custom
routing optimizer, the warehouse is encoded as a PDDL+ planning problem and
solved with ENHSP. This allows carrying capacity, continuous package aging,
movement, deadlines, and delivery actions to be represented within the same
planning model.

## B. Robotic Warehouse Systems

Warehouse automation has increasingly incorporated autonomous and robotic
handling systems. Azadeh, De Koster, and Roy survey robotized and automated
warehouse technologies and identify planning and control as major research
areas, including storage decisions, order picking, routing, batching, and
assignment [5]. Their review emphasizes that the autonomous and networked
nature of modern warehouse systems creates operational characteristics that
require dedicated planning and optimization methods.

Barros and Nascimento provide a complementary survey focused specifically on
Robotic Mobile Fulfillment Systems [6]. Their work reviews warehouse layouts,
routing methods, system architectures, and algorithmic approaches involving
mobile robots, while also identifying continuing opportunities for research
in robotic warehouse planning. These surveys motivate the simplified
warehouse abstraction used in the present study: although the experimental
environment contains only a small number of locations and a single robot, it
isolates a fundamental operational variable—carrying capacity—that can affect
routing decisions and task feasibility.

## C. Pickup-and-Delivery Problems, Capacity, and Deadlines

The warehouse task considered here is closely related to pickup-and-delivery
routing. Savelsbergh and Sol describe the general pickup-and-delivery problem
as the transportation of loads from origins to destinations and survey the
characteristics and methods that distinguish these problems from conventional
vehicle-routing formulations [8]. Carrying capacity is therefore a natural
constraint in this class of transportation problems.

Temporal constraints introduce an additional dimension. Dumas, Desrosiers,
and Soumis formulate the pickup-and-delivery problem with time windows as a
routing problem in which transportation requests must satisfy pickup and
delivery requirements together with capacity, temporal, and precedence
constraints [7]. This combination is conceptually close to the present
warehouse experiment, where packages must be collected and delivered before
their individual deadlines.

The present study differs from these classical vehicle-routing formulations
in both representation and evaluation objective. Instead of optimizing a
fleet-routing formulation directly, it represents a single warehouse robot as
a numeric PDDL+ planning domain. More importantly, carrying capacity is
treated as the experimental variable in a paired study. The analysis therefore
examines not only its effect on route-level quantities such as makespan, but
also its effect on plan feasibility and heuristic-search complexity.

This distinction is particularly important for the experimental design.
Increasing capacity can reduce repeated travel when several packages are
clustered at the same location, but it may offer little or no route-level
benefit when packages are spatially separated. By explicitly varying both
package distribution and deadline tightness, the experiment investigates this
interaction rather than assuming that a higher capacity is universally
beneficial.
