import pygame as pg
import json
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
import constants as c

# Initialize the game
pg.init()

# Play background music
pg.mixer.init()
pg.mixer.music.load('assets/audio/background_music.mp3')
pg.mixer.music.set_volume(0.1)
pg.mixer.music.play(-1)

# Create clock
clock = pg.time.Clock()

# Create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defense")

# Game variables
game_over = False
game_outcome = 0  # -1 = loss, 0 = ongoing, 1 = win
level_started = False
last_enemy_spawn = pg.time.get_ticks()
placing_turrets = False
selected_turret = None

# Load images
# Map
map_img = pg.image.load("levels/level.png").convert_alpha()
# Turret spritesheets
turret_spritesheets = []
for i in range(1, c.TURRET_LEVELS + 1):
    turret_sheet = pg.image.load(f"assets/images/turrets/turret_{i}.png").convert_alpha()
    turret_spritesheets.append(turret_sheet)
# Individual turret image for  mouse cursor
cursor_turret = pg.image.load("assets/images/turrets/cursor_turret.png").convert_alpha()
# Enemies
enemy_images = {
    "weak": pg.image.load("assets/images/enemies/enemy_1.png").convert_alpha(),
    "medium": pg.image.load("assets/images/enemies/enemy_2.png").convert_alpha(),
    "strong": pg.image.load("assets/images/enemies/enemy_3.png").convert_alpha(),
    "elite": pg.image.load("assets/images/enemies/enemy_4.png").convert_alpha()
}
# Buttons
buy_turret_img = pg.image.load("assets/images/buttons/buy_turret.png").convert_alpha()
cancel_img = pg.image.load("assets/images/buttons/cancel.png").convert_alpha()
upgrade_turret_img = pg.image.load("assets/images/buttons/upgrade_turret.png").convert_alpha()
begin_img = pg.image.load("assets/images/buttons/begin.png").convert_alpha()
restart_img = pg.image.load("assets/images/buttons/restart.png").convert_alpha()
fast_forward_img = pg.image.load("assets/images/buttons/fast_forward.png").convert_alpha()
# GUI
heart_img = pg.image.load("assets/images/gui/heart.png").convert_alpha()
coin_img = pg.image.load("assets/images/gui/coin.png").convert_alpha()
logo_img = pg.image.load("assets/images/gui/cover.png").convert_alpha()

# Load sounds
shot_fx = pg.mixer.Sound("assets/audio/shot.wav")
shot_fx.set_volume(0.2)

# Load JSON data
with open("levels/level.tmj") as file:
    world_data = json.load(file)
    print(world_data)

# Load fonts
text_font = pg.font.SysFont("Consolas", 24, bold=True)
large_font = pg.font.SysFont("Consolas", 36)


# Function for outputting text to screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def display_data():
    # Draw panel
    pg.draw.rect(screen, "maroon", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, c.SCREEN_HEIGHT))
    pg.draw.rect(screen, "purple", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, 400), 3)
    screen.blit(logo_img, (c.SCREEN_WIDTH, 400))
    # Display
    draw_text("LEVEL: " + str(world.level), text_font, "grey100", c.SCREEN_WIDTH + 10, 10)
    screen.blit(heart_img, (c.SCREEN_WIDTH + 10, 35))
    draw_text(str(world.health), text_font, "grey100", c.SCREEN_WIDTH + 50, 40)
    screen.blit(coin_img, (c.SCREEN_WIDTH + 10, 65))
    draw_text(str(world.money), text_font, "grey100", c.SCREEN_WIDTH + 50, 70)


def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    # Calculate the sequential index of the tile
    mouse_tile_num = (mouse_tile_y * c.COLUMNS) + mouse_tile_x
    # Check if the tile is grass
    if world.tile_map[mouse_tile_num] == 7:
        # Check if there is already a turret on the tile
        space_is_free = True
        for turret in turret_group:
            if turret.tile_x == mouse_tile_x and turret.tile_y == mouse_tile_y:
                space_is_free = False
                break
        # Create a turret if the space is free
        if space_is_free:
            new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y, shot_fx)
            turret_group.add(new_turret)
            # Deduct the cost of the turret
            world.money -= c.BUY_COST


def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    for turret in turret_group:
        if turret.tile_x == mouse_tile_x and turret.tile_y == mouse_tile_y:
            return turret


def clear_selection():
    for turret in turret_group:
        turret.selected = False


# Create world
world = World(world_data, map_img)
world.process_data()
world.process_enemies()

# Create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

# Create buttons
turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_img, True)
cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_img, True)
upgrade_button = Button(c.SCREEN_WIDTH + 5, 180, upgrade_turret_img, True)
begin_button = Button(c.SCREEN_WIDTH + 60, 300, begin_img, True)
restart_button = Button(310, 300, restart_img, True)
fast_forward_button = Button(c.SCREEN_WIDTH + 50, 300, fast_forward_img, False)

# Game loop
run = True
while run:

    clock.tick(c.FPS)

    ############################
    # UPDATING SECTION
    ############################

    if not game_over:
        # Check if player has lost
        if world.health <= 0:
            game_over = True
            game_outcome = -1  # loss
        # Check if player has won
        if world.level > c.TOTAL_LEVELS:
            game_over = True
            game_outcome = 1  # win

        # Update groups
        enemy_group.update(world)
        turret_group.update(enemy_group, world)

        # Highlight selected turret
        if selected_turret:
            selected_turret.selected = True

    ############################
    # DRAWING SECTION
    ############################

    screen.fill("grey100")

    # Draw world
    world.draw(screen)

    # Draw enemy path
    # pg.draw.lines(screen, "red", False, world.waypoints, 5)

    # Draw groups
    enemy_group.draw(screen)
    for turret in turret_group:
        turret.draw(screen)

    display_data()

    if not game_over:
        # Check if the level has started
        if not level_started:
            if begin_button.draw(screen):
                level_started = True
        else:
            # Fast-forward option
            world.game_speed = 1
            if fast_forward_button.draw(screen):
                world.game_speed = 5
            # Spawn enemies
            if pg.time.get_ticks() - last_enemy_spawn > (c.SPAWN_COOLDOWN - world.level * 5):
                if world.spawned_enemies < len(world.enemy_list):
                    enemy_type = world.enemy_list[world.spawned_enemies]
                    enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                    enemy_group.add(enemy)
                    world.spawned_enemies += 1
                    last_enemy_spawn = pg.time.get_ticks()

        # Check if the wave is finished
        if world.check_level_complete():
            world.money += c.LEVEL_COMPLETE_REWARD
            level_started = False
            world.level += 1
            last_enemy_spawn = pg.time.get_ticks()
            world.reset_level()
            world.process_enemies()

        # Draw buttons
        # Button for placing turrets
        # Show the cost of turret
        draw_text(str(c.BUY_COST), text_font, "grey100", c.SCREEN_WIDTH + 205, 135)
        screen.blit(coin_img, (c.SCREEN_WIDTH + 250, 130))
        if turret_button.draw(screen):
            placing_turrets = True
        # If placing turrets is enabled, show the cancel button
        if placing_turrets:
            # Show cursor turret
            cursor_rect = cursor_turret.get_rect()
            cursor_pos = pg.mouse.get_pos()
            cursor_rect.center = cursor_pos
            if cursor_pos[0] < c.SCREEN_WIDTH:
                screen.blit(cursor_turret, cursor_rect)
            if cancel_button.draw(screen):
                placing_turrets = False
        # If a turret is selected, show the upgrade button
        if selected_turret:
            # If a turret can be upgraded, show the upgrade button
            if selected_turret.upgrade_level < c.TURRET_LEVELS:
                # Show the cost of turret upgrade
                draw_text(str(c.UPGRADE_COST), text_font, "grey100", c.SCREEN_WIDTH + 215, 195)
                screen.blit(coin_img, (c.SCREEN_WIDTH + 260, 190))
                if upgrade_button.draw(screen):
                    if world.money >= c.UPGRADE_COST:
                        world.money -= c.UPGRADE_COST
                        selected_turret.upgrade()
    else:
        pg.draw.rect(screen, "dodgerblue", (200, 200, 400, 200), border_radius=30)
        if game_outcome == -1:
            draw_text("GAME OVER", large_font, "black", 310, 230)
        elif game_over == 1:
            draw_text("YOU WIN!", large_font, "white", 310, 230)
        # Restart level
        if restart_button.draw(screen):
            game_over = False
            level_started = False
            placing_turrets = False
            last_enemy_spawn = pg.time.get_ticks()
            world = World(world_data, map_img)
            world.process_data()
            world.process_enemies()
            # Empty groups
            enemy_group.empty()
            turret_group.empty()

    # Event handling
    for event in pg.event.get():
        # Quit program
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            # Check if mouse is within the game window
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                # Clear selection
                selected_turret = None
                clear_selection()
                if placing_turrets:
                    # Check if there is enough money to buy a turret
                    if world.money >= c.BUY_COST:
                        create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)

    # Update display
    pg.display.flip()

pg.quit()
