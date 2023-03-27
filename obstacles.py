import pygame as pg
from parameters import get_parameters

WIDTH, HEIGHT, FLOOR_WIDTH, FLOOR_HEIGHT, FLOOR_POS, COLORS, gravity = get_parameters()

class Obstacles:

    '''
    Represents a collection of obstacles or surfaces in the game. It is used to check for collisions and to
    handle the movement of the enemy tank.
    
    We define two types of obstacles : the ones that act as a WALL (tanks and bullets cannot pass through)
    and the ones that behave as a FLOOR, in which a tank can move above.

    Attributes:

        - obstacles (list): a list of pygame.Rect representing the obstacles in the game
        - boundary (list): a list of tuples containing the x-coordinates of the left and right borders of each obstacle, seen by the enemy tank*

    Methods:

        - add_obstacle:     Adds a new obstacle to the collection of obstacles
        - draw_obstacles:   Draws all the obstacles in the collection on a given window surface

    *Depending on the relative position of the tank and the obstacle, the boundary can coincide with the left or right border of the obstacle.
    For example, if the tank is above the obstacle (it is a surface), the left border of the obstacle will coincide with the left boundary.
    However, if the obstacle acts as a wall, the left border of the obstacle will act as the right boundary, from the perspective of the tank.

    '''

    def __init__(self):
        self.obstacles = []
        self.boundaries = []

    def add_obstacle(self, x, y, width, height):

        '''
        Adds a new obstacle to the list of obstacles.

        Parameters:

            - x (int):      the x-coordinate of the top-left corner of the obstacle
            - y (int):      the y-coordinate of the top-left corner of the obstacle
            - width (int):  the width of the obstacle
            - height (int): the height of the obstacle

        Returns: None
        '''

        obstacle = pg.Rect(x, y, width, height)
        self.obstacles.append(obstacle)

        #Determining the boundaries of the obstacle
        #Case 1: obstacle acts as a surface
        if width > height:
            self.boundaries.append((obstacle.left, obstacle.right))

        #Case 2: obstacle acts as a wall 
        else:
            self.boundaries.append((obstacle.right, obstacle.left))

    def draw_obstacles(self, WINDOW, color = 'LIGHT_GREY'):

        '''
        Draws all the obstacles in the collection, with a given color on a given window surface.

        Parameters:

            - WINDOW (pygame.Surface): the window surface to draw on
            - color (str):             the color to use for the obstacles (default: 'LIGHT_GREY')

        Returns: None
    '''
        
        for obstacle in self.obstacles:
            pg.draw.rect(WINDOW, COLORS[color], obstacle)