import pygame
from settings import *


class Utils:
    def __init__(self, screen):
        self.screen = screen

    def draw_text(self, text, position, font_name, font_size, font_color, x_center=False, y_center=False):
        font = pygame.font.SysFont(font_name, font_size)
        writing = font.render(text, False, font_color)
        if x_center:
            writing_size = writing.get_size()
            position[0] = SCREEN_WIDTH // 2 - writing_size[0] // 2
        if y_center:
            writing_size = writing.get_size()
            position[1] = SCREEN_HEIGHT // 2 - writing_size[1] // 2
        self.screen.blit(writing, position)

    def draw_score(self, score, enemies, vaccinated, mode):
        if mode:
            md = 'Easy'
        else:
            md = 'HARD'
        temp_text = f'SCORE: {score}    Enemies:{enemies}   Vaccinated:{vaccinated} - {md}'
        self.draw_text(temp_text, TEXT_SCORE_POSITION, FONT_INTRO_FAMILY, TEXT_SIZE_20, COLOR_WHITE)

    def draw_grid(self):
        for x in range(MAZE_WIDTH // XCELL):

            pygame.draw.line(self.screen, COLOR_GRAY, (x * XCELL, MAZE_BANNER), (x * XCELL, SCREEN_HEIGHT))
        for y in range(MAZE_HEIGHT // YCELL):
            yy = y * YCELL + MAZE_BANNER
            pygame.draw.line(self.screen, COLOR_GRAY, (0, yy), (MAZE_WIDTH, yy))
