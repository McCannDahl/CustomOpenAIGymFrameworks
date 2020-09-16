"""Imports"""
from enum import Enum
from custom_openai_frameworks.envs.examples.pymunk_envs.pymunk_shapes.floor import Floor
from custom_openai_frameworks.envs.examples.pymunk_envs.pymunk_shapes.crawler import Crawler
from custom_openai_frameworks.envs.examples.pymunk_envs.pymunk_shapes.pole import Pole
from custom_openai_frameworks.envs.pymunk_env import PymunkEnv
import pymunk
import random
import pygame
import numpy as np

class SimpleCrawler(PymunkEnv):
    """Class for Custom Pymunk environment"""

    def center_crawler_on_view(self) -> None:
        """
            move crawler to center
            move pole same amount
                if pole is off screen, move it on screen
        """
        px, py = self.crawler.body_body.position
        diff = px - 400
        self.crawler.body_body.position = (400, py)
        #if px > self.last_x_position:
        #    self.last_x_position = px
        polex, poley = self.pole.body_pole.position
        self.pole.body_pole.position = (polex-diff, poley)
        if polex < -400:
            self.pole.body_pole.position = (400, poley)
        if polex > 400:
            self.pole.body_pole.position = (-400, poley)
        
    
    def get_reward_notdone(self) -> float:
        """Reward the crawler for the amount of horizontal progresss it's made"""
        return_val = 0
        diff = self.crawler.get_x_position() - self.last_x_position
        if diff > 0:
            return_val = self.crawler.get_x_position() - self.last_x_position
        #if self.crawler.get_x_position() > 400.001:
            #print("x pos = "+str(self.crawler.get_x_position()))
            #print("return_val = "+str(return_val))
        self.center_crawler_on_view()
        self.totalReward += return_val
        if self.crawler.is_upsidedown():
            return_val = -100
        
        if abs(diff) < 0.01:
            return_val = -1
        #x, y = self.crawler.body_body.position
        #if y > 200:
        #    return_val = -10
        #if return_val > 0:
        #if self.totalReward > 10:
            #print("Total reward = "+str(self.totalReward))
        return return_val

    def set_state(self, action) -> None:
        """Sets state"""
        if self.manual:
            print(self.crawler.body_body.angle)
            if abs(self.crawler.body_body.angle) % 3.14 < 0.1:
                print("is upsidedown")
            if self.leg_up and self.crawler.joint_drs.rest_angle < self.crawler.min_angle*-1:
                self.crawler.joint_drs.rest_angle += self.change_amount
            if self.leg_down  and self.crawler.joint_drs.rest_angle > self.crawler.max_angle*-1:
                self.crawler.joint_drs.rest_angle -= self.change_amount
        else:
            if action == Actions.leg_up and self.crawler.joint_drs.rest_angle < self.crawler.min_angle*-1:
            #if action == Actions.leg_up:
                self.crawler.joint_drs.rest_angle += self.change_amount
            elif action == Actions.leg_down  and self.crawler.joint_drs.rest_angle > self.crawler.max_angle*-1:
            #elif action == Actions.leg_down:
                self.crawler.joint_drs.rest_angle -= self.change_amount
                
        #print('>'+str(self.crawler.joint_drs.rest_angle))
        
        self.state = (
            self.crawler.get_body_distance_from_ground(),
            self.crawler.get_body_angle(),
            self.crawler.get_body_y_vel(),
            self.crawler.get_body_x_vel(),
            self.crawler.get_body_angular_vel(),
            self.crawler.get_leg_angle_relative_to_body(),
            self.crawler.get_leg_angle_angular_vel_relative_to_body()
        )
        #print(self.state)
                
        super().set_state(action)


    def __init__(self) -> None:
        """Define variables"""
        super().__init__()
        self.crawler: Crawler = None
        self.floor: Floor = None
        self.setup(None, None)
        
        self.last_x_position = 400
        
        # manual overrides
        self.change_amount = 0.2
        self.leg_up = False
        self.leg_down = False
        
        self.env_name = "SimpleCrawler-v1"
        
        #debug
        self.totalReward = 0

    def add_shapes(self) -> None:
        """Add Shapes"""
        self.crawler = Crawler()
        self.floor = Floor(self.b0)
        self.pole = Pole(self.b0)
        self.space.add(self.crawler.get_all())
        self.space.add(self.floor.get_all())
        self.space.add(self.pole.get_all())
        # TODO randomly assign state values to crawler
        # This is to make up for the reset_state method. Because our state is only observatory
        self.crawler.randomize()
        
        self.totalReward = 0

    def setup(self, num_actions, observations):
        """setup"""
        observations: list(float) = [
            Observations.body_distance_from_ground,
            Observations.body_angle,
            Observations.body_y_vel,
            Observations.body_x_vel, 
            Observations.body_angular_vel,
            Observations.leg_angle_relative_to_body,    
            Observations.leg_angle_angular_vel_relative_to_body
        ]
        num_actions = 2
        super().setup(num_actions, observations)
    
    def handle_event(self, event):
        """close the viewer"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.leg_up = True
            elif event.key == pygame.K_w:
                self.leg_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                self.leg_up = False
            elif event.key == pygame.K_w:
                self.leg_down = False
    
class Actions():
    """Actions enum"""
    leg_down = 0
    leg_up = 1
    
class Observations():
    """Obsdervations enum"""
    body_distance_from_ground = np.finfo(np.float32).max
    body_angle = 3.14
    body_y_vel = np.finfo(np.float32).max
    body_x_vel = np.finfo(np.float32).max
    body_angular_vel = np.finfo(np.float32).max
    leg_angle_relative_to_body = 3.14
    leg_angle_angular_vel_relative_to_body = np.finfo(np.float32).max
    
