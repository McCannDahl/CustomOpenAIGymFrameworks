"""Imports"""
from enum import Enum
from custom_openai_frameworks.envs.examples.pymunk_envs.pymunk_shapes.floor import Floor
from custom_openai_frameworks.envs.examples.pymunk_envs.pymunk_shapes.crawler import Crawler
from custom_openai_frameworks.envs.examples.pymunk_envs.pymunk_shapes.pole import Pole
from custom_openai_frameworks.envs.no_display_env import NoDisplayEnv
import pymunk
import random
import pygame
import numpy as np

class GolfCardGameEnv(NoDisplayEnv):
    """Class for Golf Card Game environment"""

    def __init__(self) -> None: # ovveride
        """Define variables"""
        NoDisplayEnv.__init__(self)

    def set_state(self, action) -> None: # override & Super
        """Sets state"""
        NoDisplayEnv.set_state(self, action)

    def get_done(self) -> bool: # override
        """Gets done"""
        NoDisplayEnv.get_done(self)

    def get_reward_notdone(self) -> float: # override
        """Gets done"""
        NoDisplayEnv.get_reward_notdone(self)

    def get_reward_done(self) -> float: # override
        """Gets done"""
        NoDisplayEnv.get_reward_done(self)
    
