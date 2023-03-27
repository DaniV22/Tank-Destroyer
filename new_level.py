from enemy import EnemyTank
from obstacles import Obstacles
from tank import Tank
from parameters import get_parameters

WIDTH, HEIGHT, FLOOR_WIDTH, FLOOR_HEIGHT, FLOOR_POS, COLORS, gravity = get_parameters()

def create_new_level(level):

    '''
    
    A function that defines the parameters of the game depending on the current level of the game.
    It changes the number of enemies, their positions and the obstacles.

    Parameters : 
    
        level (int) :      The current level of the game.

    Returns :

        tank (Tank) :      The tank object of the player.
        enemies (list) :   A list of enemy tank objects that contains the enemies of the new level.
        obstacles (Obstacles) : An object of the Obstacles class that contains the obstacles of the new level.

    '''

    if level == 1:
        tank = Tank(100, FLOOR_POS[1] - 54)

        enemies = [EnemyTank(700, FLOOR_POS[1] - 54, 100000)]   #Not firing

        obstacles = Obstacles()
        obstacles.add_obstacle(500, HEIGHT/2 + 50, 40, HEIGHT/2)

    elif level == 2:
        tank = Tank(100, FLOOR_POS[1] - 54 )

        enemies = [EnemyTank(700, FLOOR_POS[1] - 54, 5000)]

        obstacles = Obstacles()
        obstacles.add_obstacle(500, HEIGHT/2 + 50, 40, HEIGHT/2)

    elif level == 3:
        tank = Tank(100, FLOOR_POS[1] - 54 )

        enemies = [EnemyTank(700, FLOOR_POS[1] - 54, 4000),
                   EnemyTank(1000, FLOOR_POS[1] - 54, 5500)]
        
        obstacles = Obstacles()
        obstacles.add_obstacle(500, HEIGHT/2 + 50, 40, HEIGHT/2)

    elif level == 4:
        tank = Tank(100, FLOOR_POS[1] - 54 )

        enemies = [EnemyTank(700, FLOOR_POS[1] - 54, 2500),
                   EnemyTank(1000, FLOOR_POS[1] - 54, 3500)]
        
        obstacles = Obstacles()
        obstacles.add_obstacle(500, HEIGHT/2 + 50, 40, HEIGHT/2)

    elif level == 5:
        tank = Tank(100, FLOOR_POS[1] - 54 )

        enemies = [EnemyTank(700, FLOOR_POS[1] - 54, 3000),
                   EnemyTank(1000, FLOOR_POS[1] - 54, 3500), EnemyTank(850, FLOOR_POS[1] - 54, 4000)]
        
        obstacles = Obstacles()
        obstacles.add_obstacle(500, HEIGHT/2 + 50, 40, HEIGHT/2)

    elif level == 6:
        tank = Tank(100, FLOOR_POS[1] - 54 )

        enemies = [EnemyTank(700, FLOOR_POS[1] - 54, 3500),
                   EnemyTank(1000, FLOOR_POS[1] - 54, 3000),
                   EnemyTank(1000, HEIGHT/2 - 104, 2000)]
        
        obstacles = Obstacles()
        obstacles.add_obstacle(500, HEIGHT/2 + 50, 40, HEIGHT/2)
        obstacles.add_obstacle(WIDTH / 2 + 250, HEIGHT/2 - 50, WIDTH / 2 - 250, 40)

    elif level == 7:
        tank = Tank(100, FLOOR_POS[1] - 54 )

        enemies = [EnemyTank(700, FLOOR_POS[1] - 54, 3500),
                   EnemyTank(1000, FLOOR_POS[1] - 54, 3000),
                   EnemyTank(1000, HEIGHT/2 - 104, 2000),
                   EnemyTank(900, HEIGHT/2 - 104, 4500)]
        
        obstacles = Obstacles()
        obstacles.add_obstacle(500, HEIGHT/2 + 50, 40, HEIGHT/2)
        obstacles.add_obstacle(WIDTH / 2 + 250, HEIGHT/2 - 50, WIDTH / 2 - 250, 40)

    elif level == 8:
        tank = Tank(100, FLOOR_POS[1] - 54 )

        enemies = [EnemyTank(700, FLOOR_POS[1] - 54, 3500),
                   EnemyTank(1000, FLOOR_POS[1] - 54, 3000),
                   EnemyTank(1000, HEIGHT/2 - 104, 2000),
                   EnemyTank(900, HEIGHT/2 - 104, 4500), EnemyTank(550, 96, 100)]
        
        obstacles = Obstacles()
        obstacles.add_obstacle(500, HEIGHT/2 + 50, 40, HEIGHT/2)
        obstacles.add_obstacle(WIDTH / 2 + 250, HEIGHT/2 - 50, WIDTH / 2 - 250, 40)
        obstacles.add_obstacle(500, 150, 200, 40)

    return tank, enemies, obstacles