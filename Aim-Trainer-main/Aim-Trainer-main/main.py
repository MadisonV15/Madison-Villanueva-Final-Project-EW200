import pygame
import target as t
import score as s
from constants import *

pygame.init()
clock = pygame.time.Clock()

# SOUNDS
sandstorm = pygame.mixer.Sound("../assets/sandstorm.mp3")
pygame.mixer.Sound.play(sandstorm)
blaster = pygame.mixer.Sound("../assets/blaster.mp3")
scream = pygame.mixer.Sound("../assets/scream.mp3")

# OBJECTS
SPEED = 0.3  # Define SPEED before using it in the targets list
targets = [t.Target(SPEED, TARGET_RADIUS)]
score = s.Score()
high_score = 0
elapsed_time = 0  # Add elapsed_time variable

def draw_clock(elapsed_time):
    #global elapsed_time
    # elapsed_time = pygame.time.get_ticks() // 1000
    time_text = font.render("TIME:" + str(elapsed_time), True, WHITE)
    WIN.blit(time_text, (WIDTH - time_text.get_width() - 50, 50))  # Adjust the position as needed

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
            targets.remove(target)  # Remove the clicked target
            targets.append(t.Target(SPEED, TARGET_RADIUS))
            score.increase()
            pygame.mixer.Sound.play(blaster)
    SPEED = max(SPEED, 0.3)  # Move outside the for loop

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

def draw_back(elapsed_time):
    WIN.blit(BACKGROUND_IMAGE, (0,0))
    draw_targets()
    score.draw()
    high_score_text = font.render("High Score: " + str(high_score), True, WHITE)  # Add high score text
    WIN.blit(high_score_text, (50, 100))  # Display high score
    draw_clock(elapsed_time)
    pygame.display.update()


def reset_game():
    global high_score, elapsed_time
    elapsed_time = 0  # Reset elapsed time to 0
    if score.score > high_score:
        high_score = score.score
    targets.clear()
    targets.append(t.Target(SPEED, TARGET_RADIUS))
    score.score = 0

def main():
    run = True
    clock = pygame.time.Clock()
    in_main_menu = True

    while run:
        clock.tick(60)  # Move clock.tick(60) inside the game loop

        if in_main_menu:
            draw_main_menu()
            in_main_menu = not handle_main_menu_input()
            continue
        elapsed_time = pygame.time.get_ticks() // 1000
        shrink_targets()
        draw_back(elapsed_time)
        #

        # Check if all targets have been missed
        if all(target.pressed for target in targets):
            # Game over
            game_over_text = font.render("Game Over", True, RED)
            game_over_text1 = font.render("Press q to quit", True, RED)
            WIN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
            WIN.blit(game_over_text1, (WIDTH // 2 - game_over_text1.get_width() // 2, HEIGHT // 2))
            elapsed_time = 0
            pygame.display.update()
            pygame.time.wait(2000)  # Wait for 2 seconds
            reset_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                handle_target_clicks(pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Restart the game
                    reset_game()
                elif event.key == pygame.K_q:
                    # Quit the game
                    run = False

    pygame.quit()

main()
