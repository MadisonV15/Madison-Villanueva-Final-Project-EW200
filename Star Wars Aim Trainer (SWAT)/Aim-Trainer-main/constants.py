import pygame

pygame.font.init()

# CONSTANTS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (255, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 232, 31)
GREEN = (47, 249, 36)
BLUE = (46,103,248)

WIDTH = 1300
HEIGHT = 750
WIN = pygame.display.set_mode()
pygame.display.set_caption("Target Practice")
BACKGROUND_COLOR = BLACK
TARGET_RADIUS = 75
RING_WIDTH = 5
SPEED = 0.25
ACCELERATION = 0.0175
PRESSED_SPEED = 1

font = pygame.font.SysFont("Comicsans", 50)

BACKGROUND_IMAGE = pygame.image.load("../assets/space.jpg")
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

TARGET_COLOR = GREEN
PRESSED_COLOR = BLUE
