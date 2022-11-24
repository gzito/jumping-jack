FPS = 60

# current resolution
RESOLUTION = (1024, 768)

# original size of ZX Spectrum screen
ORIGINAL_RESOLUTION = (256, 192)
# 8x8 blocks
ORIGINAL_BLOCKS = (32, 24)

# original size of sprites
ORIGINAL_PLAYER_SIZE = (16, 16)
ORIGINAL_LIFE_SIZE = (8, 8)
ORIGINAL_ENEMIES_SIZE = (24, 16)

# scale factors
SCALE_FACTOR_X = RESOLUTION[0] / ORIGINAL_RESOLUTION[0]
SCALE_FACTOR_Y = RESOLUTION[1] / ORIGINAL_RESOLUTION[1]

# player
SCALED_PLAYER_SIZE = (ORIGINAL_PLAYER_SIZE[0] * SCALE_FACTOR_X, ORIGINAL_PLAYER_SIZE[1] * SCALE_FACTOR_Y)
SCALED_PLAYER_WIDTH = SCALED_PLAYER_SIZE[0]
SCALED_PLAYER_HEIGHT = SCALED_PLAYER_SIZE[1]
PLAYER_SPEED = 1.5
SCALED_PLAYER_SPEED = PLAYER_SPEED * SCALE_FACTOR_X

# life
SCALED_LIFE_SIZE = (ORIGINAL_LIFE_SIZE[0] * SCALE_FACTOR_X, ORIGINAL_LIFE_SIZE[1] * SCALE_FACTOR_Y)

# screen
BORDER_WIDTH = 8
L_SCREEN_EDGE = BORDER_WIDTH
R_SCREEN_EDGE = ORIGINAL_RESOLUTION[0] - BORDER_WIDTH
SCALED_BORDER_WIDTH = BORDER_WIDTH * SCALE_FACTOR_X
SCALED_L_SCREEN_EDGE = L_SCREEN_EDGE * SCALE_FACTOR_X
SCALED_R_SCREEN_EDGE = R_SCREEN_EDGE * SCALE_FACTOR_X

# lines
LINE_WIDTH = (R_SCREEN_EDGE + 1) - L_SCREEN_EDGE
LINE_THICKNESS = 2
LINES_DISTANCE = 24
SCALED_LINE_WIDTH = LINE_WIDTH * SCALE_FACTOR_X
SCALED_LINE_THICKNESS = LINE_THICKNESS * SCALE_FACTOR_Y
SCALED_LINES_DISTANCE = LINES_DISTANCE * SCALE_FACTOR_Y

# holes
HOLE_WIDTH = 24
SCALED_HOLE_WIDTH = HOLE_WIDTH * SCALE_FACTOR_X
HOLE_SPEED = 1.5
SCALED_HOLE_SPEED = HOLE_SPEED * SCALE_FACTOR_X

COLOR_BASIC_BLACK = (0, 0, 0)
COLOR_BASIC_BLUE = (0, 0, 215)
COLOR_BASIC_RED = (215, 0, 0)
COLOR_BASIC_MAGENTA = (215, 0, 215)
COLOR_BASIC_GREEN = (0, 215, 0)
COLOR_BASIC_CYAN = (0, 215, 215)
COLOR_BASIC_YELLOW = (215, 215, 0)
COLOR_BASIC_WHITE = (215, 215, 215)

COLOR_BRIGHT_BLACK = (0, 0, 0)
COLOR_BRIGHT_BLUE = (0, 0, 255)
COLOR_BRIGHT_RED = (255, 0, 0)
COLOR_BRIGHT_MAGENTA = (255, 0, 255)
COLOR_BRIGHT_GREEN = (0, 255, 0)
COLOR_BRIGHT_CYAN = (0, 255, 255)
COLOR_BRIGHT_YELLOW = (255, 255, 0)
COLOR_BRIGHT_WHITE = (255, 255, 255)

# colors
BACKGROUND_COLOR = COLOR_BASIC_WHITE
FLASH_COLOR = COLOR_BRIGHT_WHITE
LINE_COLOR = COLOR_BASIC_RED
SCORE_COLOR = COLOR_BASIC_MAGENTA

# miscellaneous
MAX_HOLES = 8  # max 8 holes - spawns 1 hole every time the player gets up one line
LIVES = 6

GROUP_BCKGRND = "bg"
GROUP_HUD = "hud"
GROUP_ENEMIES = "enemies"
GROUP_PLAYER = "player"
