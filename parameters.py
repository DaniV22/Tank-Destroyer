'''
Defining the main parameters of the game

WIDTH :         width of the game window
HEIGHT :        height of the game window
FLOOR_WIDTH :   width of the floor
FLOOR_HEIGHT :  height of the floor
FLOOR_POS :     position of the floor
COLORS :        a dictionary that contains some useful colors used in the game
gravity :       the gravity of the game. It determines the motion of the projectiles

'''

WIDTH = 1100
HEIGHT = 700
FLOOR_WIDTH = WIDTH
FLOOR_HEIGHT = 50
FLOOR_POS = (0, HEIGHT - FLOOR_HEIGHT)

COLORS = {'BLACK': (0,0,0), 'WHITE': (255, 255, 255), 'RED': (255, 0, 0),
 'GREEN': (0, 255, 0), 'BLUE': (0,0,255), 'DARK_GREEN': (0, 150, 0),
 'YELLOW': (255, 255, 20), 'DARK_GREY': (65, 65, 65), 'LIGHT_GREY': (200, 200, 200), 
 'LIGHT_BLUE': (170, 220, 230), 'WOOD':(220, 180, 135)}

gravity = 1

def get_parameters():
    return WIDTH, HEIGHT, FLOOR_WIDTH, FLOOR_HEIGHT, FLOOR_POS, COLORS, gravity