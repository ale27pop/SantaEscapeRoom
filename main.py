import pygame
import sys
import random
from config import screen, font, SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, GRID_ROWS, GRID_COLS, STATUS_HEIGHT, LEGEND_WIDTH
from constants import COLORS, ELEMENT_COLORS
from game_logic import validate_move, santa_move, grinch_move, check_collision, ai_decision
from grid import load_assets, draw_grid, draw_legend, clear_clues


def draw_status_section(feedback_message, collected_presents):
    """
    Draws the status section at the bottom of the screen.
    Displays the feedback message and presents collected.
    """
    status_y = SCREEN_HEIGHT - STATUS_HEIGHT
    pygame.draw.rect(screen, COLORS["background"], (0, status_y, SCREEN_WIDTH, STATUS_HEIGHT))

    # Feedback message
    feedback_text = font.render(feedback_message, True, ELEMENT_COLORS["exit"])
    screen.blit(feedback_text, (20, status_y + 20))

    # Presents collected
    presents_text = font.render(f"Presents collected: {collected_presents}", True, ELEMENT_COLORS["present"])
    screen.blit(presents_text, (20, status_y + 60))


def main_menu():
    """
    Main menu for the game.
    """
    menu_options = ["Start Game", "Instructions", "Exit"]
    selected_option = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        start_game()
                    elif selected_option == 1:
                        show_instructions()
                    elif selected_option == 2:
                        pygame.quit()
                        sys.exit()

        screen.fill(COLORS["background"])
        title = font.render("Santa's Escape Room", True, ELEMENT_COLORS["grinch"])
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        for i, option in enumerate(menu_options):
            color = ELEMENT_COLORS["exit"] if i == selected_option else COLORS["black"]
            menu_text = font.render(option, True, color)
            screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 150 + i * 60))

        pygame.display.flip()


def show_instructions():
    """
    Displays the instructions for the game.
    """
    instructions_running = True
    instructions_text = [
        "1. Use arrow keys to navigate the grid.",
        "2. Avoid the Grinch, he moves too!",
        "3. Collect all presents before exiting.",
        "4. Avoid obstacles (black squares).",
        "5. Solve puzzles (purple squares).",
        "6. Reach the exit (blue square) to win!",
    ]

    while instructions_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                instructions_running = False

        screen.fill(COLORS["background"])
        title = font.render("Instructions", True, COLORS["black"])
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        for i, line in enumerate(instructions_text):
            text = font.render(line, True, COLORS["black"])
            screen.blit(text, (50, 150 + i * 50))

        footer = font.render("Press Enter to return to the menu.", True, ELEMENT_COLORS["exit"])
        screen.blit(footer, (SCREEN_WIDTH // 2 - footer.get_width() // 2, SCREEN_HEIGHT - 100))

        pygame.display.flip()


def start_game():
    """
    Main game loop with enhanced visuals and logic.
    """
    santa_position = [0, 0]
    grinch_position = [random.randint(0, GRID_ROWS - 1), random.randint(0, GRID_COLS - 1)]  # Grinch starts randomly
    exit_point = (GRID_ROWS - 1, GRID_COLS - 1)

    # Ensure Grinch does not start where Santa or the exit point is
    while grinch_position == santa_position or grinch_position == list(exit_point):
        grinch_position = [random.randint(0, GRID_ROWS - 1), random.randint(0, GRID_COLS - 1)]

    obstacles = {(random.randint(0, GRID_ROWS - 1), random.randint(0, GRID_COLS - 1)) for _ in range(15)}
    presents = {(random.randint(0, GRID_ROWS - 1), random.randint(0, GRID_COLS - 1)) for _ in range(5)}
    puzzles = {(random.randint(0, GRID_ROWS - 1), random.randint(0, GRID_COLS - 1)) for _ in range(3)}

    assets = load_assets()
    game_running = True
    feedback_message = "Welcome to Santa's Escape Room!"
    collected_presents = 0
    grinch_last_move = pygame.time.get_ticks()

    while game_running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                direction = ai_decision(santa_position, presents, puzzles, obstacles, exit_point, {})
                new_position = santa_move(santa_position, direction)
                if validate_move(santa_position, new_position, obstacles, {}):
                    santa_position = new_position
                    feedback_message = check_collision(santa_position, grinch_position, presents, puzzles, obstacles, exit_point)
                    if feedback_message == "Present collected!":
                        collected_presents += 1
                        clear_clues(screen, santa_position)

        if current_time - grinch_last_move >= 2000:
            grinch_position = grinch_move(grinch_position, (GRID_ROWS, GRID_COLS), obstacles)
            grinch_last_move = current_time

        if santa_position == grinch_position:
            feedback_message = "Santa was caught by the Grinch! Game Over!"
            game_running = False

        screen.fill(COLORS["background"])

        # Draw sections: game grid, legend, and status
        draw_grid(screen, assets, santa_position, grinch_position, presents, puzzles, obstacles, exit_point)
        draw_legend(screen, font, GRID_COLS * CELL_SIZE + 20, 20)  # Legend on the right
        draw_status_section(feedback_message, collected_presents)  # Status at the bottom

        pygame.display.flip()


if __name__ == "__main__":
    main_menu()
