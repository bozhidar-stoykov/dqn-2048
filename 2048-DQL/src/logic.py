"""
Clone of 2048 game.
"""
import sys
import random
import constants as cons

def merge(line):
    """
    Helper function that merges a single row or column in 2048.
    """
    points = 0
    n_elements = len(line)
    # Remove 0 entries and slide to the left
    line = [value for value in line if value != 0]
    index = 0
    # Iterate while there are possible pairs
    while index < len(line)-1:
        # If a pair is found, merge
        # and remove second element
        if line[index] == line[index+1]:
            line[index] *= 2
            line.pop(index+1)
            points += line[index]
        # Move on to next item
        index += 1
    # Fill the merged line with 0s so it has the
    # same number of elements than the original
    line += [0]*(n_elements-len(line))
    return line, points


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width, offsets):
        self._offsets = offsets
        self._height = grid_height
        self._width = grid_width
        self._grid = None
        self._score = 0
        self.reset()
        self._initial_tiles = [[(0, col, self._height) for col in range(self._width)],
                               [(-1, col, self._height) for col in range(self._width)],
                               [(row, 0, self._width) for row in range(self._height)],
                               [(row, -1, self._width) for row in range(self._height)]]

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._score = 0
        self._grid = [[0]*self._width for dummy_i in range(self._height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self._grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        moved = False
        displacement_vector = list(self._offsets[direction])
        initial_tiles = [list(initial_t) for initial_t in self._initial_tiles[direction]]
        # Get row/col to merge in the correct order
        for tile_pos in initial_tiles:
            to_merge = []
            for dummy_i in range(tile_pos[2]):
                to_merge += [self.get_tile(tile_pos[0], tile_pos[1])]
                tile_pos[0] += displacement_vector[0]
                tile_pos[1] += displacement_vector[1]
            merged, points = merge(to_merge)
            merged.reverse()
            self.set_score(self.get_score() + points)
            for index in range(tile_pos[2]):
                tile_pos[0] -= displacement_vector[0]
                tile_pos[1] -= displacement_vector[1]
                if merged[index] != self.get_tile(tile_pos[0], tile_pos[1]):
                    moved = True
                self.set_tile(tile_pos[0], tile_pos[1], merged[index])
        if moved:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # Look for empty tiles
        candidate_tiles = []
        for row_index in range(self._height):
            for col_index in range(self._width):
                if self._grid[row_index][col_index] == 0:
                    candidate_tiles += [(row_index, col_index)]
        # Randomly select tile
        if candidate_tiles:
            tile_pos = random.choice(candidate_tiles)
            tile_row, tile_col = tile_pos[0], tile_pos[1]
            # Randomly select value with probs: 2->90%, 4->10%
            tile_value = 2 if random.random() <= 0.9 else 4
            self.set_tile(tile_row, tile_col, tile_value)

    def is_game_over(self):
        """
        Check if the game is over
        """
        # Check if there are empty tiles
        for row_index in range(self._height):
            for col_index in range(self._width):
                if self._grid[row_index][col_index] == 0:
                    return False
        # Check if there are possible moves
        for direction in self._offsets:
            for row_index in range(self._height):
                for col_index in range(self._width):
                    move_row = row_index + direction[0]
                    move_col = col_index + direction[1]

                    if (move_row >= 0 and move_row < self._height and
                        move_col >= 0 and move_col < self._width):
                            if self._grid[row_index][col_index] == self._grid[move_row][move_col]:
                                return False

        return True

    def get_possible_moves(self):
        """
        Return a list of all possible moves
        """
        possible_moves = []
        for direction in self._offsets:
            for row_index in range(self._height):
                for col_index in range(self._width):
                    move_row = row_index + direction[0]
                    move_col = col_index + direction[1]

                    if (move_row >= 0 and move_row < self._height and
                        move_col >= 0 and move_col < self._width):
                            if self._grid[row_index][col_index] == self._grid[move_row][move_col]:
                                possible_moves += [direction]
                                break
        return possible_moves

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]

    def get_game_state(self):
        """
        Return the game grid at its current state
        """
        return self._grid

    def get_score(self):
        """
        Return the current score
        """
        return self._score

    def set_score(self, score):
        """
        Set the current score
        """
        self._score = score
