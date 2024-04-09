import pygame as pg
from math import cos, sin , pi
pg.init()
screen = pg.display.set_mode((800, 600))
font = pg.font.SysFont("Verdana", 15)
cur_color = 'white'


def get_distance(a,b):
    return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5

def right_triangle(screen, cur, end, d, color):
    x1, y1, x2, y2 = cur[0], cur[1], end[0], end[1]
    # difx = abs(x1-x2)
    dify = abs(y1-y2)
    # if x1 <= x2:
    if y1 < y2:
        pg.draw.polygon(screen, color, [(x1, y1), (x1, y1 + dify), (x2, y2)], d)
    else:
        pg.draw.polygon(screen, color, [(x1, y1), (x1, y1 - dify), (x2, y2)], d)

def triangle(color, pos):
    pg.draw.polygon(screen, color, pos, 3)

def square(screen, start, end, d, color):
    x1 = start[0]
    y1 = start[1]
    x2 = end[0]
    y2 = end[1]

    a = abs(x1-x2)
    if x1 <= x2:
        if y1 < y2:
            pg.draw.rect(screen, color, (x1, y1, a, a), d)
        else:
            pg.draw.rect(screen, color, (x1, y2, a, a), d)
    else:
        if y1 < y2:
            pg.draw.rect(screen, color, (x2, y1, a, a), d)
        else:
            pg.draw.rect(screen, color, (x2, y2, a, a), d)

def rhombus(color, pos):
    pg.draw.polygon(screen, color, pos, 3)

last_pos = (0, 0)
w = 2
draw_line = False
erase = False
# ed = 50

di = {
    'sqr': False,
    'triangle': False,
    'rhombus': False,
    'right_triangle': False
}
screen.fill((0,0,0))
# screen.blit(surf, (0,0))
running = True
while running:
    pos = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                di['sqr'] = True
                for i, j in di.items(): # for i in di.keys():
                    if i != 'sqr':
                        di[i] = False
            if event.key == pg.K_a:
                di['triangle'] = True
                for i, j in di.items():
                    if i != 'triangle':
                        di[i] = False
            if event.key == pg.K_s:
                di['rhombus'] = True
                for i, j in di.items():
                    if i != 'rhombus':
                        di[i] = False
            if event.key == pg.K_d:
                di['right_triangle'] = True
                for i, j in di.items():
                    if i != 'right_triangle':
                        di[i] = False


        elif di['sqr'] == True:
            if event.type == pg.MOUSEBUTTONDOWN:
                last_pos = pos
            if event.type == pg.MOUSEBUTTONUP:
                square(screen, last_pos, pos, w, cur_color)
        elif di['triangle'] == True:
            if event.type == pg.MOUSEBUTTONDOWN:
                last_pos = pos
            if event.type == pg.MOUSEBUTTONUP:
                d = get_distance(last_pos, pos)
                triangle(cur_color,[last_pos, pos,((pos[0] - last_pos[0])*cos(pi/3) - (pos[1] - last_pos[1])*sin(pi/3) + last_pos[0], (pos[0] - last_pos[0])*sin(pi/3) + (pos[1] - last_pos[1])*cos(pi/3) + last_pos[1])])
        if di['right_triangle'] == 1:
            if event.type == pg.MOUSEBUTTONDOWN:
                last_pos = pos
            if event.type == pg.MOUSEBUTTONUP:
                right_triangle(screen, last_pos, pos, w, cur_color)
        elif di['rhombus'] == 1:
            if event.type == pg.MOUSEBUTTONDOWN:
                last_pos = pos
            if event.type == pg.MOUSEBUTTONUP:
                d = get_distance(last_pos, pos)
                rhombus(cur_color, [last_pos, (last_pos[0] + d, last_pos[1]), (pos[0] + d, pos[1]), pos])
        txt = font.render("Draw square - w;        Draw right triangle - d;        Draw equilateral triangle - a;          Draw rhombus - s.", True, (255,255,255))
        screen.blit(txt, (0,0))

    pg.display.update()
pg.quit()