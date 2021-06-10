import random, math, pickle
import numpy as np

from utils import distance, Point, Vector
from figures import plotPoints
from images import binarize_color


class RRT:
    def __init__(self, matrix):
        self.matrix = matrix
        self.nodes = []
        self.distance_matrix = {}

    def rrt(self, startN : Point, endN : Point, termination_threshold=10, delta_x_threshold=20):
        if not startN.z >= self.matrix[startN.x][startN.y] or not endN.z >= self.matrix[endN.x][endN.y]:
            raise Exception

        self.nodes.append(startN)
        self.distance_matrix[startN] = {}

        tree = [[startN], [endN]]

        while True:
            newNode = Point(random.randint(0,len(self.matrix) - 1), random.randint(0,len(self.matrix[0]) - 1), random.random())
            while len([point for point in self.nodes if point.equals(newNode)]) > 0:
                newNode = Point(random.randint(0,len(self.matrix) - 1), random.randint(0,len(self.matrix[0]) - 1), random.random())

            if not newNode.z < self.matrix[newNode.x][newNode.y]:
                # Point is in an obstacle  
                print('Point is in an obstacle')
                # plotPoints([obstacles, [newNode]], 'In Obstacle')
                continue

            minDistance = None
            minDistanceNode = None
            for node in self.nodes:
                curr_distance = distance(node, newNode)
                if curr_distance > 20 and (minDistance is None or curr_distance < minDistance):
                    minDistanceNode = node
                    minDistance = curr_distance

            if minDistance is None or minDistance > 100:
                #Point is two close to its nearest node
                continue


            # plotPoints([obstacles, [newNode, minDistanceNode]], 'Current Testing Points')

            validLine, line = self.validateLine(newNode, minDistanceNode)
            if not validLine:
                # Line between nearest node and new node intersected an object
                print('Point connection to nearest node intersects Maze')
                continue


            self.nodes.append(newNode)
            if not newNode in self.distance_matrix:
                self.distance_matrix[newNode] = {}

            self.distance_matrix[newNode][minDistanceNode] = minDistance
            self.distance_matrix[minDistanceNode][newNode] = minDistance
            tree.append(line)
            print('Point passed')
            # plotPoints(tree, 'Progress')



            if distance(newNode, endN) < termination_threshold:
                self.distance_matrix[newNode][endN] = distance(newNode, endN)
                self.distance_matrix[endN] = {}
                self.distance_matrix[endN][newNode] = distance(newNode, endN)
                print('Termination Condition Met')
                break
        return tree


    def getDistanceMatrix(self):
        return self.distance_matrix

    def validateLine(self, p1 : Point, p2: Point):
        line = [p1, p2]

        vec = Vector(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)      

        vec_norm = vec.normalize()
        vec_traversed = Vector(0,0,0)

        p1Vector = Vector(p1.x, p1.y, p1.z) 

        while not vec_traversed.magnitude() > vec.magnitude() - 1.0:
            vec_traversed = vec_traversed.add(vec_norm)
            check = vec_traversed.add(p1Vector)

            line.extend([Point(check.x, check.y, check.z)])

            if not check.z < self.matrix[math.floor(check.x)][math.floor(check.y)] and not check.z < self.matrix[math.ceil(check.x)][math.ceil(check.y)]:
                return False, line

        # plotPoints([obstacles, line], 'Validation')
        return True, line



res, image = pickle.load(open('v0DepthOutput_ms1.pkl', 'rb'))
image = np.flip(np.reshape(image, (res[0], res[1])), 0)

controller = RRT(image)

tree = controller.rrt(Point(255, 359, z=image[int(255)][int(359)]), Point(211, 317, z=image[int(211)][int(317)]))
plotPoints(tree, "FINAL")
pickle.dump(controller.getDistanceMatrix(), open('distance_matrix.pkl', 'wb'))