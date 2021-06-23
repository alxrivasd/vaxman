import pygame
from settings import *


class Maze:

    def __init__(self, screen):
        self.maze = []
        self.screen = screen
        self.map_width = 0
        self.map_height = 0
        self.pills_count = -1
        self.ghost_home = []

    def read_map(self, map_filename):
        with open(map_filename, 'rt') as f:
            for line in f:
                self.map_width = 0
                self.map_height += 1
                maze_line = []
                for char in line:
                    if char != '\n' and char != ',':
                        maze_line.append(int(char))
                        self.map_width += 1
                        if int(char) == MAP_GHOST_HOME_2:
                            self.ghost_home.append([self.map_width - 1, self.map_height - 1])
                        if int(char) == MAP_PILL:
                            self.pills_count += 1
                first = False
                self.maze.append(maze_line)
        f.close()

    def reload_maze(self):
        del self.maze[:]
        self.pills_count = -1
        self.load_maze()

    def load_maze(self):
        self.read_map(MAP_FILENAME)

    def draw_maze(self):
        x = 0
        y = MAZE_BANNER
        for row in self.maze:
            for col in row:
                if col == MAP_WALL:
                    pygame.draw.rect(self.screen, COLOR_BLUE, (x, y, XCELL, YCELL))
                if col == MAP_GHOST_HOME_2 or col == MAP_GHOST_HOME_4:
                    pygame.draw.rect(self.screen, COLOR_GRAY_L, (x, y, XCELL, YCELL))
                if col == MAP_PILL:
                    pygame.draw.circle(self.screen, COLOR_PILL, ((x + XCELL // 2), (y + YCELL // 2)), 4)
                x += XCELL
            x = 0
            y += YCELL

    def get_maze_size(self):
        map_size = [self.map_width, self.map_height]
        return map_size

