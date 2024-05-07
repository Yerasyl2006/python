import pygame
import time
import random
import psycopg2


connection = psycopg2.connect(
    host="localhost",
    database="labs",
    user="postgres",
    password="12345678",
    port="5432"
)

cur = connection.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(255) PRIMARY KEY,
    current_level INT DEFAULT 1
);
""")

cur.execute("""CREATE TABLE IF NOT EXISTS user_score (
    username VARCHAR(255) PRIMARY KEY,
    score INT DEFAULT 0
);
""")

window_x = 720
window_y = 480


boundry = []

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


levels = {
     1: {
        "speed": 15,
        "wall_color": pygame.Color(100, 100, 100),
        "walls": [
            (0, 0, window_x, 10),
            (0, 10, 10, window_y - 20),
            (window_x - 10, 10, 10, window_y - 20),
            (0, window_y - 10, window_x, 10),
            (window_x // 2 - 10, 10, 20, window_y // 8 - 20),
            (window_x // 2 - 10, window_y // 8 + 40, 20, window_y // 4 - 40),
            (window_x // 2 - 10, window_y // 2 + 10, 20, window_y // 8 - 20),
            (window_x // 2 - 10, window_y * 5 // 8 + 40, 20, window_y // 4 - 40),
            (window_x // 2 - 10, window_y * 3 // 4 + 10, 20, window_y // 8 - 20)
        ]
    }

,
    2: {
        "speed": 20,
        "wall_color": pygame.Color(150, 75, 0),
        "walls": [
            (300, 150, window_x / 2, 100),
            (0, 100, 140, window_y - 203),
            (window_x - 170, 230, 10, window_y - 20),
            (340, window_y - 110, window_x / 2, 104)
        ]
    },
    3: {
        "speed": 25,
        "wall_color": pygame.Color(0, 100, 100),
        "walls": [
            (300, 15, window_x / 2, 100),
            (140, 100, 140, window_y - 203),
            (window_x - 70, 330, 10, window_y - 20),
            (240, window_y - 110, window_x / 2, 184)
        ]
    }
}


def createWall():
    global boundry
    boundry = []
    for i in range(0, window_x):
        boundry.append((i, 0))
        boundry.append((i, window_y - 18))
    for i in range(0, window_y):
        boundry.append((0, i))
        boundry.append((window_x - 18, i))


def drawWall():
    for each in boundry:
        wallRect = pygame.Rect(each[0], each[1], 10, 10)
        pygame.draw.rect(game_window, green, wallRect)


pygame.init()


pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))


fps = pygame.time.Clock()


snake_position = [100, 50]


snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]]


fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                  random.randrange(1, (window_y // 10)) * 10]

fruit_spawn = True


direction = 'RIGHT'
change_to = direction


score = 0


fruit_timer = 0

def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)


def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    update_user_score(user)
    pygame.quit()
    quit()


def insert_new_user(new_user):
    cur.execute("""INSERT INTO users VALUES ('{}', 1)""".format(new_user))
    cur.execute("""INSERT INTO user_score VALUES ('{}', 0)""".format(new_user))
    connection.commit()


def update_user_score(user_name):
    cur.execute("""UPDATE user_score
    SET score={}
    WHERE username='{}'
    """.format(score, user_name))
    connection.commit()


def get_user_level(user_name):
    cur.execute("SELECT current_level FROM users WHERE username='{}'".format(user_name))
    data = cur.fetchone()
    return data[0]


def set_user_level(user_name, level):
    cur.execute("""UPDATE users
    SET current_level={}
    WHERE username='{}'
    """.format(level, user_name))
    connection.commit()

def draw_walls(level):
    for wall in levels[level]["walls"]:
        pygame.draw.rect(game_window, levels[level]["wall_color"], pygame.Rect(wall))


def check_collisions():

    for boundary in boundry:
        if snake_position[0] == boundary[0] and snake_position[1] == boundary[1]:
            game_over()
   
    for wall in levels[get_user_level(user)]["walls"]:
        wall_rect = pygame.Rect(wall)
        if wall_rect.colliderect(pygame.Rect(snake_position[0], snake_position[1], 10, 10)):
            game_over()


start_time = time.time()


print("Enter your username:")
user = input()


while time.time() - start_time < 7:
    pass


cur.execute("SELECT count(*) FROM users WHERE username='{}'".format(user))
if cur.fetchone()[0] == 0:
    insert_new_user(user)
    print("New user {} has been created.".format(user))
else:
    print("Welcome back, {}!".format(user))
    print("Current level: {}".format(get_user_level(user)))


while True:
   
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            elif event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            elif event.key == pygame.K_p:
               
                paused = True
                while paused:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                            
                            paused = False

    fruit_timer += 1

   
    if fruit_timer > 7 * levels[get_user_level(user)]["speed"]:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]
        fruit_timer = 0

    
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

   
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    
    check_collisions()

   
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
        fruit_timer = 0  
        update_user_score(user)
        
        if score >= 30:
            current_level = get_user_level(user)
            next_level = current_level + 1
            if next_level <= 3: 
                set_user_level(user, next_level)
                print(f"Congratulations! You've reached level {next_level}.")
                score = 0  
                print("Congratulations! You've completed all levels.")
                game_over()
    else:
        snake_body.pop()


    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]
        
        while fruit_position in boundry:
            fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                              random.randrange(1, (window_y // 10)) * 10]
        fruit_spawn = True

   
    game_window.fill(black)
    
    draw_walls(get_user_level(user))  
    drawWall()
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

  
    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over()
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

   
    show_score(1, white, 'times new roman', 20)

  
    pygame.display.update()

    
    fps.tick(levels[get_user_level(user)]["speed"])