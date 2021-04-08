import pygame
import sys
import random
import math

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

    top_rect = top_pipe.get_rect().copy()
    top_rect.bottom = bottom_rect.top - 200
    top_rect.x = bottom_rect.x

    return (bottom_rect, top_rect)

pipe_rects = [generate_pipes()]

# start, playing, dead
state = "start"

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()

    acceleration.y = 0.5
    
    if keys[pygame.K_SPACE]:
        if state == "start":
            state = "playing"  
        elif state == "playing":
            acceleration.y = -0.5
        elif state == "dead":
            frankie_rect.center = pygame.math.Vector2(60,300)
            acceleration = pygame.math.Vector2(0,0)
            velocity = pygame.math.Vector2(0,0)
            pipe_rects = [generate_pipes()]
            state = "start"
    
    if state == "playing":
        velocity += acceleration
        frankie_rect = frankie_rect.move(velocity)
        for bottom_rect, top_rect in pipe_rects:
            bottom_rect.x -= 2
            top_rect.x -= 2
            bottom_rect.top = height/2 + 100*math.sin(pygame.time.get_ticks()/1000)
            top_rect.bottom = bottom_rect.top - 200
            if frankie_rect.colliderect(bottom_rect) or frankie_rect.colliderect(top_rect):
                state = "dead"
        if pipe_rects[-1][0].centerx <= width/2:
            pipe_rects.append(generate_pipes())
        

    screen.fill((0,0,0))

    screen.blit(frankie, frankie_rect)

    for bottom_rect, top_rect in pipe_rects:
        screen.blit(bottom_pipe, bottom_rect)
        screen.blit(top_pipe, top_rect)
    pygame.display.flip()
    