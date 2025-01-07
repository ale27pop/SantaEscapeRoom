# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Grid Settings
GRID_ROWS = 10
GRID_COLS = 10
CELL_SIZE = SCREEN_WIDTH // GRID_COLS  # Dynamically calculate cell size to fit the screen width

# Core Colors
COLORS = {
    "background": (255, 255, 255),  # White background
    "grid": (200, 200, 200),        # Light gray grid lines
    "black": (0, 0, 0),             # Black text
}

# Game Element Colors
ELEMENT_COLORS = {
    "santa": (255, 0, 0),           # Red for Santa
    "grinch": (0, 128, 0),          # Green for the Grinch
    "obstacle": (0, 0, 0),          # Black for obstacles
    "present": (255, 255, 0),       # Yellow for presents
    "exit": (0, 0, 255),            # Blue for the exit
}

# Clue and Hint Colors
CLUE_COLORS = {
    "cookie_smell": (255, 255, 0),  # Yellow for cookie smell (presents proximity)
    "flour_smell": (169, 169, 169), # Dark gray for flour smell (obstacles proximity)
    "cold_breeze": (0, 191, 255),   # Light blue for cold breeze (exit proximity)
    "grinch_sound": (0, 100, 0),    # Dark green for Grinch's sound proximity
}

# Legend Labels
LEGEND_LABELS = {
    "Cookie Smell": CLUE_COLORS["cookie_smell"],
    "Uncovered Steps": CLUE_COLORS["flour_smell"],  # Updated label for consistency
    "Cold Breeze": CLUE_COLORS["cold_breeze"],
    "Grinch Sound": CLUE_COLORS["grinch_sound"],
}
