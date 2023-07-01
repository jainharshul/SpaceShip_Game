"""Class to make obstacles in game"""

import pygame


class Block(pygame.sprite.Sprite):
    """Block object class"""
    def __init__(self, size, color, x, y):
        """Block object constructor"""
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

	
shape = [
    "xxxxxxxxxxx",
    "xxxxxxxxxxx",
    "xxxxxxxxxxx",
    "xxxxxxxxxxx",
    "xxxxxxxxxxx",
]
