import pygame

pygame.init()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
size = height, weight = (600, 600)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

x, y, dx, dy, velocity = 0, 0, 0, 0, 5

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                dy, dx = 0, -velocity
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                dy, dx = 0, velocity
            elif event.key in (pygame.K_UP, pygame.K_w):
                dx, dy = 0, -velocity
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                dx, dy = 0, velocity

    screen.fill(WHITE)
    y += dy
    x += dx
    x, y = max(0, min(x, height - 50)), max(0, min(y, weight - 50))
    pygame.draw.ellipse(screen, RED, (x, y, 50, 50))
    clock.tick(60)
    pygame.display.update()
pygame.quit()