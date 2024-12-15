import random
from constants import GRID_ROWS, GRID_COLS


def validate_move(santa_position, new_position, obstacles, clues):
    """
    Validates Santa's move against grid boundaries, obstacles, and Prover9 rules.
    """
    new_x, new_y = new_position
    if 0 <= new_x < GRID_ROWS and 0 <= new_y < GRID_COLS:
        if tuple(new_position) not in obstacles:
            # Check Prover9 for additional validation
            if validate_move_with_prover9(santa_position, new_position, clues, obstacles):
                return True
            else:
                return False  # Prover9 rejected the move
    return False


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


def check_collision(santa_position, grinch_position, presents, puzzles, obstacles, exit_point):
    """
    Handles collisions with obstacles, presents, puzzles, the Grinch, and the exit.
    """
    santa_tuple = tuple(santa_position)

    # Check if Santa is caught by the Grinch
    if santa_tuple == tuple(grinch_position):
        return "Santa caught by the Grinch! Game Over!"

    # Check for presents
    if santa_tuple in presents:
        presents.remove(santa_tuple)
        return "Present collected!"

    # Check for puzzles
    if santa_tuple in puzzles:
        puzzles.remove(santa_tuple)
        return "Puzzle encountered!"

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


def validate_move_with_prover9(current_pos, target_pos, clues, obstacles):
    """
    Uses Prover9 to validate whether a move from current_pos to target_pos is safe.
    """
    prover9_input = generate_prover9_input(current_pos, target_pos, clues, obstacles)
    input_file = "prover_logic.p9"
    output_file = "prover_logic.out"

    # Write Prover9 input to a file
    with open(input_file, "w") as file:
        file.write(prover9_input)

    # Run Prover9
    try:
        subprocess.run(["prover9", f"-f{input_file}", f"-o{output_file}"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Prover9 encountered an error: {e}")
        return False

    # Parse Prover9 output
    with open(output_file, "r") as file:
        output = file.read()

    # Check if Prover9 proved the move valid
    if "THEOREM PROVED" in output:
        return True
    return False


def generate_prover9_input(current_pos, target_pos, clues, obstacles):
    """
    Generates the Prover9 input file content dynamically based on the current state.
    """
    cx, cy = current_pos
    tx, ty = target_pos

    input_data = f"""
    % Define grid boundaries
    boundary(0, {GRID_ROWS - 1}).
    boundary(0, {GRID_COLS - 1}).

    % Define obstacles
    {generate_prover9_facts("obstacle", obstacles)}

    % Define clues
    {generate_prover9_clue_facts(clues)}

    % Rules for valid moves
    valid_move(CurrentX, CurrentY, TargetX, TargetY) :-
        boundary(0, {GRID_ROWS - 1}),
        boundary(0, {GRID_COLS - 1}),
        not obstacle(TargetX, TargetY),
        (
            (TargetX = CurrentX + 1, TargetY = CurrentY);  % Down
            (TargetX = CurrentX - 1, TargetY = CurrentY);  % Up
            (TargetX = CurrentX, TargetY = CurrentY + 1);  % Right
            (TargetX = CurrentX, TargetY = CurrentY - 1)   % Left
        ).

    % Goal: Check if the move is valid
    goal: valid_move({cx}, {cy}, {tx}, {ty}).
    """
    return input_data


def generate_prover9_facts(fact_type, positions):
    """
    Generates Prover9 facts for obstacles or clues.
    """
    return "\n".join([f"{fact_type}({x}, {y})." for x, y in positions])


def generate_prover9_clue_facts(clues):
    """
    Generates Prover9 facts for clues like cookie_smell, puzzle_hint, etc.
    """
    facts = []
    for clue_type, clue_positions in clues.items():
        for x, y in clue_positions:
            facts.append(f"clue({clue_type}, {x}, {y}).")
    return "\n".join(facts)


def ai_decision(santa_position, presents, puzzles, obstacles, exit_point, clues):
    """
    Determines the next move for Santa based on AI or Prover9 inference.
    Clues include proximity indicators for all relevant elements.
    """
    def manhattan_distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    # Step 1: Prioritize closest present
    closest_present = min(presents, key=lambda p: manhattan_distance(santa_position, p), default=None)
    if closest_present:
        if santa_position[0] < closest_present[0]:
            return "DOWN"
        elif santa_position[0] > closest_present[0]:
            return "UP"
        elif santa_position[1] < closest_present[1]:
            return "RIGHT"
        elif santa_position[1] > closest_present[1]:
            return "LEFT"

    # Step 2: Move towards closest puzzle if no presents are left
    closest_puzzle = min(puzzles, key=lambda p: manhattan_distance(santa_position, p), default=None)
    if closest_puzzle:
        if santa_position[0] < closest_puzzle[0]:
            return "DOWN"
        elif santa_position[0] > closest_puzzle[0]:
            return "UP"
        elif santa_position[1] < closest_puzzle[1]:
            return "RIGHT"
        elif santa_position[1] > closest_puzzle[1]:
            return "LEFT"

    # Step 3: Move towards the exit if no presents or puzzles remain
    if len(presents) == 0 and len(puzzles) == 0:
        if santa_position[0] < exit_point[0]:
            return "DOWN"
        elif santa_position[0] > exit_point[0]:
            return "UP"
        elif santa_position[1] < exit_point[1]:
            return "RIGHT"
        elif santa_position[1] > exit_point[1]:
            return "LEFT"

    # Default move if nothing to prioritize
    return "UP"
