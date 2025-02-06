from tkinter import Tk, BOTH, Canvas

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
            self.window.draw_line(line, "black")
        if self.has_right_wall:
            line = Line(Point(self.x2, self.y1), Point(self.x2, self.y2))
            self.window.draw_line(line, "black")
        if self.has_top_wall:
            line = Line(Point(self.x1, self.y1), Point(self.x2, self.y1))
            self.window.draw_line(line, "black")
        if self.has_bottom_wall:
            line = Line(Point(self.x1, self.y2), Point(self.x2, self.y2))
            self.window.draw_line(line, "black")

    def draw_move(self, other, undo=False):
        colour = "red"
        if undo:
            colour = "gray"

        line = Line(Point((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2), Point((other.x1 + other.x2) / 2, (other.y1 + other.y2) / 2))
        self.window.draw_line(line, colour)

def main():
    window = Window(800, 600)
    cells = []
    for i in range(10):
        cells.append(Cell(Point(i*16, i*16), Point(i*16+16, i*16+16), window))
        if i % 2:
            cells[i].has_left_wall = False
        if i % 3:
            cells[i].has_top_wall = False

        cells[i].draw()

    cells[8].draw_move(cells[7])
    cells[6].draw_move(cells[5], undo=True)
    window.wait_for_close()

main()
