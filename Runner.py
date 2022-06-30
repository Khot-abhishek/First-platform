import pygame
from sys import exit
from random import randint, choice
from pathlib import Path


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        CWD_PATH = Path().absolute()
        player_walk_1 = pygame.image.load(CWD_PATH / 'graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load(CWD_PATH / 'graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load(CWD_PATH / 'graphics/Player/jump.png').convert_alpha()
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(150, 300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def apply_animation(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.apply_animation()
        

class Obstacles(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        CWD_PATH = Path().absolute()
        
        if type == 'fly':
            fly_1 = pygame.image.load(CWD_PATH / 'graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load(CWD_PATH / 'graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos = 210
            print('added fly ---------------')
            
        else:
            snail_1 = pygame.image.load(CWD_PATH / 'graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load(CWD_PATH / 'graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1,snail_2]
            y_pos = 300
            print('added snail ============')
            
            self.animation_index = 0
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(midbottom=(randint(910,1100),y_pos))
    
    def apply_animation(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
            
    def update(self):
        self.apply_animation()
        self.rect.x -= 5
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
    
    
def display_score():
    current_time = (pygame.time.get_ticks() // 1000) - LAST_SCORE
    score_surface = test_font.render(f'Score:{current_time}',False, 'Black')
    score_rectangle = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface,score_rectangle)
    return current_time 

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True
    

# my_files = Path.cwd()
# x = my_files / 'Runner.py'
# print('cwd:',x)
# print("cwd-absolute:",Path.absolute())
# print("CWD_PATH: ",CWD_PATH)
# p = CWD_PATH / 'font/Pixeltype.ttf'
# print(f"-->{p}") 


pygame.init()

WINDOW_SIZE = (800, 400)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
CWD_PATH = Path().absolute()
test_font = pygame.font.Font(CWD_PATH / 'font\Pixeltype.ttf', 50)
# PLAYER_GRAVITY = -20
GAME_ACTIVE = False
LAST_SCORE = 0
       
enimies = []

## Player & enemy groups
player = pygame.sprite.GroupSingle()
player.add(Player())

# obstacles_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()


sky_surface = pygame.image.load(CWD_PATH / 'graphics\sky.png').convert()
ground_surface = pygame.image.load(CWD_PATH / 'graphics\ground.png').convert()


player_stand = pygame.image.load(CWD_PATH / 'graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rectangle = player_stand.get_rect(center=(400,200))

game_name = test_font.render('Pixel Runner',False,(111,196,169))
game_name_rectangle = game_name.get_rect(center=(400,80))

game_message = test_font.render('Press Space to Run',False,(111,196,169))
game_message_rectangle = game_message.get_rect(center=(400,330))



obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)
  
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if GAME_ACTIVE:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacles(choice(['fly','snail','snail','snail'])))
                print('sprite_added +++++++++++++++++++++')
		

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                GAME_ACTIVE = True
                LAST_SCORE = pygame.time.get_ticks() // 1000
                print('Game restarted')

    if GAME_ACTIVE:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()
        
        print('draw-player')
        player.draw(screen)
        player.update()
        print('draw-enemy')
        
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        print('before collision')
        GAME_ACTIVE = collision_sprite()
        print('after collision')

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rectangle)

        score_message = test_font.render(f'Your Score:{LAST_SCORE}',False,(111,196,169))        
        score_message_rectangle = score_message.get_rect(center=(400,330))
        screen.blit(game_message,game_message_rectangle)

        if LAST_SCORE == 0:
            screen.blit(game_message,game_message_rectangle)
        else:
            screen.blit(score_message,score_message_rectangle)

        print('Dead_here')
    pygame.display.update()
    clock.tick(60)
