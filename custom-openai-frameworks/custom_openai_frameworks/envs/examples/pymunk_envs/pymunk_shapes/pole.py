"""Imports"""
import pymunk

class Pole:
    """Pole"""

    def __init__(self, b0):
        p0 = (400, 10)
        p1 = (400, 690)
        d = 2
        
        mass = 1
        moment = 1
        self.body_pole = pymunk.Body(mass, moment, pymunk.Body.KINEMATIC)
        self.shape_pole = pymunk.Segment(self.body_pole, p0, p1, d)
        self.shape_pole.elasticity = 1
        self.shape_pole.friction = 1
        self.shape_pole.filter = pymunk.ShapeFilter(group=1)
        self.shape_pole.filter = pymunk.ShapeFilter(group=2)

    def get_all(self):
        """get all"""
        return (self.body_pole, self.shape_pole)
