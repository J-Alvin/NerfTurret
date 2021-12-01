"""
    Tracked Object is a class fopr managing the actively tracked person that enters the frame.
    Responsibilities inlcude:
        Determining if a box in frame is moving
        Determining if the Box in a frame is the current object
        Prediction of objects location
"""
import cv2
from numpy.lib.function_base import select
from math import sqrt

def get_box_center(box):
    x = ( box[0] + box[2] ) / 2
    y = ( box[1] + box[3] ) / 2

    return x, y


class Point:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
    def divide(self, other):
        self.x = self.x / other
        self.y = self.y / other
        return self

    def multiply(self, other):
        self.x = self.x * other
        self.y = self.y * other
        return self

    def __str__(self):
        return f"({self.x}, {self.y})"

    def get_distance_to(self, target_point):
        temp = target_point - self
        return sqrt(temp.x ** 2 + temp.y ** 2)


class Velocity:
    x_target = 0
    y_target = 0

    def __init__(self):
        self.points = list()
        self.max_points = 30
        self.fiter_distance = 500

    def add_point(self, x, y):
        new_point = Point(x,y)
        if len(self.points) > 0:
            if new_point.get_distance_to(self.points[-1]) <= self.fiter_distance:
                self.points.append(Point(x,y))
            else:
                return
        else:
            self.points.append(Point(x,y))

        # If list is at its max length, remove the first index
        if len(self.points) > self.max_points:
           self.points.pop(0)


    
    def calc_direction(self):

        # We need at least 2 points to calculate direction
        if len(self.points) > 1:
            start = None
            target = None

            average_direction = Point(0, 0)


            for p in self.points:  

                # Initialize the values we need          
                if start is None:
                    start = p
                elif target is None:
                    target = p

                # We can start math
                if (start is not None and target is not None):
                    average_direction = average_direction + (target - start)
                    start = target
                    target = None

            # Gets us the average vector over the list
            average_direction = average_direction.divide( len(self.points) )
            return average_direction


        return Point(0, 0)


class TrackedObject: 
    def __init__(self):
        self.tracked_box = None
        self.velocity = Velocity()
    

    def update(self, image, box):

        # Box related Updates
        if box is not None:

            # Initialize tracking
            if self.tracked_box is None:
                self.tracked_box = box

            # Add the point to the list
            x,y = get_box_center(box)
            self.velocity.add_point(x, y)

        else:
            if len(self.velocity.points) > 0:
                direction = self.velocity.calc_direction()
                last_p = self.velocity.points[-1]
                projected_p = last_p + direction.multiply( 1 )
                self.velocity.add_point(projected_p.x, projected_p.y)



        direction = self.velocity.calc_direction()
        if len(self.velocity.points) > 0:
            last_p = self.velocity.points[-1]
            projected_p = last_p + direction.multiply( 1 )
            image = cv2.circle(image, (int(projected_p.x),int( projected_p.y)), 20, (250, 250, 250), 2)
            print(direction)
            

    