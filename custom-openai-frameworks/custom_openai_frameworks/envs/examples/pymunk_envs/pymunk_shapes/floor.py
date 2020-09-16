"""Imports"""
import pymunk

class Floor:
    """Floor"""

    def __init__(self, b0):
        p0 = (0, 10)
        p1 = (800, 10)
        d = 2

        self.segment1 = pymunk.Segment(b0, p0, p1, d)
        self.segment1.elasticity = 1
        self.segment1.friction = 1

    def get_all(self):
        """get all"""
        return self.segment1
