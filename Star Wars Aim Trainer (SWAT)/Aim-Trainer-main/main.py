import pygame
import target as t
import score as s
from constants import *
import os

pygame.init()
clock = pygame.time.Clock()

# SOUNDS
sandstorm = pygame.mixer.Sound("../assets/trap.mp3")
pygame.mixer.Sound.play(sandstorm)
blaster = pygame.mixer.Sound("../assets/blaster.mp3")
scream = pygame.mixer.Sound("../assets/scream.mp3")

# OBJECTS
targets = [t.Target(SPEED, TARGET_RADIUS)]
score = s.Score()
high_score = 0
start_time = 0
speed_increase_timer = 0

def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def draw_clock():
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    time_text = font.render("TIME:" + str(elapsed_time), True, WHITE)
    WIN.blit(time_text, (WIDTH - time_text.get_width() - 50, 50))

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
            if event.key == pygame.K_l:
                start_game()
                return True
            if event.key == pygame.K_RETURN:
                reset_game()
                return True
    return False

def handle_target_clicks(pos):
    for target in targets:
        if target.isOver(pos):
            target.pressed = True
            targets.remove(target)  # Remove the clicked target
            targets.append(t.Target(SPEED, TARGET_RADIUS))
            score.increase()
            pygame.mixer.Sound.play(blaster)

def draw_targets():
    for target in targets:
        target.draw()

def shrink_targets():
    for target in targets:
        if not target.pressed:
            target.shrink(targets)

def draw_back():
    WIN.blit(BACKGROUND_IMAGE, (0,0))
    draw_targets()
    score.draw()
    high_score_text = font.render("High Score: " + str(high_score), True, WHITE)
    WIN.blit(high_score_text, (50, 100))
    draw_clock()
    pygame.display.update()

def reset_game():
    global high_score, start_time
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    if score.score > high_score:
        high_score = score.score
        save_high_score(high_score)
    targets.clear()
    targets.append(t.Target(SPEED, TARGET_RADIUS))
    score.score = 0
    reset_clock()

def reset_clock():
    global start_time
    start_time = pygame.time.get_ticks()

def start_game():
    global start_time
    start_time = pygame.time.get_ticks()

def main():
    global speed_increase_timer, high_score  # Mark the variables as global

    run = True
    in_main_menu = True
    global SPEED

    high_score = load_high_score()  # Load the high score from file

    while run:
        clock.tick(60)
        speed_increase_timer += clock.get_time()

        if speed_increase_timer >= 10000:
            SPEED += 0.15
            speed_increase_timer = 0

        if speed_increase_timer >= 20000:
            SPEED += 0.15
            speed_increase_timer = 0

        if in_main_menu:
            draw_main_menu()
            in_main_menu = not handle_main_menu_input()
            continue

        elapsed_time = pygame.time.get_ticks() // 1000
        shrink_targets()
        draw_back()

        if all(target.pressed for target in targets):
            pygame.mixer.Sound.play(scream)
            game_over_text = font.render("Game Over", True, RED)
            game_over_text1 = font.render("Press q to quit", True, RED)
            WIN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
            WIN.blit(game_over_text1, (WIDTH // 2 - game_over_text1.get_width() // 2, HEIGHT // 2))
            elapsed_time = 0
            pygame.display.update()
            pygame.time.wait(2000)
            reset_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_target_clicks(pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_q:
                    run = False

    pygame.quit()

main()
