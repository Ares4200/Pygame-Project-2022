# Pygame Project

import random
import time

import pygame

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 1920
HEIGHT = 1080
TITLE = "<Pygame Project 2022>"


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./Assets/Background.jpg")
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))

        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("./Assets/Anya_Forger_Anime_2.png")
        self.image = pygame.transform.scale(self.image, (120, 250))  # scale

        # Rectangle
        self.rect = self.image.get_rect()

        # Speed
        self.vel_x = 0
        self.vel_y = 0
        self.player_speed = 5

    def update(self):
        self.rect.x += self.vel_x * self.player_speed
        self.rect.y += self.vel_y * self.player_speed

    # Controls for up, down, left, right
    def go_up(self):
        self.vel_y = -4

    def go_down(self):
        self.vel_y = 4

    def go_left(self):
        self.vel_x = -4

    def go_right(self):
        self.vel_x = 4

    def stop(self):
        self.vel_x = 0
        self.vel_y = 0

class Peanut(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("./Assets/Peanut.png")
        self.image = pygame.transform.scale(self.image, (10, 10))  # scale

        # Rectangle
        self.rect = self.image.get_rect()


def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()

    # ------ SPRITE GROUPS
    all_sprites_group = pygame.sprite.RenderUpdates()
    background_group = pygame.sprite.Group()


    # Player creation
    player = Player()
    all_sprites_group.add(player)

    # Background creation
    background = Background()
    background_group.add(background)



    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # ----- LOGIC
        all_sprites_group.update()

        # ----- RENDER
        screen.fill(BLACK)
        background_group.draw(screen)
        all_sprites_group.draw(screen)

        # ----- UPDATE DISPLAY
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()