"""Imports"""
import pymunk
import random

class Crawler:
    """Crawler"""

    def __init__(self):
        p = pymunk.Vec2d(400, 50)
        width = 60
        height = 20
        stiffness = 1000000
        damping = 100000
        armLength = 80
        
        self.min_angle = -3.14
        self.max_angle = 0

        mass = 3
        vs = [(-width, height), (width, height), (width, -height), (-width, -height)]
        v0, v1, v2, v3 = vs
        moment = pymunk.moment_for_poly(mass=mass, vertices=vs, radius=0)
        self.body_body = pymunk.Body(mass=mass, moment=moment)
        self.body_body.position = p
        self.shape_body = pymunk.Poly(body=self.body_body, vertices=vs)
        self.shape_body.friction = 1
        self.shape_body.filter = pymunk.ShapeFilter(group=2)

        mass = 1
        radius = 5
        armLength = 80
        moment = pymunk.moment_for_segment(mass, (0,0), (armLength,0), radius)
        self.body_leg = pymunk.Body(mass, moment)
        self.body_leg.position = p+pymunk.Vec2d(width, 0)
        self.shape_leg = pymunk.Segment(body=self.body_leg, a=(0,0), b=(armLength,0), radius=radius) 
        self.shape_leg.friction = 3
        self.shape_leg.filter = pymunk.ShapeFilter(group=2)
        self.joint_p = pymunk.PivotJoint(self.body_body, self.body_leg, (width, 0), (-radius*2,0))
        #self.joint_p.max_force = 100
        self.joint_p.error_bias = 0
        self.joint_p.max_bias = 1000
        self.joint_drs = pymunk.DampedRotarySpring(self.body_body, self.body_leg, 0, stiffness, damping)
        #self.joint_drs.max_force = 10
        #self.joint_drs.error_bias = 0
        self.joint_rlj = pymunk.RotaryLimitJoint(self.body_body, self.body_leg, self.min_angle, self.max_angle)
        #self.joint_rlj.max_force = 100
        #self.joint_rlj.error_bias = 0
        

    def get_all(self):
        """get all"""
        return (
            self.body_body, self.shape_body, 
            self.body_leg, self.shape_leg, self.joint_p, self.joint_drs, self.joint_rlj
        )
    
    def get_body_distance_from_ground(self):
        x, y = self.body_body.position
        return y
    
    def get_body_angle(self):
        return self.body_body.angle
    
    def get_body_y_vel(self):
        x, y = self.body_body.velocity
        return y
    
    def get_body_x_vel(self):
        x, y = self.body_body.velocity
        return x
    
    def get_body_angular_vel(self):
        return self.body_body.angular_velocity
    
    
    def get_leg_angle_relative_to_body(self):
        return self.body_leg.angle
    
    def get_leg_angle_angular_vel_relative_to_body(self):
        return self.body_leg.angular_velocity
    

    def get_x_position(self):
        x, y = self.body_body.position
        return x
    
    def is_upsidedown(self):
        if abs(self.body_body.angle) > 1:
            return True
        #if abs(self.body_body.angle) % 3.14 < 0.1 and abs(self.body_body.angle) % 3.14*2 > 1 and abs(self.body_body.angle) > 1:
            #return True
        return False

    def randomize(self):
        x, y = self.body_body.position
        x += random.uniform(-1, 1)
        y += random.uniform(0, 10)
        self.body_body.position = x, y
        self.body_body.angle += random.uniform(-1, 1)
        x, y = self.body_body.velocity
        x += random.uniform(-1, 1)
        y += random.uniform(-1, 1)
        self.body_body.velocity = x, y
        self.body_body.angular_velocity += random.uniform(-1, 1)
        self.body_body.angle += random.uniform(-1, 1)
        self.body_leg.angular_velocity += random.uniform(-1, 1)
