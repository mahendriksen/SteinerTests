import numpy as np
from shapely import affinity 
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon, LinearRing, LineString
import random
from itertools import permutations, combinations
from math import perm, comb, radians, sin, cos, sqrt
import sys
import matplotlib.pyplot as plt

def calculate_point_on_other_side_of_p2(p1, p2, distance_p2_to_p3): #what it says on the tin
    deltaX = p1[0]-p2[0]
    deltaY = p1[1]-p2[1]
    distance_p1_to_p2 = sqrt(deltaX*deltaX + deltaY*deltaY)
    scale = distance_p2_to_p3 / distance_p1_to_p2 
    p3= (p2[0] - deltaX * scale, p2[1] - deltaY * scale)
    return(Point(p3))

def perpline(p1,p2,p3): #makes the  lines containing the edges of the pentagon incident to p3
    dist = sqrt((p1[0]-p3[0])**2 + (p1[1]-p3[1])**2)
    newpoint = calculate_point_on_other_side_of_p2(p1, p2, dist)
    return(LineString([newpoint,p3]))
 
def angle(p1,p2,p3): #finds angle of p1,p2,p3 in degrees
    ba = [p1[0] - p2[0],p1[1] - p2[1]]
    bc = [p3[0] - p2[0],p3[1] - p2[1]]

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    return(np.degrees(angle))

def rotatedpoint(p1, p2, angle): #rotates p2 around p1 by given angle
    qx = p1[0] + cos(radians(angle)) * (p2[0] - p1[0]) - sin(radians(angle)) * (p2[1] - p1[1])
    qy = p1[1] + sin(radians(angle)) * (p2[0] - p1[0]) + cos(radians(angle)) * (p2[1] - p1[1])
    return Point(qx, qy)    

def verticalconstraint(p1,p2,p3): #check if p3 is in Jae's vertical constraint made by p1,p2.
    if p1[1] == p2[1]:
        return (min(p1[0],p2[0]) <= p3[0] <= max(p1[0],p2[0]))
    else:
        m = -(p1[0]-p2[0])/(p1[1]-p2[1])
        return (min(p1[1]-m*p1[0],p2[1]-m*p2[0]) <= p3[1] - m*p3[0] <= max(p1[1]-m*p1[0],p2[1]-m*p2[0]))


n= int(input("How many terminals (in numerals)? "))

pointlist = []

for i in range(n): #randomly generates points
	newpoint = (random.random(),random.random())
	pointlist.append(newpoint)

interiorcounter = 0
i = 0
perms = perm(n,3)
combs = comb(n,3)

for combo in combinations(pointlist, 3):  # 2 for pairs, 3 for triplets, etc
    polygon = Polygon(list(combo))
    polygonempty = True
    for j in pointlist:
        if polygon.contains(Point(j)):
            polygonempty = False
    if not polygonempty:
        interiorcounter += 1
    i += 1                
    sys.stdout.write("\rCalculating iteration %i of %i of Part 1. That's %f %%" % (i,combs, i/combs *100))
    sys.stdout.flush()

print("\nWe discounted ", interiorcounter, " of ", combs, " possibilities using the triangle. That's ", 100*interiorcounter/(combs), "%")

vertcounter = 0
pentinteriorcounter = 0
bothcounter = 0
i = 0

for combo in permutations(pointlist, 3):  # 2 for pairs, 3 for triplets, etc
    vertchecker = verticalconstraint(combo[0],combo[1],combo[2])
    if not vertchecker: #for checking vertical constraint
        vertcounter += 1
    if angle(combo[0],combo[1],combo[2]) < 60 and angle(combo[1],combo[0],combo[2]): #for checking pentagonal constraint. If this angle condition not satisfied it reverts to the triangle case.
        if LinearRing(list(combo)).is_ccw: #counterclockwise case
            first60line = LineString([Point(combo[0]),rotatedpoint(combo[0],combo[1],60)])
            firstperpline = perpline(combo[1],combo[0],combo[2])
            firstpoint = first60line.intersection(firstperpline)
            second60line = LineString([Point(combo[1]),rotatedpoint(combo[1],combo[0],300)])
            secondperpline = perpline(combo[0],combo[1],combo[2])
            secondpoint = second60line.intersection(secondperpline)
            if firstpoint.is_empty or secondpoint.is_empty: #i.e. the pentagon does not exist
                # print('PING1')
                polygon = Polygon(list(combo)) 
            else:
                # print('PING2')
                polygon = Polygon([combo[0],combo[1],secondpoint,combo[2],firstpoint])
        else: #clockwise case
            first60line = LineString([Point(combo[0]),rotatedpoint(combo[0],combo[1],-60)])
            firstperpline = perpline(combo[1],combo[0],combo[2])
            firstpoint = first60line.intersection(firstperpline)
            second60line = LineString([Point(combo[1]),rotatedpoint(combo[1],combo[0],60)])
            secondperpline = perpline(combo[0],combo[1],combo[2])
            secondpoint = second60line.intersection(secondperpline)
            # xs = [point[0] for point in combo] # this part is for plotting if troubleshooting 
            # ys = [point[1] for point in combo]
            # print(firstpoint,secondpoint)
            # for i, txt in enumerate(['A','B','C']):
                # plt.annotate(txt, (xs[i], ys[i]))
            # plt.scatter(xs,ys)
            # plt.plot(*firstperpline.xy)
            # plt.plot(*first60line.xy)
            # plt.plot(*secondperpline.xy)
            # plt.plot(*second60line.xy)
            # plt.show()
            if firstpoint.is_empty or secondpoint.is_empty: #i.e. the pentagon does not exist
                # print('PING3')
                polygon = Polygon(list(combo)) 
            else:
                # print('PING4')
                polygon = Polygon([combo[0],firstpoint,combo[2],secondpoint, combo[1]])
                # xs = [point[0] for point in combo]
                # ys = [point[1] for point in combo]
                # for i, txt in enumerate(['A','B','C']):
                    # plt.annotate(txt, (xs[i], ys[i]))
                    # plt.scatter(xs,ys)
                    # plt.plot(*polygon.exterior.xy)
                    # plt.show()
    else:
        polygon = Polygon(list(combo))     
    polygonempty = True
    for j in pointlist:
        if polygon.contains(Point(j)):
            polygonempty = False
    if not polygonempty:
        pentinteriorcounter += 1
    if not vertchecker or not polygonempty: #for checking either constraint
        bothcounter += 1
    i += 1                
    sys.stdout.write("\rCalculating iteration %i of %i of Part 2. That's %f %%" % (i,perms, i/perms *100))
    sys.stdout.flush()

print("\nWe discounted ", vertcounter, " of ", perms, " possibilities using the vertical constraint. That's ", 100*vertcounter/(perms), "%")
print("We discounted ", pentinteriorcounter, " of ", perms, " possibilities using the pentagon. That's ", 100*pentinteriorcounter/(perms), "%")
print("We discounted ", bothcounter, " of ", perms, " possibilities combining the pentagon and vertical constraint. That's ", 100*bothcounter/(perms), "%")

print("\nThe improvement by considering the pentagon over the triangle was", 100*(pentinteriorcounter/(perms*(n-3)))/(interiorcounter/(combs*(n-3))) -100, "%")

xs = [point[0] for point in pointlist] # this part is for plotting the points 
ys = [point[1] for point in pointlist]
plt.scatter(xs,ys)
plt.show()
