import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake and food sizes
BLOCK_SIZE = 20

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Set up the snake and food
snake = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
food = (random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
        random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)

# Snake movement directions
UP = (0, -BLOCK_SIZE)
DOWN = (0, BLOCK_SIZE)
LEFT = (-BLOCK_SIZE, 0)
RIGHT = (BLOCK_SIZE, 0)

# Initial movement direction
direction = RIGHT

# Set up game variables
score = 0
level = 1
speed = 10
clock = pygame.time.Clock()

# Define food types and their weights
food_types = {
    "normal": 8,
    "special": 2  # Special food appears less frequently
}

# Timer for special food disappearance
special_food_timer = 0
special_food_duration = 5  # Special food lasts for 5 seconds

# Function to draw the snake
def draw_snake(snake):
    for block in snake:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))

# Function to draw the food
def draw_food(food):
    pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))

# Function to check for border collision
def check_border_collision(snake_head):
    return (snake_head[0] < 0 or snake_head[0] >= SCREEN_WIDTH or
            snake_head[1] < 0 or snake_head[1] >= SCREEN_HEIGHT)

# Function to check if snake hits itself
def check_self_collision(snake):
    return len(snake) != len(set(snake))

# Function to generate random position for food
def generate_food_position(snake):
    while True:
        food_position = (random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
                         random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
        if food_position not in snake:
            return food_position

# Function to generate random food type based on weights
def generate_food_type():
    food_pool = []
    for food_type, weight in food_types.items():
        food_pool.extend([food_type] * weight)
    return random.choice(food_pool)

# Main game loop
while True:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle key events
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != DOWN:
        direction = UP
    elif keys[pygame.K_DOWN] and direction != UP:
        direction = DOWN
    elif keys[pygame.K_LEFT] and direction != RIGHT:
        direction = LEFT
    elif keys[pygame.K_RIGHT] and direction != LEFT:
        direction = RIGHT

    # Move the snake
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, new_head)

    # Check for collisions
    if check_border_collision(new_head) or check_self_collision(snake):
        print("Game Over!")
        pygame.quit()
        sys.exit()

    # Check if the snake eats food
    if new_head == food:
        food_type = generate_food_type()
        if food_type == "normal":
            score += 1
        elif food_type == "special":
            score += 5  # Special food gives more points
            special_food_timer = pygame.time.get_ticks()  # Reset special food timer
        if score % 3 == 0:  # Increase level after every 3 foods
            level += 1
            speed += 2  # Increase speed
        food = generate_food_position(snake)
    else:
        snake.pop()

    # Draw snake and food
    draw_snake(snake)
    draw_food(food)

    # Draw score and level
    font = pygame.font.Font(None, 30)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 30))

    # Check and handle special food disappearance
    if special_food_timer != 0:
        if pygame.time.get_ticks() - special_food_timer >= special_food_duration * 1000:
            special_food_timer = 0  # Reset timer
            # Disappear special food by resetting its position
            food = generate_food_position(snake)

    pygame.display.update()
    clock.tick(speed)
