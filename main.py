import pygame
import sys
import random
from config import (
    screen,
    font,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    CELL_SIZE,
    GRID_ROWS,
    GRID_COLS,
    STATUS_HEIGHT,
)
from constants import COLORS, ELEMENT_COLORS, CLUE_COLORS
from grid import load_assets, draw_grid
from instructions import instructions_screen
from game_logic import play_game, grinch_move, check_collision
from validator import validate_move_and_update, update_clues, generate_neighbors



def draw_status_section(feedback_message, collected_presents):
    """
    Draws the status section at the bottom of the screen.
    Displays the feedback message and presents collected.
    """
    status_y = SCREEN_HEIGHT - STATUS_HEIGHT
    pygame.draw.rect(screen, COLORS["background"], (0, status_y, SCREEN_WIDTH, STATUS_HEIGHT))

    feedback_text = font.render(feedback_message, True, ELEMENT_COLORS["exit"])
    screen.blit(feedback_text, (20, status_y + 20))

    presents_text = font.render(f"Presents collected: {collected_presents}", True, ELEMENT_COLORS["present"])
    screen.blit(presents_text, (20, status_y + 60))

def format_popup_message(message, max_words=6):
    """
    Formats the popup message to have a maximum of `max_words` per line.
    """
    words = message.split()
    lines = [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]
    return lines

def show_popup_message(message):
    """
    Displays a pop-up message at the center of the screen and pauses for 3 seconds.
    """
    popup_font = pygame.font.Font(None, 40)
    formatted_message = format_popup_message(message)

    popup_height = len(formatted_message) * 50
    start_y = (SCREEN_HEIGHT - popup_height) // 2

    screen.fill(COLORS["background"])
    for i, line in enumerate(formatted_message):
        popup_surface = popup_font.render(line, True, ELEMENT_COLORS["grinch"])
        popup_rect = popup_surface.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * 50))
        screen.blit(popup_surface, popup_rect)

    pygame.display.flip()
    pygame.time.delay(3000)

def add_clues(grid, presents, obstacles, exit_point, grinch_position):
    """
    Adds clues to adjacent cells for specific objects:
    - Cookie smell for presents.
    - Flour smell for obstacles.
    - Cold breeze for the exit.
    - Grinch sound for the Grinch.
    """
    offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Neighboring directions

    for present in presents:
        for dx, dy in offsets:
            nx, ny = present[0] + dx, present[1] + dy
            if 0 <= nx < GRID_ROWS and 0 <= ny < GRID_COLS:
                grid[nx][ny] |= 32  # Cookie smell clue

    for obstacle in obstacles:
        for dx, dy in offsets:
            nx, ny = obstacle[0] + dx, obstacle[1] + dy
            if 0 <= nx < GRID_ROWS and 0 <= ny < GRID_COLS:
                grid[nx][ny] |= 64  # Flour smell clue

    for dx, dy in offsets:
        nx, ny = exit_point[0] + dx, exit_point[1] + dy
        if 0 <= nx < GRID_ROWS and 0 <= ny < GRID_COLS:
            grid[nx][ny] |= 128  # Cold breeze clue

    for dx, dy in offsets:
        nx, ny = grinch_position[0] + dx, grinch_position[1] + dy
        if 0 <= nx < GRID_ROWS and 0 <= ny < GRID_COLS:
            grid[nx][ny] |= 256  # Grinch sound clue

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
                        instructions_screen()
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

def start_game():
    """
    Main game loop with manual control and Prover9-based decision-making after Enter is pressed.
    """
    santa_position = [0, 0]
    grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    grid_size = (GRID_ROWS, GRID_COLS)

    grinch_position = [random.randint(1, GRID_ROWS - 1), random.randint(1, GRID_COLS - 1)]
    exit_point = (GRID_ROWS - 1, GRID_COLS - 1)
    obstacles = {(random.randint(0, GRID_ROWS - 1), random.randint(0, GRID_COLS - 1)) for _ in range(15)}
    presents = {(random.randint(0, GRID_ROWS - 1), random.randint(0, GRID_COLS - 1)) for _ in range(5)}

    obstacles.discard((0, 0))
    presents.discard((0, 0))
    presents = {pos for pos in presents if pos not in obstacles}
    obstacles.discard(exit_point)

    assets = load_assets()
    game_running = True
    auto_mode = False
    feedback_message = "Welcome to Santa's Escape Room!"
    collected_presents = 0
    grinch_last_move = pygame.time.get_ticks()
    known_clues = {}

    while game_running:
        current_time = pygame.time.get_ticks()
        grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        grid[santa_position[0]][santa_position[1]] |= 1  # Santa
        grid[grinch_position[0]][grinch_position[1]] |= 16  # Grinch
        grid[exit_point[0]][exit_point[1]] |= 8  # Exit
        for present in presents:
            grid[present[0]][present[1]] |= 2  # Present
        for obstacle in obstacles:
            grid[obstacle[0]][obstacle[1]] |= 4  # Obstacle

        add_clues(grid, presents, obstacles, exit_point, grinch_position)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not auto_mode:
                    direction = None
                    if event.key == pygame.K_UP:
                        direction = "UP"
                    elif event.key == pygame.K_DOWN:
                        direction = "DOWN"
                    elif event.key == pygame.K_LEFT:
                        direction = "LEFT"
                    elif event.key == pygame.K_RIGHT:
                        direction = "RIGHT"

                    if direction:
                        new_position = santa_position[:]
                        if direction == "UP":
                            new_position[0] -= 1
                        elif direction == "DOWN":
                            new_position[0] += 1
                        elif direction == "LEFT":
                            new_position[1] -= 1
                        elif direction == "RIGHT":
                            new_position[1] += 1

                        if 0 <= new_position[0] < GRID_ROWS and 0 <= new_position[1] < GRID_COLS:
                            santa_position = new_position
                            feedback_message = check_collision(santa_position, grinch_position, presents, obstacles, exit_point)

                            if feedback_message == "Present collected!":
                                collected_presents += 1
                                presents.discard(tuple(santa_position))
                            elif feedback_message == "Blocked by an obstacle!":
                                show_popup_message("The kids outsmarted you! Your steps are uncovered with flour.")
                                game_running = False

                if event.key == pygame.K_RETURN:
                    auto_mode = True
                    feedback_message = "Autonomous mode activated!"

        if current_time - grinch_last_move >= 2000:
            grinch_position = grinch_move(grinch_position, grid_size, obstacles)
            grinch_last_move = current_time

        if auto_mode:
            santa_position, feedback_message = play_game(
                santa_position,
                None,
                auto_mode,
                {"cookie_smell": presents, "grinch_sound": {tuple(grinch_position)}},
                known_clues,
                grid,
                grid_size
            )

            if tuple(santa_position) in presents:
                collected_presents += 1
                presents.discard(tuple(santa_position))
                feedback_message = "Present collected!"

        # Win Condition
        if santa_position == exit_point and collected_presents == len(presents):
            show_popup_message("Santa saved the Christmas!")  # Show winning message
            game_running = False  # Stop the game
            continue

        # Lose Condition
        if santa_position == grinch_position:
            show_popup_message("Grinch stole the Christmas!")
            game_running = False

        draw_grid(screen, assets, santa_position, grinch_position, presents, obstacles, exit_point)
        draw_status_section(feedback_message, collected_presents)
        pygame.display.flip()


if __name__ == "__main__":
    main_menu()
