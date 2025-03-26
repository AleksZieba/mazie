import time
from cell import Cell
from window import Window
import random

class Maze:

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

        for row in self._cells:
            for col in row:
                col.visited = False


    def _draw_cell(self, animation_delay: float) -> None:
        for row in self._cells:
            for cell in row:
                cell.draw()
                self._animate(animation_delay)
    
    def _animate(self, animation_delay: float) -> None:

        if self.window:
            self.window.redraw()
        time.sleep(animation_delay)