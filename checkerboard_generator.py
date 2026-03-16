from dataclasses import dataclass
from itertools import cycle
from math import sqrt
import pygame as pg
import sys

@dataclass
class Square:
    rect: pg.Rect
    surface: pg.Surface
    img: tuple[int,int,int] | str

    def get_pos(self):
        return self.rect.center

# checkerboard class
# instance variables:
    # center:tuple = the center of the checkerboard
    # square_colors:Tuple[tuple, tuple] = the colors of the two squares
    # board_width:int = the width of the board in px
    # num_of_squares:int = the width of the board in number of squares
    # top_left_color:tuple[int,int,int]: the color of the top left square of the board
    # squares:List[sting, string] = an optional argument, a list of strings who are the names of the files for the images of the two square types (the lighter and the darker)
class Checkerboard:
    @staticmethod
    def _rects_generator(num_of_squares, square_width, board_center):
        # STATICMETHOD: Creates the self.rects dictionary
        # key -> the position of the rect in terms of checkerboard coord, i.e. topleft is (0,0) and bottom right is (4,4) for a 5x5 board
        # value -> the rect object(coords and size)

        rect_dictionary = {(y,x) : None for x in range(num_of_squares) for y in range(num_of_squares)}

        y = board_center[1] - ((num_of_squares / 2) * square_width)
        for row in range(num_of_squares):
            x = board_center[0] - ((num_of_squares / 2) * square_width)
            for row_item in range(num_of_squares):
                rect_dictionary[(row_item, row)] = pg.Rect((x, y), (square_width, square_width))  # we generate and add the rect w/ its format to self.rects
                x += square_width
            y += square_width
        return rect_dictionary

    @staticmethod
    def _add_colors(rects, square_colors, top_left_color):
        # STATICMETHOD:
        # grabs the rects dictionary and makes a copy so each value is a list of [rect, color]
        rects_dict = rects
        coordinates = list(rects_dict.keys())
        new_dictionary = {}

        def _skip_last_row_color(index, coordinates_list, current_coordinate):
            nonlocal cycler

            current = current_coordinate
            last = coordinates_list[max(0, index - 1)]
            if current[1] != last[1]: # compares then y-values of the coordinates
                next(cycler)

        def _cycler_from_top_left_color(tl_color, sqr_color):
            color1, color2 = sqr_color[0], sqr_color[1]
            if tl_color == color1:
                return cycle([color1, color2])
            else:
                return cycle([color2, color1])

        cycler = _cycler_from_top_left_color(top_left_color, square_colors)

        num_of_squares = sqrt(len(rects_dict))

        for coord in coordinates:
            ind = coordinates.index(coord)
            if num_of_squares % 2 == 0: _skip_last_row_color(ind, coordinates, coord)
            new_dictionary[coord] = [rects_dict[coord], next(cycler)]
        return new_dictionary

    def __init__(self,
                 center: tuple[float, float],
                 square_colors: tuple[tuple, tuple],
                 board_width: float,
                 num_of_squares_per_side: int,
                 top_left_color: tuple[int, int, int] = 0,
                 square_files: list[str, str] | None = None) -> None:
        self.center = center
        self.square_colors = square_colors
        self.square_width = board_width/num_of_squares_per_side
        self.num_of_squares_per_side = num_of_squares_per_side
        
        if top_left_color not in self.square_colors: # a check to see if the top left color is actually one of the given square colors
            raise TypeError("Top left color must be one of the colors in square_colors")
        self.top_left_color = top_left_color
        
        if square_files:
            self.square1_file = square_files[0]
            self.square2_file = square_files[1]

        self.rects = self._rects_generator(self.num_of_squares_per_side, self.square_width, self.center)
        self.rects_w_colors = self._add_colors(self.rects, self.square_colors, self.top_left_color)

    def draw(self, screen):
        for rec, col in self.rects_w_colors.values():
            pg.draw.rect(screen, col, rec)


if __name__ == '__main__':
    # pygame vars
    SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
    BACKGROUNDCOLOR = (42, 45, 51)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PINK = (255, 0, 255)
    CYAN = (0, 255, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    
    # instantiate checkerboard
    C = Checkerboard(
        (SCREEN_WIDTH/2, SCREEN_HEIGHT/2),
        (BLUE, RED),
        300,
        8,
        RED
    )
    
    # for debugging
    for k,v in C.rects.items():
        print(f"{k}: {v}")

    # Pygame initate
    pg.init()  # initiate pg
    SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create display surface
    clock = pg.time.Clock()  # Create clock object
    select_sound = pg.mixer.Sound("retro-select-236670.mp3")
    select_sound.set_volume(0.3)

    def distance(point1, point2):
        return sqrt(
            ((point2[0] - point1[0]) ** 2) + (point2[1] - point1[1]) ** 2)

    current_square = None
    is_colliding = False

    while True:  # Game loop
        for event in pg.event.get():  # Check for all events
            if event.type == pg.QUIT:  # Close game
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:  # Close game if escape is pressed
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

        SCREEN.fill(BACKGROUNDCOLOR)  # Fill display with a deep purple color
        C.draw(SCREEN)

        # if there is a collision between a rect and the mouse, it draws a green circle on the rect
        collisions_results = {}
        colliding_square = None

        for key in C.rects.keys():
            rect1 = C.rects[key]
            collisions_results[key] = rect1.collidepoint(pg.mouse.get_pos())

            if collisions_results[key] == True:
                colliding_square = C.rects[key]

        if colliding_square:
            pg.draw.circle(SCREEN, GREEN, colliding_square.center, C.square_width / 2)
            if colliding_square != current_square or not is_colliding: # compares new state vs. prev frame state to see if a new square is selected
                select_sound.stop()
                select_sound.play()
            is_colliding = True
            current_square = colliding_square
        else:
            is_colliding = False

        pg.display.flip()  # Draw frame
        clock.tick(120)  # Framerate

# MAE A SQUARE CLASS:
# W/ attributes: Rect(position info), surface, image/color