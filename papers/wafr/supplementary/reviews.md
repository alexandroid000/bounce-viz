Todo:
-----

-   Section 4 needs a few more figures to more clearly explain some of the
    concepts. As this is the foundational contribution of this paper, clarity
    here is vital. Suggestions include a figure of a visibility polygon and a
    bounce visibility graph (or subset of one) for a very simple example. In
    addition, it would be helpful to add labels to Figure 3 denoting the origin
    of the ray v_i and the intersection with the boundary v_i'.

-   More discussion on how obstacles/holes can be treated with this approach.
    Rarely does a practical application operate in an obstacle-free environment,
    so this needs to be more thoroughly addressed. Even if the approach is to
    partition the environment polygon into monotone pieces to remove holes, this
    should be explained. One sentence at the end of the paper about such an
    important practical issue is not sufficient.

-  Proof of Corollary 1 and Proposition 3: In the proof of Corollary 1 and
    subsequently Proposition 3, it is unlcear to me how the authors are handling
    the situation of two consecutive edges with an angle of 180 deg. between
    them. Such cases will arise frequently in the polygon P' by construction of
    introducing vertices along edges of P. Since a reflex vertex is a vertex
    with internal angle strictly greater than 180, vertices with internal angles
    equal to 180 are not reflex vertices. For example in Figure 5, consider the
    edge (7,8). Corollary 1 says that for edge (7,8) there exists a safe action
    between (7,8) and (7,6), which is true. It also says that there exists a
    safe action between (7,8) and (8,9), which does not seem to be true. The
    safe action is between (7,8) and (0,1), which does not share a vertex.

-  An action is defined to be safe, if there is some interval of angle (however
    small it might be) that exists. However, in practice, the robot may
    have some accuracy limitation when turning, which implies even though an action
    may be deemed safe by the algorithm, the robot may not be able to accomplish the
    action reliably. Since the goal of using safe actions is to guarantee that a
    robot can reach one edge from another, it seems that the robot's capability (of
    turning by a certain angle within an error bound) should be part of the
    definition of safe action. I understand that the theorems/proofs become messy if
    we consider this, since it would become difficult to guarantee existence of
    contraction maps and limit cycles based on the environment alone. However, a
    discussion about this would be helpful.

-   Authors have well explained algorithm 2 example scenario of graph G\_safe in
    Fig 9 but experimental result is not analysed.
-   On reading along the line in the application and future work section, the
    contribution of work is lost. The paper describes about the contribution
    really well in section 4,5 and 6 but in section 7 and 8, the efficiency or
    stability of the algorithms proposed is questionable and what improvements
    the visibility based boundary partition contributes. The performance
    analysis of proposed work is not shown in the paper.
-   Comparison with other existing algorithms for navigation and patrolling is
    not discussed.


Done:
-----

-   Obstacles in the environment has not been considered. Robot bouncing off
    obstacles can be a viable topic to consider in the future work section.
-   Algorithm 2 is unclear, as how does it determine a best strategy ?, are
    there any set of strategies given during runtime among which it chooses the
    strategy best fitted for the path ?
-   The methods used within Algorithm 1 and 2 are not explained.
-   In Introduction, authors claim to be proposing a dual approach where at
    first, global geometric information about environment boundaries is provided
    to the system and secondly this global geometry is then processed to produce
    a strategy providing strong formal guarantees. I do not see any proof of it
    in the paper.
-   There are few typo errors in the paper. For example in proof of proposition
    5, first two lines doesn't give a clear understanding of what authors are
    trying to say ? as well as where does the parentheses end ?
-   In Definition 2, the part "In this paper" can be omitted. As readers do get
    an idea that the conditions are restricted for analysis in this paper.
- I have another nit picky comment about the use of the term "bounce law". In
  science, the terminology law is used to describe an observed physical
  phenomenon. In this paper, the bouncing rules are computational constructs
  that helps in designing algorithms with certain properties. They are not for
  describing any observed phenomenon. So, to avoid implicitly redefining
  existing terms that can be potentially confusing, I would request the
  authors to use bounce rules or bounce maps instead of bounce laws.

Summaries:
----------


Summary:
This paper builds the theoretical framework for reasoning about paths for planar
robots that travel in straight lines and "bounce" off boundaries. Many
commercial robots behave this way for various applications. Instead of assuming
either high environment knowledge and high-res sensors or no environment
knowledge and low-res sensors, they target typically deployments where the basic
environment is known (e.g., a floorplan) but the robot has limited sensing
(e.g., a bump sensor). They use the known environment to precompute a bounce
visibility graph which encodes how the visibility of environment boundary
vertices change as the robot bounces off the boundary. They can use this
structure to classify path families and define "safe actions" that are
guaranteed to be successful. They show how they can then use this framework to
reason about navigation and patrolling applications.

Comments:
While seemingly simple, this application domain is under-studied and of
practical importance as many commercially available mobile robots operate with
this motion model (straight line traversal and bouncing) with limited sensing
capabilities. The theoretical development for reasoning about these types of
paths is highly relevant to this audience.

Summary:
In this paper, the authors present strategies for simple mobile robots equipped
with sensors to detect obstacles and capable of turning in place to move within
a simple polygon by bouncing off walls, when they reach a wall. They show that
one can compute bouncing strategies that are robust to the uncertainty in
turning to accomplish a periodic motion within the polygon. This capability of
periodic safe motion is then utilized to solve some simple navigation and
patrolling problems in a simple polygon. Overall, the paper is very well written
and well organized. The literature cited is adequate. The technical problem
proposed here is very interesting and the use of limit cycles to design
trajectories is elegant. Although, the results are restricted to a simple
polygon, I believe that the results presented here are an important contribution
towards understanding the capabilities that we can accomplish with simple robots
and strategies in more complex environments, which are robust to uncertainty.
These results will also be useful even if the robots have more capabilities. I
have a minor technical concern regarding the completeness of a couple of proofs
which is detailed below.


In this paper, the authors attempt to propose navigation and patrolling
approaches in simply connected polygons that would result in the robot
navigating and performing the behavior. The authors described their approach
on a polygon and simplifications made to model the robot (as a point
robot). They also described the allowable motion being that of rotation and
driving straight until hitting an obstacle. They also described bounce
moves that are allowed and how the polygon is partitioned along with the
graph that is created and used in their approach. They describe safe
actions that can be taken given the bounce approaches they use. Although
some examples are shown, no real results are presented.

The authors didn't clearly describe how they used the resulting graph or
even why it's very important. I was left with thinking that this was some
structure that they can create but was never really clear on why they
created it. This highlights that portions of the paper were somewhat
confusing. The problem description was okay and the motion model used was
also clear. Sections after that seemed to lack the clarity of the initial
sections.

It's really not clear how uncertainty plays a part in the paths they are
describing. By page 9, it's still not clear how they want to handle this.
It would seem that by Sec. 6 they would have clearly defined how they model
uncertainty in this system and what the maximum amount of uncertainty is
for their approach to be viable.

The distinction they make between navigation and patrolling isn't very
clear. It's really not clear why their approach is needed for this. In one
example they describe how the robot leaves one area and then goes on to
patrol but it's not clear if the approach being used is for patrolling or
the navigation one.


Even a basic 2D office building with many rooms might make
this approach more interesting. Additionally, the authors should compare
their work against something. Unless their only contribution is to say
using safe actions and their approach they can achieve their desired
results but this alone hardly seems to be a contribution. It seems like one
of the main things missing is some real motivation on why this approach is
needed. They mentioned early on that other approaches require much more
computational power and that this approach requires less and only bump
sensor information. Surely they could come up with an algorithm to test
against in a somewhat real-world environment. In fact, given the early
discussion on the similarities of their approach to that of the
roomba/iCreate, I was expecting some application of their approach on that
type of robotic platform. It would have been a nice addition to their work
to show their approach applied to real robots.

The paper introduces a new data structure, the bounce visibility graph, which is
generated from a polygonal environment definition. It considers simple robots
with "bouncing" behaviors: robots that travel in straight lines in the plane,
until encountering an environment boundary, at which point they rotate in place
and set off again. This data structure was used to determine the feasibility of
path-based tasks such as navigation and patrolling under actuator uncertainties.
It have been used to generate a strategy (sequence of non-deterministic
rotations), or to limit uncertainty in the robot's position.

The work also focuses on building strategies for mobile robots such as vacuum
cleaners, pool cleaners, lawn mowers, etc. The path strategized for these robots
have certain properties, based on the task achieved by the robot. They mentined
two existing algorithmic approaches to build a path for these robots as SLAM
(high-fidelity sensors and map generating algorithms) and Random navigation
strategies. This paper proposes a dual approach in which, a global geometric
information about the environment boundaries is provided to system, either
beforehand or calculated using SLAM. This geometry is then processed to produce
a strategy that consumes minimal power and low bandwidth local sensors.

Strengths :
-   The work simplifies characterization and generation of paths by using the
    geometric structure of a polygonal environment to create a combinatorial
    representation of the environment over a finite number of families of paths.
-   The work controls uncertainty in the robot's position using dynamical
    properties of path of the linear mapping function, i.e. contraction, points
    between line segments are often contracts : two points under the function become closer together.
-   The bouncing visibility diagram and bounce law is well explained with
    example in Fig 5. A visibility-based boundary partition has been defined
    that partitions the given polygonal environment into partial local sequence
    based on the robot's "bouncing laws".
-   All definitions, laws, and algorithms are supported using mathematical
    diagrams.
-   Mathematical analysis of given problem are simple and effective.
-   Based on bounce law results, authors describe safe actions required for
    robot to take to avoid collision with boundaries of the environment. This
    safe action is determined by rotation or diversion robot needs to take to
    follow a straight line path in the free space.
-   The work uses concept of limit cycles to determine the fixed points on edges
    of polygon using Banach fixed point theorem. This condition can be used to
    terminate the generation of paths once all fixed points in the space are
    covered.
-   The work considers application of bouncing visibility graph for Navigation
    and Patrolling tasks. The definitions provide with suggestions/informations
    to perform these tasks successfully.
    
