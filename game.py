import pygame as pg
from power_bar import PowerBar
from new_level import create_new_level
from parameters import get_parameters

WIDTH, HEIGHT, FLOOR_WIDTH, FLOOR_HEIGHT, FLOOR_POS, COLORS, gravity = get_parameters()

class Game:

    '''

    A class that handles the possible states of the game.

    Attributes

        current_level (int) :   The current level of the game.
        tank_lives (int) :      The number of lives of the tank.
        tank (Tank) :           A Tank object that represents the player.
        enemies (list) :        A list of EnemyTank objects.
        obstacles (Obstacles) : An Obstacles object.
        power_bar (PowerBar) :  A PowerBar object.
        play_again (bool) :     A boolean that indicates if the player wants to play again.
        BACKGROUND (Surface) :  The background of the game.
        LIVES (Surface) :       The image of the lives of the tank.
        max_levels (int) :      The maximum number of levels of the game.

    Methods

        init :                      Initializes the game (creates the tank, enemies, obstacles, etc).
        handle_tank :               Handles the tank (movement, firing, etc).
        handle_enemy :              Handles the enemies (movement, firing, etc).
        check_tank_is_dead :        Checks if the (player) tank is dead.
        handle_end_game :           Handles the end of the game (victory or defeat).
        draw_next_level_window :    Draws the window that indicates the next level.
        draw_play_again_window :    Draws the window to decide if the player wants to play again.
        draw_window :               Draws the main window of the game (background, tank, enemies, obstacles, etc).
        draw_lives :                Draws on the window the current number of lives of the tank.
        draw_num_enemies :          Draws on the window the current number of enemies.
        draw_current_level :        Draws on the window the current level of the game.

    '''

    def __init__(self):

        self.power_bar = PowerBar(30, HEIGHT/4, 40, 250, 100, 0)
        self.current_level = 1
        self.tank_lives = 3
        self.play_again = True
        self.BACKGROUND = pg.transform.scale(pg.image.load( r'images\background1.png'), (WIDTH, HEIGHT))
        self.LIVES = pg.transform.scale(pg.image.load( r'images\life.png'), (30, 30))
        self.max_levels = 8

    def init(self):

        '''
        Initializes the game, creating a new level with new enemies, obstacles, and a player's tank.
        It is called at the beginning of the game, when the player passes to the next level, and when the player wants to play again.

        Parameters: None

        Returns:    None

        '''
            
        self.tank, self.enemies, self.obstacles = create_new_level(self.current_level)

    def handle_tank(self, keys_pressed):

        '''
        Handles all possible actions of the tank (movement, firing, etc).
        It is called every frame by the game loop.

        Parameters

            keys_pressed (list) :   A list of booleans that indicates if a key is pressed or not.

        Returns: None
        
        '''

        self.tank.move(keys_pressed)

        if self.tank.firing:
            self.tank.bullet.update()

        if hasattr(self.tank, 'bullet'):
            collision = any([self.tank.bullet.check_bullet_collision(self.obstacles, enemy) for enemy in self.enemies])

            if collision:
                self.tank.firing = False
                del self.tank.bullet

    def handle_enemy(self):

        '''
        Handles all possible actions of the enemies (movement, firing, etc). It is called every frame by the game loop.

        Parameters: None

        Returns: None
    '''

        for enemy in self.enemies:

            #Updating firing angle
            enemy.update_firing_angle(enemy.x - self.tank.x, enemy.y - self.tank.y, self.obstacles)
            
            #List of enemies excluding the current enemy
            enemies_to_check = self.enemies.copy()
            enemies_to_check.remove(enemy)

            enemy.move(self.obstacles, enemies_to_check)

            #Check if enemy is firing and if it is time to fire
            if not enemy.firing and enemy.time_counter > enemy.loading_time:
                enemy.fire(enemy.x - self.tank.x, enemy.y - self.tank.y, self.obstacles)
                enemy.time_counter = 0

            #Update enemy bullet
            if enemy.firing:
                enemy.bullet.update()
            
            #Check if enemy bullet hit the tank
            if hasattr(enemy, 'bullet'):
                collision = enemy.bullet.check_bullet_collision(self.obstacles, self.tank)

                #If collision, delete bullet
                if collision:
                    enemy.firing = False
                    del enemy.bullet

            #Check if enemy is dead
            if enemy.hp <= 0:
                self.enemies.remove(enemy)

    def check_tank_is_dead(self, WINDOW):

        '''
        Checks if the (user) tank is dead and handles the game over accordingly.
        It distinguishes between the case where the tank has no more lives and the case
        where the tank has at least one life left and can continue playing.

        Parameters:

            WINDOW (pygame.Surface): The window surface to draw on

        Returns: None
        '''

        #Case where the tank has no more lives
        if self.tank.hp <= 0 and self.tank_lives == 1:
            self.handle_end_game(WINDOW, victory=False)

        #Case where the tank has at least one life left
        elif self.tank.hp <= 0 and self.tank_lives > 0:
            self.draw_next_level_window(WINDOW, self.current_level, passed=False)
            self.tank_lives -= 1
            self.init()

    def handle_end_game(self, WINDOW, victory):

        '''
        
        Handles the end of the game (victory or defeat) and calls the function to draw the window to decide if the player wants to play again.

        Parameters:

            WINDOW (pygame.Surface):    The window surface to draw on
            victory (bool):             Whether the player has won or lost the game.

        Returns: None
        
        '''

        self.play_again = self.draw_play_again(WINDOW, victory)

        #Continue playing
        if self.play_again:
            self.current_level = 1
            self.tank_lives = 3
            self.init()

    def draw_next_level_window(self, WINDOW, level, passed = True):

        '''
        Draws the window that indicates the next level. It is called when the player passes to the next level or when the player fails a level.
        Depending on the case, the window will indicate that the player has passed the level or that the player has failed the level.

        Parameters:

            WINDOW (pygame.Surface):    The window surface to draw on
            level (int):                The current level.
            passed (bool):              Whether the player has passed the level or not.

        Returns: None
        
        '''

        #Counter to keep track of the time the window is displayed
        counter = 3

        while counter > 0:

            #Big background rect
            pg.draw.rect(WINDOW, COLORS['LIGHT_BLUE'], (WIDTH/2 - 250, HEIGHT/2 -200, 500, 400))

            #Draw a rect with a smaller size to make a border
            pg.draw.rect(WINDOW, COLORS['BLACK'], (WIDTH/2 - 250, HEIGHT/2 -200, 500, 400), 5)

            font = pg.font.SysFont('comicsans', 40)

            #Two possible texts depending on whether the player has passed the level or not
            if passed:
                text1 = font.render(f"You've passed level {level}!", 1, COLORS['BLACK'])
                text2 = font.render(f"Next level in...", 1, COLORS['BLACK'])
            else:
                text1 = font.render(f"You've failed level {level}!", 1, COLORS['BLACK'])
                text2 = font.render(f"Try again in...", 1, COLORS['BLACK'])

            WINDOW.blit(text1, (WIDTH/2 - text1.get_width()/2, HEIGHT/2 - 150 - text1.get_height()/2))
            WINDOW.blit(text2, (WIDTH/2 - text2.get_width()/2, HEIGHT/2 - 30 - text2.get_height()/2))

            #Displaying the counter
            font = pg.font.SysFont('comicsans', 100)
            text = font.render(str(counter), 1, COLORS['BLACK'])
            WINDOW.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 + 20))

            #Draw circle around the counter
            pg.draw.circle(WINDOW, COLORS['BLACK'], (WIDTH/2, HEIGHT/2 + 20 + text.get_height()/2), text.get_height()/2 + 5, 5)

            pg.display.update()
            pg.time.delay(1000)

            counter -= 1

    def draw_play_again(self, WINDOW, victory = False):

        '''
        Draws the window that asks the user if he wants to play again or not.
        It is called when the player has lost all his lives or when the player has won the game, inside the handle_end_game function.

        Parameters:

            WINDOW (pygame.Surface):    The window surface to draw on
            victory (bool):             Whether the player has won or lost the game.

        Returns:
            bool : True if the player wants to play again, False otherwise.
        
        '''
        
        while True:

            #Big background rect
            pg.draw.rect(WINDOW, COLORS['LIGHT_BLUE'], (WIDTH/2 - 200, HEIGHT/2 -200, 400, 400))
            #Draw a rect with a smaller size to make a border
            pg.draw.rect(WINDOW, COLORS['BLACK'], (WIDTH/2 - 200, HEIGHT/2 -200, 400, 400), 5)
            
            font = pg.font.SysFont('comicsans', 60)

            #Two possible texts depending on whether the player has won or lost the game
            if victory:
                text = font.render('Victory!', 1, COLORS['BLACK'])
            else:
                text = font.render('Game Over', 1, COLORS['BLACK'])

            WINDOW.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - 150 - text.get_height()/2))

            pg.draw.rect(WINDOW, COLORS['LIGHT_GREY'], (WIDTH/2 - 100, HEIGHT/2 -80, 200, 100))
            pg.draw.rect(WINDOW, COLORS['LIGHT_GREY'], (WIDTH/2 - 100, HEIGHT/2 + 40, 200, 100))

            #Background rect
            pg.draw.rect(WINDOW, COLORS['WHITE'], (WIDTH/2 - 100, HEIGHT/2 -80, 200, 100), 5)
            pg.draw.rect(WINDOW, COLORS['WHITE'], (WIDTH/2 - 100, HEIGHT/2 + 40, 200, 100), 5)

            #Play again and quit buttons
            font = pg.font.SysFont('comicsans', 30)
            text = font.render('Play again', 1, COLORS['BLACK'])
            WINDOW.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 -80 + text.get_height()/2))

            text = font.render('Quit', 1, COLORS['BLACK'])
            WINDOW.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 + 50 + text.get_height()/2))

            pg.display.update()

            #Event handling (play again or quit)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    run = False
                    break

                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()

                    if WIDTH/2 - 100 <= mouse_pos[0] <= WIDTH/2 + 100 and HEIGHT/2 -80 <= mouse_pos[1] <= HEIGHT/2 + 20:
                        return True
                    
                    elif WIDTH/2 - 100 <= mouse_pos[0] <= WIDTH/2 + 100 and HEIGHT/2 + 40 <= mouse_pos[1] <= HEIGHT/2 + 140:
                        return False
                    
    def draw_window(self, WINDOW):

        '''
        
        Draws the main events of the game on the window. 

        Parameters:

            WINDOW (pygame.Surface):    The window surface to draw on

        Returns: None
        
        '''
        #Background
        WINDOW.blit(self.BACKGROUND, (0, 0))

        #Number of lives
        self.draw_lives(WINDOW, self.tank_lives)

        #Number of enemies
        self.draw_num_enemies(WINDOW)

        #Current level
        self.draw_current_level(WINDOW, self.current_level)

        #Floor
        floor = pg.Rect(FLOOR_POS[0], FLOOR_POS[1], FLOOR_WIDTH, FLOOR_HEIGHT)
        pg.draw.rect(WINDOW, COLORS['LIGHT_GREY'], floor)

        #User tank
        self.tank.draw_tank(WINDOW)

        #Bullet (user tank)
        if self.tank.firing:
            self.tank.bullet.draw_bullet(WINDOW)

        #Obstacles
        self.obstacles.draw_obstacles(WINDOW)

        #Power bar
        self.power_bar.draw_power_bar(WINDOW, self.tank.firing_power)

        #Enemy
        for enemy in self.enemies:
            enemy.draw_tank(WINDOW)

            #Bullet (enemy)
            if enemy.firing:
                enemy.bullet.draw_bullet(WINDOW)

        pg.display.update()

    def draw_lives(self, WINDOW, num_lives):

        '''
        Draws the number of lives the user has left on the window.

        Parameters:

            WINDOW (pygame.Surface):    The window surface to draw on
            num_lives (int):            The number of lives the user has left

        Returns: None
        
        '''

        for i in range(num_lives):
            WINDOW.blit(self.LIVES, (20 + i * 35, 20))

    def draw_num_enemies(self, WINDOW):

        '''
        
        Draws the number of enemies left on the window.

        Parameters:

            WINDOW (pygame.Surface):    The window surface to draw on

        Returns: None
        
        '''

        font = pg.font.SysFont('comicsans', 30)
        text = font.render('Enemies: ' + str(len(self.enemies)), 1, COLORS['BLACK'])
        WINDOW.blit(text, (WIDTH - text.get_width() - 10, 10))

    def draw_current_level(self, WINDOW, level):

        '''
        
        Draws the current level on the window.

        Parameters:

            WINDOW (pygame.Surface):    The window surface to draw on

        Returns: None
        
        '''

        font = pg.font.SysFont('comicsans', 30)
        text = font.render('Level: ' + str(level), 1, COLORS['BLACK'])
        WINDOW.blit(text, (WIDTH/2 - text.get_width()/2, 10))