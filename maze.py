import time
from cell import Cell
from window import Window
import random

class Maze:
    """
    num_rows, num_cols (int): Number of rows and collumns on the Maze Matrix
    padding_x, padding_y (int): Distance in pixels that the Maze has from the Window
    cell_size_x, cell_size_y (int): Size that one Cell will have in pixels
        so if a Cell has 10 of size it means that it will have
        padding_x + cell_size_x then padding_y + cell_size_y.
    window (Window | None): Window in which the maze should be draw

    1st Cell top_left_x, top_left_y are the padding_x and padding_y then
    cell_size_<x/y> is the equivalent of bottom_right_x, bottom_right_y Cell position
    next Cell calculate its position based on the previous one.

    If you want a specific maze you can set its seed variable to some int and call update_seed().
    """
    def __init__(
            self,
            num_rows: int,
            num_cols: int,
            padding_x: int,
            padding_y: int,
            cell_size_x: int,
            cell_size_y: int,
            window: Window | None = None,
            seed: int | None = None,
            animation_delay: float = 0.01
        ) -> None:
        self.window: Window | None = window

        self.num_rows: int = num_rows
        self.num_cols: int = num_cols

        self.padding_x: int = padding_x
        self.padding_y: int = padding_y

        self.cell_size_x: int = cell_size_x
        self.cell_size_y: int = cell_size_y

        self.animation_delay: float = animation_delay

        self.seed: int | None = seed
        self.update_seed()

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r()
        self._reset_cells_visited()

    def update_seed(self, seed: int | None = None)-> None:
        """
        Updates radom.seed() based on self.seed, optionally you can pass a seed
        in this method, which will update both self.seed and random.seed() to
        the given seed.
        """
        self.seed = seed if seed else self.seed
        random.seed(self.seed)


    def solve(self) -> bool:
        return self._solve_r(0,0)


    def _solve_r(self, row: int, col: int) -> bool:
        self._animate(self.animation_delay)
        self._cells[row][col].visited = True

        if self._cells[row][col] == self._cells[self.num_rows -1][self.num_cols -1]:
            return True

        if not self._cells[row][col].has_top_wall:
            if row - 1 >= 0: # top
                if not self._cells[row - 1][col].has_bottom_wall and not self._cells[row - 1][col].visited:
                    self._cells[row][col].draw_move(self._cells[row - 1][col])
                    is_right_path = self._solve_r(row -1, col)
                    if is_right_path:
                        return True
                    self._cells[row][col].draw_move(self._cells[row - 1][col], True)

        if not self._cells[row][col].has_bottom_wall:
            if row + 1 < self.num_rows: # bottom
                if not self._cells[row + 1][col].has_top_wall and not self._cells[row + 1][col].visited:

                    self._cells[row][col].draw_move(self._cells[row + 1][col])
                    is_right_path = self._solve_r(row + 1, col)
                    if is_right_path:
                        return True
                    self._cells[row][col].draw_move(self._cells[row + 1][col], True)


        if not self._cells[row][col].has_left_wall:
            if col - 1 >= 0: # left
                if not self._cells[row][col - 1].has_right_wall and not self._cells[row][col - 1].visited:

                    self._cells[row][col].draw_move(self._cells[row][col - 1])
                    is_right_path = self._solve_r(row, col - 1)
                    if is_right_path:
                        return True
                    self._cells[row][col].draw_move(self._cells[row][col - 1], True)

        if not self._cells[row][col].has_right_wall:
            if col + 1 < self.num_cols: # right
                if not self._cells[row][col + 1].has_left_wall and not self._cells[row][col + 1].visited:

                    self._cells[row][col].draw_move(self._cells[row][col + 1])
                    is_right_path = self._solve_r(row, col + 1)
                    if is_right_path:
                        return True
                    self._cells[row][col].draw_move(self._cells[row][col + 1], True)

        return False



    def _create_cells(self) -> None:
        """
        Create a matrix with Cells to draw the maze

        with the maze Maze(Window, 3, 3, 10, 10, 10,10) you get the Matrix:
        [
         [(Cell at 10 10 to 20 20), (Cell at 20 10 to 30 20), (Cell at 30 10 to 40 20)],
         [(Cell at 10 20 to 20 30), (Cell at 20 20 to 30 30), (Cell at 30 20 to 40 30)],
         [(Cell at 10 30 to 20 40), (Cell at 20 30 to 30 40), (Cell at 30 30 to 40 40)]
        ]
        """
        # TODO: Refactor this method to be more easy to understand
        # if possible faster too.

        self._cells: list[list[Cell]] = []

        first_row = True
        for row in range(self.num_rows):
            self._cells.append([])

            first_col = True
            for col in range(self.num_cols):
                if first_row == True:
                    first_row = False
                    first_col = False
                    self._cells[row].append(Cell(
                        self.padding_x,
                        self.padding_y,
                        self.padding_x + self.cell_size_x,
                        self.padding_y + self.cell_size_y,
                        self.window
                    ))
                    continue

                if first_col == True:
                    first_col = False
                    self._cells[row].append(Cell(
                        self.padding_x,
                        self._cells[row-1][0]._top_left_y + self.cell_size_y,
                        self.padding_x + self.cell_size_x,
                        self._cells[row-1][0]._bottom_right_y + self.cell_size_y,
                        self.window
                    ))
                    continue

                self._cells[row].append(Cell(
                    self._cells[row][col-1]._top_left_x + self.cell_size_x,
                    self._cells[row][col-1]._top_left_y,
                    self._cells[row][col-1]._bottom_right_x + self.cell_size_x,
                    self._cells[row][col-1]._bottom_right_y,
                    self.window
                ))
        if self.window:
            self._draw_cell(0.0)


    def _break_entrance_and_exit(self) -> None:
        self._cells[0][0].has_top_wall = False
        self._cells[self.num_rows -1][self.num_cols -1].has_bottom_wall = False
        if self.window:
            self._draw_cell(0.0)


    def _break_walls_r(self, row: int = 0, col: int = 0) -> None:
        """
        Starts at 0,0 and break walls using a depth-first traversal recursive
        technique to create a random maze.

        self.seed affects the randomness of the maze.
        """
        self._cells[row][col].visited = True
        while True:
            to_visit: list[tuple[int,int]] = []
            if row - 1 >= 0: # top
                if not self._cells[row - 1][col].visited:
                    to_visit.append((row -1, col))
            if row + 1 < self.num_rows: # bottom
                if not self._cells[row + 1][col].visited:
                    to_visit.append((row+1, col))

            if col - 1 >= 0: # left
                if not self._cells[row][col - 1].visited:
                    to_visit.append((row, col-1))
            if col + 1 < self.num_cols: # right
                if not self._cells[row][col +1].visited:
                    to_visit.append((row, col +1))

            if len(to_visit) <= 0:
                self._cells[row][col].draw()
                return

            row_cell, col_cell = random.choice(to_visit)
            if row_cell < row and col_cell == col: # moved top
                self._cells[row][col].has_top_wall = False
                self._cells[row_cell][col_cell].has_bottom_wall = False

            if row_cell > row and col_cell == col: # moved bottom
                self._cells[row][col].has_bottom_wall = False
                self._cells[row_cell][col_cell].has_top_wall = False

            if row_cell == row and col_cell < col: # moved left
                self._cells[row][col].has_left_wall = False
                self._cells[row_cell][col_cell].has_right_wall = False

            if row_cell == row and col_cell > col: # moved right
                self._cells[row][col].has_right_wall = False
                self._cells[row_cell][col_cell].has_left_wall = False

            self._break_walls_r(row_cell, col_cell)


    def _reset_cells_visited(self) -> None:
        """
        Make all _cells.visited = False
        """
        for row in self._cells:
            for col in row:
                col.visited = False


    def _draw_cell(self, animation_delay: float) -> None:
        for row in self._cells:
            for cell in row:
                cell.draw()
                self._animate(animation_delay)
    
    def _animate(self, animation_delay: float) -> None:
        """
        Adds a delay into the maze drawing, pass self.animation_delay in case
        you want the default delay instead of passing a custom one.
        """
        if self.window:
            self.window.redraw()
        time.sleep(animation_delay)