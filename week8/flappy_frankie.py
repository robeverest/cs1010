import pygame
import sys
import random

pygame.init()

width = 800
height = 600

screen = pygame.display.set_mode((width, height))

frankie = pygame.image.load('week8/foxr.gif')
frankie_rect = frankie.get_rect()

bottom_pipe = pygame.image.load('week8/bp.png')
top_pipe = pygame.image.load('week8/tp.png')

frankie = pygame.transform.rotozoom(frankie, 0, 4)
frankie_rect.center = pygame.math.Vector2(60,300)
frankie_rect.width = frankie_rect.width*4
frankie_rect.height = frankie_rect.height*4

acceleration = pygame.math.Vector2(0,0)
velocity = pygame.math.Vector2(0,0)

clock = pygame.time.Clock()

# Pipes
def generate_pipes():
    bottom_rect = bottom_pipe.get_rect().copy()
    bottom_rect.bottom = height + random.randint(0, 300)
    bottom_rect.x = width + random.randint(0, 30)

    return bottom_rect

pipe_rects = [generate_pipes()]

# start, playing, dead
state = "start"

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()

    acceleration.y = 1
    
    if keys[pygame.K_SPACE]:
        if state == "start":
            state = "playing"  
        elif state == "playing":
            acceleration.y = -1
        elif state == "dead":
            frankie_rect.center = pygame.math.Vector2(60,300)
            acceleration = pygame.math.Vector2(0,0)
            velocity = pygame.math.Vector2(0,0)
            pipe_rects = [generate_pipes()]
            state = "start"
    
    if state == "playing":
        velocity += acceleration
        frankie_rect = frankie_rect.move(velocity)
        for pipe in pipe_rects:
            pipe.x -= 1
            if frankie_rect.colliderect(pipe):
                state = "dead"
        if pipe_rects[-1].centerx <= width/2:
            pipe_rects.append(generate_pipes())
        

    screen.fill((0,0,0))

    screen.blit(frankie, frankie_rect)

    for pipe in pipe_rects:
        screen.blit(bottom_pipe, pipe)
    pygame.display.flip()
    