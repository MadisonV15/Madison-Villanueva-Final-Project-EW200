import pygame
import target as t
import score as s
from constants import *
import pickle
import os

pygame.init()
clock = pygame.time.Clock()

# SOUNDS
sandstorm = pygame.mixer.Sound("../assets/sandstorm.mp3")
pygame.mixer.Sound.play(sandstorm)
blaster = pygame.mixer.Sound("../assets/blaster.mp3")
scream = pygame.mixer.Sound("../assets/scream.mp3")

# OBJECTS
targets = [t.Target(SPEED, TARGET_RADIUS)]
score = s.Score()
high_score = 0
start_time = 0
speed_increase_timer = 0

def save_game():
    print("Saving game...")
    game_state = {
        'targets': targets,
        'score': score.score,
        'high_score': high_score,
        'start_time': start_time
    }
    directory = 'saved_games'
    if not os.path.isdir(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, 'game_state.pickle')
    if os.access(file_path, os.W_OK):
        with open(file_path, 'wb') as file:
            pickle.dump(game_state, file)
    else:
        print("Unable to save game state. Check file permissions.")

def load_game():
    print("Loading game...")
    global targets, score, high_score, start_time
    file_path = os.path.join('saved_games', 'game_state.pickle')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            game_state = pickle.load(file)
        targets = game_state['targets']
        score.score = game_state['score']
        high_score = game_state['high_score']
        start_time = game_state['start_time']
    else:
        # Handle the case where the file is not found
        print("Game state file not found. Starting a new game.")
        targets = [t.Target(SPEED, TARGET_RADIUS)]
        score = s.Score()
        high_score = 0
        start_time = 0

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
            if event.key == pygame.K_RETURN:
                if not load_game():
                    start_game()
                return True
            if event.key == pygame.K_r:
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
    global speed_increase_timer  # Mark the variable as global

    run = True
    in_main_menu = True
    global SPEED

    while run:
        clock.tick(60)
        speed_increase_timer += clock.get_time()

        if speed_increase_timer >= 10000:
            SPEED += 0.25
            speed_increase_timer = 0

        if speed_increase_timer >= 20000:
            SPEED += 0.25
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
