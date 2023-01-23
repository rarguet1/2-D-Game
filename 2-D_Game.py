import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)

sky_surface = pygame.image.load('graphics/Sky.png').convert() # Convert makes images easier to run for python
ground_surface = pygame.image.load('graphics/ground.png').convert()
text_surface = test_font.render("My game", False, 'Black') # AA = antialiasing, smoothing text

snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha() # Same as convert but also removes alpha values, messy backround stuff
snail_x_pos = 600
snail_y_pos = 300

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface, (0,0)) # Blit = Block image transfer, esesentially putting on surface on another surface
    screen.blit(ground_surface, (0,300))
    screen.blit(text_surface, (300,50))
    snail_x_pos -= 4
    if snail_x_pos < -100:
        snail_x_pos = 800
    screen.blit(snail_surface,(snail_x_pos,250))

    pygame.display.update()
    clock.tick(60)
