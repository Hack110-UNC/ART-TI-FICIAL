import numpy
import pygame
import pygame_gui
import random
import time 
import os
import processing as imageProcessing
import parsing
from drawing import * 
USEAPI=True

SCREEN_WIDTH: int = 1000
SCREEN_HEIGHT: int = 600
TICK_RATE: int = 60
BLACK = (0,0,0)
WHITE = (255,255,255)
brushSize = 2
score = 0
round = 0
sec = 0

pygame.init()
pygame.font.init()

#Screen Display Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(WHITE)

#Converting Text to Label
text_font = pygame.font.SysFont("verdana", 25, bold=True)
def label_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))
nounsPath = os.path.join(os.getcwd(),"assets","nouns.csv") #to ensure it works on all operating systems
drawingNouns=parsing.csvNounsToList(nounsPath)

def main():
    drawing=True
    timerActive=False
    imageSent=False
    finishEarly=False
    roundTime=30
    index=random.randint(0,len(drawingNouns)-1)
    targetWord=drawingNouns[index]
    sec=roundTime
    pen_color = BLACK
    eraser_size = 1
    num = 0
    score = 0
    pos_list = []
    clock = pygame.time.Clock()
    running = True


    while running: 
        #Labels Display Setup
        label_text(f"Score: {score}", text_font, (0,0,0), 10, 10)
        label_text(f"Round: {round}", text_font, (0,0,0), 835, 10)
        label_text(f"Timer: {sec}", text_font, (0,0,0), 425, 10)
        label_text(f"Draw: {targetWord}", text_font, (0,0,0),375,570)
        if drawing and not timerActive:
            startTime = time.time()
            timerActive=True 
        #Tracks whether an event happens
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    finishEarly=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    num += 1
                    if num % 2 == 1:
                        pen_color = WHITE
                        eraser_size = 3
                    else:
                        pen_color = BLACK
                        eraser_size = 1
        if drawing:
            if pygame.mouse.get_pressed()[0]: 
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos not in pos_list:
                    pos_list.append(mouse_pos)
                last_pos = pos_list[len(pos_list)-1]
                second_last_pos = pos_list[len(pos_list)-2]
                pygame.draw.circle(surface=screen, 
                                   color=pen_color, center=mouse_pos, 
                                   radius=int(brushSize*eraser_size))
                pygame.draw.lines(surface=screen, 
                                  color=pen_color, closed=True, 
                                  width=int(brushSize*2.5*eraser_size), 
                                  points=(second_last_pos, last_pos))
                
            elif pygame.mouse.get_pressed()[0] == False:
                pos_list = []
        pygame.display.flip()
        clock.tick(TICK_RATE)
        endTime = time.time()
        elasped=endTime-startTime
        clearTopSection(screen)
        if (elasped >= roundTime) or (finishEarly and not imageSent): #30 sec draw time, period over
            drawing=False
            timerActive=False
            time.sleep(2)
            if (not imageSent) and USEAPI==True:
                surface_array = pygame.surfarray.pixels2d(surface=screen)
                surface_array=surface_array/16777215 #b&w
                path=imageProcessing.imgData2Png(surface_array)
                del surface_array
                base64String=imageProcessing.filePath2AIPayload(path)
                AIresponse=imageProcessing.getResponseFromAI(base64String,targetWord)
                AItext = parsing.getRawOutputText(AIresponse)
                objectAccordingToAI,AIscore=parsing.parseRawText(AItext)
                print("API called successfully")
                clearTopSection(screen)
                label_text(f"You drew: {objectAccordingToAI}. Score: {AIscore}/5000", text_font, (0,0,0), 200, 10)
                pygame.display.flip()
                score=score+AIscore
                time.sleep(10)
                clearTopSection(screen)
                imageSent=True
            elif USEAPI==False and not imageSent:
                print("API use is disabled currently.")
                imageSent=True
        else:
            if elasped<30:
                sec=int(roundTime-elasped)

main()