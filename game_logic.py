import random
from constants import GRID_ROWS, GRID_COLS
from validator import validate_move_and_update, update_clues, generate_neighbors


def santa_move(santa_position, direction):
    """
    Calculates Santa's new position based on the input direction.
    """
    new_position = santa_position[:]
    if direction == "UP":
        new_position[0] -= 1
    elif direction == "DOWN":
        new_position[0] += 1
    elif direction == "LEFT":
        new_position[1] -= 1
    elif direction == "RIGHT":
        new_position[1] += 1
    return new_position

    """
    Handles collisions with obstacles, presents, the Grinch, and the exit.
    """
    santa_tuple = tuple(santa_position)

    # Check if Santa is caught by the Grinch
    if santa_tuple == tuple(grinch_position):
        return "Santa caught by the Grinch! Game Over!"

    # Check for presents
    if santa_tuple in presents:
        presents.remove(santa_tuple)
        return "Present collected!"

    # Check for obstacles
    if santa_tuple in obstacles:
        return "Blocked by an obstacle!"

    # Check for exit
    if santa_tuple == exit_point:
        if len(presents) == 0:
            return "Congratulations! You've saved Christmas!"
        else:
            return "Collect all presents before exiting!"

    return "Move successful!"


def grinch_move(grinch_position, grid_size, obstacles):
    """
    Moves the Grinch randomly in one of the four directions: up, down, left, or right.
    Grinch avoids obstacles and respects grid boundaries.
    """
    directions = [
        (0, -1),  # Left
        (0, 1),   # Right
        (-1, 0),  # Up
        (1, 0),   # Down
    ]

    random.shuffle(directions)  # Shuffle directions to make movement random

    for dx, dy in directions:
        new_x = grinch_position[0] + dx
        new_y = grinch_position[1] + dy

        # Check if the new position is within grid boundaries and not an obstacle
        if 0 <= new_x < grid_size[0] and 0 <= new_y < grid_size[1]:
            if (new_x, new_y) not in obstacles:
                return [new_x, new_y]

    # If no valid move is found, stay in the same position
    return grinch_position

def check_collision(santa_position, grinch_position, presents, obstacles, exit_point):
    """
    Handles collisions with obstacles, presents, the Grinch, and the exit.
    """
    santa_tuple = tuple(santa_position)

    # Check if Santa is caught by the Grinch
    if santa_tuple == tuple(grinch_position):
        return "Santa caught by the Grinch! Game Over!"

    # Check for presents
    if santa_tuple in presents:
        presents.remove(santa_tuple)
        return "Present collected!"

    # Check for obstacles
    if santa_tuple in obstacles:
        return "Blocked by an obstacle!"

    # Check for exit
    if santa_tuple == exit_point:
        if len(presents) == 0:
            return "Congratulations! You've saved Christmas!"
        else:
            return "Collect all presents before exiting!"

    return "Move successful!"

def determine_next_move(santa_position, last_position, clues, grid, known_clues, grid_size):
    """
    Determines the next move for Santa using Prover9 validation or manual fallback.
    """
    # Update clues based on adjacent cells
    known_clues = update_clues(santa_position, clues, known_clues, grid_size)

    # Use Prover9 to validate and determine the next move
    next_position = validate_move_and_update(santa_position, last_position, clues, grid, grid_size)
    return next_position

def manual_move(santa_position, direction, grid_size):
    """
    Moves Santa manually based on player input.
    """
    new_position = santa_move(santa_position, direction)
    if 0 <= new_position[0] < GRID_ROWS and 0 <= new_position[1] < GRID_COLS:
        return new_position
    return santa_position

def play_game(santa_position, direction, auto_mode, clues, known_clues, grid, grid_size):
    """
    Handles the main game logic, allowing both manual and autonomous play.
    """
    if auto_mode:
        # Autonomous mode: Use Prover9 to determine the next move
        last_position = [santa_position[0], santa_position[1]]
        next_position = determine_next_move(santa_position, last_position, clues, grid, known_clues, grid_size)
        return next_position, "Prover9 determined the next move."
    else:
        # Manual mode: Move based on player input
        new_position = manual_move(santa_position, direction, grid_size)
        feedback_message = check_collision(new_position, None, clues.get("cookie_smell", []), grid, None)
        return new_position, feedback_message
