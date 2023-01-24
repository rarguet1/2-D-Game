import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.transform.rotozoom(pygame.image.load('graphics/player/player_walk_1.png').convert_alpha(),0,2.5)
        player_walk_2 = pygame.transform.rotozoom(pygame.image.load('graphics/player/player_walk_2.png').convert_alpha(),0,2.5)
        player_walk_3 = pygame.transform.rotozoom(pygame.image.load('graphics/player/player_walk_3.png').convert_alpha(),0,2.5)
        player_walk_4 = pygame.transform.rotozoom(pygame.image.load('graphics/player/player_walk_4.png').convert_alpha(),0,2.5)
        player_walk_5 = pygame.transform.rotozoom(pygame.image.load('graphics/player/player_walk_5.png').convert_alpha(),0,2.5)
        player_walk_6 = pygame.transform.rotozoom(pygame.image.load('graphics/player/player_walk_6.png').convert_alpha(),0,2.5)
        player_walk_7 = pygame.transform.rotozoom(pygame.image.load('graphics/player/player_walk_7.png').convert_alpha(),0,2.5)

        self.player_walk = [player_walk_1,player_walk_2, player_walk_3, player_walk_4, player_walk_5, player_walk_6, player_walk_7]
        self.player_index = 0
        self.player_jump = pygame.transform.rotozoom(pygame.image.load('graphics/player/jump.png').convert_alpha(),0,2.5)


        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/audio_jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300: 
            self.image = self.player_jump
        else:
            self.player_index += 0.2
            if self.player_index >= len(self.player_walk):self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'bird':
            bird1 = pygame.transform.rotozoom(pygame.image.load('graphics/Bird/bird1.png').convert_alpha(),0,2.5)
            bird2 = pygame.transform.rotozoom(pygame.image.load('graphics/Bird/bird2.png').convert_alpha(),0,2.5)
            bird3 = pygame.transform.rotozoom(pygame.image.load('graphics/Bird/bird3.png').convert_alpha(),0,2.5)
            bird4 = pygame.transform.rotozoom(pygame.image.load('graphics/Bird/bird4.png').convert_alpha(),0,2.5)
            self.frames = [bird1, bird2, bird3, bird4]
            y_pos = 210
        else:
            snake1 = pygame.transform.rotozoom(pygame.image.load('graphics/Snake/snake1.png').convert_alpha(),0,2.5)
            snake2 = pygame.transform.rotozoom(pygame.image.load('graphics/Snake/snake2.png').convert_alpha(),0,2.5)
            snake3 = pygame.transform.rotozoom(pygame.image.load('graphics/Snake/snake3.png').convert_alpha(),0,2.5)
            snake4 = pygame.transform.rotozoom(pygame.image.load('graphics/Snake/snake4.png').convert_alpha(),0,2.5)

            self.frames = [snake1,snake2,snake3,snake4]
            y_pos  = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1 
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100: 
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True


pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Intro screen
player_stand = pygame.transform.rotozoom(pygame.image.load('graphics/player/player_stand.png').convert_alpha(),0,3)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Foxy Run',False,(0,0,0))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to run',False,(0,0,0))
game_message_rect = game_message.get_rect(center = (400,330))

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['bird','Snake','Snake','Snake'])))
        
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)


    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = display_score()
        
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()
        
    else:
        screen.fill("#005e6a")
        screen.blit(player_stand,player_stand_rect)

        score_message = test_font.render(f'Your score: {score}',False,(0,0,0))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name,game_name_rect)

        if score == 0: screen.blit(game_message,game_message_rect)
        else: screen.blit(score_message,score_message_rect)

    pygame.display.update()
    clock.tick(60)