"""Class to make Laser Object in game"""
import pygame

class Laser(pygame.sprite.Sprite):
    """Laser object class for game"""
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.image.fill("white")
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.height_y_constraint = screen_height

    def destroy(self):
        """Destroy the laser function"""
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        """Update the laser on the screen make it move"""
        self.rect.y += self.speed
        self.destroy()
