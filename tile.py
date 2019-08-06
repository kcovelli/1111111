from pygame import freetype
import pygame as pg
from mytoken import *
from typing import List, Union

THICC = 2
LAYER_GAP_X, LAYER_GAP_Y, = 16, 8
PRIM_WIDTH, PRIM_HEIGHT = 64, 64  # width of base level tiles (1's)

FONT = None


def getfont():
    global FONT
    if pg.freetype.get_init():
        if FONT is not None:
            FONT = pg.freetype.SysFont('arialblack', 85)
        return FONT
    else:
        pg.freetype.init()
        return None


class Tile(pg.Rect):
    """
        Represents a tile to be represented on the screen

        token: token object that this tile will be drawing for
        gpos: position of this tile on the main screen
        size: width/height of this tile


    """

    token: Token
    token_symbol: str
    font: pg.font.Font
    inner: pg.Rect
    subl: Union['Tile', None]
    subr: Union['Tile', None]
    parent: Union['Tile', None]

    def __init__(self, token: Token, parent: Union['Tile', None], *args, **kwargs):
        super().__init__(*args, **kwargs)

        # noinspection PyArgumentList
        self.bcolor = pg.Color('green') if token is not None else pg.Color(155, 255, 185)
        self.icolor = pg.Color('red')
        self.tcolor = pg.Color('blue')

        self.token = token
        self.token_symbol = token.getsymbol() if isinstance(token, Token) else ''
        self.parent = parent

        if token is None or isinstance(token, int):
            self.width, self.height = PRIM_WIDTH, PRIM_HEIGHT
            self.subr = None
            self.subl = None
        else:
            self.subl = Tile(token.left, self, (self.x + LAYER_GAP_X, self.y + LAYER_GAP_Y, 1000, 1000))
            self.subr = Tile(token.right, self, (self.x + LAYER_GAP_X, self.y + LAYER_GAP_Y, 1000, 1000))

            self.width = self.subl.width + self.subr.width + PRIM_WIDTH + LAYER_GAP_X * 2
            self.height = max(self.subl.height, self.subr.height) + LAYER_GAP_Y * 2

        self.move_ip(*self.center)
        self.font = getfont()
        if self.font is None:
            print("freetype not initialized, creating tile without font")

    def get_lowest_collide(self, pos) -> 'Tile':
        if self.subl is None and self.subr is None:
            # if self.token is None:
            #    return self.parent
            # else:
            return self
        else:
            if self.subl.collidepoint(*pos):
                return self.subl.get_lowest_collide(pos)
            elif self.subr.collidepoint(*pos):
                return self.subr.get_lowest_collide(pos)
            else:
                return self

    def get_root(self):
        return self if self.parent is None else self.parent

    def update_width(self, flag):
        if self.parent is not None and flag:
            self.get_root().update_width(False)
        else:
            if self.subl is not None:
                self.subl.update_width(False)
            if self.subr is not None:
                self.subr.update_width(False)

            if self.subl is not None and self.subr is not None:
                self.width = self.subl.width + self.subr.width + PRIM_WIDTH + LAYER_GAP_X * 2
                self.height = max(self.subl.height, self.subr.height) + LAYER_GAP_Y * 2
            else:
                self.width, self.height = PRIM_WIDTH, PRIM_HEIGHT
            self.update_pos()

    def update_pos(self):
        self.move_ip(self.centerx, self.centery)

    def unlink_from_parent(self, tile_list):
        if self.parent is not None:
            if self.parent.subl == self:
                self.parent.token.left = None
                self.parent.subl = Tile(None, self.parent, tuple(self))
            elif self.parent.subr == self:
                self.parent.token.right = None
                self.parent.subr = Tile(None, self.parent, tuple(self))
            else:
                assert False
            # moving out of my parents house
            self.update_width(True)
            self.parent = None
            tile_list.append(self)

    def move_ip(self, x, y):
        self.center = x, y

        if self.subl is not None:
            assert self.subr is not None
            self.subl.move_ip(self.x + LAYER_GAP_X + self.subl.width // 2, y)
            self.subr.move_ip(self.subl.right + PRIM_WIDTH + self.subr.width // 2, y)

    def get_inner_rect(self):
        return self.inflate(-2 * THICC, -2 * THICC)

    def draw(self, surface: pg.Surface):
        pg.draw.rect(surface, self.bcolor, self)
        if self.token is not None:
            pg.draw.rect(surface, self.icolor, self.get_inner_rect())
            if self.subl is not None:
                self.subl.draw(surface)
            if self.subr is not None:
                self.subr.draw(surface)
            if getfont() is not None:
                fontrect = getfont().get_rect(self.token_symbol)
                fontpos = (self.centerx - fontrect.width // 2, self.centery - fontrect.height // 2)

                getfont().render_to(surface, fontpos, self.token_symbol)
            else:
                if self.subl is not None:
                    pg.draw.circle(surface, self.tcolor, (self.subl.right + PRIM_WIDTH // 2, self.centery), 16)
                else:
                    pg.draw.circle(surface, pg.Color('black'), self.center, 16)
