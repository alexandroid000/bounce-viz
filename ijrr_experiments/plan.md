
Both reviewers request additional evaluations of the method. The Guest Editors
also agree with this assessment and feel that, in particular, the authors should
run additional experiments to characterize the algorithmic performance of the
paper with respect to which parts of polygons are not reachable using safe
actions. This should sufficiently expand the experimental evaluation.


One interesting result is that sometimes the geometry of a polygon means that
some of its parts are not reachable by a safe action. There is not currently a
good understanding of how prohibitive this is. The paper can be improved by the
addition of new experiments to characterize this phenomenon (e.g., using monte
carlo sampling). Possible questions include: (A) With respect to some random
polygon generation process, what percentage of polygons contain parts that are
not reachable using safe actions. (B) With respect to some random polygon
generation process, what is the expected percentage of a polygon (i.e., its edge
count) that is not reachable using safe actions.

The most interesting result (at least to this reviewer) is the two room example.
While this was interesting, it was made to seem like this approach would be
beneficial in something like an office or building example. This seems to be a
somewhat limiting their contribution as they do not show more interesting
examples where their approach works. Even a basic 2D office building with many
rooms might make this approach more interesting. Additionally, the authors
should compare their work against something (even just purely random). Unless
their only contribution is to say using safe actions and their approach they can
achieve their desired results but that alone seems to be less of a contribution.

- polygon generation processes:
    - random tree of convex rooms
    - random spiky polygon (sweep queries over range of irregularity/spikiness)
- generate initial state:
    - monte carlo (uniform from boundary)
    - iterate reachability query over all edges
- queries:
    - what percentage of polygons contain parts that are not reachable using
      safe actions from anywhere except themselves
    - what is the expected percentage of a polygon (edge count / measure) that
      is not reachable using safe actions from anywhere
    - same queries but for "sinks" (edges of polygon with no outgoing safe
actions)
    - what percentage of the polygon can reach the sink under safe actions?
