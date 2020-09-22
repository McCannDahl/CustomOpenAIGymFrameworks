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

class GolfCardGameEnv(NoDisplayEnv):
    """Class for Golf Card Game environment"""

    def __init__(self) -> None: # ovveride
        """Define variables"""
        #print('__init__')
        super().__init__()
        self.reward = 0
        self.setup(None,None)

    def setup_game(self):
        self.setup_deck()
        self.setup_hand()
        self.drawn_card =  self.draw_card()

    def setup_deck(self):
        self.deck = []
        for i in range(11):
            for j in range(4):
                self.deck.append(i) # A,2-10,K
        for i in range(2):
            for j in range(4):
                self.deck.append(10) # J,Q
        for i in range(2):
            self.deck.append(-2) # W
    
    def setup_hand(self):
        self.hand =  []
        for i in range(2):
            self.hand.append(self.draw_card())
        for i in range(4):
            self.hand.append(11)
        #print('New hand =  ',self.hand)

    def draw_card(self):
        if len(self.deck) > 0:
            return self.deck.pop(random.randrange(len(self.deck))) 
        return 10

    def setup(self, num_actions, observations): # override
        #print('setup')
        self.setup_game()
        self.low_inputs: list(float) = [
            -2,
            -2,
            -2,
            -2,
            -2,
            -2,
            -2, # drawn card
        ]
        self.high_inputs: list(float) = [
            11, # 11 = not known
            11,
            11,
            11,
            11,
            11,
            11, # drawn card
        ]
        self.outputs: list(int) = [
            'LT',
            'LB',
            'MT',
            'MB',
            'RT',
            'RB',
            'D',
        ]
        self.num_obervations: int = len(self.low_inputs)
        low_inputs_np = np.array(self.low_inputs, dtype=np.float32)
        high_inputs_np = np.array(self.high_inputs, dtype=np.float32)
        self.observation_space: spaces.Box = spaces.Box(low_inputs_np, high_inputs_np, dtype=np.float32)
        self.action_space: spaces.Discrete = spaces.Discrete(len(self.outputs))
        self.seed()

    def get_score_improvement(self,hand1,hand2):
        return self.calculate_score(hand1) - self.calculate_score(hand2)
    
    def calculate_score(self,hand):
        score  =  0
        for i in range(3):
            if hand[i*2] == -2 and hand[i*2+1] == -2:
                score += hand[i*2] + hand[i*2+1]
            elif hand[i*2] == 11 and hand[i*2+1] == 11:
                score += hand[i*2] + hand[i*2+1]
            elif hand[i*2] == hand[i*2+1]:
                score += 0
            else:
                score += hand[i*2] + hand[i*2+1]
        return score

    def set_state(self, action) -> None: # override & Super
        """Sets state"""
        #print('set_state')
        old_hand = []
        for h in self.hand:
            old_hand.append(h)

        if action < 6:
            #print('You just replaced ',self.hand[action],' with ',self.drawn_card)
            self.hand[action] = self.drawn_card
        if action == 6:
            pass # discard card

        self.reward = self.get_score_improvement(old_hand,self.hand)

        #print('Your reward is',self.reward)
        #print('Your hand is',self.hand)
        #print('Deck has left ',len(self.deck))
        
        self.drawn_card = self.draw_card()
        
        self.state = (
            self.hand[0],
            self.hand[1],
            self.hand[2],
            self.hand[3],
            self.hand[4],
            self.hand[5],
            self.drawn_card,
        )
                
        super().set_state(action)

    def get_done(self) -> bool: # override
        """Gets done"""
        #print('get_done')
        is_done = True
        for h in self.hand:
            if h == 11:
                is_done = False
        if len(self.deck) < 1:
            is_done = True
        #print('returning',is_done)
        #if is_done:
            #print('score = ',self.calculate_score(self.hand))
            #print('hand = ',(self.hand))
        return is_done


    def get_reward_notdone(self) -> float: # override
        """Gets done"""
        #print('get_reward_notdone')
        return self.reward

    def get_reward_done(self) -> float: # override
        """Gets done"""
        #print('get_reward_done')
        return 11*6 - self.calculate_score(self.hand)
        

    
