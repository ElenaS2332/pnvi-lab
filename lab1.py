import random
import sys

import pygame
from pygame import QUIT, KEYUP, K_ESCAPE, MOUSEBUTTONUP

COLORS = {
    "RED": (155, 0, 0),
    "GREEN": (0, 155, 0),
    "BLUE": (0, 0, 155),
    "YELLOW": (155, 155, 0),
}

BACKGROUND_COLOR = (0, 0, 0)
FPS = 30

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
BOARD_WIDTH = 5
BOARD_HEIGHT = 5
TILE_SIZE = 60
GAP_X = int((WINDOW_WIDTH - (TILE_SIZE * BOARD_WIDTH + (BOARD_WIDTH - 1))) / 2)
GAP_Y = int((WINDOW_HEIGHT - (TILE_SIZE * BOARD_HEIGHT + (BOARD_HEIGHT - 1))) / 2)

NEIGHBOURS = {
    "UP": (0, 1),
    "DOWN": (0, -1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}


def main() -> None:
    global FPS_CLOCK, BOARD_SURFACE

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    BOARD_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Color Fill Puzzle")

    board = generate_board(10)

    while True:
        draw_board(board)
        check_for_quit()

        if has_won(board):
            pygame.display.update()
            pygame.time.wait(1000)
            animate_win()
            board = generate_board(10)

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                pos_x, pos_y = event.pos
                clicked_tile = get_clicked_tile(board, pos_x, pos_y)

                if clicked_tile is None:
                    continue

                tile_x, tile_y = clicked_tile
                tile_color = board[tile_x][tile_y]
                next_color = get_next_color(tile_color)
                board[tile_x][tile_y] = next_color

                draw_tile(tile_x, tile_y, tile_color)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def has_won(board: list[list[str]]) -> bool:
    return is_board_fair(board, 0, 0)


def animate_win() -> None:
    for color in COLORS.values():
        BOARD_SURFACE.fill(color)
        pygame.display.update()
        pygame.time.wait(500)


def get_next_color(color: str) -> str:
    colors = list(COLORS.keys())
    index = colors.index(color)
    next_index = (index + 1) % len(colors)

    return colors[next_index]


def get_clicked_tile(board: list[list[str]], pos_x: int, pos_y: int) -> tuple[int, int] | None:
    for i in range(len(board)):
        for j in range(len(board[0])):
            tile_x, tile_y = get_tile_top_left_corner(i, j)
            tile_rect = pygame.Rect(tile_x, tile_y, TILE_SIZE, TILE_SIZE)

            if tile_rect.collidepoint(pos_x, pos_y):
                return i, j

    return None


def get_neighbours(x: int, y: int) -> list[tuple[int, int]]:
    neighbours = [(x + i, y + j) for i, j in list(NEIGHBOURS.values())]
    return [(i, j) for i, j in neighbours if 0 <= i < BOARD_WIDTH and 0 <= j < BOARD_HEIGHT]


def is_board_fair(board: list[list[str]], min_overlap: int, max_overlap: int) -> bool:
    overlapping_colors = 0

    for row in range(len(board)):
        for col in range(len(board[0])):
            color = board[row][col]
            neighbours = get_neighbours(row, col)
            neighbour_colors = [board[i][j] for i, j in neighbours]

            if color in neighbour_colors:
                overlapping_colors += 1

    if overlapping_colors < min_overlap or overlapping_colors > max_overlap:
        return False

    return True


def generate_board(min_overlap=1) -> list[list[str]]:
    while True:
        board = generate_random_board()

        if not is_board_fair(board, min_overlap, 100):
            continue

        return board


def generate_random_board() -> list[list[str]]:
    return [[random.choice(list(COLORS.keys())) for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]


def draw_board(board: list[list[str]]) -> None:
    BOARD_SURFACE.fill(BACKGROUND_COLOR)

    for x in range(len(board)):
        for y in range(len(board[0])):
            color = board[x][y]
            draw_tile(x, y, color)


def draw_tile(
        x: int,
        y: int,
        color: str
) -> None:
    pos_x, pos_y = get_tile_top_left_corner(x, y)
    color_rgb = COLORS[color]

    pygame.draw.rect(BOARD_SURFACE, color_rgb, (pos_x, pos_y, TILE_SIZE, TILE_SIZE))


def get_tile_top_left_corner(
        x: int,
        y: int
) -> tuple[int, int]:
    return (
        GAP_X + (x * TILE_SIZE) + (x - 1),
        GAP_Y + (y * TILE_SIZE) + (y - 1)
    )


def terminate() -> None:
    pygame.quit()
    sys.exit()


def check_for_quit():
    for _ in pygame.event.get(QUIT):  # get all the QUIT events
        terminate()  # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP):  # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate()  # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event)  # put the other KEYUP event objects back


if __name__ == '__main__':
    main()
