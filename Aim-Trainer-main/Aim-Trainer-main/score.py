from constants import *

class Score(object):
    def __init__(self):
        self.score = 0

    def increase(self):
        self.score += 1
    
    def draw(self):
        score = font.render(str(self.score), 1, WHITE)
        WIN.blit(score, (0, 0))
