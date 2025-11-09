try:
    import pygame
    import pygame_gui
    import random
    import time 
    import os
    import processing as imageProcessing
    import parsing
    from drawing import * 
    from utils import *
except Exception as e:
    print(f"Error importing modules, exiting now: {e}")
    exit()
USEAPI=True

SCREEN_WIDTH: int = 900
SCREEN_HEIGHT: int = 600
TICK_RATE: int = 60
BLACK = (0,0,0)
WHITE = (255,255,255)
brushSize = 2
score = 0
round = 0
sec = 0

bg_img = pygame.image.load("Drawin.jpg")

pygame.init()
pygame.font.init()

#Screen Display Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(WHITE)

#Converting Text to Label
text_font = pygame.font.SysFont("Comic Sans MS", 25, bold=True)
title_font = pygame.font.SysFont("Comic Sans MS", 60, bold=True)
def label_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

easyNounsPath = os.path.join(os.getcwd(),"assets","easynouns.csv") #to ensure it works on all operating systems
easyNouns=parsing.csvNounsToList(easyNounsPath)
medNounsPath = os.path.join(os.getcwd(),"assets","mednouns.csv") #to ensure it works on all operating systems
medNouns=parsing.csvNounsToList(medNounsPath)
hardNounsPath = os.path.join(os.getcwd(),"assets","mednouns.csv") #to ensure it works on all operating systems
hardNouns=parsing.csvNounsToList(hardNounsPath)
drawingNouns=[easyNouns,medNouns,hardNouns]

def main():
    #INITALIZATIONS
    drawing=True
    timerActive=False
    imageSent=False
    finishEarly=False
    roundTime=30
    targetWord,difficulty=getNewWord(drawingNouns)
    sec=roundTime
    pen_color = BLACK
    eraser_size = 1
    num = 0
    score = 0
    pos_list = []
    round = 1
    clock = pygame.time.Clock()
    running = True
    menu_state = "main"

    while running: 
        #Tracks whether an event happens
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    finishEarly=True
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_RETURN:
                    menu_state = "game"
                if event.key == pygame.K_e:
                    num += 1
                    if num % 2 == 1:
                        pen_color = WHITE
                        eraser_size = 3
                    else:
                        pen_color = BLACK
                        eraser_size = 1
        #Main Menu Setup
        if menu_state == "main": 
            screen.blit(bg_img)
            label_text(f"ART-ti-ficial", title_font, (0,0,0), 250, 40)
            label_text(f"press enter to begin", text_font, (0,0,0), 310, 450)
            pygame.display.flip()
            clearAll(screen)
        #Game Meny Setup
        elif menu_state == "game":
            if imageSent==True:
                targetWord,difficulty=getNewWord(drawingNouns)
                round+=1
                drawing=True
                timerActive=False
                imageSent=False
            #Labels Display Setup
            label_text(f"Score: {score}", text_font, (0,0,0), 10, 10)
            label_text(f"Round: {round}", text_font, (0,0,0), 750, 10)
            label_text(f"Timer: {sec}", text_font, (0,0,0), 380, 10)
            label_text(f"Draw: {targetWord} ({difficulty})", text_font, (0,0,0),320,550)
            if drawing and not timerActive:
                startTime = time.time()
                timerActive=True
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
                    path=imageProcessing.imgData2Png(surface_array[0:999,61:938])
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
                    time.sleep(6)
                    clearAll(screen)
                    pygame.display.flip()
                    imageSent=True
            elif USEAPI==False and not imageSent:
                print("API use is disabled currently.")
                imageSent=True
            else:
                if elasped<30:
                    sec=int(roundTime-elasped)
main()