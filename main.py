import pygame as pg
from game import Game
from parameters import get_parameters

'''
Main file for the game. Initializes the game and runs the main loop.

ABOUT THE GAME:

The player controls a tank that can fire projectiles. The goal is to destroy all the enemies on the screen and pass all the levels.
The player can move the tank left and right (LEFT ARROW and RIGTH ARROW), and fire projectiles (SPACEBAR).
The player can also adjust the power of the projectile by holding the SPACEBAR.
It can also adjust the angle of the projectile by pressing UP ARROW and DOWN ARROW.

The enemies move in a straight line, and can be destroyed by the player's projectiles. They will try to destroy the player's tank.

Each level is progressively more difficult than the previous one. There are (currently) 8 levels in the game.
The player has 3 lives to pass all the levels.

'''

def main():

    pg.font.init()
    pg.init()

    WIDTH, HEIGHT, FLOOR_WIDTH, FLOOR_HEIGHT, FLOOR_POS, COLOR, gravity = get_parameters()

    FPS = 60

    WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('Tank destroyer')

    clock = pg.time.Clock()

    #Initialize game
    game = Game()
    game.init()

    #Main loop
    while game.play_again:
        
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            
            #Check if the player wants to fire
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and not game.tank.firing :
                game.tank.firing_power = 0
            
            #Fire
            elif event.type == pg.KEYUP and event.key == pg.K_SPACE and not game.tank.firing:
                game.tank.fire()
                game.tank.firing_power = 0

        keys_pressed = pg.key.get_pressed()

        #Handle (user) tank and enemies
        game.handle_tank(keys_pressed)
        game.handle_enemy()

        #Draw everything
        game.draw_window(WINDOW)

        #Check if all enemies are dead
        if len(game.enemies) == 0:

            #Check if player has passed all levels
            if game.current_level == game.max_levels:
                game.handle_end_game(WINDOW, victory=True)
            
            #If not, next level
            else:
                game.draw_next_level_window(WINDOW, game.current_level, passed=True)
                game.current_level += 1
                game.init()

        #Update time counter (loading) for enemies
        for enemy in game.enemies:
            enemy.time_counter += clock.get_time()

        game.check_tank_is_dead(WINDOW)

    pg.quit()

if __name__ == '__main__':
    main()





