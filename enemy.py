import math
import pygame as pg
from pygame.math import Vector2
import constants as c
from enemy_data import ENEMY_DATA


class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_type,waypoints, images):
        pg.sprite.Sprite.__init__(self)
        self.movement = None
        self.target = None
        self.waypoints = waypoints
        self.pos = Vector2(waypoints[0])
        self.target_waypoint = 1
        self.health = ENEMY_DATA.get(enemy_type).get("health")
        self.speed = ENEMY_DATA.get(enemy_type).get("speed")
        self.angle = 0
        self.original_image = images.get(enemy_type)
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, world):
        self.move(world)
        self.rotate()
        self.check_alive(world)

    def move(self, world):
        if self.target_waypoint < len(self.waypoints):
            # Define a target waypoint
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            self.kill()
            world.health -= 1
            world.missed_enemies += 1

        # Calculate distance to target waypoint
        dist = self.movement.length()
        # Check if the enemy has reached the target waypoint
        if dist >= (self.speed * world.game_speed):
            self.pos += self.movement.normalize() * (self.speed * world.game_speed)
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

    def rotate(self):
        # Calculate distance to next waypoint
        dist = self.target - self.pos
        # Use distance to calculate angle
        self.angle = math.degrees(math.atan2(-dist.y, dist.x))
        # Rotate the image and update the rect
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def check_alive(self, world):
        if self.health <= 0:
            world.killed_enemies += 1
            world.money += c.KILL_REWARD
            self.kill()
