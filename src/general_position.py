def IsThreePointsOnLine(p1, p2, p3):
    degeneracy_error = 0.00001
    cross_prod = (p1[1] - p2[1]) * (p3[0] - p2[0]) - (p1[0] - p2[0]) * (p3[1] - p2[1])
    return abs(cross_prod)<degeneracy_error

# true if p3 is in line with and in between p1 and p2
def IsThreePointsOnLineSeg(p1, p2, p3):
    if IsThreePointsOnLine(p1, p2, p3):
        v1 = (p1[0]-p3[0], p1[1]-p3[1])
        v2 = (p2[0]-p3[0], p2[1]-p3[1])
        return (v1[0]*v2[0]+v1[1]*v2[1])<0
    return False

# return true if the four given points are not in general position
def SegsInGeneralPos(p1, p2, q1, q2):
    tests = (IsThreePointsOnLine(p1, p2, q1) or
           IsThreePointsOnLine(p1, p2, q2) or
           IsThreePointsOnLine(q1, q2, p1) or
           IsThreePointsOnLine(q1, q2, p2))
    return (not tests)

def PolyInGeneralPos(poly):
    for (a,b,c) in combinations(poly,3):
        if IsThreePointsOnLine(a,b,c):
            return False
    return True
