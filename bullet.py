import math
from parameters import get_parameters
import pygame as pg

WIDTH, HEIGHT, FLOOR_WIDTH, FLOOR_HEIGHT, FLOOR_POS, COLORS, gravity = get_parameters()

class Bullet:


    '''
    Represents a bullet object that can be shot from a tank. It is created when a tank (user or enemy) fires and 
    destroyed when it collides with an obstacle or target.

    Attributes:
    
        - bullet_damage (int): the damage that the bullet will inflict on the tanks it impact on
        - x (int):             the x-coordinate of the bullet's top-left corner
        - y (int):             the y-coordinate of the bullet's top-left corner
        - v0 (int):            the initial velocity of the bullet
        - theta (float):       the angle at which the bullet is fired (in radians)
        - vx (float):          the x-component of the bullet's velocity vector
        - vy (float):          the y-component of the bullet's velocity vector
        - gravity (float):     the acceleration due to gravity
        - delta_t (float):     the time step for the simulation
        - rect (pygame.Rect):  the rectangle object that represents the bullet in the game window

    Methods:

        - update:                 updates the position of the bullet based on its current velocity and acceleration. It updates the rect object too
        - draw_bullet:            draws the bullet on a given window surface
        - check_bullet_collision: checks if the bullet has collided with any obstacles or tanks, and updates the game accordingly.

    '''

    def __init__(self,x0, y0, v0, angle):
        self.bullet_damage = 50
        self.x = x0
        self.y = y0
        self.v0 = v0
        self.theta = math.radians(angle)
        self.vx = v0 * math.cos(self.theta)
        self.vy = - v0 * math.sin(self.theta)
        self.gravity = gravity
        self.delta_t = 0.5
        self.rect = pg.Rect(self.x, self.y, 7, 7)
        

    def update(self):

        '''
        Updates the position of the bullet based on its current velocity and acceleration.
        It updates the rect object too.

        Parameters: None

        Returns: None
        '''

        self.x += self.vx * self.delta_t
        self.y += self.vy * self.delta_t - 0.5 * self.gravity * self.delta_t ** 2
        self.vy += self.gravity * self.delta_t

        self.rect = pg.Rect(self.x, self.y, 7, 7)

    def draw_bullet(self, WINDOW, color = 'RED'):

        '''
        Draws the bullet on a given window surface. 

        Parameters:

            - WINDOW (pygame.Surface): the window surface to draw on
            - color (str):             the color to use for the bullet (default: 'RED')

        Returns: None
        '''

        pg.draw.rect(WINDOW, COLORS[color], self.rect)

    def check_bullet_collision(self, obstacles, tank):

        
        '''
        Checks if the bullet has collided with any obstacles or tank, and updates the game accordingly.

        Parameters:
        
            - obstacles (list): a list of Obstacle objects that the bullet could potentially collide with
            - tank (Tank):      the tank object that the bullet could potentially collide with

        Returns: None
        '''

        #Checking collision with tank and updating tank health accordingly
        if self.rect.colliderect(tank.rect):
            tank.handle_bullet_hit(self.bullet_damage)
            return True

        #Checking collision with obstacles and updating obstacle
        for obstacle in obstacles.obstacles:
            if self.rect.colliderect(obstacle):
                return True

        #Checking if bullet has gone out of bounds
        if (self.y > FLOOR_POS[1] or self.y < 0):
            return True
        
        elif self.x > WIDTH:
            return True

        return False