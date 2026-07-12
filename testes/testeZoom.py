import pygame
import sys

pygame.init()

# 1. Base Dimensions & Initialization
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Pixel-Perfect Masking Zoom")

FONT_SIZE = 18
font = pygame.font.SysFont("consolas", FONT_SIZE)

COLOR_BG = (12, 12, 12)       
COLOR_FORE = (100, 100, 100)  
COLOR_BACK = (0, 255, 150)    
FLASHLIGHT_RADIUS = 80

# Your original artwork profiles
FOREGROUND_ART = [
    "   /\\   ", 
    "  /  \\  ", 
    " /    \\ ", 
    " \\    / ", 
    "  \\  /  ", 
    "   \\/   "]

BACKGROUND_ART = [
    "       /\\       ", 
    "      /  \\      ",
    "     /    \\     ",
    "    /  /\\  \\    ",
    "   /  /  \\  \\   ", 
    "  /  /    \\  \\  ", 
    " /  /______\\  \\ ", 
    " \\  \\------/  / ",
    "  \\  \\    /  /  ", 
    "   \\  \\  /  /   ", 
    "    \\  \\/  /    ", 
    "     \\    /     ",
    "      \\  /      ", 
    "       \\/       "
]

# 2. Pre-Render Art Layers to Hidden Surfaces
# This draws the text blocks once onto solid digital canvases
def text_to_surface(art_array, text_color):
    char_surf = font.render("#", True, (0,0,0))
    c_w, c_h = char_surf.get_width(), char_surf.get_height()
    
    rows = len(art_array)
    cols = max(len(line) for line in art_array)
    
    surf = pygame.Surface((cols * c_w, rows * c_h), pygame.SRCALPHA)
    for r_idx, line in enumerate(art_array):
        for c_idx, char in enumerate(line):
            if char != " ":
                t_surf = font.render(char, True, text_color)
                surf.blit(t_surf, (c_idx * c_w, r_idx * c_h))
    return surf

# Create raw unscaled textures
fg_texture = text_to_surface(FOREGROUND_ART, COLOR_FORE)
bg_texture = text_to_surface(BACKGROUND_ART, COLOR_BACK)

clock = pygame.time.Clock()
running = True

while running:
    # Handle dynamic resizing cleanly
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Get center window coordinates
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # 3. Create a Mask Layer for the Lens Circle
    # Blends layers via pixel transparencies instead of grid text slots
    mask = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    mask.fill((0, 0, 0, 0)) # Start completely transparent
    pygame.draw.circle(mask, (255, 255, 255, 255), (mouse_x, mouse_y), FLASHLIGHT_RADIUS)

    # 4. Scale surfaces dynamically to match window width/height perfectly
    scaled_fg = pygame.transform.scale(fg_texture, (SCREEN_WIDTH, SCREEN_HEIGHT))
    scaled_bg = pygame.transform.scale(bg_texture, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Apply the circular stencil mask directly onto the background detail layer
    scaled_bg.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    # 5. Composite everything on the display window
    screen.fill(COLOR_BG)
    screen.blit(scaled_fg, (0, 0)) # Base Low-res background
    screen.blit(scaled_bg, (0, 0)) # High-res lens reveal floating over top

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
