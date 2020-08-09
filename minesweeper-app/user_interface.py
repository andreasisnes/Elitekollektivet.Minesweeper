from minesweeper import core
from minesweeper import sprites
from typing import Callable
import pygame
from pygame.locals import MOUSEBUTTONUP, MOUSEBUTTONDOWN

try:
    from .user_interface_board import UserInterfaceBoard
    from .user_interface_score import UserInterfaceScore
    from .user_interface_face import UserInterfaceFace
except ImportError:
    from user_interface_board import UserInterfaceBoard
    from user_interface_score import UserInterfaceScore
    from user_interface_face import UserInterfaceFace


class UserInterface:
    def __init__(self, rows: int, cols: int, mines: int):
        offset = 10
        self._screen = self.init_screen(rows, cols, offset)
        self._board = core.Board(rows, cols, mines)
        tmp = UserInterfaceBoard(self._board, sprites.TileBuilder().build(), offset)
        self._components = [
            tmp,
            UserInterfaceScore(self._board, sprites.ScoreBuilder(), offset, tmp.flagged),
            UserInterfaceFace(self._board, sprites.FaceBuilder().build(), offset, self.game_reset),
        ]

    def game_reset(self):
        self._board.game_reset()
        [component.game_reset() for component in self._components]

    def event_handler(self, event) -> bool:
        for component in self._components:
            if event.type == MOUSEBUTTONDOWN:
                component.mouse_down(event)
            if event.type == MOUSEBUTTONUP:
                component.mouse_up(event)

    def draw(self) -> bool:
        return [component.draw(self._screen) for component in self._components]

    def init_screen(self, rows: int, cols: int, offset: int):
        rows, cols, offset = int(rows), int(cols), int(offset)
        self._screen = pygame.display.set_mode((10, 10))
        tiles = sprites.TileBuilder().build().eight
        score = sprites.ScoreBuilder().build().eight
        width = cols * tiles.get_width() + offset * 2
        height = rows * tiles.get_height() + score.get_height() + offset * 3
        return pygame.display.set_mode((width, height))