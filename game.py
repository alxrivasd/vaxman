import sys
import pygame.time
from ghost import *
from player import *
from Maze import *
from score import *
from utils import *

pygame.init()
vec = pygame.math.Vector2


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GAME_STATE_INTRO
        self.utils = Utils(self.screen)
        self.maze = Maze(self.screen)
        self.maze.load_maze()
        self.player = Player(self.screen, PLAYER_START_POSITION, self.maze.maze, self.maze.get_maze_size())
        self.SPAWN_ENEMY = pygame.USEREVENT
        self.EASY = True
        self.now_timer = GAME_TIMER_EASY
        self.set_timer(self.now_timer)
        self.great_score = 0
        self.scores = Score()
        self.enemies = []
        self.restart(True)
        self.counter = 0

    def remove_enemies(self):
        del self.enemies[:]

    def restart(self, reset_score):
        if reset_score:
            self.great_score = 0
            self.scores.set_score(0)
            self.state = GAME_STATE_INTRO
        else:
            self.great_score += self.player.get_score()
        self.player.set_player_position()
        self.player.reset_player_score()
        self.maze.reload_maze()
        self.spawn_enemies()

    def spawn_enemies(self):
        self.enemies.append(Ghost(GHOST_INKY, self.screen, self.maze))
        self.enemies.append(Ghost(GHOST_BLINKY, self.screen, self.maze))

    def count_vaccinated_not(self):
        vaccinated_num = 0
        for ghost in self.enemies:
            if not ghost.vaccinated:
                vaccinated_num += 1
        return vaccinated_num

    def count_vaccinated(self):
        vaccinated_num = 0
        for ghost in self.enemies:
            if ghost.vaccinated:
                vaccinated_num += 1
        return vaccinated_num

    def duplicate_enemies(self):
        for _ in range(self.count_vaccinated_not()):
            self.enemies.append(Ghost(random.randint(0, 3), self.screen, self.maze))

    def check_game_status(self):
        if self.player.get_score() >= self.maze.pills_count:
            self.state = GAME_STATE_WIN
        if self.count_vaccinated_not() >= MAX_GHOST_LOSE:
            self.state = GAME_STATE_LOSE

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == self.SPAWN_ENEMY:
                self.duplicate_enemies()
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))
                if event.key == pygame.K_p:
                    self.player.move(vec(0, 0))

    def playing_update(self):
        self.check_game_status()
        self.player.update()
        for ghost in self.enemies:
            ghost.update(self.player.get_grid_pos())

    def playing_draw(self):
        print(self.now_timer)
        self.screen.fill(COLOR_BLACK)
        self.maze.draw_maze()
        self.utils.draw_grid()
        self.scores.set_score(self.great_score + self.player.get_score())
        self.utils.draw_score(self.scores.score, len(self.enemies), self.count_vaccinated_not(), self.EASY)
        self.player.draw()
        for ghost in self.enemies:
            ghost.draw()
        pygame.display.update()

    def set_timer(self, x_timer):
        pygame.time.set_timer(self.SPAWN_ENEMY, x_timer)

    def intro_update(self):
        pass

    def intro_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                self.EASY = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                self.EASY = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = GAME_STATE_PLAY
                if self.EASY:
                    self.set_timer(GAME_TIMER_EASY)
                else:
                    self.set_timer(GAME_TIMER_HARD)

    def intro_draw(self):
        self.screen.fill(COLOR_BLACK)
        self.utils.draw_score(self.scores.high, 0, 0, self.EASY)
        vax_text_pos = [80, 80]
        self.utils.draw_text(GAME_TITLE,
                             vax_text_pos, FONT_INTRO_FAMILY, FONT_VAXMAN_SIZE_32, COLOR_YELLOW, x_center=True)
        self.utils.draw_text(GAME_TEXT_START,
                             TEXT_START_POSITION, FONT_INTRO_FAMILY, FONT_INTRO_SIZE, COLOR_ORANGE, True, True)
        vax_text_pos[YY] = 420
        self.utils.draw_text(GAME_TEXT_START1,
                             vax_text_pos, FONT_INTRO_FAMILY, TEXT_SIZE_16, COLOR_BLUE, True, False)
        vax_text_pos[YY] = 440
        self.utils.draw_text(GAME_TEXT_START2,
                             vax_text_pos, FONT_INTRO_FAMILY, TEXT_SIZE_16, COLOR_RED, True, False)
        pygame.display.update()

    def lossing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.remove_enemies()
                self.restart(True)

    def lossing_draw(self):
        self.screen.fill(COLOR_RED)
        self.utils.draw_text(GAME_TEXT_LOSE,
                             TEXT_START_POSITION, FONT_INTRO_FAMILY, 64, COLOR_BLACK, True, True)
        vax_text_pos = [80, 440]
        self.utils.draw_text(GAME_TEXT_START,
                             vax_text_pos, FONT_INTRO_FAMILY, FONT_INTRO_SIZE, COLOR_BLACK, True)
        pygame.display.update()

    def winning_draw(self):
        self.screen.fill(COLOR_GREEN)
        self.utils.draw_text(GAME_TEXT_WIN,
                             TEXT_START_POSITION, FONT_INTRO_FAMILY, 48, COLOR_BLACK, True, True)
        vax_text_pos = [80, 440]
        self.utils.draw_text(GAME_TEXT_START,
                             vax_text_pos, FONT_INTRO_FAMILY, FONT_INTRO_SIZE, COLOR_BLACK, True)
        pygame.display.update()

    def winning_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.remove_enemies()
                self.now_timer -= TIMER_HARDENING
                self.set_timer(self.now_timer)
                self.restart(False)
                self.state = GAME_STATE_PLAY

    def run(self):
        self.clock.tick(CLOCK_FPS)
        while self.running:
            if self.state == GAME_STATE_INTRO:
                self.intro_events()
                self.intro_update()
                self.intro_draw()
            if self.state == GAME_STATE_PLAY:
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            if self.state == GAME_STATE_WIN:
                self.winning_events()
                self.winning_draw()
            if self.state == GAME_STATE_LOSE:
                self.lossing_events()
                self.lossing_draw()
        self.set_timer(0)
        pygame.quit()
        sys.exit()
