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
        CustomEnv.__init__(self)

    def set_state(self, action) -> None: # override & Super
        """Sets state"""
        CustomEnv.set_state(self, action)

    def get_done(self) -> bool: # override
        """Gets done"""
        CustomEnv.get_done(self)

    def get_reward_notdone(self) -> float: # override
        """Gets done"""
        CustomEnv.get_reward_notdone(self)

    def get_reward_done(self) -> float: # override
        """Gets done"""
        CustomEnv.get_reward_done(self)