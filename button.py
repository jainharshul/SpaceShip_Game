# pylint: disable=R0902
# pylint: disable=R0913

"""Class to make Start Button on initial game screen"""
import pygame

class Button:
    """Class for start button at beginning of game"""
    def __init__(
        self,
        text,
        x_pos,
        y_pos,
        width,
        height,
        inactive_color,
        active_color,
        action=None,
        instruction_text=None,
        score_text=None,
    ):
        self.text = text
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.action = action
        self.instruction_text = instruction_text
        self.score_text = score_text
        self.font = pygame.font.Font("./font/custom_font.ttf", 15)

    def is_clicked(self, event):
        """Fucntiont to handle event if button is clicked"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, screen, event):
        """Function to draw instruction and score text on screen along with button"""
        mouse = pygame.mouse.get_pos()

        if (
            self.x_pos + self.width > mouse[0] > self.x_pos
            and self.y_pos + self.height > mouse[1] > self.y_pos
        ):
            pygame.draw.rect(
                screen, self.active_color, (self.x_pos, self.y_pos, self.width, self.height)
            )
            if self.action is not None and self.is_clicked(event):
                self.action()
        else:
            pygame.draw.rect(
                screen, self.inactive_color, (self.x_pos, self.y_pos, self.width, self.height)
            )

        small_text = pygame.font.Font("./font/custom_font.ttf", 15)
        text_surf, text_rect = self.text_objects(self.text, small_text)
        text_rect.center = ((self.x_pos + (self.width / 2)), (self.y_pos + (self.height / 2)))
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
        """Funtion to return rect and surf or given text"""
        text_surface = font.render(text, True, (255, 255, 255))
        return text_surface, text_surface.get_rect()
