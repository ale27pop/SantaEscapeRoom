import pygame
import sys
from config import screen, font, SCREEN_WIDTH, SCREEN_HEIGHT
from constants import COLORS


def instructions_screen():
    """
    Displays instructions and starts the game upon pressing Enter.
    """
    instructions_text = [
        "Welcome to Santa's Escape Room!",
        "",
        "Instructions:",
        "1. Use arrow keys to navigate the grid.",
        "2. Press Enter to let Santa solve automatically.",
        "3. Avoid the Grinch, he moves too!",
        "4. Collect all presents before exiting.",
        "5. Avoid obstacles- uncovered steps.",
        "",
        "Press Enter to start the game.",
    ]

    instructions_running = True
    while instructions_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                instructions_running = False
                from main import start_game  # Import and call start_game to start the game
                start_game()

        screen.fill(COLORS["background"])
        title = font.render("Instructions", True, COLORS["black"])
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        # Display each line of instructions
        for i, line in enumerate(instructions_text):
            text = font.render(line, True, COLORS["black"])
            screen.blit(text, (50, 150 + i * 40))

        pygame.display.flip()
