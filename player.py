from settings import *
import pygame
from pygame.math import Vector2 as vec
from time import sleep


class Player:

    def __init__(self, screen, position, map_maze, map_size):
        self.screen = screen
        self.home = vec(position.x * XCELL, position.y * YCELL + MAZE_BANNER)
        self.pix_pos = vec(self.home[XX] + PLAYER_RADIO, self.home[YY] + PLAYER_RADIO)
        self.grid_position = [int((self.pix_pos[XX] // XCELL)), int(((self.pix_pos[YY] - MAZE_BANNER) // YCELL))]
        self.new_pix_pos = self.pix_pos
        self.direction = vec(0, 0)
        self.map = map_maze
        self.map_size = map_size
        self.score = 0

    def set_player_position(self):
        position = PLAYER_START_POSITION
        self.home = vec(position.x * XCELL, position.y * YCELL + MAZE_BANNER)
        self.pix_pos = vec(self.home[XX] + PLAYER_RADIO, self.home[YY] + PLAYER_RADIO)
        self.grid_position = [int((self.pix_pos[XX] // XCELL)), int(((self.pix_pos[YY] - MAZE_BANNER) // YCELL))]
        self.new_pix_pos = self.pix_pos

    def reset_player_score(self):
        self.score = 0

    def update_map(self):
        if self.map[self.grid_position[YY]][self.grid_position[XX]] == 0:
            self.map[self.grid_position[YY]][self.grid_position[XX]] = -1
            self.score += 1

    def update(self):
        new_pix_pos = self.pix_pos + self.direction
        new_grid_pos = [int((new_pix_pos[XX] // XCELL)), int(((new_pix_pos[YY] - MAZE_BANNER) // YCELL))]

        if self.map[new_grid_pos[YY]][new_grid_pos[XX]] == MAP_WALL:
            self.direction = vec(0, 0)
            return

        if new_grid_pos[XX] != self.grid_position[XX] or new_grid_pos[YY] != self.grid_position[YY]:
            if self.map[new_grid_pos[YY]][new_grid_pos[XX]] == MAP_PORTAL_RIGHT:
                self.pix_pos[XX] = XCELL
            if self.map[new_grid_pos[YY]][new_grid_pos[XX]] == MAP_PORTAL_LEFT:
                self.pix_pos[XX] = XCELL * (self.map_size[XX] - 1)
            self.grid_position[XX] = int((self.pix_pos[XX] // XCELL))
            self.grid_position[YY] = int(((self.pix_pos[YY] - MAZE_BANNER) // YCELL))
        self.pix_pos += self.direction
        self.update_map()
        sleep(GAME_SLOWER)

    def draw(self):
        pygame.draw.circle(self.screen, PLAYER_COLOR,
                           ((self.grid_position[XX] * XCELL) + (XCELL // 2),
                            (self.grid_position[YY] * YCELL) + (XCELL // 2) + MAZE_BANNER),
                           PLAYER_RADIO)

    def move(self, direction):
        self.direction = direction

    def get_score(self):
        return self.score

    def get_pix_pos(self):
        return self.pix_pos

    def get_grid_pos(self):
        return self.grid_position
