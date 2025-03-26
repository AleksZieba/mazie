from cell import Cell
from line import Line
from maze import Maze
from point import Point
from window import Window


def main():
    """
    x=0 is the left of the screen.
    y=0 is the top of the screen.
    """
    win = Window(800, 800, "Beautiful window")
    '''
    point_A = Point(10,100)
    point_B = Point(100,10)
    line = Line(point_A, point_B)
    point_C = Point(10,10)
    point_D = Point(100,100)
    line2 = Line(point_C, point_D)
    win.draw_line(line, "#232136")
    win.draw_line(line2, "#232136")

    cell1 = Cell(win, 10, 10, 20, 20)
    cell1.has_right_wall = False
    cell1.has_left_wall = False

    cell2 = Cell(win, 20, 10, 30, 20)
    cell2.has_left_wall = False
    cell2.has_bottom_wall = False

    cell3 = Cell(win, 20, 20, 30, 30)
    cell3.has_top_wall = False
    cell3.has_bottom_wall = False

    cell4 = Cell(win, 20, 30, 30, 40)
    cell4.has_top_wall = False

    cell1.draw()
    cell2.draw()
    cell1.draw_move(cell2)
    cell3.draw()
    cell2.draw_move(cell3, True)
    cell4.draw()
    cell3.draw_move(cell4, True)
    '''

    maze = Maze(25, 25, 10, 10, 30, 30, win, animation_delay=0.05)
    maze.solve()

    win.wait_for_close()


if __name__ == "__main__":
    main()