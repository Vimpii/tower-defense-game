import pygame as pg
from pygame.math import Vector2
import math


class Enemy(pg.sprite.Sprite):
    def __init__(self, waypoints, image):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(waypoints[0])
        self.target_waypoint = 1
        self.speed = 2
        self.angle = 0
        self.original_image = image
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        self.move()
        self.rotate()

    def move(self):
        if self.target_waypoint < len(self.waypoints):
            # Define a target waypoint
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            self.kill()
        # Calculate distance to target waypoint
        dist = self.movement.length()
        # Check if the enemy has reached the target waypoint
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
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
