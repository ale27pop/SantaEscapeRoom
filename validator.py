import subprocess

def check_collision(santa_position, presents, puzzles, obstacles, exit_point):
    """
    Handles collisions with obstacles, presents, puzzles, and the exit.
    """
    santa_tuple = tuple(santa_position)

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


def validate_move_with_prover9(current_pos, target_pos, clues, obstacles, grid_size):
    """
    Uses Prover9 to validate whether a move from current_pos to target_pos is valid and safe.
    """
    prover9_input = generate_prover9_input(current_pos, target_pos, clues, obstacles, grid_size)
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


def generate_prover9_input(current_pos, target_pos, clues, obstacles, grid_size):
    """
    Generates the Prover9 input file content dynamically based on the current state.
    """
    cx, cy = current_pos
    tx, ty = target_pos
    rows, cols = grid_size

    input_data = f"""
    % Define grid boundaries
    boundary(0, {rows - 1}).
    boundary(0, {cols - 1}).

    % Define obstacles
    {generate_prover9_facts("obstacle", obstacles)}

    % Define clues
    {generate_prover9_clue_facts(clues)}

    % Rules for valid moves
    valid_move(CurrentX, CurrentY, TargetX, TargetY) :-
        boundary(0, {rows - 1}),
        boundary(0, {cols - 1}),
        not obstacle(TargetX, TargetY),
        (
            (TargetX = CurrentX + 1, TargetY = CurrentY);  % Down
            (TargetX = CurrentX - 1, TargetY = CurrentY);  % Up
            (TargetX = CurrentX, TargetY = CurrentY + 1);  % Right
            (TargetX = CurrentX, TargetY = CurrentY - 1)   % Left
        ).

    % Move desirability based on clues
    desirable_move(TargetX, TargetY, Score) :-
        (clue(cookie_smell, TargetX, TargetY), Score = 50);
        (clue(puzzle_hint, TargetX, TargetY), Score = 30);
        (clue(cold_breeze, TargetX, TargetY), Score = 20);
        (clue(grinch_sound, TargetX, TargetY), Score = -50).

    % Goal: Check if the move is valid and desirable
    goal: valid_move({cx}, {cy}, {tx}, {ty}).
    """
    return input_data


def generate_prover9_facts(fact_type, positions):
    """
    Generates Prover9 facts for obstacles, clues, or other elements.
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


# Example usage within game loop:
def validate_move(santa_position, new_position, clues, obstacles, grid_size):
    """
    Validates a move using Prover9 logic.
    """
    is_valid = validate_move_with_prover9(
        current_pos=santa_position,
        target_pos=new_position,
        clues=clues,
        obstacles=obstacles,
        grid_size=grid_size,
    )
    return is_valid
