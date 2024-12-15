import pygame
from constants import COLORS, ELEMENT_COLORS, CLUE_COLORS, GRID_ROWS, GRID_COLS, CELL_SIZE, LEGEND_LABELS

def load_assets():
    """Load and scale assets for the grid elements."""
    santa_image = pygame.image.load("assets/santa.jpg")
    present_image = pygame.image.load("assets/present.jpg")
    obstacle_image = pygame.image.load("assets/flour.jpg")
    puzzle_image = pygame.image.load("assets/quiz.jpg")
    exit_image = pygame.image.load("assets/exit.jpg")
    grinch_image = pygame.image.load("assets/grinch.jpg")

    # Scale images to fit the grid cells
    assets = {
        "santa": pygame.transform.scale(santa_image, (CELL_SIZE, CELL_SIZE)),
        "present": pygame.transform.scale(present_image, (CELL_SIZE, CELL_SIZE)),
        "obstacle": pygame.transform.scale(obstacle_image, (CELL_SIZE, CELL_SIZE)),
        "puzzle": pygame.transform.scale(puzzle_image, (CELL_SIZE, CELL_SIZE)),
        "exit": pygame.transform.scale(exit_image, (CELL_SIZE, CELL_SIZE)),
        "grinch": pygame.transform.scale(grinch_image, (CELL_SIZE, CELL_SIZE)),
    }
    return assets


def draw_grid(screen, assets, santa_position, grinch_position, presents, puzzles, obstacles, exit_point):
    """Draws the game grid and all elements."""
    screen.fill(COLORS["background"])

    # Draw grid
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, COLORS["grid"], rect, 1)

    # Add proximity indicators
    for present in presents:
        add_proximity_indicator(screen, present, "cookie", CLUE_COLORS["cookie_smell"])
    for obstacle in obstacles:
        add_proximity_indicator(screen, obstacle, "flour", CLUE_COLORS["flour_smell"])
    for puzzle in puzzles:
        add_proximity_indicator(screen, puzzle, "puzzle", CLUE_COLORS["puzzle_hint"])
    add_proximity_indicator(screen, exit_point, "cold_breeze", CLUE_COLORS["cold_breeze"])
    add_proximity_indicator(screen, grinch_position, "grinch_sound", CLUE_COLORS["grinch_sound"])

    # Draw elements
    for obstacle in obstacles:
        screen.blit(assets["obstacle"], (obstacle[1] * CELL_SIZE, obstacle[0] * CELL_SIZE))
    for present in presents:
        screen.blit(assets["present"], (present[1] * CELL_SIZE, present[0] * CELL_SIZE))
    for puzzle in puzzles:
        screen.blit(assets["puzzle"], (puzzle[1] * CELL_SIZE, puzzle[0] * CELL_SIZE))
    screen.blit(assets["exit"], (exit_point[1] * CELL_SIZE, exit_point[0] * CELL_SIZE))
    screen.blit(assets["santa"], (santa_position[1] * CELL_SIZE, santa_position[0] * CELL_SIZE))
    screen.blit(assets["grinch"], (grinch_position[1] * CELL_SIZE, grinch_position[0] * CELL_SIZE))


def add_proximity_indicator(screen, position, indicator_type, color):
    """Adds visual clues around specific cells."""
    x, y = position
    offsets = [
        (0, -1),  # Left
        (0, 1),   # Right
        (-1, 0),  # Up
        (1, 0),   # Down
    ]

    for dx, dy in offsets:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_ROWS and 0 <= ny < GRID_COLS:  # Ensure within bounds
            rect_x = ny * CELL_SIZE
            rect_y = nx * CELL_SIZE

            if indicator_type == "cookie":
                pygame.draw.circle(screen, color, (rect_x + CELL_SIZE - 10, rect_y + 10), 5)
            elif indicator_type == "flour":
                pygame.draw.circle(screen, color, (rect_x + 10, rect_y + 10), 5)
            elif indicator_type == "puzzle":
                pygame.draw.circle(screen, color, (rect_x + 10, rect_y + CELL_SIZE - 10), 5)
            elif indicator_type == "cold_breeze":
                pygame.draw.circle(screen, color, (rect_x + CELL_SIZE - 10, rect_y + CELL_SIZE - 10), 5)
            elif indicator_type == "grinch_sound":
                pygame.draw.circle(screen, color, (rect_x + 10, rect_y + CELL_SIZE - 10), 5)


def clear_clues(screen, position):
    """
    Clears clues around the given position.
    """
    x, y = position
    offsets = [
        (0, -1),  # Left
        (0, 1),   # Right
        (-1, 0),  # Up
        (1, 0),   # Down
    ]

    for dx, dy in offsets:
        nx, ny = x + dx, y + dy
        # Ensure within grid boundaries
        if 0 <= nx < GRID_ROWS and 0 <= ny < GRID_COLS:
            rect_x = ny * CELL_SIZE
            rect_y = nx * CELL_SIZE

            # Redraw the cell background to "clear" the clue
            pygame.draw.rect(screen, COLORS["background"], (rect_x, rect_y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, COLORS["grid"], (rect_x, rect_y, CELL_SIZE, CELL_SIZE), 1)


def draw_legend(screen, font, legend_x, legend_y):
    """
    Draws the legend on the specified position of the screen.
    """
    line_spacing = 40  # Space between legend items

    # Background for the legend
    pygame.draw.rect(screen, (255, 255, 255), (legend_x - 10, legend_y - 10, 220, len(LEGEND_LABELS) * line_spacing + 20))

    # Legend title
    title = font.render("Legend", True, (0, 0, 0))
    screen.blit(title, (legend_x, legend_y))
    legend_y += line_spacing

    # Legend items
    for label, color in LEGEND_LABELS.items():
        pygame.draw.rect(screen, color, (legend_x, legend_y + 10, 20, 20))
        text = font.render(label, True, (0, 0, 0))  # Black text
        screen.blit(text, (legend_x + 30, legend_y))
        legend_y += line_spacing
