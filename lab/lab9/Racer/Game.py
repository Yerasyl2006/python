import random
import pygame

# Initialize pygame
pygame.init()

# Set the width and height of the screen
WIDTH, HEIGHT = 400, 600

# Create the game screen and loss screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
LOSS_SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# Define some colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Initialize score and life
SCORE = 0
LIFE = 3

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Load background image
background = pygame.image.load('AnimatedStreet.png')

# Create font objects for displaying score and life
score_font = pygame.font.SysFont("Verdana", 30)
life_font = pygame.font.SysFont("Verdana", 30)

# Load sounds
background_sound = pygame.mixer.Sound("background.wav")
crush_sound = pygame.mixer.Sound("crash.wav")

# Initialize background position
background_y = 0


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = random.randint(6, 8)
        self.image = pygame.image.load('Enemy.png')
        self.rect = self.image.get_rect()
        self.rect.center = (
            random.randint(self.rect.width, WIDTH - self.rect.width),
            0,
        )

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.y > HEIGHT:
            self.rect.center = (
                random.randint(self.rect.width, WIDTH - self.rect.width),
                0,
            )


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 7
        self.image = pygame.image.load('Player.png')
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - self.rect.height // 2 - 20)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT] and self.rect.x - self.speed >= 0:
            self.rect.move_ip(-self.speed, 0)
        elif pressed[pygame.K_RIGHT] and self.rect.x + self.speed + self.rect.width <= WIDTH:
            self.rect.move_ip(self.speed, 0)


# Create a group for coins
coins = pygame.sprite.Group()


# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = random.randint(5, 8)
        self.random_number = random.randint(0, 6)
        if self.random_number in [0, 1, 2]:
            self.image = pygame.image.load("Coin.png")
        else:
            self.image = pygame.image.load("cent.png")
        self.resized_image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.resized_image.get_rect()
        if WIDTH - self.rect.width > self.rect.width:
            x = random.randint(self.rect.width, WIDTH - self.rect.width)
        else:
            x = random.randint(WIDTH - self.rect.width, self.rect.width)
        self.rect.center = (x, 0)

    def draw(self, surface):
        surface.blit(self.resized_image, self.rect)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.y > HEIGHT:
            global LIFE
            LIFE -= 1
            self.rect.center = (
                random.randint(self.rect.width, WIDTH - self.rect.width),
                0,
            )

    def collide(self, player):
        if pygame.sprite.collide_rect(self, player):
            self.kill()  # Remove the sprite from all sprite groups it belongs to
            return True

        return False

    def is_mega_coin(self):
        return self.random_number in [0, 1, 2]


# Main function
def main():
    # Declare global variables
    global background_y
    global coins
    global SCORE
    global LIFE

    # Initialize the game loop
    running = True

    # Create player, enemy, and coin objects
    player = Player()
    enemy = Enemy()
    coin = Coin()

    # Create sprite groups for enemies and add the initial enemy
    enemies = pygame.sprite.Group()
    enemies.add(enemy)

    # Add the initial coin to the coin group
    coins.add(coin)

    # Start playing background music
    background_sound.play(-1)

    # Game loop
    while running:
        # Clear the screen
        SCREEN.fill(WHITE)

        # Display the background image
        background_rect = background.get_rect()
        SCREEN.blit(background, (0, background_y))
        SCREEN.blit(background, (0, background_y - background_rect.height))
        background_y += 4  # Update the y-coordinate to make the image move
        if background_y > background_rect.height:
            background_y = 0

        # Display score and life
        score = score_font.render(f"Your score: {SCORE}", True, BLACK)
        SCREEN.blit(score, (5, 0))
        life = life_font.render(f"Your life: {LIFE}", True, BLACK)
        SCREEN.blit(life, (5, 30))

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or LIFE == 0:
                running = False

        # Update player and enemy
        player.update()
        enemy.update()

        # Check for collisions between player and coins
        for coin in coins:
            if coin.collide(player):
                coins.remove(coin)
                SCORE += 1
                coins.add(Coin())
                if coin.is_mega_coin():
                    SCORE += 4

        # Increase enemy speed after certain score threshold
        if SCORE > 30:
            enemy.speed = random.randint(8, 11)

        # End game if life reaches 0
        if LIFE == 0:
            running = False

        # Update and draw coins, player, and enemy
        for coin in coins:
            coin.draw(SCREEN)
            coin.update()

        player.draw(SCREEN)
        enemy.draw(SCREEN)

        # Check for collisions between player and enemies
        if pygame.sprite.spritecollide(player, enemies, False):
            background_sound.stop()  # Stop playing the background music
            crush_sound.play()  # Play the crash sound effect
            pygame.time.wait(2000)
            running = False

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)


# Call the main function to start the game
main()