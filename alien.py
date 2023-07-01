# pylint: disable=too-few-public-methods

"""Class to make Alien Object in game"""
import pygame

class Alien(pygame.sprite.Sprite):
    """Alien object class for game"""
    def __init__(self, color, x_pos, y_pos):
        super().__init__()
        file_path = "./graphics/" + color + ".png"
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x_pos, y_pos))

        if color == "red":
            self.value = 100
        elif color == "green":
            self.value = 200
        else:
            self.value = 300

    def update(self, direction):
        """Updates the direction that the alien moves"""
        self.rect.x_pos += direction
