import pygame as pg
from bullet import Bullet
import math
import numpy as np
import random

from parameters import get_parameters

WIDTH, HEIGHT, FLOOR_WIDTH, FLOOR_HEIGHT, FLOOR_POS, COLORS, gravity = get_parameters()

class EnemyTank:

    '''
    Represents an enemy tank in the game. It is used to handle the movement and shooting of the enemy tank.

    Attributes:

        - hp (int):                       the health points of the tank
        - size (int):                     the size of the tank
        - x (int):                        the x-coordinate of the top-left corner of the tank
        - y (int):                        the y-coordinate of the top-left corner of the tank
        - tank_speed (int):               the speed at which the tank moves
        - moving_steps (int):             the number of steps the tank has to move
        - direction (int):                the direction the tank is moving (1 for right, -1 for left)
        - firing_power (float):           the power of the tank's next shot
        - firing_angle (float):           the angle at which the tank will fire its next shot
        - firing (bool):                  True if the tank is currently firing, False otherwise
        - got_hit (bool):                 True if the tank was hit by a projectile, False otherwise
        - time_counter (int):             the number of game ticks that have passed since the tank last fired
        - loading_time (int):             the time it takes for the tank to reload after firing
        - TANK_IMAGE (Surface):           a Pygame Surface object representing the enemy tank's image
        - TANK_EXPLOSION_IMAGE (Surface): a Pygame Surface object representing the image of an exploding tank
        - rect (Rect):                    a Pygame Rect object representing the bounding box of the tank's image

    Methods:

        - draw_tank:                Draws the enemy tank on a given window surface
        - draw_gun:                 Draws the gun of the tank on a given window surface
        - fire:                     Fires a bullet from the tank
        - get_possible_trajectory:  Computes the angle and power for the bullet trajectory that hits the player tank
        - update_firing_angle :     Updates the firing angle of the tank
        - collision:                Checks if the bullet has collided with the list of obstacles
        - handle_bullet_hit:        Handles the case when the bullet hits the tank
        - draw_hp_bar:              Draws the health bar of the tank on a given window surface
        - distance_to_obstacles:    Computes the distance to the nearest obstacle (left and rigth) from the tank's position
        - move:                     Moves the tank in a given direction and a certain distance

    '''

    def __init__(self, x0, y0, loading_time):
        self.hp = 100
        self.size = 70
        self.x = x0
        self.y = y0
        self.tank_speed = 2
        self.moving_steps = 0
        self.direction = 1
        self.firing_power = 0
        self.firing_angle = 30
        self.firing = False
        self.got_hit = False
        self.time_counter = 0
        self.loading_time = loading_time
        self.TANK_IMAGE = pg.transform.scale(pg.image.load(r'images\enemy_image.png'), (self.size, self.size))
        self.TANK_EXPLOSION_IMAGE = pg.transform.scale(pg.image.load(r'images\enemy_tank_explosion.png'), (self.size, self.size))
        self.rect = pg.Rect(self.x, self.y, self.size, self.size)

    @property
    def firing_x0(self):
        return self.x + 0.4*self.size

    @property
    def firing_y0(self):
        return self.y + 0.4*self.size
    
    def draw_tank(self, WINDOW):

        '''
        Draws the tank on a given window surface. It draws the tank's gun, firing angle, and health bar,
        and then draws the tank itself, depending on whether it has been hit by a bullet or not.

        Parameters:
            - WINDOW (Surface): The window surface on which to draw the tank.

        Returns:
            - None
    '''

        self.rect = pg.Rect(self.x, self.y, self.size, self.size)
        self.draw_gun(WINDOW)
        self.draw_hp_bar(WINDOW)

        if self.got_hit:
            WINDOW.blit(self.TANK_EXPLOSION_IMAGE, self.rect)
            self.got_hit = False

        else:
            WINDOW.blit(self.TANK_IMAGE, self.rect)

    def draw_gun(self, WINDOW, gun_length = 20, gun_width = 5, gun_color = 'DARK_GREY'):

        '''
        Draws the tank's gun on a given window surface.

        Parameters:

            - WINDOW (Surface):     The window surface on which to draw the gun.
            - gun_length (float):   The length of the gun. Defaults to 20.
            - gun_width (float):    The width of the gun. Defaults to 5.
            - gun_color (str):      The color of the gun. Defaults to 'DARK_GREY'.

        Returns: None

        '''

        x0, y0 = self.firing_x0, self.firing_y0
        theta = math.radians(self.firing_angle + 90)    #We add 90 degrees because the tank's gun is flipped
        x, y = x0 + gun_length*math.cos(theta), y0 - gun_length*math.sin(theta)
        pg.draw.line(WINDOW, COLORS[gun_color],(x0, y0), (x, y), width = gun_width)

    def fire(self, tank_x0, tank_y0, obstacles):

        '''
        
        Fires a bullet (if possible) from the tank. It computes the angle and initial velocity of firing needed to hit the player tank.

        Parameters:

            - tank_x0 (float): The x coordinate of the player tank top-left corner.
            - tank_y0 (float): The y coordinate of the player tank top-left corner.
            - obstacles (list): A list of Obstacle objects.

        Returns: None
        
        '''

        self.firing_angle, self.firing_power = self.get_possible_trajectory(tank_x0, tank_y0, obstacles)

        if self.firing_angle is None:
            self.firing = False
            self.firing_angle = 30
        
        else:
            self.firing = True
            self.bullet = Bullet(
                self.firing_x0, self.firing_y0, self.firing_power, self.firing_angle + 90) #We add 90 degrees because the bullet is fired from rigth to left
            self.time_counter = 0

    def get_possible_trajectory(self, tank_x0, tank_y0, obstacles):

        '''

        Computes the angle and initial velocity of firing needed to hit the player tank.
        It returns, if possible, the ones that do not collide with any obstacle.

        Parameters:

            - tank_x0 (float): The x coordinate of the player tank top-left corner.
            - tank_y0 (float): The y coordinate of the player tank top-left corner.
            - obstacles (list): A list of obstacles.

        Returns:

            - theta (float): The firing angle (in degrees).
            - v (float): The initial velocity of the bullet.
        '''
        
        #A range of velocities (adapted to the size of the window)
        possible_v = np.linspace(1, 41, 21)

        for v in possible_v:

            #The discriminant of the quadratic equation that determines the possible firing angles
            discriminant = (v**4) - (gravity*(gravity*tank_x0**2 + 2*tank_y0*v**2))

            #If real solution
            if discriminant >= 0:

                #The two possible firing angles
                theta1 = math.degrees(math.atan((v**2 + math.sqrt(discriminant))/(gravity*tank_x0)))
                theta2 = math.degrees(math.atan((v**2 - math.sqrt(discriminant))/(gravity*tank_x0)))

                #If the angle is in the range [0, 90] and does not collide with any obstacle, return it
                if theta1 >= 0 and theta1 <= 90 and not self.collision(theta1 +90, v, obstacles):
                    return theta1, v
                elif theta2 >= 0 and theta2 <= 90 and not self.collision(theta2+ 90, v, obstacles):
                    return theta2, v
        
        return None, None
    
    def update_firing_angle(self, tank_x0, tank_y0, obstacles):

        '''
        Updates the firing angle of the enemy tank based on the position of the user tank and the obstacles. 
        If there is no possible trajectory, the firing angle is set to 30 degrees.

        Parameters:

            - tank_x0 (float): The x coordinate of the user tank.
            - tank_y0 (float): The y coordinate of the user tank.
            - obstacles (Obstacles): The list of obstacles objects.

        Returns: None
        
        '''
        theta, _ = self.get_possible_trajectory(tank_x0, tank_y0, obstacles)

        if theta is not None:
            self.firing_angle = theta
    
    def collision(self, theta, v, obstacles):

        '''
        Checks if the bullet fired by the enemy tank will collide with an obstacle.
        It is used to determine if there is a possible trajectory for the bullet.

        Parameters:

            - theta (float): The firing angle of the bullet.
            - v (float): The initial velocity of the bullet.
            - obstacles (Obstacles): The list of obstacles objects.

        Returns:

            - True if the bullet collides with an obstacle, False otherwise.

        '''

        #Initial position  and x-y components of the velocity of the bullet
        x, y = self.firing_x0, self.firing_y0
        vx, vy = v*math.cos(math.radians(theta)), -v*math.sin(math.radians(theta))

        #Time step
        delta_t = 0.1

        #While the bullet does not hit the ground
        while y < HEIGHT - 50:

            #Updating the position and y-velocity of the bullet, 
            x += vx * delta_t
            y += vy * delta_t - 0.5 * gravity * delta_t ** 2
            vy += gravity * delta_t

            #Checking if the bullet collides with an obstacle
            for obstacle in obstacles.obstacles:
                if obstacle.collidepoint(x, y) :
                    return True

        #No collision   
        return False
    
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

        x0, y0 = self.x, self.y - 10
        pg.draw.rect(WINDOW, COLORS['RED'], (x0, y0, self.size, 5))
        pg.draw.rect(WINDOW, COLORS['GREEN'], (x0, y0, self.size*self.hp/100, 5))

    def distance_to_obstacles(self, obstacles, other_enemies):

        '''
        Computes the left and rigth distances to the nearest obstacle (including tanks) from the tank's position.
        We need to check that the obstacle is on the same y-level as the tank, as they don't interfere with each other. 
        It is used when handling the motion of the tank.

        Parameters:

            - obstacles:  a list of obstacles present in the game.
            - other_enemies: a list of the enemies, excluding the tank itself.

        Returns:

            A tuple containing the minimum left and right distances to the nearest obstacle or enemy tank.
        '''
 
        #Initial distance to the right wall
        min_left_distance = 999999
        min_right_distance = WIDTH - self.rect.right

        for i, boundary in enumerate(obstacles.boundaries):

            #If the obstacle is on the same y level as the tank
            if abs(self.y - obstacles.obstacles[i].centery) < 100:

                left_boundary, right_boundary = boundary

                #Right and left distances to the obstacle
                right_distance = right_boundary - self.rect.right
                left_distance = left_boundary - self.rect.left

                #Updating the (right) minimum distance
                if right_distance > 0 and right_distance < min_right_distance:
                    min_right_distance = right_distance

                #Updating the (left) minimum distance
                if left_distance < 0 and abs(left_distance) < min_left_distance:
                    min_left_distance = abs(left_distance)

        for enemy in other_enemies:

            #If the enemy is on the same y level as the tank
            if enemy.y == self.y:

                #For right distance
                enemy_left, enemy_right = enemy.x, enemy.x + enemy.size

                #Right and left distances to the enemy
                right_distance = enemy_left - self.rect.right
                left_distance = enemy_right - self.rect.left

                #Updating the (right) minimum distance
                if right_distance > 0 and right_distance < min_right_distance:
                    min_right_distance = right_distance

                #Updating the (left) minimum distance
                if left_distance < 0 and abs(left_distance) < min_left_distance:
                    min_left_distance = abs(left_distance)

        return min_left_distance, min_right_distance
    
    def move(self, obstacles, enemies):

        '''
        Moves the tank a random distance based on the distance to the nearest obstacle (including oder enemy tanks).
        It computes the distance to the nearest obstacle on the left and on the right of the tank, 
        and moves the tank in the direction of the greatest minimum distance, avoiding collisions or getting stuck.

        Parameters:

            obstacles:  a list of obstacles present in the game.
            enemies:    a list of enemies present in the game.

        Returns: None
        '''
    
        #If not moving, we compute the moving distance and direction
        if self.moving_steps == 0:

            nearest_left, nearest_right = self.distance_to_obstacles(obstacles, enemies)

            #Case 1: moves to the right
            if nearest_left < nearest_right:
                self.direction = 1
                moving_distance = random.randint(0, math.floor(nearest_right / 2)) #We divide by 2 to avoid collisions of two tanks moving in opposite directions
                self.moving_steps = math.floor(moving_distance / self.tank_speed)
            
            #Case 2: moves to the left
            elif nearest_left > nearest_right:
                self.direction = -1
                moving_distance = random.randint(0, math.floor(nearest_left / 2))
                self.moving_steps = math.floor(moving_distance / self.tank_speed)
        
        #If moving, we update the tank's position, depending on the direction and the tank's speed
        if self.moving_steps > 0:
            self.x += self.direction*self.tank_speed
            self.moving_steps -= 1

    