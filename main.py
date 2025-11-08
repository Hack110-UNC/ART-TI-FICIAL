import numpy
import pygame
import pygame_gui
import random
import time 
import processing as imageProcessing
import parsing
USEAPI=True

SCREEN_WIDTH: int = 500
SCREEN_HEIGHT: int = 300
TICK_RATE: int = 60
BLACK = (0,0,0)
WHITE = (255,255,255)
brushSize = 2
score = 0

#TEMPORARAY
targetWord='tree'
def main():
    drawing=True
    timerActive=False
    imageSent=False
    finishEarly=False
    pygame.init()
    pygame.font.init()

    #Screen Display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(WHITE)

    #GUI Display
    #drawing period over

    pos_list = []
    clock = pygame.time.Clock()
    running = True
    while running: 
        time_delta = clock.tick(TICK_RATE)/1000 #For GUI Manager: Tracks the time between each loop in program
        if drawing and not timerActive:
            startTime = time.time()
            timerActive=True 
        #Tracks whether an event happens
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    finishEarly=True
        if drawing:
            if pygame.mouse.get_pressed()[0]: 
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos not in pos_list:
                    pos_list.append(mouse_pos)
                last_pos = pos_list[len(pos_list)-1]
                second_last_pos = pos_list[len(pos_list)-2]
                pygame.draw.circle(surface=screen, 
                                   color=BLACK, center=mouse_pos, 
                                   radius=int(brushSize))
                pygame.draw.lines(surface=screen, 
                                  color=BLACK, closed=True, 
                                  width=int(brushSize*2.5), 
                                  points=(second_last_pos, last_pos))
            elif pygame.mouse.get_pressed()[0] == False:
                pos_list = []
        pygame.display.flip()
        # clock.tick(TICK_RATE) Moved: Kept in case of broken function
        endTime = time.time()
        if (endTime-startTime >= 30) or (finishEarly and not imageSent): #30 sec draw time, period over
            drawing=False
            timerActive=False
            surface_array = pygame.surfarray.pixels2d(surface=screen)
            if (not imageSent) and USEAPI==True:
                surface_array=surface_array/16777215 #b&w
                path=imageProcessing.imgData2Png(surface_array)
                base64String=imageProcessing.filePath2AIPayload(path)
                AIresponse=imageProcessing.getResponseFromAI(base64String,targetWord)
                AItext = parsing.getRawOutputText(AIresponse)
                objectAccordingToAI,AIscore=parsing.parseRawText(AItext)
                imageSent=True
            elif USEAPI==False:
                print("API use is disabled currently.")
                imageSent=True


                

main()