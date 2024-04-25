import pygame as pg
import random
import constants as c
from enemy_data import ENEMY_SPAWN_DATA


class World:
    def __init__(self, data, map_img):
        self.level = 1
        self.health = c.HEALTH
        self.money = c.MONEY
        self.tile_map = []
        self.waypoints = []
        self.level_data = data
        self.img = map_img
        self.enemy_list = []
        self.spawned_enemies = 0

    def process_data(self):
        # Extract relevant info
        for layer in self.level_data["layers"]:
            if layer["name"] == "tilemap":
                self.tile_map = layer["data"]
            elif layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    waypoint_data = obj["polyline"]
                    self.process_waypoints(waypoint_data)

    def process_waypoints(self, data):
        for point in data:
            temp_x = point.get("x")
            temp_y = point.get("y")
            self.waypoints.append((temp_x, temp_y))

    def process_enemies(self):
        enemies = ENEMY_SPAWN_DATA[self.level - 1]
        for enemy_type in enemies:
            enemies_to_spawn = enemies[enemy_type]
            for enemy in range(enemies_to_spawn):
                self.enemy_list.append(enemy_type)
        # Randomize the order of the enemies
        random.shuffle(self.enemy_list)

    def draw(self, surface):
        surface.blit(self.img, (0, 0))
