import pygame
import sys

pygame.init()

width = 800
height = 600
speed = [1, 1]

screen = pygame.display.set_mode((width, height))

frankie = pygame.image.load('week8/foxr.gif')
frankie_rect = frankie.get_rect()

frankie = pygame.transform.rotozoom(frankie, 0, 4)
frankie_rect.centerx = 400
frankie_rect.centery = 300
frankie_rect.width = frankie_rect.width*4
frankie_rect.height = frankie_rect.height*4

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    screen.fill((0,0,0))
    screen.blit(frankie, frankie_rect)
    pygame.display.flip()

    frankie_rect = frankie_rect.move(speed)
    if frankie_rect.right > width or frankie_rect.left < 0:
        speed[0] = -speed[0]
    if frankie_rect.bottom > height or frankie_rect.top < 0:
        speed[1] = -speed[1]
