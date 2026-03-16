This is a WORK IN PROGRESS project.
The goal of this project is to make a functional class for generating checkerboard objects in Python's Pygame Library.
For each object the user is able to specify:
  The center coordinates (in Pygame's x,y system)
  The square colors (in Pygame's RGB system)
  The width (in pixels)
  The number of squares on each side
  What color is the top left square
  The files for each of the squares if colors are desired instead of colors (NOT YET IMPLEMENTED)

Each object has the arguments as attributes along with:
  self.rects: a dictionary with
    key = (X, Y) coordinates in board coordinates NOT screen coordinates --- (0,0) is top left
    values = a Rect obj of the square
  self.rects_w_colors: a copy of the rects dictionary just with the values now being a list of [color, Rect]
