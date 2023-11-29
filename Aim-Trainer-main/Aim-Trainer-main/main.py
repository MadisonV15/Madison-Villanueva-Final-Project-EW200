import pygame
import target as t
import score as s
from constants import *

pygame.init()

# SOUNDS
sandstorm = pygame.mixer.Sound("../assets/sandstorm.mp3")
pygame.mixer.Sound.play(sandstorm)
blaster = pygame.mixer.Sound("../assets/blaster.mp3")
scream = pygame.mixer.Sound("../assets/scream.mp3")

# OBJECTS
targets = [t.Target(SPEED, TARGET_RADIUS)]
score = s.Score()
SPEED = 0.3

def reset_game():
    targets.clear()
    targets.append(t.Target(SPEED, TARGET_RADIUS))
    score.score = 0

def draw_main_menu():
    # Draw the main menu on the screen
    menu_text = font.render("Main Menu", True, WHITE)
    start_text = font.render("Press Enter to Start", True, WHITE)
    restart_text = font.render("Press R to Restart", True, WHITE)
    WIN.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 - 50))
    WIN.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
    WIN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.update()

def handle_main_menu_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return True
            if event.key == pygame.K_r:
                reset_game()
                return True
    return False

def handle_target_clicks(pos):
    global SPEED
    for target in targets:
        if target.isOver(pos):
            target.pressed = True
            SPEED += ACCELERATION
            targets.append(t.Target(SPEED, TARGET_RADIUS))
            score.increase()
            pygame.mixer.Sound.play(blaster)
        SPEED = max(SPEED, 0.3)


def draw_targets():
    for target in targets:
        target.draw()

def shrink_targets():
    SPEED = 0.3
    for target in targets:
        if not target.pressed:
            target.shrink(targets)
        else:
            SPEED -= ACCELERATION

def draw_back():
    WIN.blit(BACKGROUND_IMAGE, (0,0))
    draw_targets()
    score.draw()
    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    in_main_menu = True

    while run:
        clock.tick(60)

        if in_main_menu:
            draw_main_menu()
            in_main_menu = not handle_main_menu_input()
            continue

        shrink_targets()
        draw_back()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_target_clicks(pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Restart the game
                    reset_game()

    pygame.quit()  # Move pygame.quit() here

main()
