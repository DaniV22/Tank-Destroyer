import pygame as pg
from parameters import get_parameters

WIDTH, HEIGHT, FLOOR_WIDTH, FLOOR_HEIGHT, FLOOR_POS, COLORS, gravity = get_parameters()

class PowerBar:

    '''

    Represents a power bar object that it is used by the user to see the
    firing power of the tank.

    Attributes:
    
        - x (int):         the x-coordinate of the power bar's top-left corner
        - y (int):         the y-coordinate of the power bar's top-left corner
        - width (int):     the width of the power bar
        - height (int):    the height of the power bar
        - max_power (int): the maximum power value that can be set for the power bar
        - min_power (int): the minimum power value that can be set for the power bar

    Methods:

        - draw_lines:           Draws the lines (border) around a given rectangle on a given window surface in a given color.
        - draw_background_rect: Draws a background rectangle on a given window surface in a given color with lines around it.
        - draw_power_bar:       Draws the power bar on a given window surface with a given firing power value.

    '''

    def __init__(self, x, y, width, height, max_power, min_power):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_power = max_power
        self.min_power = min_power

    def draw_lines(self, WINDOW, rect, color):

        '''
         Draws the lines around a given rectangle on a given window surface in a given color.

        Parameters:

            - WINDOW (pygame.Surface): the window surface to draw on
            - rect (pygame.Rect):      the rectangle to draw lines around
            - color (str):             the color to use for the lines

        Returns: None
        '''

        #Drawing lines around the rectangle
        pg.draw.line(WINDOW, COLORS[color], rect.topleft, rect.bottomleft, 4)
        pg.draw.line(WINDOW, COLORS[color], rect.topright, rect.bottomright, 4)
        pg.draw.line(WINDOW, COLORS[color], rect.topleft, rect.topright, 4)
        pg.draw.line(WINDOW, COLORS[color], rect.bottomright, rect.bottomleft, 4)

    def draw_background_rect(self, WINDOW, color):

        '''
        Draws a background rectangle on a given window surface in a given color with lines around it.
        It is used to draw the background of the power bar.

        Parameters:

            - WINDOW (pygame.Surface): the window surface to draw on
            - color (str):             the color to use for the rectangle and lines

        Returns: None
        '''

        background_rect = pg.Rect((self.x, self.y), (self.width, self.height))
        pg.draw.rect(WINDOW, COLORS[color], background_rect)
        self.draw_lines(WINDOW, background_rect, 'BLACK')
    
    def draw_power_bar(self, WINDOW, firing_power):

        '''
        Draws the power bar on a given window surface with a given firing power value.
        It draws a rectangle with a height that is proportional to the firing power value.
        The color of the rectangle is determined by the firing power value (red for low values, green for high values)

        Parameters:

            - WINDOW (pygame.Surface): the window surface to draw on
            - firing_power (int): the firing power value to represent on the power bar
            
        Returns: None
        '''

        self.draw_background_rect(WINDOW, 'DARK_GREY')

        color_range = [COLORS['RED'], COLORS['GREEN']]
        color_index = min(int(firing_power * len(color_range) / 100), len(color_range) - 1)
        power_bar_color = color_range[color_index]

        power_height = (firing_power/(self.max_power - self.min_power))*self.height
        power_rect = pg.Rect((self.x + 2, self.y + self.height - power_height), (self.width - 2, power_height))

        pg.draw.rect(WINDOW, power_bar_color, power_rect)