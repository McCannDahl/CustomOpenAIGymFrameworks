"""Imports"""
import math
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np

class CustomEnv(gym.Env):
    """Class for any environment"""

    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second' : 50
    }

    def __init__(self) -> None: # ovveride
        """Define variables"""
        self.viewer = None
        self.state = None
        self.steps_beyond_done = None
        self.np_random = None
        self.num_obervations = None

    def setup_viewer(self) -> None: # ovveride
        """Setsup the viewer"""

    def update_viewer(self) -> None: # ovveride
        """Updates the viewer"""

    def close_viewer(self) -> None: # ovveride
        """close the viewer"""

    def set_state(self, action) -> None: # override & Super
        """Sets state"""
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))

    def get_done(self) -> bool: # override
        """Gets done"""
        return True

    def get_reward_notdone(self) -> float: # override
        """Gets done"""
        return 1

    def get_reward_done(self) -> float: # override
        """Gets done"""
        return 0


    def get_reward(self, done):
        """Gets the reward"""
        reward = 0.0
        if not done:
            reward = self.get_reward_notdone()
        elif self.steps_beyond_done is None:
            self.steps_beyond_done = 0
            reward = self.get_reward_done()
        else:
            if self.steps_beyond_done == 0:
                logger.warn("You are calling 'step()' even though this environment has \
                    already returned done = True. You should always call 'reset()' once \
                    you receive 'done = True' -- any further steps are undefined behavior.")
            self.steps_beyond_done += 1
        return reward

    def setup(self, num_actions, observations): # override
        self.num_obervations: int = len(observations)
        obs_np = np.array(observations, dtype=np.float32)
        self.observation_space: spaces.Box = spaces.Box(-obs_np, obs_np, dtype=np.float32)
        self.action_space: spaces.Discrete = spaces.Discrete(num_actions)

        self.seed()


    def seed(self, seed=None):
        """seed"""
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        """step"""
        self.set_state(action)
        done = self.get_done()
        reward = self.get_reward(done)
        return np.array(self.state), reward, done, {}

    def reset_state(self): 
        """only override if your state vars do not start at 0, or you want more randomness"""
        self.state = self.np_random.uniform(low=0, high=0, size=(self.num_obervations,))

    def reset(self):
        """reset"""
        self.reset_state()
        self.steps_beyond_done = None
        return np.array(self.state)

    def render(self, mode='human'):
        """render"""
        if self.viewer is None:
            self.setup_viewer()
        if self.state is None:
            return None
        self.update_viewer()
        return

    def close(self):
        """close"""
        if self.viewer:
            self.close_viewer()
            self.viewer = None
