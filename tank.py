import pygame as pg
import math
from bullet import Bullet
from parameters import get_parameters

WIDTH, HEIGHT, FLOOR_WIDTH, FLOOR_HEIGHT, FLOOR_POS, COLORS, gravity = get_parameters()

class Tank:

    '''
    Represents a tank object that can move, fire, take damage, and be drawn on the game window. It is the tank controlled by the user.

    Attributes:

        - hp (int):                       the tank's current health points
        - size (int):                     the size of the tank
        - x (int):                        the x-coordinate of the tank's top-left corner
        - y (int):                        the y-coordinate of the tank's top-left corner
        - tank_speed (int):               the speed at which the tank can move
        - firing_power (int):             the current firing power of the tank
        - firing_angle (int):             the angle at which the tank's gun is aimed
        - gun_velocity (int):             the speed at which the firing angle can be changed
        - firing (bool):                  whether the tank is currently firing or not
        - got_hit (bool):                 whether the tank has been hit by a bullet
        - TANK_IMAGE (Surface):           the image of the tank
        - TANK_EXPLOSION_IMAGE (Surface): the image of the tank exploding (when it is hit by a bullet)
        - rect (Rect):                     the rectangular hitbox of the tank

    Methods:

        - firing_x0:         returns the x-coordinate of the point from which the tank fires
        - firing_y0:         returns the y-coordinate of the point from which the tank fires
        - move:              handles the tank's movement based on the keys pressed by the user
        - draw_tank:         draws the tank on a given window surface
        - draw_firing angle: draws the tank's firing angle on a given window surface
        - draw_gun:          draws the tank's gun on a given window surface
        - fire:              fires a bullet from the tank's gun
        - handle_bullet_hit: updates the tank's health points and sets got_hit to True if the tank is hit by a bullet
        - draw_hp_bar:       draws the tank's health bar above the tank on a given window surface

    '''

    def __init__(self, x0, y0):
        self.hp = 100
        self.size = 70
        self.x = x0
        self.y = y0
        self.tank_speed = 3
        self.firing_power = 0
        self.firing_angle = 30
        self.gun_velocity = 1
        self.firing = False
        self.got_hit = False
        self.TANK_IMAGE = pg.transform.scale(pg.image.load(r'images\tank_image.png'), (self.size, self.size))
        self.TANK_EXPLOSION_IMAGE = pg.transform.scale(pg.image.load(r'images\tank_explosion.png'), (self.size, self.size))
        self.rect = pg.Rect(self.x, self.y, self.size, self.size)

    @property   #Used to update firing_x0 when it's called
    def firing_x0(self):
        return self.x + 0.6*self.size

    @property
    def firing_y0(self):
        return self.y + 0.4*self.size

    def move(self, keys_pressed):

        '''
        Handles the tank's motion based on the keys pressed by the user.

        Parameters:
            - keys_pressed (dict): A dictionary containing the state of all keyboard keys. 

        Returns:
            - None
        '''
     
        #Moving the tank to the left
        if keys_pressed[pg.K_LEFT] and self.x - self.tank_speed > 0:
            self.x -= self.tank_speed

        #Moving the tank to the right
        if keys_pressed[pg.K_RIGHT] and self.x + self.tank_speed + self.size < 500:
            self.x += self.tank_speed

        #Changing the firing angle (up)
        if keys_pressed[pg.K_UP] and self.firing_angle + self.gun_velocity < 90:
            self.firing_angle += self.gun_velocity

        #Changing the firing angle (down)
        if keys_pressed[pg.K_DOWN] and self.firing_angle - self.gun_velocity > 0:
            self.firing_angle -= self.gun_velocity

        #Increasing the firing power (max power = 100)
        if keys_pressed[pg.K_SPACE] and not self.firing and self.firing_power + 2 < 101:
            self.firing_power = min(self.firing_power + 2, 100)

    def draw_tank(self, WINDOW):

        '''
        Draws the tank on a given window surface. It draws the tank's gun, firing angle, and health bar,
        and then draws the tank itself, depending on whether it has been hit by a bullet or not.

        Parameters:
            - WINDOW (Surface): The window surface on which to draw the tank.

        Returns: None
    '''

        self.rect = pg.Rect(self.x, self.y, self.size, self.size)
        self.draw_gun(WINDOW)
        self.draw_firing_angle(WINDOW, 'RED')
        self.draw_hp_bar(WINDOW)

        if self.got_hit:
            WINDOW.blit(self.TANK_EXPLOSION_IMAGE, self.rect)
            self.got_hit = False

        else:
            WINDOW.blit(self.TANK_IMAGE, self.rect)

    def draw_firing_angle(self, WINDOW, color = 'RED'):

        '''
        Draws the firing angle of the tank's next shot on a given window surface in a given color.
        It draws small rectangles equally spaced along the line of the firing angle.

        Parameters:
            - WINDOW (Surface): The window surface on which to draw the trajectory.
            - color (str):      The color of the trajectory. Defaults to 'RED'.

        Returns:
            - None
    '''

        for i in range(15):

            theta = math.radians(self.firing_angle)

            x = self.firing_x0 + 8*i*math.cos(theta)
            y = self.firing_y0 - 8*i*math.sin(theta)

            rect = pg.Rect(x, y, 3, 3)
            pg.draw.rect(WINDOW, COLORS[color], rect)

    def draw_gun(self, WINDOW, gun_length = 20, gun_width = 5, gun_color = 'DARK_GREY'):

        '''
        Draws the tank's gun on a given window surface.

        Parameters:
            - WINDOW (Surface): The window surface on which to draw the gun.
            - gun_length (float): The length of the gun. Defaults to 20.
            - gun_width (float):  The width of the gun. Defaults to 5.
            - gun_color (str):  The color of the gun. Defaults to 'DARK_GREY'.

        Returns: None

        '''

        x0, y0 = self.firing_x0, self.firing_y0
        theta = math.radians(self.firing_angle)
        x, y = x0 + gun_length*math.cos(theta), y0 - gun_length*math.sin(theta)
        pg.draw.line(WINDOW, COLORS[gun_color],(x0, y0), (x, y), width = gun_width)

    def fire(self):

        '''
        Fires a bullet from the tank's gun, with the current firing power and angle.
        It is called when the user stops pressing the space bar.

        Parameters: None

        Returns: None

        '''

        initial_velocity = 20 + 15*self.firing_power/100

        self.firing = True
        self.bullet = Bullet(self.firing_x0, self.firing_y0, initial_velocity, self.firing_angle)

    def handle_bullet_hit(self, bullet_damage):

        '''
        Updates the tank's health points and sets got_hit to True.
        It is called when the tank is hit by a bullet.

        Parameters:
            - bullet_damage (int): The damage dealt by the bullet that hit the tank.

        Returns: None
        '''

        self.hp -= bullet_damage
        self.got_hit = True

    def draw_hp_bar(self, WINDOW):

        '''
        Draws the tank's health bar on a given window surface.
        It draws a green rectangle (representing the tank's current health) on top of a red rectangle (representing the tank's maximum health

        Parameters:

            - WINDOW (Surface): The window surface on which to draw the health bar.

        Returns: None
        '''

        rect = pg.Rect(self.x, self.y - 10, self.size, 5)
        pg.draw.rect(WINDOW, COLORS['RED'], rect)
        rect = pg.Rect(self.x, self.y - 10, self.hp*self.size/100, 5)
        pg.draw.rect(WINDOW, COLORS['GREEN'], rect)
