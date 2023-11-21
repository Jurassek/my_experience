import curses
from curses import wrapper
import queue
import time

maze = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", " ", "#", "#", "#", " ", "#"],
    ["#", " ", " ", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", " ", " ", "X"],
    ["#", " ", "#", " ", "#", "#", "#", " ", "#"],
    ["#", "#", "#", " ", "#", " ", "#", "#", "#"],
    ["O", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#"]
]

def show_maze(maze, stdscr, path=[]):
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j*2, 'X', RED)
            else:
                stdscr.addstr(i, j*2, value, BLUE)

def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j
    return None


def find_path(maze, stdscr):
    start = 'O'
    end = 'X'
    start_pos = find_start(maze, 'O')

    q = queue.Queue()
    q.put((start_pos, [start_pos]))

    visited = set()
    
    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        stdscr.clear()
        show_maze(maze, stdscr, path)
        time.sleep(0.5)
        stdscr.refresh()

        if maze[row][col] == end:
            return path
        
        neig = find_neig(maze, row, col)
        for n in neig:
            if n in visited:
                continue

            r, c = n
            if maze[r][c] == '#':
                continue

            new_path = path + [n]
            q.put((n, new_path))
            visited.add(n)

def find_neig(maze, row, col):
    neig = []

    if row > 0:
        neig.append((row - 1, col))
    if row + 1 < len(maze):
        neig.append((row + 1, col))
    if col > 0:
        neig.append((row, col - 1))
    if row + 1 < len(maze[0]):
        neig.append((row, col + 1))

    return neig



def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    find_path(maze, stdscr)
    stdscr.getch()


wrapper(main)