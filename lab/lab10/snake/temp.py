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


cur.execute("""CREATE TABLE IF NOT EXISTS snakegame (
    username VARCHAR(255),
    user_score INT,
    user_level INT
);
""")

snake_speed = 15

# размер окна
window_x = 720
window_y = 480

# определение цветов
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# инициализация
pygame.init()

# Инициализация игрового окна
pygame.display.set_caption('Змейка')
game_window = pygame.display.set_mode((window_x, window_y))

# Контроллер FPS (кадры в секунду)
fps = pygame.time.Clock()

# определение положения змеи по умолчанию
snake_position = [100, 50]

# определение первых 4 блоков тела змеи
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]

# fruit position
fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                  random.randrange(1, (window_y // 10)) * 10]

fruit_spawn = True

# установка направления змеи по умолчанию к
# право
direction = 'RIGHT'
change_to = direction

# начальная оценка
score = 0

fruit_time = 5

# переменная для отслеживания времени появления фрукта
fruit_timer = 0

# отображение функции Score
def show_score(choice, color, font, size) :
    # создание объекта шрифта score_font
    score_font = pygame.font.SysFont(font, size)

    # создать объект поверхности отображения
    # score_surface
    score_surface = score_font.render('Score : ' + str(score), True, color)

    # создаем прямоугольный объект для текста
    # поверхностный объект
    score_rect = score_surface.get_rect()

    # отображение текста
    game_window.blit(score_surface, score_rect)


# функция завершения игры
def game_over() :
    # создание объекта шрифта my_font
    my_font = pygame.font.SysFont('times new roman', 50)

    # создание текстовой поверхности, на которой текст
    # будет нарисовано
    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, red)

    # создать прямоугольный объект для текста
    # surface object
    game_over_rect = game_over_surface.get_rect()

    # установка положения текста
    game_over_rect.midtop = (window_x / 2, window_y / 4)

    # blit нарисует текст на экране
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    # через 2 секунды мы выйдем из программы
    time.sleep(2)

    # деактивация библиотеки pygame
    pygame.quit()

    # quit the program
    quit()

def insert(newuser):
    cur.execute("""INSERT INTO snakegame VALUES ('{}',0,0)""".format(newuser))
    
def update(curuser):
    cur.execute("SELECT * FROM snakegame WHERE username='{}'".format(curuser))
    data=cur.fetchone()
    cur.execute("""UPDATE snakegame
    SET user_score={}, user_level={}
    WHERE username='{}'
    """.format(max(data[1],score),max(data[2],score*5//10),curuser))
    connection.commit()

# Инициализация времени начала игры
start_time = time.time()

# Запрос имени пользователя
print("Enter your username:")
user=input()

# Ожидание ввода имени пользователя на 5 секунд
while time.time() - start_time < 5:
    pass

cur.execute("SELECT count(*) FROM snakegame WHERE username='{}'".format(user))
if cur.fetchone()[0]==0:
    insert(user)
    connection.commit()
else:
    cur.execute("SELECT * FROM snakegame WHERE username='{}'".format(user))
    data=cur.fetchone()
    print("User's max score:{}".format(data[1]))
    print("User's max level:{}".format(data[2]))

# Main Function
while True :
    # обработка ключевых событий
    for event in pygame.event.get() :
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_UP :
                change_to = 'UP'
            if event.key == pygame.K_DOWN :
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT :
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT :
                change_to = 'RIGHT'

    # Увеличение таймера
    fruit_timer += 1

    # Если прошло более 7 секунд, сбросить фрукт
    if fruit_timer > 7 * snake_speed:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]
        fruit_timer = 0

    # Если две клавиши нажаты одновременно
    # мы не хотим, чтобы змея разделялась на две
    # направлений одновременно
    if change_to == 'UP' and direction != 'DOWN' :
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP' :
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT' :
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT' :
        direction = 'RIGHT'

    # Перемещение змеи
    if direction == 'UP' :
        snake_position[1] -= 10
    if direction == 'DOWN' :
        snake_position[1] += 10
    if direction == 'LEFT' :
        snake_position[0] -= 10
    if direction == 'RIGHT' :
        snake_position[0] += 10

    # Механизм роста тела змеи
    # если фрукты и змеи сталкиваются, то очки
    # будет увеличено на 10
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1] :
        score += 10
        fruit_spawn = False
        fruit_timer = 0  # сбросить таймер при поедании фрукта
        update(user)
    else :
        snake_body.pop()

    if not fruit_spawn :
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]
        fruit_spawn = True

    game_window.fill(black)

    for pos in snake_body :
        pygame.draw.rect(game_window, green,
                         pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, white, pygame.Rect(
        fruit_position[0], fruit_position[1], 10, 10))

    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > window_x - 10 :
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y - 10 :
        game_over()

    # Touching the snake body
    for block in snake_body[1 :] :
        if snake_position[0] == block[0] and snake_position[1] == block[1] :
            game_over()
            
            
    

    # displaying score continuously
    show_score(1, white, 'times new roman', 20)

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    fps.tick(snake_speed)