from constants import *

class Score(object):
    def __init__(self):
        self.score = 0

    def increase(self):
        self.score += 1
    
    def draw(self):
        score = font.render(str(self.score), 1, WHITE)
        restart1 = font.render(str("Press r to restart"), 1, WHITE)
        WIN.blit(score, (25, 25))
        WIN.blit (restart1, (850, 650))
