# pylint: disable=R0902

"""Main file to run game"""
import sys
import os
import pickle
from random import choice
import pygame
from player import Player
import obstacle
import button
from alien import Alien
from laser import Laser

class Game:
    """Game class makes everything Game needs to run"""
    def __init__(self):
        pygame.mixer.init()
        self.alien_speed = 1
        self.og_sound = pygame.mixer.Sound("./music/sound.mp3")
        self.life_lost_sound = pygame.mixer.Sound("./music/lifelost.mp3")
        self.blaster_sound = pygame.mixer.Sound("./music/blaster.mp3")
        self.alien_kill_sound = pygame.mixer.Sound("./music/kill.mp3")
        self.win_sound = pygame.mixer.Sound("./music/win.mp3")
        self.og_sound.play(-1)

        player_sprite = Player((    SCREEN_WIDTH // 2,  SCREEN_HEIGHT),  SCREEN_WIDTH, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        self.lives = 3
        self.live_surf = pygame.image.load("./graphics/player.png").convert_alpha()
        self.live_x_start_pos =     SCREEN_WIDTH - (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.high_score = self.load_high_score()
        self.font = pygame.font.Font("./font/custom_font.ttf", 20)

        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows=6, cols=8)
        self.alien_direction = 1

        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [
            num * ( SCREEN_WIDTH / self.obstacle_amount)
            for num in range(self.obstacle_amount)
        ]
        self.create_multiple_obstacles(
            *self.obstacle_x_positions, x_start=    SCREEN_WIDTH / 15, y_start=480
        )

        self.game_over = False
        self.play_again = False

        self.restart_text = self.font.render("Press R to play again", False, "white")
        self.restart_rect = self.restart_text.get_rect(
            center=(    SCREEN_WIDTH // 2,  SCREEN_HEIGHT // 2)
        )

    def create_obstacle(self, x_start, y_start, offset_x):
        """Creates obstacles in game screen"""
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == "x":
                    x_poss = x_start + col_index * self.block_size + offset_x
                    y_poss = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size, (241, 79, 80), x_poss, y_poss)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        """Creates and sets 4 obstacles ons screen"""
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def alien_setup(
        self, rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=100
    ):
        """Setup of alien grid and more"""
        for row_index in range(rows):
            for col_index in range(cols):
                x_pos = col_index * x_distance + x_offset
                y_pos = row_index * y_distance + y_offset

                if row_index == 0:
                    alien_sprite = Alien("yellow", x_pos, y_pos)
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien("green", x_pos, y_pos)
                else:
                    alien_sprite = Alien("red", x_pos, y_pos)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        """Function to move aliens in grid down each time they reach end of screen"""
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >=  SCREEN_WIDTH:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        """Increases the speed of the movement of aliens when they move down"""
        for alien in self.aliens.sprites():
            alien.rect.y += distance * self.alien_speed

    def alien_shoot(self):
        """Function to handle aliens shooting"""
        if self.aliens.sprites() and not self.game_over:
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6,   SCREEN_HEIGHT)
            self.alien_lasers.add(laser_sprite)

    def collision_checks(self):
        """Checks the laser collision betweeen and from aliens and player"""
        if self.player.sprite.lasers and not self.game_over:
            for laser in self.player.sprite.lasers:
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                        self.alien_kill_sound.play()
                        laser.kill()
                if pygame.sprite.spritecollide(laser, self.blocks, False):
                    laser.kill()

        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser, self.blocks, False):
                    laser.kill()
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.life_lost_sound.play()
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True

        if self.aliens and not self.game_over:
            if pygame.sprite.spritecollideany(self.player.sprite, self.aliens):
                self.game_over = True

    def display_lives(self):
        """Display the player.png as lives"""
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf, (x, 8))

    def display_score(self):
        """Display the "Score" text on the top left of the screen"""
        score_surf = self.font.render(f"Score: {self.score}", False, "white")
        score_rect = score_surf.get_rect(topleft=(10, 10))
        screen.blit(score_surf, score_rect)

    def display_high_score(self):
        """This displalays the highscore on screen"""
        high_score_surf = self.font.render(
            f"High Score: {self.high_score}", False, "white"
        )
        high_score_rect = high_score_surf.get_rect(
            center=(    SCREEN_WIDTH // 2,  SCREEN_HEIGHT // 2 + 40)
        )
        screen.blit(high_score_surf, high_score_rect)

    def wait_for_player_decision(self):
        """Function to wait and react to player decision C, Q"""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self.alien_speed += 0.5
                        self.reset_level()
                        waiting = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

    def victory_message(self):
        """Display victory message play victory sound and ask for input"""
        if not self.aliens.sprites() and not self.game_over:
            victory_surf = self.font.render("You won", False, "white")
            self.win_sound.play()
            victory_rect = victory_surf.get_rect(
                center=(    SCREEN_WIDTH / 2,   SCREEN_HEIGHT / 2)
            )
            screen.blit(victory_surf, victory_rect)

            continue_surf = self.font.render(
                "Press C to continue or Q to quit", False, "white"
            )
            continue_rect = continue_surf.get_rect(
                center=(    SCREEN_WIDTH / 2,   SCREEN_HEIGHT / 2 + 40)
            )
            screen.blit(continue_surf, continue_rect)
            pygame.display.flip()

            self.wait_for_player_decision()

    def restart_game(self):
        """Restart game function"""
        self.aliens.empty()
        self.alien_lasers.empty()
        self.blocks.empty()
        self.lives = 3
        self.score = 0
        self.alien_speed = 1
        self.reset_level()
        self.game_over = False

    def reset_level(self):
        """Resets the aliens if the player chooses to keep playing"""
        self.aliens.empty()
        self.alien_setup(rows=6, cols=8)

        self.blocks.empty()
        self.create_multiple_obstacles(
            *self.obstacle_x_positions, x_start=    SCREEN_WIDTH / 15, y_start=480
        )

    def load_high_score(self):
        """Loads the highscore intto high_score.pkl file"""
        if os.path.exists("high_score.pkl"):
            with open("high_score.pkl", "rb") as file:
                return pickle.load(file)
        else:
            return 0

    def save_high_score(self):
        """Saves the highschore to pkl file"""
        with open("high_score.pkl", "wb") as file:
            pickle.dump(self.high_score, file)

    def handle_input(self):
        """Handles the input from the user if they decide to restart or quit game"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                self.restart_game()
            if event.key == pygame.K_q and self.game_over:
                pygame.quit()
                sys.exit()

    def run(self):
        """Main run function"""
        self.player.update()
        self.alien_lasers.update()

        if not self.game_over:
            self.aliens.update(self.alien_direction)

        self.alien_position_checker()
        self.collision_checks()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        if not self.game_over:
            self.aliens.draw(screen)

        self.alien_lasers.draw(screen)
        self.display_lives()
        self.display_score()
        self.victory_message()

        if self.game_over:
            quit_text = self.font.render("Press Q to quit", False, "white")
            quit_rect = quit_text.get_rect(
                center=(    SCREEN_WIDTH // 2,  SCREEN_HEIGHT // 2 + 80)
            )
            screen.blit(quit_text, quit_rect)
            screen.blit(self.restart_text, self.restart_rect)
            self.display_high_score()
            pygame.mixer.music.stop()
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()


def main_game():
    """Main game function with game loop"""
    game = Game()

    alien_laser = pygame.USEREVENT + 1
    pygame.time.set_timer(alien_laser, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == alien_laser:
                game.alien_shoot()
            game.handle_input(event)

        screen.fill((30, 30, 30))
        game.run()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    pygame.init()

    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((  SCREEN_WIDTH,   SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    start_button = button.Button(
        "Start Game",
            SCREEN_WIDTH / 2 - 90,
        SCREEN_HEIGHT / 2 - 25,
        200,
        50,
        (0, 200, 0),
        (0, 255, 0),
        action=lambda: setattr(__builtins__, "start_game", True),
        instruction_text="<-  -> to move and and space bar to shoot!",
        score_text="Red = 100 | Green = 200 | Yellow = 300",
    )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if start_button.is_clicked(event):
                main_game()

        screen.fill((30, 30, 30))
        start_button.draw(screen, event)
        pygame.display.flip()
        clock.tick(60)
