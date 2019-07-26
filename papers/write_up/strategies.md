Strategies
==========

Let the action space $U$ be the set of all possible bounce angles a robot may execute
(defined either in the robot's local frame, or in a wall-plane frame).

A strategy is a sequence of actions.

If a strategy incorporates sensor feedback, it can be represented as a state
machine. States in this machine are strategies, and in general will be repeated
indefinitely until a sensor signal or counter interrupts.

Take a robot with possible bounce angles $b_1, b_2,$ and $b_3$. Strategies will
be lists of these three elements (free monoids over the set). We may also allow
strategies to be defined by their *generator*, which may be a function over some
previous window of bounce angles, or a randomized choice from the set of bounce
angles.

Allows for time-evolving strategies like "for 10 bounces, choose bounce uniformly 
at random from ${b_1, b_2, b_3}$. Then, for 100 bounces, choose bounce uniformly at random
from set of all bounces which have previously occurred."

bounce until close enough to pebble. Then pick up pebble, drop again after X
bounces in next strategy.

alternate between two bounce angles.

alternate between three bounce angles (loop through list).

Equivalent:
- fixed list of n actions 
- $\pi_k: Z+ \to U$ action at each stage
- n-state DFA on bounce angles with one outgoing edge per state (unifilar)
- 1-state DFA on strategies

DFA on bounce angles with counter as sensor -> reduction in state space

Can also let $U$ be the set of bounce intervals that the robot may accomplish.

Strategy options:
-----------------

Always assume start and goal intervals are convex; later can investigate
strategies that work from multiple disconnected starts.

Our fundamental assumption is that the robot's actions have *some* amount of
uncertainty. So we search for strategies which are transitions in the safe bounce
visibility graph: these transitions represent actions which may be successful
under uncertainty from *anywhere* on the orginating segment. It may be true that 
for certain navigation tasks (ie: getting through a narrow hallway or doorway), 
lots of uncertainty cannot be tolerated.

The visibility decomposition provides a natural partition that does not depend
on any particular design parameters of the robot. In most polygons, it provides
good coverage in the safe visibility graph (**what about orthogonal polygons as
special case?**).

Our approach is not complete even within this assumption; in particular, we do
not find strategies that are asymptotically complete, such as bouncing randomly
until the robot makes it through the doorway, or the last example in [Jason's
paper]. (Though, structure in the nondeterminism of robotic maneuvers may make
such strategies not feasible anyway...)

Types of Problem Formulation:

Assume that if robot is in same partition segment as G, can navigate to G with
local sensors. So why not just wall follow? Possible answers: goal could be on
different connected component of dP. Could be less efficient to wall-follow.
Some strategies may have coverage criteria.

1. start and goal intervals are within one partition of P'
    - strategy <-> path in P'
2. start interval spans multiple partitions of P', goal interval is within one
partition
    - find paths from each node in S to G node in P'
    - while searching:
        for all start states:
            take one step forward
            find all ranges that work for all start states (intersection); add
                each to a different strategy. Resulting states are new start states.
            discard steps/strategies which do not admit common strategy
    - stop when goal node is found by all start states on the same step
3. start and goal intervals span multiple partitions of P'
    - same as 2, but stop when all start states transition to any goal states
      on same step


Strategies:
1. shortest path in bounce-viz graph (shortest # of bounces)
2. path with largest valid angle interval (for constant bounce controller)
    - can intersect safe angle intervals as you search graph
    - stop when interval empty or goal is found
        - "goal is found" when robot interval covers goal on same segment
    - can we do branch and bound to discard paths with very small angle
      intervals? not sure we have enough structure
3. shortest path in bounce-viz graph where edge weights encode expected distance
    - uniform expectation over interval?
    - otherwise would have to propagate intervals from start state (constant time calc per
      edge)
4. use limit cycles

