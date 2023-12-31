"""Class to make Player Object in game"""

import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
    """Player object class"""

    def __init__(self, pos, constraint, speed):
        super().__init__()
        self.image = pygame.image.load("./graphics/player.png").convert_alpha()
        self.blaster_sound = pygame.mixer.Sound("./music/blaster.mp3")
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 500

        self.lasers = pygame.sprite.Group()

    def get_input(self):
        """Get input function for player to see if left or right key pressed"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def recharge(self):
        """Function to make sure that laser cannot be clicked very fast"""
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def constraint(self):
        """Restricts the player from leaving screen"""
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot_laser(self):
        """Function to handle the shooting of player laser"""
        self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))
        self.blaster_sound.play()

    def update(self):
        """General update function for player object"""
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()
