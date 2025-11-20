import pygame, time, random

speed = 15
SPEED_INCREMENT = 2
FRUITS_PER_LEVEL = 3  # speed and level manipulations

window_x = 720
window_y = 480  # game window sizes

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0)
purple = pygame.Color(255, 0, 255)  # needed colors

pygame.init()
pygame.display.set_caption('amanbol snake')
game_window = pygame.display.set_mode((window_x, window_y))  # setting window and caption
fps = pygame.time.Clock()

snake_position = [100, 50]  # starting pos
snake_body = [
    [100, 50],
    [90, 50],
    [80, 50],
    [70, 50]
]  # starting positions of body

FOOD_TYPES = [
    {"value": 50, "color": red, "weight": 50},
    {"value": 100, "color": yellow, "weight": 30},
    {"value": 200, "color": blue, "weight": 15},
    {"value": 500, "color": purple, "weight": 5},
]

def get_random_food_type():
    total_weight = sum(food["weight"] for food in FOOD_TYPES)
    rand = random.randint(1, total_weight)
    
    cumulative_weight = 0
    for food_type in FOOD_TYPES:
        cumulative_weight += food_type["weight"]
        if rand <= cumulative_weight:
            return food_type
    
    return FOOD_TYPES[0]

def spawn_fruit():  # func for spawning food
    while True:
        x = random.randrange(1, (window_x // 10) - 1) * 10
        y = random.randrange(1, (window_y // 10) - 1) * 10
        if [x, y] not in snake_body:
            food_type = get_random_food_type()
            spawn_time = time.time()
            return [x, y], food_type, spawn_time

FRUIT_LIFETIME = 5.0

fruit_data = spawn_fruit()
fruit_position = fruit_data[0]
fruit_type = fruit_data[1]
fruit_spawn_time = fruit_data[2]
fruit_spawn = True  # setting default(or starting) values

direction = 'RIGHT'
change_to = direction
score = 0
level = 1
fruits_eaten_this_level = 0

def show_score_and_level(color, font, size):  # func for showing both score and level atm
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    score_rect.topleft = (10, 10)
    game_window.blit(score_surface, score_rect)
    level_surface = score_font.render('Level : ' + str(level), True, color)
    level_rect = level_surface.get_rect()
    level_rect.topright = (window_x - 10, 10)
    game_window.blit(level_surface, level_rect)

def game_over():  # game over screen
    my_font = pygame.font.SysFont('impact', 50)
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

while True:  # main game loop
    for event in pygame.event.get():  # buttons settings
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
    
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
    
    if direction == 'UP':
        snake_position[1] -= 10  # moving snake
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10
    
    snake_body.insert(0, list(snake_position))  # growing mechanic
    
    current_time = time.time()
    time_elapsed = current_time - fruit_spawn_time
    fruit_expired = time_elapsed >= FRUIT_LIFETIME
    
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:  # if snake and food touch then add points
        score += fruit_type["value"]
        fruit_spawn = False
        fruits_eaten_this_level += 1
        if fruits_eaten_this_level >= FRUITS_PER_LEVEL:  # if number of eaten food at the level is bigger than 3, increase level and set count to 0
            level += 1
            fruits_eaten_this_level = 0
            speed += SPEED_INCREMENT
    elif fruit_expired:
        fruit_spawn = False
    else:
        snake_body.pop()  # prevents snake from growing endlessly without taking food
    
    if not fruit_spawn:
        fruit_data = spawn_fruit()
        fruit_position = fruit_data[0]
        fruit_type = fruit_data[1]
        fruit_spawn_time = fruit_data[2]
    
    fruit_spawn = True
    
    game_window.fill(black)  # game background
    
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    
    if not fruit_expired:
        pygame.draw.rect(game_window, fruit_type["color"], pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))
    
    if snake_position[0] < 10 or snake_position[0] > window_x - 20:
        game_over()
    if snake_position[1] < 10 or snake_position[1] > window_y - 20:
        game_over()
    
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()  # ending game if snake touches the borders or itself
    
    show_score_and_level(white, 'impact', 20)  # color font and sizes
    pygame.display.update()  # adding drawn objects to the screen
    fps.tick(speed)  # fps
