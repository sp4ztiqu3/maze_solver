from tkinter import Tk, BOTH, Canvas
import time, random

CLEAR_COLOUR = "grey20"

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
        self.visited = False

    def draw(self):
        if self.has_left_wall:
            line = Line(Point(self.x1, self.y1), Point(self.x1, self.y2))
            self.window.draw_line(line, "white")
        else:
            line = Line(Point(self.x1, self.y1), Point(self.x1, self.y2))
            self.window.draw_line(line, CLEAR_COLOUR)
        if self.has_right_wall:
            line = Line(Point(self.x2, self.y1), Point(self.x2, self.y2))
            self.window.draw_line(line, "white")
        else:
            line = Line(Point(self.x2, self.y1), Point(self.x2, self.y2))
            self.window.draw_line(line, CLEAR_COLOUR)
        if self.has_top_wall:
            line = Line(Point(self.x1, self.y1), Point(self.x2, self.y1))
            self.window.draw_line(line, "white")
        else:
            line = Line(Point(self.x1, self.y1), Point(self.x2, self.y1))
            self.window.draw_line(line, CLEAR_COLOUR)
        if self.has_bottom_wall:
            line = Line(Point(self.x1, self.y2), Point(self.x2, self.y2))
            self.window.draw_line(line, "white")
        else:
            line = Line(Point(self.x1, self.y2), Point(self.x2, self.y2))
            self.window.draw_line(line, CLEAR_COLOUR)

    def draw_move(self, other, undo=False):
        colour = "red"
        if undo:
            colour = "gray"

        line = Line(Point((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2), Point((other.x1 + other.x2) / 2, (other.y1 + other.y2) / 2))
        self.window.draw_line(line, colour)

class Maze:
    def __init__(self, x1, y1, num_cols, num_rows, cell_size_x, cell_size_y, win, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.window = win
        self.cells = [[Cell(Point(0,0), Point(0,0), self.window) for _ in range(self.num_rows)] for _ in range(self.num_cols)]
        if seed == None:
            self.seed = random.seed(0)
        else:
            self.seed = random.seed(seed)

        self.create_cells()

    def create_cells(self):
        for x in range(self.num_cols):
            for y in range(self.num_rows):
                self.cells[x][y] = Cell(Point(self.x1 + x * self.cell_size_x, self.y1 + y * self.cell_size_y), Point(self.x1 + (x + 1) * self.cell_size_x, self.y1 + (y + 1) * self.cell_size_y), self.window)

        for x in range(self.num_cols):
            for y in range(self.num_rows):
                self.cells[x][y].draw()

                self.animate()

        self.break_entrance_and_exit()
        self.break_walls_r(0, 0)
        self.reset_cells_visited()

        self.solve()

    def break_entrance_and_exit(self):
        self.cells[0][0].has_top_wall = False
        self.cells[0][0].draw()
        self.animate()

        self.cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
        self.cells[self.num_cols - 1][self.num_rows - 1].draw()
        self.animate()

    def break_walls_r(self, x, y):
        self.cells[x][y].visited = True
        while True:
            to_visit = []
            if x > 0:
                if not self.cells[x-1][y].visited:
                    to_visit.append("left")
            if y > 0:
                if not self.cells[x][y-1].visited:
                    to_visit.append("up")
            if x < self.num_cols-1:
                if not self.cells[x+1][y].visited:
                    to_visit.append("right")
            if y < self.num_rows-1:
                if not self.cells[x][y+1].visited:
                    to_visit.append("down")
            if len(to_visit) == 0:
                self.cells[x][y].draw()
                self.animate()
                return
            random.shuffle(to_visit)
            dir = to_visit[0]
            if dir == "left":
                self.cells[x][y].has_left_wall = False
                self.cells[x-1][y].has_right_wall = False
                self.break_walls_r(x-1, y)
            if dir == "up":
                self.cells[x][y].has_top_wall = False
                self.cells[x][y-1].has_bottom_wall = False
                self.break_walls_r(x, y-1)
            if dir == "right":
                self.cells[x][y].has_right_wall = False
                self.cells[x+1][y].has_left_wall = False
                self.break_walls_r(x+1, y)
            if dir == "down":
                self.cells[x][y].has_bottom_wall = False
                self.cells[x][y+1].has_top_wall = False
                self.break_walls_r(x, y+1)

    def reset_cells_visited(self):
        for x in range(self.num_cols):
            for y in range(self.num_rows):
                self.cells[x][y].visited = False


    def animate(self):
        self.window.redraw()
        time.sleep(0.01)


    def solve_r(self, x, y):
        self.animate()
        self.cells[x][y].visited = True
        if x == self.num_cols - 1 and y == self.num_rows - 1:
            return True
        if y < self.num_rows - 1 and self.cells[x][y].has_bottom_wall == False:
            if self.cells[x][y+1].visited == False:
                self.cells[x][y].draw_move(self.cells[x][y+1])
                if self.solve_r(x, y+1):
                    return True
                self.cells[x][y].draw_move(self.cells[x][y+1], undo=True)
        if x < self.num_cols - 1 and self.cells[x][y].has_right_wall == False:
            if self.cells[x+1][y].visited == False:
                self.cells[x][y].draw_move(self.cells[x+1][y])
                if self.solve_r(x+1, y):
                    return True
                self.cells[x][y].draw_move(self.cells[x+1][y], undo=True)
        if x > 0 and self.cells[x][y].has_left_wall == False:
            if self.cells[x-1][y].visited == False:
                self.cells[x][y].draw_move(self.cells[x-1][y])
                if self.solve_r(x-1, y):
                    return True
                self.cells[x][y].draw_move(self.cells[x-1][y], undo=True)
        if y > 0 and self.cells[x][y].has_top_wall == False:
            if self.cells[x][y-1].visited == False:
                self.cells[x][y].draw_move(self.cells[x][y-1])
                if self.solve_r(x, y-1):
                    return True
                self.cells[x][y].draw_move(self.cells[x][y-1], undo=True)

        return False


    def solve(self):
        return self.solve_r(0, 0)

def main():
    window = Window(800, 600)
    test = Maze(8, 8, 20, 20, 16, 16, window)
    window.wait_for_close()

main()
