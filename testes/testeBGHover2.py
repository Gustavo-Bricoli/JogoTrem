import pygame
import sys
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Flashlight ASCII Reveal")

FONT_SIZE = 20
font = pygame.font.SysFont("consolas", FONT_SIZE)
COLOR_BG = (12, 12, 12)       # Dark CMD Black
COLOR_BRACKET = (60, 60, 60)  # Dim gray for unrevealed brackets
COLOR_SECRET = (255, 255, 255)  # Matrix Green for revealed content

sample_surface = font.render("[]", True, (255, 255, 255))
CHAR_WIDTH = sample_surface.get_width()
CHAR_HEIGHT = sample_surface.get_height()
X_SPACING = CHAR_WIDTH + 2
Y_SPACING = CHAR_HEIGHT

# 1. Define the Hidden Background Layer
# This can be anything: text, code chunks, or ASCII maps
SECRET_BACKGROUND = [
    "╔══════════════════╗",
    "║                  ║",
    "║     ░░░░░░░░     ║",
    "║    ░░░░░░██░░    ║",
    "║    ░▓██████▓░    ║",
    "║    ▓▓▀▀██▀▀▓▓    ║",
    "║    ▓████████▓    ║",
    "║     ▓██████▓     ║",
    "║     ▓██████▓     ║",
    "║      ▀▀▀▀▀▀      ║",
    "║       ████       ║",
    "║   ░▒█▄▀▀▀▀▄█▒░   ║",
    "║ ░░░▒▒█▄  ▄█▒▒░░░ ║",
    "║ ░░░▒▒▒█▌▐█▒▒▒░░░ ║",
    "║ ░░░░▒▒▒  ▒▒▒░░░░ ║",
    "║ ░░░░░░▒  ▒░░░░░░ ║",
    "║ ░░░░░░░▒▒░░░░░░░ ║",
    "║ ░░░░░░░░░░░░░░░░ ║",
    "║ ░░░░░░░░░░░░░░░░ ║",
    "╚══════════════════╝ "
]

def generate_grid(width, height):
    positions = []
    # Convert text buffer into a grid index map
    row_index = 0
    for y in range(10, height, Y_SPACING):
        col_index = 0
        for x in range(10, width, X_SPACING):
            center_x = x + (CHAR_WIDTH // 2)
            center_y = y + (CHAR_HEIGHT // 2)
            
            # Check if this position lines up with our secret text map
            secret_char = " "
            if row_index < len(SECRET_BACKGROUND):
                line = SECRET_BACKGROUND[row_index]
                if col_index < len(line):
                    secret_char = line[col_index]
                    
            positions.append((x, y, center_x, center_y, secret_char))
            col_index += 1
        row_index += 1
    return positions

grid_positions = generate_grid(SCREEN_WIDTH, SCREEN_HEIGHT)
FLASHLIGHT_RADIUS = 100  # Size of your flashlight ring

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            grid_positions = generate_grid(SCREEN_WIDTH, SCREEN_HEIGHT)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.fill(COLOR_BG)

    # 2. Render each block based on mouse proximity
    for x, y, center_x, center_y, secret_char in grid_positions:
        distance = math.sqrt((mouse_x - center_x) ** 2 + (mouse_y - center_y) ** 2)
        
        if distance <= FLASHLIGHT_RADIUS:
            # Inside Flashlight: Reveal the hidden background map element!
            # If the background is empty space, we can draw a dot or leave it empty
            char_to_draw = secret_char if secret_char != " " else " "
            text_surface = font.render(char_to_draw, True, COLOR_SECRET)
        else:
            # Outside Flashlight: Obscure the background with regular brackets
            char_to_draw = "[]"
            text_surface = font.render(char_to_draw, True, COLOR_BRACKET)
            
        screen.blit(text_surface, (x, y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
