import pygame
def clearTopSection(screen): #screen is pygame surface
    topScreenRect=(0,0,1000,60)
    pygame.draw.rect(screen,"white",topScreenRect)
