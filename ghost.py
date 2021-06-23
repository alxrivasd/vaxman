import random
import pygame
from pygame.math import Vector2 as vec
from settings import *
from time import sleep


def get_grid_position(new_pos):
    return [int((new_pos[XX] // XCELL)), int(((new_pos[YY] - MAZE_BANNER) // YCELL))]


class Ghost:

    def __init__(self, ghost_num, screen, map_maze):
        self.ghost_id = ghost_num
        self.screen = screen
        self.map = map_maze
        self.home = vec(self.map.ghost_home[self.ghost_id][XX] * XCELL,
                        self.map.ghost_home[self.ghost_id][YY] * YCELL + MAZE_BANNER)
        self.pix_pos = vec(self.home[XX] + PLAYER_RADIO, self.home[YY] + PLAYER_RADIO)
        self.grid_position = [int((self.pix_pos[XX] // XCELL)), int(((self.pix_pos[YY] - MAZE_BANNER) // YCELL))]
        self.rotation = [DIR_RIGHT, DIR_DOWN, DIR_LEFT, DIR_UP]
        self.neighbours = [DIR_DOWN, DIR_RIGHT, DIR_UP, DIR_LEFT]
        self.rotation_id = self.ghost_id
        self.stage = 'warming'
        self.moves = random.randint(1, 4)
        self.player_grid = [0, 0]
        self.direction = self.rotation[self.ghost_id]
        self.init_direction()
        self.vaccinated = False

    def init_direction(self):
        if self.ghost_id == 0:
            self.direction = self.rotation[2]
        elif self.ghost_id == 2:
            self.direction = self.rotation[0]

    def hit_wall(self, new_pos):
        if self.map.maze[new_pos[YY]][new_pos[XX]] == MAP_WALL:
            return True
        return False

    def move_random(self):
        while True:
            dirs = random.choice(self.rotation)
            new_pos = self.pix_pos + dirs
            if not self.hit_wall(get_grid_position(new_pos)):
                return dirs

    def move_fast(self):
        while True:
            dirs = random.choice(self.rotation)
            new_pos = self.pix_pos + (dirs * 2)
            if not self.hit_wall(get_grid_position(new_pos)):
                return dirs

    def move(self):
        self.pix_pos += self.direction
        self.grid_position = get_grid_position(self.pix_pos)

    def check_vaccinated(self, new_grid_pos):
        if new_grid_pos[XX] == self.player_grid[XX] and new_grid_pos[YY] == self.player_grid[YY]:
            self.vaccinated = True

    def think_to_move(self):
        new_pix_pos = self.pix_pos + self.direction
        new_grid_pos = get_grid_position(new_pix_pos)

        if new_grid_pos[XX] != self.grid_position[XX] or new_grid_pos[YY] != self.grid_position[YY]:
            if self.hit_wall(new_grid_pos):
                if self.moves > 0:
                    self.moves -= 1
                else:
                    if self.stage == 'warming':
                        self.rotation_id = self.ghost_id
                        self.stage = 'out'

                if self.stage == 'out':
                    self.pix_pos += self.direction
                    self.stage = 'play'
                    return True
                if self.stage == 'play':
                    if self.ghost_id == 0:
                        self.direction = self.move_random()
                    if self.ghost_id == 1:
                        self.direction = self.move_fast()
                    if self.ghost_id == 2:
                        self.direction = self.move_random()
                    if self.ghost_id == 3:
                        self.direction = self.move_fast()
                if self.stage == 'warming':
                    self.rotation_id += 1
                    self.direction = self.rotation[self.rotation_id % 4]
                return False
        return True

    def update(self, player_grid):
        self.player_grid = player_grid
        if self.think_to_move():
            self.move()
            self.check_vaccinated(self.grid_position)

    def draw(self):
        if self.vaccinated:
            color = GHOST_COLORS[4]
        else:
            color = GHOST_COLORS[self.ghost_id]
        pygame.draw.circle(self.screen, color,
                           ((self.grid_position[XX] * XCELL) + (XCELL // 2),
                            (self.grid_position[YY] * YCELL) + (XCELL // 2) + MAZE_BANNER),
                           PLAYER_RADIO, 2)
