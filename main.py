import pygame as pg
from enemy import Enemy
import constants as c

# Initialize the game
pg.init()

# Create clock
clock = pg.time.Clock()

# Create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defense")

# Load images
enemy_img = pg.image.load("assets/images/enemies/enemy_1.png").convert_alpha()

# Create groups
enemy_group = pg.sprite.Group()

waypoints = [(200, 300), (600, 300), (600, 100), (400, 100), (400, 500), (800, 500)]

enemy = Enemy(waypoints, enemy_img)
enemy_group.add(enemy)

# Game loop
run = True
while run:

    clock.tick(c.FPS)

    screen.fill("grey100")

    # Draw enemy path
    pg.draw.lines(screen, "red", False, waypoints, 5)

    # Update groups
    enemy_group.update()

    # Draw groups
    enemy_group.draw(screen)

    # Event handling
    for event in pg.event.get():
        # Quit program
        if event.type == pg.QUIT:
            run = False

    # Update display
    pg.display.flip()

pg.quit()
