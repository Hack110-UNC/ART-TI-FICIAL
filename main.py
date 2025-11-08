# import numpy as np
import pygame
import random

SCREEN_WIDTH: int = 1000
SCREEN_HEIGHT: int = 600
TICK_RATE: int = 60
BLACK = (0,0,0)
WHITE = (255,255,255)

# class Boulder(pygame.sprite.Sprite):
#     speed: int
#     surf: pygame.Surface
#     rect: pygame.Rect

#     def __init__(self):
#         super(Boulder, self).__init__()

#         self.speed = random.randint(4, 12)
#         self.surf = pygame.image.load("assets/boulder.png").convert()
#         self.rect = self.surf.get_rect(bottomleft = (SCREEN_WIDTH, ))

def main():
    pygame.init()

    #Display Style
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(WHITE)

    pos_list = []

    clock = pygame.time.Clock()
    running = True
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pass
        if pygame.mouse.get_pressed()[0]: 
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos not in pos_list:
                pos_list.append(mouse_pos)
            last_pos = pos_list[len(pos_list)-1]
            print(last_pos)
            second_last_pos = pos_list[len(pos_list)-2]
            pygame.draw.circle(surface=screen, color=BLACK, center=mouse_pos, radius=13)
            pygame.draw.lines(surface=screen, color=BLACK, closed=True, width=30, points=(second_last_pos, last_pos))
        elif pygame.mouse.get_pressed()[0] == False:
            pos_list = []

        pygame.display.flip()
        clock.tick(TICK_RATE)
   
main()