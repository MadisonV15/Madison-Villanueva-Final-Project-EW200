from constants import *

class Score(object):
    def __init__(self):
        self.score = 0

    def increase(self):
        self.score += 1
    
    def draw(self):
        score = font.render(str(self.score), 1, WHITE)
        restart1 = font.render(str("Press r to restart"), 1, WHITE)
        # high_score_text = font.render("High Score: " + str(high_score), True, RED)
        WIN.blit(score, (50, 25))
        WIN.blit (restart1, (850, 650))
        # WIN.blit(high_score_text,
        #          (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 50))  # Display high score
