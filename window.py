from tkinter import Tk, BOTH, Canvas

from line import Line

from utils import BACKGROUND_COLOR, LINE_COLOR

class Window:

    def __init__(self, width: int, height: int, title: str) -> None:
        self.__root = Tk()
        self.__root.title(title)
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, bg=BACKGROUND_COLOR, width=width, height=height)
        self.__canvas.pack()
        self.__is_window_running = False


    def redraw(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()
    

    def wait_for_close(self) -> None:
        self.__is_window_running = True
        while self.__is_window_running is True:
            self.redraw()


    def close(self) -> None:
        self.__is_window_running = False


    def draw_line(self, line: Line, fill_color: str = LINE_COLOR) -> None:
        line.draw(self.__canvas, fill_color)