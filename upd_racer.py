import pygame
import sys
from pygame.locals import *
import random
import time

pygame.init()
fps = pygame.time.Clock()

red = (255, 0, 0)  # colors variables
black = (0, 0, 0)
white = (255, 255, 255)

SCREEN_WIDTH = 400  # other
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0
COINS_FOR_SPEED_BOOST = 5  # Number of coins needed to increase enemy speed

font = pygame.font.SysFont("Verdana", 60)  # fonts
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, black)

background = pygame.image.load("AnimatedStreet.png")  # setting background
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # white screen
DISPLAYSURF.fill(white)
pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):  # enemy object
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > SCREEN_HEIGHT):  # if enemy car passes through the window get us 1 point, then spawn another
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):  # player object
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)  # spawn pos

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        # if pressed_keys[K_UP]:
        #     self.rect.move_ip(0, -5)
        # if pressed_keys[K_DOWN]:
        #     self.rect.move_ip(0, 5)
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):  # coin object
    # Different coin weights/types with their values
    # Weight determines probability of spawning (higher weight = more common)
    COIN_TYPES = [
        {"weight": 50, "value": 1, "color_scale": 1.0},      # Common coin (50% chance)
        {"weight": 30, "value": 2, "color_scale": 1.2},      # Uncommon coin (30% chance)
        {"weight": 15, "value": 3, "color_scale": 1.4},      # Rare coin (15% chance)
        {"weight": 5, "value": 5, "color_scale": 1.6},       # Very rare coin (5% chance)
    ]

    def __init__(self):
        super().__init__()
        # Randomly select coin type based on weights
        total_weight = sum(coin_type["weight"] for coin_type in self.COIN_TYPES)
        rand = random.randint(1, total_weight)

        cumulative_weight = 0
        self.coin_type = None
        for coin_type in self.COIN_TYPES:
            cumulative_weight += coin_type["weight"]
            if rand <= cumulative_weight:
                self.coin_type = coin_type
                break

        # If no type selected (shouldn't happen), default to first type
        if self.coin_type is None:
            self.coin_type = self.COIN_TYPES[0]

        self.image = pygame.image.load("gold.png").convert_alpha()
        # Scale coin based on its value (higher value = slightly larger)
        scale = self.coin_type["color_scale"]
        self.image = pygame.transform.scale(self.image, (int(28 * scale), int(28 * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), 0)
        self.value = self.coin_type["value"]  # Store coin value

    def move(self):
        self.rect.move_ip(0, max(1, int(SPEED / 1.5)))  # coin slower than cars
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), 0)

P1 = Player()  # sprites
E1 = Enemy()
enemies = pygame.sprite.Group()  # sprite groups
enemies.add(E1)
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
initial_coin = Coin()  # first coin
coins.add(initial_coin)
all_sprites.add(initial_coin)

# Track coins collected for speed boost
coins_collected_for_speed = 0
last_speed_boost_coins = 0

# Adding a new User event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
SPAWN_COIN = pygame.USEREVENT + 2  # event that spawns coin every 3 sec
pygame.time.set_timer(SPAWN_COIN, 3000)

# Game Loop
while True:
    # Cycles through all events occurring
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == SPAWN_COIN:  # spawns no more than 5 coins
            if len(coins) < 5:
                c = Coin()
                coins.add(c)
                all_sprites.add(c)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))  # background drawing
    scores = font_small.render(str(SCORE), True, black)
    DISPLAYSURF.blit(scores, (10, 10))
    coin_text = font_small.render(f"Coins: {COINS}", True, black)  # coins counter
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 100, 10))

    # Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        # only call move if sprite has move method
        if hasattr(entity, 'move'):
            entity.move()

    collected = pygame.sprite.spritecollide(P1, coins, True)  # checks if player touched the coins
    if collected:
        # Add up the values of all collected coins
        coins_value = sum(coin.value for coin in collected)
        COINS += coins_value
        coins_collected_for_speed += coins_value

        # Check if player has collected enough coins to increase enemy speed
        # Every N coins (COINS_FOR_SPEED_BOOST), increase enemy speed
        if coins_collected_for_speed >= last_speed_boost_coins + COINS_FOR_SPEED_BOOST:
            SPEED += 1  # Increase enemy speed by 1
            last_speed_boost_coins = coins_collected_for_speed
            # Optional: You could add a visual indicator here

        # Respawn collected coins
        for i in collected:
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)

    # To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        try:
            pygame.mixer.Sound('crash.wav').play()
        except Exception:
            pass
        time.sleep(0.5)

        DISPLAYSURF.fill(red)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    fps.tick(60)
