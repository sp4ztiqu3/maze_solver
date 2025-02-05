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

def main():
    window = Window(800, 600)
    line1 = Line(Point(100, 300), Point(300, 100))
    window.draw_line(line1, "red")
    window.wait_for_close()

main()
