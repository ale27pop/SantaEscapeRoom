import subprocess
import time

def generate_prover9_input(santa_position, last_position, clues, grid, grid_size):
    """
    Generates a Prover9 input file dynamically to evaluate the safest move for Santa.
    Includes only the 4 adjacent cells around Santa and their respective clues.
    """
    try:
        santa_x, santa_y = santa_position
        last_x, last_y = last_position
        input_file = "santa_logic.p9"

        # Ensure grid_size is correctly unpacked
        if isinstance(grid_size, (list, tuple)) and len(grid_size) == 2:
            rows, cols = grid_size
        else:
            raise TypeError("grid_size must be a list or tuple of two integers representing grid dimensions.")

        # Define the neighboring offsets
        offsets = [
            (0, -1),  # Left
            (0, 1),   # Right
            (-1, 0),  # Up
            (1, 0),   # Down
        ]

        # Generate adjacent relations dynamically based on Santa's position
        adjacent_relations = []
        adjacent_clues = []  # To hold clues for adjacent cells

        for dx, dy in offsets:
            nx, ny = santa_x + dx, santa_y + dy
            if 0 <= nx < rows and 0 <= ny < cols:  # Ensure cell is within bounds
                adjacent_relations.append(f"adjacent({santa_x}, {santa_y}, {nx}, {ny}).")

                # Check for clues in the adjacent cell
                if grid[nx][ny] & 32:  # Cookie smell (present clue)
                    adjacent_clues.append(f"cookie_smell({nx}, {ny}).")
                if grid[nx][ny] & 64:  # Flour smell (obstacle clue)
                    adjacent_clues.append(f"flour_smell({nx}, {ny}).")
                if grid[nx][ny] & 128:  # Cold breeze (exit clue)
                    adjacent_clues.append(f"cold_breeze({nx}, {ny}).")
                if grid[nx][ny] & 256:  # Grinch sound (Grinch clue)
                    adjacent_clues.append(f"grinch_sound({nx}, {ny}).")

        # Debugging information
        print(f"[DEBUG] Adjacent relations: {adjacent_relations}")
        print(f"[DEBUG] Adjacent clues: {adjacent_clues}")

        prover9_input = [
            "% --- Santa Escape Room Logic ---",
            "% Propositions:",
            "% cookie_smell(x, y), cold_breeze(x, y), grinch_sound(x, y), safe(x, y), move_to(x, y, u, v)",
            "% present(x, y), grinch(x, y), exit(x, y), obstacle(x, y), adjacent(x, y, u, v)",
            "",
            "% --- Adjacent Relations ---",
        ]

        # Add adjacent relations for the 4 neighboring cells
        prover9_input.extend(adjacent_relations)

        prover9_input.extend([
            "",
            "% --- Rules ---",
            "all x all y (",
            "    cookie_smell(x, y) <-> exists u exists v (adjacent(x, y, u, v) & present(u, v))",
            ").",
            "",
            "all x all y (",
            "    cold_breeze(x, y) <-> exists u exists v (adjacent(x, y, u, v) & exit(u, v))",
            ").",
            "",
            "all x all y (",
            "    grinch_sound(x, y) <-> exists u exists v (adjacent(x, y, u, v) & grinch(u, v))",
            ").",
            "",
            "all x all y (",
            "    safe(x, y) <-> ~grinch(x, y) & ~obstacle(x, y)",
            ").",
            "",
            "all x all y all u all v (",
            "    move_to(x, y, u, v) <-> (",
            "        adjacent(x, y, u, v) & safe(u, v) & (u != last_x | v != last_y)",
            "    )",
            ").",
            "",
            "% --- Backup Rule: Move to a position without a Grinch clue ---",
            "all x all y all u all v (",
            "    backup_move(x, y, u, v) <-> (",
            "        adjacent(x, y, u, v) & ~grinch_sound(u, v) & ~(u = last_x & v = last_y)",
            "    )",
            ").",
            "",
            "% --- Observations ---",
            f"santa_position({santa_x}, {santa_y}).",
            f"last_position({last_x}, {last_y}).",
        ])

        # Add clues for the adjacent cells
        prover9_input.extend(adjacent_clues)

        # Add game elements only for the adjacent cells
        for dx, dy in offsets:
            nx, ny = santa_x + dx, santa_y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if grid[nx][ny] & 2:  # Present
                    prover9_input.append(f"present({nx}, {ny}).")
                if grid[nx][ny] & 4:  # Obstacle
                    prover9_input.append(f"obstacle({nx}, {ny}).")
                if grid[nx][ny] & 8:  # Exit
                    prover9_input.append(f"exit({nx}, {ny}).")
                if grid[nx][ny] & 16:  # Grinch
                    prover9_input.append(f"grinch({nx}, {ny}).")

        prover9_input.extend([
            "",
            "% --- Goal: Find a safe move or backup move ---",
            f"goal: (exists u exists v (move_to({santa_x}, {santa_y}, u, v))) |",
            f"      (exists u exists v (backup_move({santa_x}, {santa_y}, u, v))).",
        ])

        # Write to file
        with open(input_file, "w") as file:
            file.write("\n".join(prover9_input))
        print(f"Prover9 input file '{input_file}' successfully generated.")
    except Exception as e:
        print(f"[ERROR] Failed to generate Prover9 input: {e}")


def run_prover9(input_file):
    """
    Runs Prover9 with the specified input file and checks for a valid move.
    """
    prover9_path = "/mnt/c/Users/aly27/OneDrive/Desktop/UT/AI/LADR-2009-11A/LADR-2009-11A/bin/prover9"

    try:
        print(f"[DEBUG] Running Prover9: {prover9_path} -f {input_file}")
        result = subprocess.run(
            [prover9_path, f"-f{input_file}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        output = result.stdout
        print("[DEBUG] Prover9 Output:")
        print(output)

        # Check if Prover9 proved the goal
        if "THEOREM PROVED" in output:
            print("[DEBUG] Prover9 found a valid move.")
            return True  # Replace with actual move parsing logic
        else:
            print("[DEBUG] Prover9 did not find a valid move.")
            return False

    except FileNotFoundError:
        print(f"[ERROR] Prover9 executable not found at {prover9_path}. Check the path and ensure Prover9 is installed.")
        return False

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Prover9 encountered an error: {e.stderr}")
        return False


def select_best_move(santa_position, neighbors, known_clues, grid):
    """
    Selects the best move when no safe move is found by Prover9.
    Avoids known dangers (Grinch, obstacles) and prioritizes lesser risks.
    """
    for neighbor in neighbors:
        x, y = neighbor
        if (x, y) not in known_clues.get("grinch_sound", []) and grid[x][y] not in [3, 4]:  # Avoid obstacles and Grinch
            print(f"[DEBUG] Selecting {neighbor} as the best available move.")
            return neighbor
    print("[DEBUG] No safe move found. Staying in the current position.")
    return santa_position  # Stay in place as the last resort


def validate_move_and_update(santa_position, last_position, clues, grid, grid_size):
    """
    Validates Santa's move using Prover9 and updates the game state for the next step.
    """
    neighbors = generate_neighbors(santa_position, grid_size)
    print(f"[DEBUG] Neighbors of Santa: {neighbors}")

    # Generate Prover9 input and validate the move
    generate_prover9_input(santa_position, last_position, clues, grid, grid_size)
    if run_prover9("santa_logic.p9"):
        # Move Santa to the safe location if Prover9 finds a valid move
        # (Replace with the actual parsed move from Prover9 output)
        print("[DEBUG] Moving Santa to a safe location.")
        safe_move = neighbors[0]  # Replace this placeholder with actual parsing
        return safe_move
    else:
        # No safe move found by Prover9, select the best move manually
        return select_best_move(santa_position, neighbors, clues, grid)


def generate_neighbors(position, grid_size):
    """
    Generates valid neighbors for a given position within the grid.
    """
    try:
        x, y = position
        rows, cols = grid_size
        neighbors = [
            (x - 1, y),  # Up
            (x + 1, y),  # Down
            (x, y - 1),  # Left
            (x, y + 1)   # Right
        ]
        valid_neighbors = [(nx, ny) for nx, ny in neighbors if 0 <= nx < rows and 0 <= ny < cols]
        print(f"[DEBUG] Generated neighbors for {position}: {valid_neighbors}")
        return valid_neighbors
    except Exception as e:
        print(f"[ERROR] Failed to generate neighbors: {e}")
        return []


def update_clues(santa_position, game_clues, known_clues, grid_size):
    """
    Updates known clues based on observations from neighboring cells.
    """
    neighbors = generate_neighbors(santa_position, grid_size)
    for neighbor in neighbors:
        x, y = neighbor
        for clue_type, positions in game_clues.items():
            if (x, y) in positions:
                known_clues.setdefault(clue_type, set()).add((x, y))
    print(f"[DEBUG] Updated clues for {santa_position}: {known_clues}")
    return known_clues
