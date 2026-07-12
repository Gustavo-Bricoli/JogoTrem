import pygame
import sys
import math

pygame.init()

# 1. Base Dimensions (Initial startup size)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

# Add the RESIZABLE flag here
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Resizable Matrix Grid")

FONT_SIZE = 20
font = pygame.font.SysFont("consolas", FONT_SIZE)
COLOR_BG = (12, 12, 12)       
COLOR_TEXT = (204, 204, 204)  

sample_surface = font.render("[]", True, COLOR_TEXT)
CHAR_WIDTH = sample_surface.get_width()
CHAR_HEIGHT = sample_surface.get_height()
X_SPACING = CHAR_WIDTH + 2
Y_SPACING = CHAR_HEIGHT

# 2. Wrap grid generation in a function so we can regenerate it when resized
def generate_grid(width, height):
    positions = []
    for y in range(10, height, Y_SPACING):
        for x in range(10, width, X_SPACING):
            center_x = x + (CHAR_WIDTH // 2)
            center_y = y + (CHAR_HEIGHT // 2)
            positions.append((x, y, center_x, center_y))
    return positions

# Initial grid generation
grid_positions = generate_grid(SCREEN_WIDTH, SCREEN_HEIGHT)
HOVER_RADIUS = 80  

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # 3. Listen for the window resize event
        elif event.type == pygame.VIDEORESIZE:
            # Update the screen size to the user's dragged dimensions
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            
            # Recalculate grid positions so brackets fill the new space
            grid_positions = generate_grid(SCREEN_WIDTH, SCREEN_HEIGHT)
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.fill(COLOR_BG)

    for x, y, center_x, center_y in grid_positions:
        distance = math.sqrt((mouse_x - center_x) ** 2 + (mouse_y - center_y) ** 2)
        
        if distance <= HOVER_RADIUS:
            char_to_draw = ":"
        else:
            char_to_draw = "[]"
            
        text_surface = font.render(char_to_draw, True, COLOR_TEXT)
        screen.blit(text_surface, (x, y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
