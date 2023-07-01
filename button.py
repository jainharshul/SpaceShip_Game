"""Class to make Start Button on initial game screen"""

import pygame


class Button:
    def __init__(
        self,
        text,
        x,
        y,
        width,
        height,
        inactive_color,
        active_color,
        action=None,
        instruction_text=None,
        score_text=None,
    ):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.action = action
        self.instruction_text = instruction_text
        self.score_text = score_text
        self.font = pygame.font.Font("./font/custom_font.ttf", 15)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, screen, event):
        mouse = pygame.mouse.get_pos()

        if (
            self.x + self.width > mouse[0] > self.x
            and self.y + self.height > mouse[1] > self.y
        ):
            pygame.draw.rect(
                screen, self.active_color, (self.x, self.y, self.width, self.height)
            )
            if self.action is not None and self.is_clicked(event):
                self.action()
        else:
            pygame.draw.rect(
                screen, self.inactive_color, (self.x, self.y, self.width, self.height)
            )

        small_text = pygame.font.Font("./font/custom_font.ttf", 15)
        text_surf, text_rect = self.text_objects(self.text, small_text)
        text_rect.center = ((self.x + (self.width / 2)), (self.y + (self.height / 2)))
        screen.blit(text_surf, text_rect)

        if self.instruction_text:
            instruction_surf = self.font.render(
                self.instruction_text, 1, (255, 255, 255)
            )
            instruction_rect = instruction_surf.get_rect(
                center=(600 // 2, 600 // 2 + 80)
            )  # Updated
            screen.blit(instruction_surf, instruction_rect)

        if self.score_text:
            score_surf = self.font.render(self.score_text, 1, (255, 255, 255))
            score_rect = score_surf.get_rect(
                center=(600 // 2, instruction_rect.bottom + 50)
            )  # Updated
            screen.blit(score_surf, score_rect)

    def text_objects(self, text, font):
        text_surface = font.render(text, True, (255, 255, 255))
        return text_surface, text_surface.get_rect()
