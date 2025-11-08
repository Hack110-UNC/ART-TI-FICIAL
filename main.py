import numpy
import pygame
import pygame_gui
import random
import time 
import processing as imageProcessing


SCREEN_WIDTH: int = 1000
SCREEN_HEIGHT: int = 600
TICK_RATE: int = 60
BLACK = (0,0,0)
WHITE = (255,255,255)

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
    manager = pygame_gui.UIManager(screen, "styles.json")
    score_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((20,20), (100,50)), text=f"Score: {score}", manager=manager, object_id="fonts")
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
            manager.process_events(event) #For GUI Manager
        manager.update(time_delta) #For GUI Manager
        if drawing:
            if pygame.mouse.get_pressed()[0]: 
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos not in pos_list:
                    pos_list.append(mouse_pos)
                last_pos = pos_list[len(pos_list)-1]
                second_last_pos = pos_list[len(pos_list)-2]
                pygame.draw.circle(surface=screen, color=BLACK, center=mouse_pos, radius=12)
                pygame.draw.lines(surface=screen, color=BLACK, closed=True, width=30, points=(second_last_pos, last_pos))
            elif pygame.mouse.get_pressed()[0] == False:
                pos_list = []
        manager.draw_ui(screen) #For GUI Manager
        pygame.display.flip()
        # clock.tick(TICK_RATE) Moved: Kept in case of broken function
        endTime = time.time()
        if (endTime-startTime >= 30) or (finishEarly and not imageSent): #30 sec draw time, period over
            drawing=False
            timerActive=False
            surface_array = pygame.surfarray.pixels2d(surface=screen)
            if not imageSent:
                surface_array=surface_array/16777215 #b&w
                path=imageProcessing.imgData2Png(surface_array)
                base64String=imageProcessing.filePath2AIPayload(path)
                AIresponse=imageProcessing.getResposeFromAI(base64String,targetWord)
                print(AIresponse)
                imageSent=True

main()

#----------------TEST STUFF----------------
# class Boulder(pygame.sprite.Sprite):
#     speed: int
#     surf: pygame.Surface
#     rect: pygame.Rect

#     def __init__(self):
#         super(Boulder, self).__init__()

#         self.speed = random.randint(4, 12)
#         self.surf = pygame.image.load("assets/boulder.png").convert()
#         self.rect = self.surf.get_rect(bottomleft = (SCREEN_WIDTH, ))