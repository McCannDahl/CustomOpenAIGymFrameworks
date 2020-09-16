"""Imports"""
import pymunk

class Ragdoll:
    """Ragdoll"""

    def __init__(self):
        p = pymunk.Vec2d(400, 200)
        width = 30
        height = 80
        stiffness = 1000000
        damping = 100000
        armLength = 80

        vs = [(-width, height), (width, height), (width, -height), (-width, -height)]
        v0, v1, v2, v3 = vs
        moment = pymunk.moment_for_poly(mass=1, vertices=vs, radius=0)
        self.body1 = pymunk.Body(mass=1, moment=moment)
        self.body1.position = p
        self.shape1 = pymunk.Poly(body=self.body1, vertices=vs)
        self.shape1.friction = 1
        #shape1.filter = pymunk.ShapeFilter(group=1)

        mass = 1
        radius = 40
        moment = pymunk.moment_for_circle(mass, 0, radius)
        self.body2 = pymunk.Body(mass, moment)
        self.body2.position = p+pymunk.Vec2d(0, height+radius)
        self.shape2 = pymunk.Circle(body=self.body2, radius=radius)
        self.shape2.friction = 1
        self.joint2 = pymunk.PivotJoint(self.body1, self.body2, (0,height), (0, -radius-1))
        self.joint22 = pymunk.DampedRotarySpring(self.body1, self.body2, 0, stiffness, damping)

        mass = 1
        radius = 5

        moment = pymunk.moment_for_segment(mass, (0,0), (armLength,0), radius)
        self.body3 = pymunk.Body(mass, moment)
        self.body3.position = p+pymunk.Vec2d(width, 0)+pymunk.Vec2d(armLength/2, 0)
        self.shape3 = pymunk.Segment(body=self.body3, a=(0,0), b=(armLength,0), radius=radius) 
        self.shape3.friction = 1
        self.joint3 = pymunk.PivotJoint(self.body1, self.body3, (width, 40), (-radius*2,0))
        self.joint32 = pymunk.DampedRotarySpring(self.body1, self.body3, 0, stiffness, damping)

        self.body4 = pymunk.Body(mass, moment)
        self.body4.position = p+pymunk.Vec2d(-width, 0)-pymunk.Vec2d(armLength/2, 0)
        self.shape4 = pymunk.Segment(body=self.body4, a=(0,0), b=(-armLength,0), radius=radius) 
        self.shape4.friction = 1
        self.joint4 = pymunk.PivotJoint(self.body1, self.body4, (-width, 40), (radius*2,0))
        self.joint42 = pymunk.DampedRotarySpring(self.body1, self.body4, 0, stiffness, damping)

        self.body5 = pymunk.Body(mass, moment)
        self.body5.position = p+pymunk.Vec2d(-width,-height)-pymunk.Vec2d(0, -armLength/2)
        self.shape5 = pymunk.Segment(body=self.body5, a=(0,0), b=(0,-armLength), radius=radius) 
        self.shape5.friction = 1
        self.joint5 = pymunk.PivotJoint(self.body1, self.body5, (-width, -height), (0,radius*2))
        self.joint52 = pymunk.DampedRotarySpring(self.body1, self.body5, 0, stiffness, damping)
        self.shape5.filter = pymunk.ShapeFilter(group=2)

        self.body6 = pymunk.Body(mass, moment)
        self.body6.position = p+pymunk.Vec2d(width,-height)-pymunk.Vec2d(0, -armLength/2)
        self.shape6 = pymunk.Segment(body=self.body6, a=(0,0), b=(0,-armLength), radius=radius) 
        self.shape6.friction = 1
        self.joint6 = pymunk.PivotJoint(self.body1, self.body6, (width, -height), (0,radius*2))
        self.joint62 = pymunk.DampedRotarySpring(self.body1, self.body6, 0, stiffness, damping)
        self.shape6.filter = pymunk.ShapeFilter(group=2)

    def get_all(self):
        """get all"""
        return (self.body1, self.shape1, 
                self.body2, self.shape2, self.joint2, self.joint22, 
                self.body3, self.shape3, self.joint3, self.joint32, 
                self.body4, self.shape4, self.joint4, self.joint42, 
                self.body5, self.shape5, self.joint5, self.joint52, 
                self.body6, self.shape6, self.joint6, self.joint62)


    def is_fallen(self) -> bool:
        """is fallen"""
        return abs(self.body1.angle) > (3.14/4.0)
