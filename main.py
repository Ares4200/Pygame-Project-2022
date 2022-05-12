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
SPEED = 3
TITLE = "<Pygame Project 2022>"


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./Assets/City Background.jpg")
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))

        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("./Assets/Anya_Forger_Anime_2.png")
        self.image = pygame.transform.scale(self.image, (100, 250))  # scale

        # Rectangle
        self.rect = self.image.get_rect()

        self.rect.centerx = (WIDTH // 10)
        self.rect.centery = (HEIGHT // 2)

        # Speed
        self.vel_x = 0
        self.vel_y = 0

        self.player_speed = 4

    def update(self):
        self.rect.x += self.vel_x * self.player_speed
        self.rect.y += self.vel_y * self.player_speed

    # Controls for up, down, left, right
    def go_up(self):
        self.vel_y = -4

    def go_down(self):
        self.vel_y = 4

    def stop(self):
        self.vel_x = 0
        self.vel_y = 0

class Peanut(pygame.sprite.Sprite):
    def __init__(self, coords):
        super().__init__()

        # Image
        self.image = pygame.image.load("./Assets/Peanut.png")
        self.image = pygame.transform.scale(self.image, (80, 120))  # scale

        # Rectangle
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.bottom = coords

        self.vel_x = 0

        def update(self):
            self.rect.x += self.vel_x



def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    bool =  True

    # ------ SPRITE GROUPS
    all_sprites_group = pygame.sprite.RenderUpdates()
    background_group = pygame.sprite.Group()
    peanut_sprites = pygame.sprite.Group()


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

            # ---- CONTROLS
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    player.vel_x = SPEED
                    player.image = pygame.image.load("./Assets/Anya_Forger_Anime_2.png")
                    player.image = pygame.transform.scale(player.image, (80, 250))
                    bool = True
                if event.key == pygame.K_a:
                    player.vel_x = -SPEED
                    player.image = pygame.image.load("./Assets/Anya_Forger_Anime_2.png")
                    player.image = pygame.transform.scale(player.image, (80, 250))
                    bool = False
                if event.key == pygame.K_w:
                    player.go_up()
                if event.key == pygame.K_s:
                    player.go_down()

                # Bullets (Peanuts)
                if event.key == pygame.K_SPACE and bool and len(peanut_sprites) < 5:
                    peanut = Peanut(player.rect.midbottom)
                    all_sprites_group.add(peanut)
                    peanut_sprites.add(peanut)
                    peanut.vel_x = 20
                if event.key == pygame.K_SPACE and not bool and len(peanut_sprites) < 5:
                    peanut = Peanut(player.rect.midbottom)
                    all_sprites_group.add(peanut)
                    peanut_sprites.add(peanut)
                    peanut.vel_x = -20


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player.vel_x < 0:
                    player.stop()
                if event.key == pygame.K_d and player.vel_x > 0:
                    player.stop()
                if event.key == pygame.K_w and player.vel_y < 0:
                    player.stop()
                if event.key == pygame.K_s and player.vel_y > 0:
                    player.stop()

        # Makes sure player is not out of screen (x-axis)
        if player.rect.right > WIDTH:
           player.rect.right = WIDTH
        if player.rect.left < 0:
           player.rect.left = 0

        # Makes sure player is not out of screen (y-axis)
        if player.rect.bottom > HEIGHT:
           player.rect.bottom = HEIGHT
        if player.rect.top < 0:
           player.rect.top = 0

        # ----- LOGIC
        all_sprites_group.update()

        # ----- RENDER
        background_group.draw(screen)
        all_sprites_group.draw(screen)

        # ----- UPDATE DISPLAY
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()