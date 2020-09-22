"""Imports"""
import random
import pygame
import pymunk.pygame_util
import time
from PIL import Image
from .custom_env import CustomEnv
from pathlib import Path

class NoDisplayEnv(CustomEnv):
    """Class for No Display environment"""

    def __init__(self) -> None: # ovveride
        """Define variables"""
        super().__init__()

    def set_state(self, action) -> None: # override & Super
        """Sets state"""
        return super().set_state(action)

    def get_done(self) -> bool: # override
        """Gets done"""
        return super().get_done()

    def get_reward_notdone(self) -> float: # override
        """Gets done"""
        return super().get_reward_notdone()

    def get_reward_done(self) -> float: # override
        """Gets done"""
        return super().get_reward_done()

    def setup(self, num_actions, observations): # override
        return super().setup(num_actions, observations)

    def reset(self):
        """reset"""
        self.setup(None, None)
        return super().reset()