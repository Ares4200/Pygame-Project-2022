# Pygame Project


import pygame
import time
import random



# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 1920
HEIGHT = 1080
SPEED = 4
font_name = pygame.font.match_font('impact')
TITLE = "<Pygame Project 2022>"
pygame.mixer.init()

# Game sounds
peanut_sound = pygame.mixer.Sound("./Sounds/Anya say peanut.ogg")


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


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
        self.rect.x = WIDTH / 2 - 97.5
        self.rect.y = HEIGHT - self.rect.height - 10

        # Speed
        self.vel_x = 0
        self.player_speed = 4

    def update(self):
        self.rect.x += self.vel_x * self.player_speed

class Peanut(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("./Assets/Peanut.png")
        self.image = pygame.transform.scale(self.image, (80, 120))  # scale

        # Rectangle
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(25, WIDTH - self.rect.width - 25)
        self.rect.y = 0

        # Speed
        self.vel_y = 5

    def update(self):
        self.rect.y += self.vel_y

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Image
        self.image = pygame.image.load("./Assets/Villain.png")
        self.image = pygame.transform.scale(self.image, (150, 200))  # scale

        # Rectangle
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = 0

        # Speed
        self.vel_y = 10

    def update(self):
        self.rect.y += self.vel_y


def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    peanut_spawn = random.randrange(4000, 6000)
    enemy_spawn = 1000
    peanut_latest_spawn = pygame.time.get_ticks()
    enemy_latest_spawn = pygame.time.get_ticks()
    score = 0
    life = 5

    # ------ SPRITE GROUPS
    all_sprites_group = pygame.sprite.RenderUpdates()
    background_group = pygame.sprite.Group()
    peanut_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()


    # Player
    player = Player()
    all_sprites_group.add(player)

    # Background
    background = Background()
    background_group.add(background)

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False

            # ---- CONTROLS
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    player.vel_x = SPEED
                elif event.key == pygame.K_a:
                    player.vel_x = -SPEED

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player.vel_x < 0:
                    player.vel_x = 0
                if event.key == pygame.K_d and player.vel_x > 0:
                    player.vel_x = 0

        # Makes sure player is not out of screen (x-axis)
        if player.rect.right > WIDTH:
           player.rect.right = WIDTH
        if player.rect.left < 0:
           player.rect.left = 0

        # ----- LOGIC
        all_sprites_group.update()

        # Peanut Spawn
        if pygame.time.get_ticks() > peanut_latest_spawn + peanut_spawn:
            # set the new time to this current time
            peanut_latest_spawn = pygame.time.get_ticks()
            # Spawn Peanut
            peanut = Peanut()
            all_sprites_group.add(peanut)
            peanut_group.add(peanut)

        # Enemy Spawn
        if pygame.time.get_ticks() > enemy_latest_spawn + enemy_spawn:
            enemy_latest_spawn = pygame.time.get_ticks()
            # Spawn enemy
            enemy = Enemy()
            all_sprites_group.add(enemy)
            enemy_group.add(enemy)

        # If a peanut hits the ground
        for peanut in peanut_group:
            if peanut.rect.y >= HEIGHT - peanut.rect.height - 7:
                peanut.kill()

            # Player collision
            peanuts_collected = pygame.sprite.spritecollide(player, peanut_group, True)
            if len(peanuts_collected) > 0:
                peanut.kill()
                peanut_sound.play()
                score += 1

        # If an enemy hits the player
        enemy_collide = pygame.sprite.spritecollide(player, enemy_group, True)
        for enemy in enemy_group:
            if len(enemy_collide) > 0:
                enemy.kill()
                # damage_sound.play()
                life -= 1

        # Gamer Over
        if life < 0:
            done = True

        # ----- RENDER
        background_group.draw(screen)
        draw = all_sprites_group.draw(screen)

        # ----- UPDATE DISPLAY
        pygame.display.update(draw)
        draw_text(screen, ("Score: " + str(score)), 36, 95, 10)
        draw_text(screen, ("Life: " + str(life)), 36, 1190, 10)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()