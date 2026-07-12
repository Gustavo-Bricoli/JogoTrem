import os
import sys
import time

import pygame

pygame.init()
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Command Prompt")

# 1. Setup Consolas and Command Prompt Colors
FONT_SIZE = 20
font = pygame.font.SysFont("consolas", FONT_SIZE)
LINE_SPACING = FONT_SIZE + 4

# Classic CMD Colors (Green on Black or White on Black)
COLOR_BG = (12, 12, 12)       # True CMD black
COLOR_TEXT = (204, 204, 204)  # Light gray text
COLOR_CURSOR = (204, 204, 204)

COLOR_NAMES = {
    "black": (0, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "cyan": (0, 255, 255),
    "red": (255, 0, 0),
    "magenta": (255, 0, 255),
    "yellow": (255, 255, 0),
    "white": (255, 255, 255),
    "gray": (128, 128, 128),
    "grey": (128, 128, 128),
}

# 2. Terminal State Variables
current_dir = os.path.abspath(".")
current_input = ""
history = [
    "Microsoft Windows [Version 10.0.19045]",
    "(c) Microsoft Corporation. All rights reserved.",
    "",
]

# Cursor blinking variables
cursor_visible = True
last_cursor_toggle = time.time()
scroll_offset = 0


def get_prompt():
    return f"{current_dir}> "


# 3. Command Parser Logic
def process_command(cmd_string):
    global current_dir, COLOR_BG, COLOR_TEXT, COLOR_CURSOR, history

    cmd_string = cmd_string.strip()
    if not cmd_string:
        return []

    parts = cmd_string.split()
    cmd = parts[0].lower()
    args = parts[1:]

    if cmd in {"help", "?"}:
        return [
            "Available commands:",
            "  help        - Show this message",
            "  clear/cls   - Clear the screen",
            "  cd <path>   - Change the current directory",
            "  ls/dir      - List directory contents",
            "  color       - Change terminal colors",
            "  exit        - Close the terminal",
            "  Scroll up with PageUp or mouse wheel",
        ]
    elif cmd in {"clear", "cls"}:
        history = []
        return []
    elif cmd in {"ls", "dir"}:
        try:
            entries = sorted(os.listdir(current_dir))
        except FileNotFoundError:
            return [f"Directory not found: {current_dir}"]

        if not entries:
            return ["<empty>"]

        output = []
        for entry in entries:
            full_path = os.path.join(current_dir, entry)
            if os.path.isdir(full_path):
                output.append(f"[{entry}]")
            else:
                output.append(entry)
        return output
    elif cmd == "cd":
        if not args:
            return [current_dir]

        target = args[0]
        new_path = os.path.abspath(os.path.join(current_dir, target))
        if os.path.isdir(new_path):
            current_dir = new_path
            return []
        return [f"The system cannot find the path specified: {target}"]
    elif cmd == "color":
        if not args:
            return [f"Current colors: fg={COLOR_TEXT}, bg={COLOR_BG}"]

        if len(args) == 1:
            color_name = args[0].lower()
            if color_name in COLOR_NAMES:
                COLOR_TEXT = COLOR_NAMES[color_name]
                COLOR_CURSOR = COLOR_NAMES[color_name]
                return []
            return [f"Unknown color: {args[0]}"]

        fg_name = args[0].lower()
        bg_name = args[1].lower()
        if fg_name not in COLOR_NAMES or bg_name not in COLOR_NAMES:
            return [f"Unknown color pair: {args[0]} {args[1]}"]

        COLOR_TEXT = COLOR_NAMES[fg_name]
        COLOR_CURSOR = COLOR_NAMES[fg_name]
        COLOR_BG = COLOR_NAMES[bg_name]
        return []
    elif cmd == "exit":
        pygame.quit()
        sys.exit()
    else:
        return [
            f"'{cmd_string}' is not recognized as an internal or external command,",
            "operable program or batch file.",
        ]


# Main Loop
clock = pygame.time.Clock()
running = True

while running:
    # 4. Handle Inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.TEXTINPUT:
            current_input += event.text
            scroll_offset = 0

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                current_input = current_input[:-1]
                scroll_offset = 0
            elif event.key == pygame.K_RETURN:
                history.append(get_prompt() + current_input)
                output_lines = process_command(current_input)
                history.extend(output_lines)
                current_input = ""
                scroll_offset = 0
            elif event.key == pygame.K_PAGEUP:
                max_scroll = max(0, len(history) + 1 - (screen.get_height() // LINE_SPACING))
                scroll_offset = min(max_scroll, scroll_offset + 1)
            elif event.key == pygame.K_PAGEDOWN:
                scroll_offset = max(0, scroll_offset - 1)

        elif event.type == pygame.MOUSEWHEEL:
            max_scroll = max(0, len(history) + 1 - (screen.get_height() // LINE_SPACING))
            scroll_offset = max(0, min(max_scroll, scroll_offset + event.y))

    # 5. Handle Cursor Blinking
    if time.time() - last_cursor_toggle > 0.53:  # Windows standard blink rate
        cursor_visible = not cursor_visible
        last_cursor_toggle = time.time()

    # 6. Rendering Logic
    screen.fill(COLOR_BG)
    
    # Compile text lines to render
    all_lines = list(history)
    all_lines.append(get_prompt() + current_input)

    # Only keep lines that fit on the screen (Scroll simulation)
    max_visible_lines = screen.get_height() // LINE_SPACING
    max_scroll = max(0, len(all_lines) - max_visible_lines)
    scroll_offset = min(scroll_offset, max_scroll)
    start_index = max(0, len(all_lines) - max_visible_lines - scroll_offset)
    visible_lines = all_lines[start_index:start_index + max_visible_lines]
    
    # Draw text lines
    for i, line in enumerate(visible_lines):
        y_pos = i * LINE_SPACING + 10
        text_surface = font.render(line, True, COLOR_TEXT)
        screen.blit(text_surface, (10, y_pos))
        
        # Draw the blinking cursor on the very last line
        if i == len(visible_lines) - 1 and cursor_visible:
            # Measure typed text width to place cursor at the end
            text_width = text_surface.get_width()
            cursor_rect = pygame.Rect(10 + text_width, y_pos + 2, 10, FONT_SIZE - 2)
            pygame.draw.rect(screen, COLOR_CURSOR, cursor_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
