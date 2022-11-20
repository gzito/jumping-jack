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

LINEA_WIDTH = 800
LINEA_SPESSORE = 6
SPAZIO_TRA_LINEE = 60
BUCO_WIDTH = 80
HOLES_SPEED = 4
PLAYER_SPEED = 4
# massimo 8 buche - 1 buca ogni volta che si salta sopra una linea
MAX_HOLES = 8

# lines list
line_list = []

# holes list
hole_list = []
