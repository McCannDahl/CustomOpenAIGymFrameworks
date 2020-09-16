"""Imports"""
import random
import pygame
import pymunk
import pymunk.pygame_util
import time
from PIL import Image
from .custom_env import CustomEnv
from pathlib import Path

class PymunkEnv(CustomEnv):
    """Class for Pymunk environment"""

    def get_done(self) -> bool: # override
        """Gets done"""
        return False

    def __init__(self) -> None: # ovveride & super
        """Define variables"""
        super().__init__()
        self.fps = 30
        self.steps = 10
        self.size = 800, 800

        self.viewer = None # only define if rendering
        self.draw_options = None # only define if rendering
        self.images = None # only define if rendering
        self.clock = None # only define if rendering

        self.space = None
        self.b0 = None
        self.manual = False
        self.finished = False
        
        self.env_name = "pymunk_env"

    def set_state(self, action) -> None: # ovveride & super(at end)
        """Sets state"""
        super().set_state(action)
        for _ in range(self.steps):
            self.space.step(1/self.fps/self.steps)

    def add_shapes(self) -> None:
        """Add Shapes"""

    def setup_viewer(self) -> None:
        """Setsup the viewer"""
        pygame.init()
        self.viewer = pygame.display.set_mode(self.size)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.viewer)
        self.images = []
        self.clock = pygame.time.Clock()

    def update_viewer(self) -> None:
        """Updates the viewer"""
        self.viewer.fill((255, 255, 255))
        self.space.debug_draw(self.draw_options)
        pygame.display.update()
        self.clock.tick(self.fps)
        if not self.manual:
            self.make_gif()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close_viewer()
                self.finished = True
            if self.manual:
                self.handle_event(event)
                
    def handle_event(self, event):
        """close the viewer"""
        

    def close_viewer(self) -> None:
        """close the viewer"""
        if not self.manual:
            self.save_gif()
        pygame.quit()

    def make_gif(self):
        """Make gif"""
        str_format = 'RGBA'
        raw_str = pygame.image.tostring(self.viewer, str_format, False)
        image = Image.frombytes(str_format, self.viewer.get_size(), raw_str)
        self.images.append(image)

    def save_gif(self):
        """Save gif"""
        Path("output/"+self.env_name+"/gifs").mkdir(parents=True, exist_ok=True)
        self.images[0].save('output/'+self.env_name+'/gifs/'+str(time.time())+'.gif',
                            save_all=True, append_images=self.images[1:],
                            optimize=True, duration=1000//self.fps, loop=0)
        self.images = []

    def setup(self, num_actions, observations):
        super().setup(num_actions, observations)
        self.space = pymunk.Space()
        self.space.gravity = 0, -800
        self.b0 = self.space.static_body
        self.add_shapes()

    def reset(self):
        """reset"""
        self.setup(None, None)
        return super().reset()
    
    def set_manual(self):
        """set_manual"""
        self.manual = True
    
    def is_finished(self):
        """"is finished"""
        return self.finished