import pygame
import logic as l
import board as b
import numpy as np
import constants as const

from gym import Env
from gym.spaces import Discrete, Box

rows = 4
cols = 4
black = 0, 0, 0
white = 222, 222, 222

class TwentyFortyEightEnv(Env):
    def __init__(self):
        self.game = l.TwentyFortyEight(4, 4, const.OFFSETS_LIST)
        self.action_space = Discrete(4)
        self.observation_space = Box(low=np.array(16*[0]), high=np.array(16*[131072]))
        self.state = np.array(self.game.get_game_state()).flatten()
        self.board, self.screen, self.font, self.SIZE = vis_init(self.game)
        self.render_mode = 'human'
        
    def step(self, action):
        old_score = self.game.get_score()
        self.game.move(action)
        game_state = np.array(self.game.get_game_state()).flatten()
        self.board.update_board(self.game.get_game_state())
        if self.render_mode == "human":
            self.render()

        new_score = self.game.get_score()
        points = new_score - old_score
        info = {}

        return game_state, points, self.game.is_game_over(), info

    def render(self):
        score = self.game.get_score()
        textsurface = self.font.render(f'Score: {score}', True, white)
        self.screen.fill(pygame.Color("black"))
        self.board.draw_board()
        self.board.draw_tiles()
        self.screen.blit(self.board.get_board(), (0, 0))
        self.screen.blit(textsurface, (20, self.SIZE[1]-80))
        pygame.display.update()
        pygame.display.flip()
        pass
    
    def reset(self):
        highest_tile = np.array(self.game.get_game_state()).flatten().max()
        print(f"\nHighest tile: {highest_tile}, Score: {self.game.get_score()}")
        append_to_file("highest_tile.txt", f"{str(highest_tile)}, ")

        self.game.reset()
        self.state = np.array(self.game.get_game_state()).flatten()
        self.board.update_board(self.state)
        return self.state

    def close(self):
        pygame.quit()

def vis_init(twenty_forty_eight):
    pygame.init()
    pygame.display.set_caption("2048")

    SIZE = width, height = cols * const.TILE_SIZE + (cols + 1) * const.PADDING,\
                        rows * const.TILE_SIZE + (rows + 1) * const.PADDING + 100
    screen = pygame.display.set_mode(SIZE)

    board = b.Board(rows, cols, twenty_forty_eight.get_game_state(), const.PADDING, const.TILE_SIZE,
                    const.BACKGROUND_COLOR, const.BACKGROUND_COLOR_EMPTY_TILE, const.BACKGROUND_TILE_COLORS,
                    const.TILE_COLORS, const.FONT)

    font = pygame.font.SysFont('Comic Sans MS', const.TEXT_SIZE)

    screen.fill(black)
    return board, screen, font, SIZE

def append_to_file(filename, data):
    f = open(filename, "a")
    f.write(data)
    f.close()