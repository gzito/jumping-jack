FPS = 60

BACKGROUND_COLOR = (181, 178, 184)

# original size of sprites
ORIGINAL_SIZE = (16, 16)

# scale factor
SCALE = 2.5

# scaled size
SCALE_SIZE = (ORIGINAL_SIZE[0] * SCALE, ORIGINAL_SIZE[1] * SCALE)

# player scaled height
SCALED_PLAYER_WIDTH = SCALE_SIZE[0]
SCALED_PLAYER_HEIGHT = SCALE_SIZE[1]

L_SCREEN_EDGE = 60
R_SCREEN_EDGE = 739

LINEA_WIDTH = (R_SCREEN_EDGE + 1) - L_SCREEN_EDGE
LINEA_SPESSORE = 6
SPAZIO_TRA_LINEE = 60
BUCO_WIDTH = 80
HOLES_SPEED = 4
PLAYER_SPEED = 4
# max 8 holes - spawns 1 hole every time you get up one line
MAX_HOLES = 8

GROUP_BCKGRND = "bg"
GROUP_ENEMIES = "enemies"
GROUP_PLAYER = "player"
