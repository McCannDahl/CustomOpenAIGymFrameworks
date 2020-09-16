"""Imports"""
from enum import Enum
from custom_openai_frameworks.envs.examples.pymunk_envs.pymunk_shapes.box import Box
from custom_openai_frameworks.envs.examples.pymunk_envs.pymunk_shapes.ragdoll import Ragdoll
from custom_openai_frameworks.envs.pymunk_env import PymunkEnv
import pymunk
import random
import pygame

class StandInRainEnv(PymunkEnv):
    """Class for Custom Pymunk environment"""

    def get_done(self) -> bool:
        """Gets done"""
        returnVal = self.ragdoll.is_fallen()
        #if returnVal:
        #    print("Ragdoll has fallen RIP")
        return returnVal

    def get_reward_notdone(self) -> float:
        """Gets done"""
        return 4 - abs(self.ragdoll.body1.angle)

    def get_reward_done(self) -> float:
        """Gets done"""
        return 0

    def set_state(self, action) -> None:
        """Sets state"""
        if self.manual:
            if self.leftLegLeft and self.ragdoll.joint52.rest_angle < 3.14/8:
                self.ragdoll.joint52.rest_angle += self.change_amount
            elif self.leftLegRight and self.ragdoll.joint52.rest_angle > -3.14/8:
                self.ragdoll.joint52.rest_angle -= self.change_amount
            elif self.rightLegLeft and self.ragdoll.joint62.rest_angle < 3.14/8:
                self.ragdoll.joint62.rest_angle += self.change_amount
            elif self.rightLegRight and self.ragdoll.joint62.rest_angle > -3.14/8:
                self.ragdoll.joint62.rest_angle -= self.change_amount
        else:
            if Actions.LeftLegLeft.value and self.ragdoll.joint52.rest_angle < 3.14/8:
                self.ragdoll.joint52.rest_angle += self.change_amount
            elif Actions.LeftLegRight.value and self.ragdoll.joint52.rest_angle > -3.14/8:
                self.ragdoll.joint52.rest_angle -= self.change_amount
            elif Actions.RightLegLeft.value and self.ragdoll.joint62.rest_angle < 3.14/8:
                self.ragdoll.joint62.rest_angle += self.change_amount
            elif Actions.RightLegRight.value and self.ragdoll.joint62.rest_angle > -3.14/8:
                self.ragdoll.joint62.rest_angle -= self.change_amount
                
        
        self.state = (
            self.ragdoll.body1.angle,
            self.ragdoll.joint52.rest_angle,
            self.ragdoll.joint62.rest_angle
        )
        
        self.count += 1
        if self.count > 10:
            self.count = 0
            self.add_rain()
                
        super().set_state(action)

    def __init__(self) -> None:
        """Define variables"""
        super().__init__()
        self.ragdoll: Ragdoll = None
        self.box: Box = None
        self.setup(None, None)
        self.change_amount = 0.04
        self.count = 0
        
        # manual overrides
        self.leftLegLeft = False
        self.leftLegRight = False
        self.rightLegLeft = False
        self.rightLegRight = False
        
        self.env_name = "StandInRain-v0"

    def add_shapes(self) -> None:
        """Add Shapes"""
        self.ragdoll = Ragdoll()
        self.box = Box(self.b0)
        self.space.add(self.ragdoll.get_all())
        self.space.add(self.box.get_all())

    def setup(self, num_actions, observations):
        """setup"""
        observations: list(float) = [
            3.14,
            3.14,
            3.14
        ] # angle of body, angle of left leg, angle of right leg
        num_actions = len(Actions) # Should be same as
        super().setup(num_actions, observations)
    
    def handle_event(self, event):
        """close the viewer"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.leftLegLeft = True
            elif event.key == pygame.K_w:
                self.leftLegRight = True
            elif event.key == pygame.K_o:
                self.rightLegLeft = True
            elif event.key == pygame.K_p:
                self.rightLegRight = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                self.leftLegLeft = False
            elif event.key == pygame.K_w:
                self.leftLegRight = False
            elif event.key == pygame.K_o:
                self.rightLegLeft = False
            elif event.key == pygame.K_p:
                self.rightLegRight = False
        
    def add_rain(self):
        """Add a ball to the given space at a random position"""
        mass = 1
        radius = 14
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
        body = pymunk.Body(mass, inertia)
        x = random.randint(-100,100)
        body.position = x+400, 800
        shape = pymunk.Circle(body, radius, (0,0))
        shape.filter = pymunk.ShapeFilter(group=1)
        self.space.add(body, shape)
    
class Actions(Enum):
    """Actions enum"""
    LeftLegLeft = 0
    LeftLegRight = 1
    RightLegLeft = 2
    RightLegRight = 3
