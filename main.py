from tkinter import Tk, BOTH, Canvas
import time

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2

    def draw(self, canvas, colour):
        canvas.create_line(self.point_1.x, self.point_1.y, self.point_2.x, self.point_2.y, fill=colour, width=2)


class Window:
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title("Maze Solver")
        self.canvas = Canvas(self.root, width=width, height=height)
        self.canvas.pack()
        self.is_running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.is_running = True
        while self.is_running:
            self.redraw()

    def draw_line(self, line, colour):
        line.draw(self.canvas, colour)

    def close(self):
        self.is_running = False

class Cell:
    def __init__(self, point_tl, point_br, window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.x1 = point_tl.x
        self.y1 = point_tl.y
        self.x2 = point_br.x
        self.y2 = point_br.y
        self.window = window

    def draw(self):
        if self.has_left_wall:
            line = Line(Point(self.x1, self.y1), Point(self.x1, self.y2))
            self.window.draw_line(line, "white")
        if self.has_right_wall:
            line = Line(Point(self.x2, self.y1), Point(self.x2, self.y2))
            self.window.draw_line(line, "white")
        if self.has_top_wall:
            line = Line(Point(self.x1, self.y1), Point(self.x2, self.y1))
            self.window.draw_line(line, "white")
        if self.has_bottom_wall:
            line = Line(Point(self.x1, self.y2), Point(self.x2, self.y2))
            self.window.draw_line(line, "white")

    def draw_move(self, other, undo=False):
        colour = "red"
        if undo:
            colour = "gray"

        line = Line(Point((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2), Point((other.x1 + other.x2) / 2, (other.y1 + other.y2) / 2))
        self.window.draw_line(line, colour)

class MazeCells:
    def __init__(self, x1, y1, num_cols, num_rows, cell_size_x, cell_size_y, win):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.window = win
        self.cells = [[Cell(Point(0,0), Point(0,0), self.window) for _ in range(self.num_rows)] for _ in range(self.num_cols)]

        self.create_cells()

    def create_cells(self):
        for x in range(self.num_cols):
            for y in range(self.num_rows):
                self.cells[x][y] = Cell(Point(self.x1 + x * self.cell_size_x, self.y1 + y * self.cell_size_y), Point(self.x1 + (x + 1) * self.cell_size_x, self.y1 + (y + 1) * self.cell_size_y), self.window)
                if x % 2:
                    self.cells[x][y].has_left_wall = False
                if y % 2:
                    self.cells[x][y].has_right_wall = False
                if x % 3:
                    self.cells[x][y].has_top_wall = False
                if y % 3:
                    self.cells[x][y].has_bottom_wall = False


        for x in range(self.num_cols):
            for y in range(self.num_rows):
                self.cells[x][y].draw()

                self.animate()

    def animate(self):
        self.window.redraw()
        time.sleep(0.01)

def main():
    window = Window(800, 600)
    test = MazeCells(8, 8, 48, 36, 16, 16, window)
    window.wait_for_close()

main()
