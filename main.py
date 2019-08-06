# noinspection PyUnresolvedReferences
from pygame import freetype
import pygame as pg
from mytoken import *
from tile import *
from typing import List, Tuple

BG_COL = pg.Color('black')
DEBUG = 0

clk = None
display_surf = None
running = True
size = width, height = 1920, 1080

tiles: List[Tile] = []
curr_tile: Union[Tile, None] = None
curr_tile_pos_offset: Tuple = (0, 0)


def on_init():
    global running, display_surf, clk, DEBUG, tiles
    pg.init()
    pg.freetype.init()

    display_surf = pg.display.set_mode(size, pg.HWSURFACE | pg.DOUBLEBUF)
    clk = pg.time.Clock()
    running = True

    tiles.append(Tile(TEST_TOKEN, None, (250, 250, 144 * 2, 256)))

    DEBUG, t = pg.USEREVENT + 1, 500
    # pg.time.set_timer(DEBUG, t)
    print('finished init')


def on_loop():
    global tiles

    if curr_tile is not None:
        mpos = pg.mouse.get_pos()
        curr_tile.move_ip(*(mpos[0] + curr_tile_pos_offset[0], mpos[1] + curr_tile_pos_offset[1]))


def on_render():
    global tiles, display_surf, clk

    display_surf.fill(BG_COL)

    for t in tiles:
        if not (curr_tile is not None and t == curr_tile):
            t.draw(display_surf)
    if curr_tile is not None:
        curr_tile.draw(display_surf)
    pg.display.flip()


def on_mouse_up(pos):
    global curr_tile, tiles
    if curr_tile is not None:
        for t in tiles:
            if not t == curr_tile:
                col = t.get_lowest_collide(pos)
                if col.token is None:
                    if col.parent.subl == col:
                        col.parent.subl = curr_tile
                    else:
                        assert col.parent.subr == col
                        col.parent.subr = curr_tile
                    curr_tile.parent = col.parent
                    col.parent.update_width(True)

        curr_tile = None


def on_mouse_down(pos):
    global curr_tile, tiles, curr_tile_pos_offset
    for t in tiles[::-1]:
        if t.collidepoint(*pos):
            col = t.get_lowest_collide(pos)
            curr_tile = col.parent if col.token is None else col
            curr_tile_pos_offset = (curr_tile.center[0] - pos[0], curr_tile.center[1] - pos[1])
            curr_tile.unlink_from_parent(tiles)
            break


def on_debug():
    global tiles
    print(tiles[0].getbounds())


def on_event(event):
    global running
    if event.type == pg.QUIT:
        running = False
    elif event.type == DEBUG:
        on_debug()
    elif event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_LEFT:
        on_mouse_down(event.pos)
    elif event.type == pg.MOUSEBUTTONUP and event.button == pg.BUTTON_LEFT:
        on_mouse_up(event.pos)


def on_cleanup():
    pg.quit()


def on_execute():
    global running
    on_init()

    while running:
        for event in pg.event.get():
            on_event(event)
        on_loop()
        on_render()

        clk.tick(144)

    on_cleanup()


if __name__ == '__main__':
    on_execute()
