import pygame
from sys import exit


def display_score():
    current_time = (pygame.time.get_ticks() - LAST_SCORE) // 1000
    score_surface = test_font.render(
        f'Score :{current_time}', False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(midbottom=(400, 50))
    screen.blit(score_surface, score_rectangle)


pygame.init()
# global Constants
WINDOW_SIZE = (800, 400)
CWD_PATH = 'I:\program\p_devlopment\python\creating game\Development\First-platform'
PLAYER_SCORE = 0
PLAYER_GRAVITY = -20
GAME_ACTIVE = True
LAST_SCORE = 0
FINAL_SCORE = 0

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
#
sky_surface = pygame.image.load(CWD_PATH + '\graphics\sky.png').convert()
ground_surface = pygame.image.load(CWD_PATH + '\graphics\ground.png').convert()

test_font = pygame.font.Font(CWD_PATH + '/font/Pixeltype.ttf', 50)


snail_surface = pygame.image.load(
    CWD_PATH + '/graphics/snail/snail1.png').convert_alpha()
snail_rectangle = snail_surface.get_rect(midbottom=(500, 300))

player_surface = pygame.image.load(
    CWD_PATH + '/graphics/Player/player_stand.png').convert_alpha()
player_rectangle = player_surface.get_rect(midbottom=(50, 300))

dp_player = pygame.image.load(
    CWD_PATH + '/graphics/Player/player_stand.png').convert_alpha()
dp_player_rectangle = dp_player.get_rect(center=(400, 200))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if GAME_ACTIVE:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 300:
                    PLAYER_GRAVITY = -20

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rectangle.collidepoint(event.pos) and player_rectangle.bottom >= 300:
                    PLAYER_GRAVITY = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                GAME_ACTIVE = True
                snail_rectangle.x = 850
                LAST_SCORE = pygame.time.get_ticks()

    if GAME_ACTIVE:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        # pygame.draw.rect(screen, '#c0e8ec', score_rectangle)
        # pygame.draw.rect(screen, '#c0e8ec', score_rectangle, 10)
        # screen.blit(score_surface, score_rectangle)
        display_score()

        screen.blit(snail_surface, snail_rectangle)
        snail_rectangle.x -= 5
        if snail_rectangle.right < 0:
            snail_rectangle.left = 810

        PLAYER_GRAVITY += 1
        player_rectangle.y += PLAYER_GRAVITY
        if player_rectangle.bottom >= 300:
            player_rectangle.bottom = 300
        screen.blit(player_surface, player_rectangle)

        # if player_rectangle.colliderect(snail_rectangle):
        #     print('player died')

        if snail_rectangle.colliderect(player_rectangle):
            GAME_ACTIVE = False
            FINAL_SCORE = (pygame.time.get_ticks() - LAST_SCORE) // 1000

    else:
        screen.fill((64, 64, 64))
        screen.blit(dp_player, dp_player_rectangle)
        # score = (pygame.time.get_ticks() - LAST_SCORE) // 1000
        dp_score_surface = test_font.render(
            f"Your Score:{FINAL_SCORE} \n Press Space-Bar to Play Again.", False, (64, 64, 64))
        dp_score_rectangle = dp_score_surface.get_rect(center=(400, 50))
        pygame.draw.rect(screen, '#c0e8ec', dp_score_rectangle)
        screen.blit(dp_score_surface, dp_score_rectangle)

    pygame.display.update()
    clock.tick(60)
