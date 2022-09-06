import pygame
import random

# Inicializace hry
pygame.init()

# obrazovka
width = 1000
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tom and Jerry GAME")

# Nastavení hry
player_start_lives = 5  # měníme v průbehu hry
player_speed = 5  # neměníme
mouse_speed = 5  # měníme
mouse_speed_acceleration = 0.5  # neměníme
mouse_behind_border = 100  #neměníme
score = 0  # měníme

player_lives = player_start_lives  # měníme
mouse_curent_speed = mouse_speed

#FPS a hodiny
fps = 60
clock = pygame.time.Clock()

# barvy
dark_yellow = pygame.Color("#938f0c")
black = (0,0,0)
white = (255, 255, 255)
red = (255, 0, 0)
green = ( 0, 255, 0)
blue = (0, 0, 255)

# fonty
game_font_big = pygame.font.Font("fonts/mujfont.ttf", 50)
game_font_middle = pygame.font.Font("fonts/mujfont.ttf", 35)


# text
game_name = game_font_big.render("Tom and Jerry Game", True, dark_yellow)
game_name_rect = game_name.get_rect()
game_name_rect.center = (width//2, 30)

game_over_text = game_font_big.render("Hra skoncila.", True, dark_yellow)
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (width//2, height//2)

continue_text = game_font_middle.render("Chces hrat znovu? Stiskni libovolnou klavesu", True, dark_yellow)
continue_text_rect = continue_text.get_rect()
continue_text_rect.center = (width//2, height//2 + 40)

# zvuky a hudba v pozadí, -1 nekonečno
pygame.mixer.music.load("music/bgmusic.wav")
pygame.mixer.music.play(-1, 0.0)
loose_life_sound = pygame.mixer.Sound("music/boom.wav")
#loose_life_sound.set_volume(0.1)
catch_mouse_sound = pygame.mixer.Sound("music/zap.wav")
#catch_mouse_sound.set_volume(0.1)


# obrázky
cat_image = pygame.image.load("img/cat-icon.png")
cat_image_rect = cat_image.get_rect()
cat_image_rect.center = (60, height//2)

mouse_image = pygame.image.load("img/mouse.png")
mouse_image_rect = mouse_image.get_rect()
mouse_image_rect.x = width + mouse_behind_border  # left
mouse_image_rect.y = random.randint(60, height-48)   # top


# Hlavní cyklus
lets_continue = True

while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False

    # pohyb klavesami
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and cat_image_rect.top > 60:
        cat_image_rect.y -= player_speed
    elif keys[pygame.K_DOWN] and cat_image_rect.bottom < height:
        cat_image_rect.y += player_speed

    # pohyb mouse
    if mouse_image_rect.x < 0:
       player_lives -= 1
       mouse_image_rect.x = width + mouse_behind_border
       mouse_image_rect.y = random.randint(60, height - 48)
       loose_life_sound.play()
    else:
        mouse_image_rect.x -= mouse_curent_speed

    # kontrola kolize
    if cat_image_rect.colliderect(mouse_image_rect):
        score += 1
        mouse_curent_speed += mouse_speed_acceleration
        mouse_image_rect.x = width + mouse_behind_border
        mouse_image_rect.y = random.randint(60, height - 48)
        catch_mouse_sound.play()

    # znovu vykresleni obrazovky
    screen.fill(black)

    # tvary
    pygame.draw.line(screen, dark_yellow, (0, 60), (width, 60), 2)

    # Nastavení textů
    lives_text = game_font_middle.render(f"Lives: {player_lives}", True, dark_yellow)
    lives_text_rect = lives_text.get_rect()
    lives_text_rect.right = width - 20
    lives_text_rect.top = 15

    score_text = game_font_middle.render(f"Skore: {score}", True, dark_yellow)
    score_text_rect = score_text.get_rect()
    score_text_rect.left = 20
    score_text_rect.top = 15

    # texty, zobrazení
    screen.blit(game_name, game_name_rect)
    screen.blit(score_text, score_text_rect)
    screen.blit(lives_text, lives_text_rect)

    # obrazky
    screen.blit(cat_image, cat_image_rect)
    screen.blit(mouse_image, mouse_image_rect)

    # kontrola konce hry, UPDATE !!!!!
    if player_lives == 0:
        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(continue_text, continue_text_rect)
        pygame.display.update()
        pygame.mixer.music.stop()

        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = player_start_lives
                    mouse_curent_speed = mouse_speed
                    cat_image_rect.y = height//2
                    pause = False
                    pygame.mixer.music.play(-1, 0.0)
                elif event.type == pygame.QUIT:
                    pause = False
                    lets_continue = False




    #update
    pygame.display.update()

    # zpomalení cyklu - tikání hodin
    clock.tick(fps)








# ukončení hry
pygame.quit()