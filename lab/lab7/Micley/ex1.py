import pygame
from datetime import datetime

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((1400, 950))
pygame.display.set_caption("Clock")

mick = pygame.transform.scale(pygame.image.load("mainclock.png"), (1400, 1050))
min = pygame.transform.scale(pygame.image.load("rightarm.png"), (1400, 1050))
sec = pygame.transform.scale(pygame.image.load("leftarm.png"), (63, 1050))

def rot_center(surf, image, angle, x, y):
    image = pygame.transform.rotate(image, angle)
    rect = image.get_rect(center=image.get_rect(center=(x, y)).center)
    surf.blit(image, rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    screen.blit(mick, (0, 0))
    t = datetime.now()
    rot_center(screen, min, -t.second * (6), 700, 525)
    rot_center(screen, sec, -t.minute * (6), 700, 525)

    pygame.display.flip()
    clock.tick(30)
