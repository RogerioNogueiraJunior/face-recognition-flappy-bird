import cv2
import pygame 
import pygame.display
from pygame.locals import *
import random

import pygame.docs

pygame.init() #start pygame 

largura = 640 #defines pygame's window width
altura = 480 #defines pygame's window height

face_cascade = cv2.CascadeClassifier('OpenCVScript-master\Haarcascade\haarcascade_frontalface_alt.xml') # the face recognition code
webcam = cv2.VideoCapture(0) #starts the webcam
screen = pygame.display.set_mode((largura, altura)) #sets the pygame window size
pygame.display.set_caption("flap bird with your face") #starts the aplication


overlay_image = pygame.image.load('flapybird/bird.png') #bird image

overlay_image = pygame.transform.scale(overlay_image, (100, 80)) # bird's size

pipe_image = pygame.image.load('flapybird\pipe.png') #pipe image
pipe_image = pygame.transform.scale(pipe_image, (120, 2628.8)) #pipe's size
point = [-1,0]
vel = [0, 20] #pipes velocity's array
speed = 0.005  #speed increasing of the pipes
random1 = random.randint(-1150, -900) #set the y value of the pipe hole randomly
point_position = 1

pipes = [(largura, -random1), (largura + 300, random1)] #spawn the first 2 pipes

bird_position_save = [] #saves curent bird's position

running = True #sets a infinite loop

while running:
    vel[1] += speed #adds 0,005 to the velocity for every loop
    screen.fill((0,0,0))
    for event in pygame.event.get(): #close the window when X is pressed
        if event.type == QUIT:
            running = False
                
    validation, frame = webcam.read() #transforms the webcam's pictures in video
    if not validation:
        continue

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #transforms video to gray scale for better reading
    face = face_cascade.detectMultiScale(frame_gray, minNeighbors=5) #recognizes the face

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)#changes the BGR image from opencv to RGB so it can be read by pygame

    frame_surface = pygame.surfarray.make_surface(frame)#puts the video on the background
    frame_surface = pygame.transform.rotate(frame_surface, 90) #makes shure that is not up side down
    frame_surface = pygame.transform.flip(frame_surface, False, True) 
    screen.blit(frame_surface, (0,0))

    random1 = random.randint(-1150, -900) #sets randonmness to the next pipe's Y

    for i, (x,y) in enumerate(pipes):
        pipe_colision = pygame.Rect((x, y, 120, 3628.8)) #bird's death colision
        pipe_point = pygame.Rect((x, y + 1220, 120, 50.2)) #point colision
        screen.blit(pipe_image, (x, y)) #shows pipe image on screen
        pipes[i] = (x - vel[1], y) #makes pipes go left
        if len(face) == 0 and len(vel) < 3: #sets pipe velocity to 0 if the face is not being recognized
            speed = 0
            pipes[i] = (x - vel[0], y) 

    if pipes and pipes[0][0] < -200: #kills the last pipe and makes another one on the pipes array
        pipes.pop(0)
        pipes.append((largura, random1))

    if len(face) == 1: #if face is being recognized
        for i in face: 
            if len(bird_position_save) < 2: #only saves the last 2 positions
                bird_position_save.append(face) 
                cleaned_data = [arr.tolist()[0] for arr in bird_position_save] #removes unessesary data from the array
                if cleaned_data :
                    for x,y,w,h in cleaned_data:
                        #saves the position values form the face on saparate variables so they can be recalled later
                        x1 = x
                        y1 = y
                        w1 = w
                        h1 = h
                        #makes the bird and it colision follow the face
                        bird_colision = pygame.Rect((x1, y1 + h1 - overlay_image.get_height()/1.5, 100, 20))
                        screen.blit(overlay_image, (x1, y1 + h1 - overlay_image.get_height()))
                       
                if len(bird_position_save) == 1:
                    bird_position_save.pop(0)

    # the bird and it colision will stay in place 
    # based on the last faces position that was recorded on the "bird_position_save" array
    bird_colision = pygame.Rect((x1, y1 + h1 - overlay_image.get_height()/1.5, 100, 20))
    screen.blit(overlay_image, (x1, y1 + h1 - overlay_image.get_height()))
    
    # colision sistem
    colision_death = bird_colision.colliderect(pipe_colision)
    colision_point = bird_colision.colliderect(pipe_point)
    if colision_death and not colision_point:
        running = False
    # Atualiza a tela
    pygame.display.update()

webcam.release()
cv2.destroyAllWindows()