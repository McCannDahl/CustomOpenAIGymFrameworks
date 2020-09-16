"""Imports"""
import pymunk

class Box:
    """Box"""

    def __init__(self, b0):
        p0 = (10, 10)
        p1 = (790, 790)
        d = 2

        x0, y0 = p0
        x1, y1 = p1
        pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

        i = 0
        self.segment1 = pymunk.Segment(b0, pts[i], pts[(i+1)%4], d)
        self.segment1.elasticity = 1
        self.segment1.friction = 1
        self.segment1.filter = pymunk.ShapeFilter(group=1)
        i = 1
        self.segment2 = pymunk.Segment(b0, pts[i], pts[(i+1)%4], d)
        self.segment2.elasticity = 1
        self.segment2.friction = 1
        self.segment2.filter = pymunk.ShapeFilter(group=1)
        i = 2
        self.segment3 = pymunk.Segment(b0, pts[i], pts[(i+1)%4], d)
        self.segment3.elasticity = 1
        self.segment3.friction = 1
        self.segment3.filter = pymunk.ShapeFilter(group=1)
        i = 3
        self.segment4 = pymunk.Segment(b0, pts[i], pts[(i+1)%4], d)
        self.segment4.elasticity = 1
        self.segment4.friction = 1
        self.segment4.filter = pymunk.ShapeFilter(group=1)

    def get_all(self):
        """get all"""
        return self.segment1, self.segment2, self.segment3, self.segment4
