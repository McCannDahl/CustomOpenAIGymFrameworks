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
from gym import spaces, logger

class CountUpEnv(NoDisplayEnv):
    """Class for Count Up Game environment"""

    def __init__(self) -> None: # ovveride
        """Define variables"""
        #print('__init__')
        super().__init__()
        self.reward = 0
        self.wrong_times = 0
        self.mynumbers = [100,100,100,100]
        self.reset_state()
        self.setup(None,None)

    def setup(self, num_actions, observations): # override
        #print('setup')
        self.outputs: list(int) = [
            0, # subtract
            1, # add
        ]
        self.inputs: list(float) = [100,100,100,100]
        self.num_obervations: int = len(self.inputs)
        inputs_np = np.array(self.inputs, dtype=np.float32)
        self.observation_space: spaces.Box = spaces.Box(-inputs_np, inputs_np, dtype=np.float32)
        self.action_space: spaces.Discrete = spaces.Discrete(len(self.outputs))
        self.seed()

    def set_state(self, action) -> None: # override & Super
        """Sets state"""
        #print('--------------------set_state',action)
        #print('self.mynumbers',self.mynumbers)


        if action == 0:
            self.reward = sum(self.mynumbers)
        elif action == 1:
            self.reward = 0
            for n in self.mynumbers:
                self.reward -= n
        if self.reward > 0:
            self.reward = 1
        if self.reward < 0:
            self.reward = 0
                
        self.wrong_times += 1
        #print('self.reward',self.reward)
        #print('self.wrong_times',self.wrong_times)
        #print('random.randrange((200))-100 ',random.randrange((200))-100)
        #if  self.reward > 0:
            #print('state self.reward',self.reward)
        
        self.state = (
            self.mynumbers[0],
            self.mynumbers[1],
            self.mynumbers[2],
            self.mynumbers[3],
        )
                
        super().set_state(action)

    def reset_state(self): 
        """only override if your state vars do not start at 0, or you want more randomness"""
        self.mynumbers[0] = random.randrange((200))-100
        self.mynumbers[1] = random.randrange((200))-100
        self.mynumbers[2] = random.randrange((200))-100
        self.mynumbers[3] = random.randrange((200))-100
        self.state = (
            self.mynumbers[0],
            self.mynumbers[1],
            self.mynumbers[2],
            self.mynumbers[3],
        )
        self.reward = None

    def get_done(self) -> bool: # override
        """Gets done"""
        return self.reward != None or self.wrong_times > 0

    def get_reward_notdone(self) -> float: # override
        """Gets done"""
        #print('get_reward_notdone',self.reward)
        #if  self.reward > 0:
            #print('self.reward',self.reward)
        return self.reward

    def get_reward_done(self) -> float: # override
        """Gets done"""
        #print('get_reward_done')
        return 0
        

    
