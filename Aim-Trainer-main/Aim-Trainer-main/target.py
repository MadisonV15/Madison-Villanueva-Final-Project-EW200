from constants import *
import random
import math

class Target(object):
    def __init__(self, speed, radius):
        self.speed = speed 
        self.radius = radius
        self.pressed = False  
        self.x = random.randint(TARGET_RADIUS*2, WIDTH-TARGET_RADIUS*2)
        self.y = random.randint(TARGET_RADIUS*2, HEIGHT-TARGET_RADIUS*2)
    
    def shrink(self, targets):
        self.radius -= self.speed
        if self.radius <= 15:
            targets.remove(self)

    def draw(self):
        if not self.pressed:
            pygame.draw.circle(WIN, TARGET_COLOR, (self.x, self.y), self.radius)
            pygame.draw.circle(WIN, BACKGROUND_COLOR, (self.x, self.y), self.radius-RING_WIDTH)
            pygame.draw.circle(WIN, PRESSED_COLOR, (self.x, self.y), 20)
        else:
            pygame.draw.circle(WIN, PRESSED_COLOR, (self.x, self.y), self.radius)
            pygame.draw.circle(WIN, BACKGROUND_COLOR, (self.x, self.y), self.radius-RING_WIDTH)
    
    def isOver(self, pos):
        height = abs(pos[1]-self.y)
        base = abs(pos[0]-self.x)
        if (math.sqrt((height**2)+(base**2)) < 20) and not self.pressed:
            return True