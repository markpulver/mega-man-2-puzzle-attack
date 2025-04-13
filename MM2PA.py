
# Mega Man 2: Puzzle Attack

# by Mark Pulver

# version 1.1: 04/12/2025
# The monolithic organization of 1.0 is terrible, but I only updated 1.1 to work
# with modern Windows, so it remains terrible.

# version 1.0: 01/16/2005

# --------------------------------------------------------------------------------


# import modules
import numpy, operator, os, pygame, random, string

from numpy import *
from operator import *
from pygame.locals import *
from string import *


# ---------------------------------- FUNCTIONS -----------------------------------


# function to print text for Best Times screen
def BTtext(surf, string, x, y):
  for i in range(len(string)):
    ch = Character(string[i])
    surf.blit(ch.image, (x + i * 8, y))


# function to print game time during gameplay
def GameTime(clear_surf, surf, integer):
  surf.blit(clear_surf.image, (44, 204))
  integer /= 1000  # all but last 3 characters, since this is in milliseconds
  m = int(floordiv(integer, 60))  # gives us minutes
  s = int(mod(integer, 60)) # gives us seconds
  mins = str(m)
  sec = str(s)
  if (len(mins) == 1):  # append '0' to front of minutes if they are less than 10
    mins = '0' + mins
  if (len(sec) == 1):
    sec = '0' + sec
  for i in range(len(mins)):
    ch = Character(mins[i])
    surf.blit(ch.image, (44 + i * 8, 204))
  for i in range(len(sec)):
    ch = Character(sec[i])
    surf.blit(ch.image, (68 + i * 8, 204))


# function to load graphics
def load_image(name, colorkey=None):
  fullname = os.path.join('data', 'graphics', name)
  try:
    image = pygame.image.load(fullname)
  except pygame.error as message:
    print('Cannot load image:', fullname)
    raise(SystemExit, message)
  image = image.convert()
  if colorkey is not None:
    if colorkey == -1:
      colorkey = image.get_at((0, 0))
    image.set_colorkey(colorkey, RLEACCEL)
  return image, image.get_rect()


# function to load music
def load_music(name):
  fullname = os.path.join('data', 'music', name)
  try:
    pygame.mixer.music.load(fullname)
  except pygame.error as message:
    print('Cannot load music:', fullname)
    raise(SystemExit, message)


# function to load sound
def load_sound(name):
  fullname = os.path.join('data', 'SFX', name)
  try:
    sound = pygame.mixer.Sound(fullname)
  except pygame.error as message:
    print('Cannot load sound:', fullname)
    raise(SystemExit, message)
  return sound


# function to multiply damage done based on weapon selected and robot being damaged
def Multiplier(selected_robot, selected_weapon):
  # BUBBLE
  if (selected_robot == 0):
    if (selected_weapon == 0):   dmg_multiplier = 0
    elif (selected_weapon == 1): dmg_multiplier = 0
    elif (selected_weapon == 2): dmg_multiplier = 1
    elif (selected_weapon == 3): dmg_multiplier = 0
    elif (selected_weapon == 4): dmg_multiplier = 1
    elif (selected_weapon == 5): dmg_multiplier = 0
    elif (selected_weapon == 6): dmg_multiplier = 3
    elif (selected_weapon == 7): dmg_multiplier = 0
    elif (selected_weapon == 8): dmg_multiplier = 2
  # AIR
  elif (selected_robot == 1):
    if (selected_weapon == 0):   dmg_multiplier = 0
    elif (selected_weapon == 1): dmg_multiplier = 0
    elif (selected_weapon == 2): dmg_multiplier = 2
    elif (selected_weapon == 3): dmg_multiplier = 2
    elif (selected_weapon == 4): dmg_multiplier = 2
    elif (selected_weapon == 5): dmg_multiplier = 4
    elif (selected_weapon == 6): dmg_multiplier = 0
    elif (selected_weapon == 7): dmg_multiplier = 0
    elif (selected_weapon == 8): dmg_multiplier = 0
  # QUICK
  elif (selected_robot == 2):
    if (selected_weapon == 0):   dmg_multiplier = 0
    elif (selected_weapon == 1): dmg_multiplier = 2
    elif (selected_weapon == 2): dmg_multiplier = 0
    elif (selected_weapon == 3): dmg_multiplier = 2
    elif (selected_weapon == 4): dmg_multiplier = 2
    elif (selected_weapon == 5): dmg_multiplier = 0
    elif (selected_weapon == 6): dmg_multiplier = 0
    elif (selected_weapon == 7): dmg_multiplier = 4
    elif (selected_weapon == 8): dmg_multiplier = 2
  # HEAT
  elif (selected_robot == 3):
    if (selected_weapon == 0):   dmg_multiplier = 4
    elif (selected_weapon == 1): dmg_multiplier = 2
    elif (selected_weapon == 2): dmg_multiplier = 2
    elif (selected_weapon == 3): dmg_multiplier = 0
    elif (selected_weapon == 4): dmg_multiplier = 2
    elif (selected_weapon == 5): dmg_multiplier = 0
    elif (selected_weapon == 6): dmg_multiplier = 1
    elif (selected_weapon == 7): dmg_multiplier = 0
    elif (selected_weapon == 8): dmg_multiplier = 0
  # WOOD
  elif (selected_robot == 4):
    if (selected_weapon == 0):   dmg_multiplier = 0
    elif (selected_weapon == 1): dmg_multiplier = 3
    elif (selected_weapon == 2): dmg_multiplier = 0
    elif (selected_weapon == 3): dmg_multiplier = 3
    elif (selected_weapon == 4): dmg_multiplier = 1
    elif (selected_weapon == 5): dmg_multiplier = 0
    elif (selected_weapon == 6): dmg_multiplier = 2
    elif (selected_weapon == 7): dmg_multiplier = 0
    elif (selected_weapon == 8): dmg_multiplier = 2
  # METAL
  elif (selected_robot == 5):
    if (selected_weapon == 0):   dmg_multiplier = 0
    elif (selected_weapon == 1): dmg_multiplier = 0
    elif (selected_weapon == 2): dmg_multiplier = 3
    elif (selected_weapon == 3): dmg_multiplier = 1
    elif (selected_weapon == 4): dmg_multiplier = 1
    elif (selected_weapon == 5): dmg_multiplier = 0
    elif (selected_weapon == 6): dmg_multiplier = 0
    elif (selected_weapon == 7): dmg_multiplier = 0
    elif (selected_weapon == 8): dmg_multiplier = 0
  # FLASH
  elif (selected_robot == 6):
    if (selected_weapon == 0):   dmg_multiplier = 2
    elif (selected_weapon == 1): dmg_multiplier = 0
    elif (selected_weapon == 2): dmg_multiplier = 0
    elif (selected_weapon == 3): dmg_multiplier = 2
    elif (selected_weapon == 4): dmg_multiplier = 2
    elif (selected_weapon == 5): dmg_multiplier = 0
    elif (selected_weapon == 6): dmg_multiplier = 3
    elif (selected_weapon == 7): dmg_multiplier = 0
    elif (selected_weapon == 8): dmg_multiplier = 3
  # CRASH
  elif (selected_robot == 7):
    if (selected_weapon == 0):   dmg_multiplier = 1
    elif (selected_weapon == 1): dmg_multiplier = 4
    elif (selected_weapon == 2): dmg_multiplier = 1
    elif (selected_weapon == 3): dmg_multiplier = 1
    elif (selected_weapon == 4): dmg_multiplier = 1
    elif (selected_weapon == 5): dmg_multiplier = 0
    elif (selected_weapon == 6): dmg_multiplier = 0
    elif (selected_weapon == 7): dmg_multiplier = 0
    elif (selected_weapon == 8): dmg_multiplier = 0
  # WILY
  elif (selected_robot == 8):
    if (selected_weapon == 0):   dmg_multiplier = 2
    elif (selected_weapon == 1): dmg_multiplier = 0
    elif (selected_weapon == 2): dmg_multiplier = 0
    elif (selected_weapon == 3): dmg_multiplier = 0
    elif (selected_weapon == 4): dmg_multiplier = 0
    elif (selected_weapon == 5): dmg_multiplier = 0
    elif (selected_weapon == 6): dmg_multiplier = 0
    elif (selected_weapon == 7): dmg_multiplier = 0
    elif (selected_weapon == 8): dmg_multiplier = 0

  return dmg_multiplier


# function to drop the active piece
def PieceDrop(piece_y):
  dropped = True  # will set to False if a collision occurs; 0 = no block, 1 = inactive block, 2 = active block
  num_lines = 0  # number of lines completed

  # determine if collision has occurred
  for i in range(14):
    for j in range(10):
      if (matrix[i][j] == 2) and (i == 13):  # piece is in bottom row; will collide with bottom of play area
        dropped = False
      elif (i < 13):  # have to check this, so that "i + 1" below doesn't exceed the dimensions of the array
        if ((matrix[i][j] == 2) or (matrix[i][j] == 3)) and (matrix[i + 1][j] == 1):  # '2' or '3' right above a '1'
          dropped = False

  # if collision occurred, change the 2's and 3's to 1's
  if (dropped is False):
    for i in range(14):
      for j in range(10):
        if (matrix[i][j] == 2) or (matrix[i][j] == 3):
          matrix[i][j] = 1

    # check to see if a line was completed
    first_line = 0  # first line that was completed (done from bottom up)
    for i in range(14):  # 0 - 13
      row = 13 - i  # do from bottom up
      if (matrix[row][0] == 1) and (matrix[row][1] == 1) and (matrix[row][2] == 1) and (matrix[row][3] == 1) and (matrix[row][4] == 1) and (matrix[row][5] == 1) and (matrix[row][6] == 1) and (matrix[row][7] == 1) and (matrix[row][8] == 1) and (matrix[row][9] == 1):
        for j in range(10):
          matrix[row][j] = 4  # signifies completed line
        num_lines += 1
        if (num_lines == 1):
          first_line = row

    # drop the blocks if any lines were completed
    if (num_lines > 0):
      lines_completed = True
      dropping = True
      row = first_line
      while (dropping is True):
        if (matrix[row][0] == 4):  # drop all the blocks above if the current row has a 4 in it (entire row will be 4's)
          for i in range(row):
            k = row - i  # need to do from the bottom up
            if (k == 0):
              break  # there is no -1 row to shift down
            for j in range(10):
              matrix[k][j] = matrix[k - 1][j]
        if (matrix[row][0] != 4):  # row shifted down was not also completed, so move up to the next one
          row -= 1
        if (row == 0):
          dropping = False

  # if no collision occurred, drop the piece
  elif (dropped is True):
    for i in range(13):  # 0 to 12
      row = 12 - i  # need to do these from the bottom up, so that pieces don't shrink by overwriting themselves
      for j in range(10):
        if (matrix[row][j] == 2):
          matrix[row][j] = 0
          matrix[row + 1][j] = 2
        elif (matrix[row][j] == 3):
          matrix[row][j] = 0
          matrix[row + 1][j] = 3
    piece_y += 1

  # return appropriate values
  return dropped, num_lines, piece_y


# function to move the active piece left or right, based on player input
def PieceMove(direction, piece_x):
  moved = True  # used internally by function only; value not returned 

  # if piece up against the side of the playing area and the player tries to go in that direction, just exit the function
  for i in range(14):
    if (direction == "left") and (matrix[i][0] == 2):
      return piece_x
    elif (direction == "right") and (matrix[i][9] == 2):
      return piece_x

  # determine if collision has occurred
  for i in range(14):
    for j in range(8):  # 0 to 7 
      col = j + 1  # 1 to 8; don't need to check outer columns, since we did that above
      # placed blocks are left of piece
      if (direction == "left") and ((matrix[i][col] == 2) or (matrix[i][col] == 3)) and (matrix[i][col - 1] == 1):
        moved = False
      # placed blocks are right of piece
      elif (direction == "right") and ((matrix[i][col] == 2) or (matrix[i][col] == 3)) and (matrix[i][col + 1] == 1):
        moved = False

  # if no collision occurred, move the piece
  if (moved is True):
    if (direction == "left"):
      for i in range(14):
        for j in range(9):  # 0 to 8
          col = j + 1  # 1 to 9
          if (matrix[i][col] == 2):
            matrix[i][col] = 0
            matrix[i][col - 1] = 2
          if (matrix[i][col] == 3):
            matrix[i][col] = 0
            matrix[i][col - 1] = 3
      piece_x -= 1
    elif (direction == "right"):
      for i in range(14):
        for j in range(9):  # 0 to 8
          col = 8 - j  # need to do these from right to left, so that pieces don't shrink themselves
          if (matrix[i][col] == 2):
            matrix[i][col] = 0
            matrix[i][col + 1] = 2
          if (matrix[i][col] == 3):
            matrix[i][col] = 0
            matrix[i][col + 1] = 3
      piece_x += 1

  # return updated matrix and x of center of piece
  return piece_x


# function to rotate the active piece clockwise, based on player input
def PieceRotate(piece_type, piece_orientation, piece_x, piece_y):
  rotated = False  # set to True if rotation successful

  j = piece_x
  i = piece_y

  if (piece_type == 1):
    if (piece_orientation == 1):
      if (piece_y == 13):  # can't rotate it against the bottom of the play area
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i-1][j] == 0) and (matrix[i+1][j] == 0) and (matrix[i+1][j+1] == 0):
        matrix[i-1][j] = 2
        matrix[i-1][j+1] = 0
        matrix[i][j-1] = 0
        matrix[i][j+1] = 0
        matrix[i+1][j] = 2
        matrix[i+1][j+1] = 2
        rotated = True
    elif (piece_orientation == 2):
      if (piece_x == 0):  # can't rotate it against the left wall
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j+1] == 0) and (matrix[i][j-1] == 0) and (matrix[i][j+1] == 0) and (matrix[i+1][j-1] == 0):
        matrix[i-1][j] = 0
        matrix[i][j-1] = 2
        matrix[i][j+1] = 2
        matrix[i+1][j-1] = 2
        matrix[i+1][j] = 0
        matrix[i+1][j+1] = 0
        rotated = True
    elif (piece_orientation == 3):
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i-1][j] == 0) and (matrix[i+1][j] == 0) and (matrix[i+1][j+1] == 0):
        matrix[i-1][j-1] = 2
        matrix[i-1][j] = 2
        matrix[i][j-1] = 0
        matrix[i][j+1] = 0
        matrix[i+1][j-1] = 0
        matrix[i+1][j] = 2
        rotated = True
    elif (piece_orientation == 4):
      if (piece_x == 9):  # can't rotate it against the right wall
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j+1] == 0) and (matrix[i][j-1] == 0) and (matrix[i][j+1] == 0) and (matrix[i+1][j-1] == 0):
        matrix[i-1][j-1] = 0
        matrix[i-1][j] = 0
        matrix[i-1][j+1] = 2
        matrix[i][j-1] = 2
        matrix[i][j+1] = 2
        matrix[i+1][j] = 0
        rotated = True
    # add 1 to orientation; if it hits 5, will go to 1
    piece_orientation = mod(piece_orientation, 4) + 1
  elif (piece_type == 2):
    if (piece_orientation == 1):
      if (piece_y == 13):  # can't rotate it against the bottom of the play area
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j] == 0) and (matrix[i-1][j+1] == 0) and (matrix[i+1][j] == 0) and (matrix[i+1][j+1] == 0):
        matrix[i-1][j-1] = 0
        matrix[i-1][j] = 2
        matrix[i-1][j+1] = 2
        matrix[i][j-1] = 0
        matrix[i][j+1] = 0
        matrix[i+1][j] = 2
        rotated = True
    elif (piece_orientation == 2):
      if (piece_x == 0):  # can't rotate it against the left wall
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i][j-1] == 0) and (matrix[i][j+1] == 0) and (matrix[i+1][j-1] == 0) and (matrix[i+1][j+1] == 0):
        matrix[i-1][j] = 0
        matrix[i-1][j+1] = 0
        matrix[i][j-1] = 2
        matrix[i][j+1] = 2
        matrix[i+1][j] = 0
        matrix[i+1][j+1] = 2
        rotated = True
    elif (piece_orientation == 3):
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i-1][j] == 0) and (matrix[i+1][j-1] == 0) and (matrix[i+1][j] == 0):
        matrix[i-1][j] = 2
        matrix[i][j-1] = 0
        matrix[i][j+1] = 0
        matrix[i+1][j-1] = 2
        matrix[i+1][j] = 2
        matrix[i+1][j+1] = 0
        rotated = True
    elif (piece_orientation == 4):
      if (piece_x == 9):  # can't rotate it against the right wall
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i-1][j+1] == 0) and (matrix[i][j-1] == 0) and (matrix[i][j+1] == 0):
        matrix[i-1][j-1] = 2
        matrix[i-1][j] = 0
        matrix[i][j-1] = 2
        matrix[i][j+1] = 2
        matrix[i+1][j-1] = 0
        matrix[i+1][j] = 0
        rotated = True
    # add 1 to orientation; if it hits 5, will go to 1
    piece_orientation = mod(piece_orientation, 4) + 1
  elif (piece_type == 3):
    if (piece_orientation == 1):
      if (piece_y == 13):  # can't rotate it against the bottom of the play area
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i][j+1] == 0) and (matrix[i+1][j+1] == 0):
        matrix[i-1][j+1] = 0
        matrix[i][j-1] = 0
        matrix[i][j+1] = 2
        matrix[i+1][j+1] = 2
        rotated = True
    elif (piece_orientation == 2):
      if (piece_x == 0):  # can't rotate it against the left wall
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j+1] == 0) and (matrix[i+1][j-1] == 0) and (matrix[i+1][j] == 0):
        matrix[i-1][j] = 0
        matrix[i+1][j-1] = 2
        matrix[i+1][j] = 2
        matrix[i+1][j+1] = 0
        rotated = True
    elif (piece_orientation == 3):
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i][j-1] == 0) and (matrix[i+1][j+1] == 0):
        matrix[i-1][j-1] = 2
        matrix[i][j-1] = 2
        matrix[i][j+1] = 0
        matrix[i+1][j-1] = 0
        rotated = True
    elif (piece_orientation == 4):
      if (piece_x == 9):  # can't rotate it against the right wall
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j] == 0) and (matrix[i-1][j+1] == 0) and (matrix[i+1][j-1] == 0):
        matrix[i-1][j-1] = 0
        matrix[i-1][j] = 2
        matrix[i-1][j+1] = 2
        matrix[i+1][j] = 0
        rotated = True
    # add 1 to orientation; if it hits 5, will go to 1
    piece_orientation = mod(piece_orientation, 4) + 1
  elif (piece_type == 4):
    if (piece_orientation == 1):
      if (piece_y == 13):  # can't rotate it against the bottom of the play area
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j+1] == 0) and (matrix[i+1][j] == 0) and (matrix[i+1][j+1] == 0):
        matrix[i-1][j-1] = 0
        matrix[i-1][j] = 0
        matrix[i-1][j+1] = 2
        matrix[i+1][j] = 2
        rotated = True
    elif (piece_orientation == 2):
      if (piece_x == 0):  # can't rotate it against the left wall
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i][j-1] == 0) and (matrix[i+1][j-1] == 0) and (matrix[i+1][j+1] == 0):
        matrix[i-1][j+1] = 0
        matrix[i][j-1] = 2
        matrix[i][j+1] = 0
        matrix[i+1][j+1] = 2
        rotated = True
    elif (piece_orientation == 3):
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i-1][j] == 0) and (matrix[i+1][j-1] == 0):
        matrix[i-1][j] = 2
        matrix[i+1][j-1] = 2
        matrix[i+1][j] = 0
        matrix[i+1][j+1] = 0
        rotated = True
    elif (piece_orientation == 4):
      if (piece_x == 9):  # can't rotate it against the right wall
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i-1][j+1] == 0) and (matrix[i][j+1] == 0):
        matrix[i-1][j-1] = 2
        matrix[i][j-1] = 0
        matrix[i][j+1] = 2
        matrix[i+1][j-1] = 0
        rotated = True
    # add 1 to orientation; if it hits 5, will go to 1
    piece_orientation = mod(piece_orientation, 4) + 1
  elif (piece_type == 5):
    if (piece_orientation == 1):
      if (piece_y == 13):  # can't rotate it against the bottom of the play area
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i-1][j+1] == 0) and (matrix[i+1][j] == 0) and (matrix[i+1][j+1] == 0):
        matrix[i][j-1] = 0
        matrix[i+1][j] = 2
        rotated = True
    elif (piece_orientation == 2):
      if (piece_x == 0):  # can't rotate it against the left wall
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j+1] == 0) and (matrix[i][j-1] == 0) and (matrix[i+1][j-1] == 0) and (matrix[i+1][j+1] == 0):
        matrix[i-1][j] = 0
        matrix[i][j-1] = 2
        rotated = True
    elif (piece_orientation == 3):
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i-1][j] == 0) and (matrix[i+1][j-1] == 0) and (matrix[i+1][j+1] == 0):
        matrix[i-1][j] = 2
        matrix[i][j+1] = 0
        rotated = True
    elif (piece_orientation == 4):
      if (piece_x == 9):  # can't rotate it against the right wall
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i-1][j+1] == 0) and (matrix[i][j+1] == 0) and (matrix[i+1][j-1] == 0):
        matrix[i][j+1] = 2
        matrix[i+1][j] = 0
        rotated = True
    # add 1 to orientation; if it hits 5, will go to 1
    piece_orientation = mod(piece_orientation, 4) + 1
  elif (piece_type == 6):
    rotated = True
  elif (piece_type == 7):
    if (piece_orientation == 1):
      if (piece_y == 13) or (piece_y == 12):  # can't rotate it against the bottom 2 rows of the play area
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i-1][j] == 0) and (matrix[i+1][j] == 0) and (matrix[i+1][j+1] == 0) and (matrix[i+1][j+2] == 0) and (matrix[i+2][j] == 0) and (matrix[i+2][j+1] == 0):
        matrix[i-1][j] = 2
        matrix[i][j-1] = 0
        matrix[i][j+1] = 0
        matrix[i][j+2] = 0
        matrix[i+1][j] = 2
        matrix[i+2][j] = 2
        rotated = True
    elif (piece_orientation == 2):
      # can't rotate it against the left wall, or against the right two columns
      if (piece_x == 0) or (piece_x == 8) or (piece_x == 9):
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i][j-1] == 0) and (matrix[i][j+1] == 0) and (matrix[i][j+2] == 0) and (matrix[i+1][j+1] == 0) and (matrix[i+1][j+2] == 0) and (matrix[i+2][j+1] == 0):
        matrix[i-1][j] = 0
        matrix[i][j-1] = 2
        matrix[i][j+1] = 2
        matrix[i][j+2] = 2
        matrix[i+1][j] = 0
        matrix[i+2][j] = 0
        rotated = True
    # add 1 to orientation; if it hits 3, will go to 1
    piece_orientation = mod(piece_orientation, 2) + 1


  return piece_orientation


# function to rotate the active piece counter-clockwise, based on player input
def PieceRotateCCW(piece_type, piece_orientation, piece_x, piece_y):
  rotated = False  # set to True if rotation successful

  j = piece_x
  i = piece_y

  if (piece_type == 1):
    if (piece_orientation == 1):
      if (piece_y == 13):  # can't rotate it against the bottom of the play area
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i-1][j] == 0) and (matrix[i+1][j-1] == 0) and (matrix[i+1][j] == 0):
        matrix[i-1][j-1] = 2
        matrix[i-1][j] = 2
        matrix[i-1][j+1] = 0
        matrix[i][j-1] = 0
        matrix[i][j+1] = 0
        matrix[i+1][j] = 2
        rotated = True
    elif (piece_orientation == 2):
      if (piece_x == 0):  # can't rotate it against the left wall
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i-1][j+1] == 0) and (matrix[i][j-1] == 0) and (matrix[i][j+1] == 0):
        matrix[i-1][j] = 0
        matrix[i-1][j+1] = 2
        matrix[i][j-1] = 2
        matrix[i][j+1] = 2
        matrix[i+1][j] = 0
        matrix[i+1][j+1] = 0
        rotated = True
    elif (piece_orientation == 3):
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j] == 0) and (matrix[i-1][j+1] == 0) and (matrix[i+1][j] == 0) and (matrix[i+1][j+1] == 0):
        matrix[i-1][j] = 2
        matrix[i][j-1] = 0
        matrix[i][j+1] = 0
        matrix[i+1][j-1] = 0
        matrix[i+1][j] = 2
        matrix[i+1][j+1] = 2
        rotated = True
    elif (piece_orientation == 4):
      if (piece_x == 9):  # can't rotate it against the right wall
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i][j-1] == 0) and (matrix[i][j+1] == 0) and (matrix[i+1][j-1] == 0) and (matrix[i+1][j+1] == 0):
        matrix[i-1][j-1] = 0
        matrix[i-1][j] = 0
        matrix[i][j-1] = 2
        matrix[i][j+1] = 2
        matrix[i+1][j-1] = 2
        matrix[i+1][j] = 0
        rotated = True
    # subtract 1 from orientation; if it hits 0, will go to 4
    piece_orientation -= 1
    if (piece_orientation == 0):
      piece_orientation = 4
  elif (piece_type == 2):
    if (piece_orientation == 1):
      if (piece_y == 13):  # can't rotate it against the bottom of the play area
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j] == 0) and (matrix[i-1][j+1] == 0) and (matrix[i+1][j-1] == 0) and (matrix[i+1][j] == 0):
        matrix[i-1][j-1] = 0
        matrix[i-1][j] = 2
        matrix[i][j-1] = 0
        matrix[i][j+1] = 0
        matrix[i+1][j-1] = 2
        matrix[i+1][j] = 2
        rotated = True
    elif (piece_orientation == 2):
      if (piece_x == 0):  # can't rotate it against the left wall
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i][j-1] == 0) and (matrix[i][j+1] == 0) and (matrix[i+1][j+1] == 0):
        matrix[i-1][j-1] = 2
        matrix[i-1][j] = 0
        matrix[i-1][j+1] = 0
        matrix[i][j-1] = 2
        matrix[i][j+1] = 2
        matrix[i+1][j] = 0
        rotated = True
    elif (piece_orientation == 3):
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j] == 0) and (matrix[i-1][j+1] == 0) and (matrix[i+1][j-1] == 0) and (matrix[i+1][j] == 0):
        matrix[i-1][j] = 2
        matrix[i-1][j+1] = 2
        matrix[i][j-1] = 0
        matrix[i][j+1] = 0
        matrix[i+1][j] = 2
        matrix[i+1][j+1] = 0
        rotated = True
    elif (piece_orientation == 4):
      if (piece_x == 9):  # can't rotate it against the right wall
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i][j-1] == 0) and (matrix[i][j+1] == 0) and (matrix[i+1][j+1] == 0):
        matrix[i-1][j] = 0
        matrix[i][j-1] = 2
        matrix[i][j+1] = 2
        matrix[i+1][j-1] = 0
        matrix[i+1][j] = 0
        matrix[i+1][j+1] = 2
        rotated = True
    # subtract 1 from orientation; if it hits 0, will go to 4
    piece_orientation -= 1
    if (piece_orientation == 0):
      piece_orientation = 4
  elif (piece_type == 3):
    if (piece_orientation == 1):
      if (piece_y == 13):  # can't rotate it against the bottom of the play area
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i+1][j-1] == 0) and (matrix[i+1][j] == 0):
        matrix[i-1][j-1] = 2
        matrix[i-1][j] = 0
        matrix[i-1][j+1] = 0
        matrix[i+1][j] = 2
        rotated = True
    elif (piece_orientation == 2):
      if (piece_x == 0):  # can't rotate it against the left wall
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i-1][j+1] == 0) and (matrix[i][j-1] == 0):
        matrix[i-1][j+1] = 2
        matrix[i][j-1] = 2
        matrix[i][j+1] = 0
        matrix[i+1][j+1] = 0
        rotated = True
    elif (piece_orientation == 3):
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j] == 0) and (matrix[i-1][j+1] == 0) and (matrix[i+1][j+1] == 0):
        matrix[i-1][j] = 2
        matrix[i+1][j-1] = 0
        matrix[i+1][j] = 0
        matrix[i+1][j+1] = 2
        rotated = True
    elif (piece_orientation == 4):
      if (piece_x == 9):  # can't rotate it against the right wall
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i][j+1] == 0) and (matrix[i+1][j-1] == 0) and (matrix[i+1][j+1] == 0):
        matrix[i-1][j-1] = 0
        matrix[i][j-1] = 0
        matrix[i][j+1] = 2
        matrix[i+1][j-1] = 2
        rotated = True
    # subtract 1 from orientation; if it hits 0, will go to 4
    piece_orientation -= 1
    if (piece_orientation == 0):
      piece_orientation = 4
  elif (piece_type == 4):
    if (piece_orientation == 1):
      if (piece_y == 13):  # can't rotate it against the bottom of the play area
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j+1] == 0) and (matrix[i][j-1] == 0) and (matrix[i+1][j-1] == 0):
        matrix[i-1][j-1] = 0
        matrix[i][j-1] = 2
        matrix[i][j+1] = 0
        matrix[i+1][j-1] = 2
        rotated = True
    elif (piece_orientation == 2):
      if (piece_x == 0):  # can't rotate it against the left wall
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i-1][j] == 0) and (matrix[i+1][j+1] == 0):
        matrix[i-1][j-1] = 2
        matrix[i-1][j] = 2
        matrix[i-1][j+1] = 0
        matrix[i+1][j] = 0
        rotated = True
    elif (piece_orientation == 3):
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j+1] == 0) and (matrix[i][j+1] == 0) and (matrix[i+1][j-1] == 0):
        matrix[i-1][j+1] = 2
        matrix[i][j-1] = 0
        matrix[i][j+1] = 2
        matrix[i+1][j+1] = 0
        rotated = True
    elif (piece_orientation == 4):
      if (piece_x == 9):  # can't rotate it against the right wall
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i+1][j] == 0) and (matrix[i+1][j+1] == 0):
        matrix[i-1][j] = 0
        matrix[i+1][j-1] = 0
        matrix[i+1][j] = 2
        matrix[i+1][j+1] = 2
        rotated = True
    # subtract 1 from orientation; if it hits 0, will go to 4
    piece_orientation -= 1
    if (piece_orientation == 0):
      piece_orientation = 4
  elif (piece_type == 5):
    if (piece_orientation == 1):
      if (piece_y == 13):  # can't rotate it against the bottom of the play area
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i-1][j+1] == 0) and (matrix[i+1][j-1] == 0) and (matrix[i+1][j] == 0):
        matrix[i][j+1] = 0
        matrix[i+1][j] = 2
        rotated = True
    elif (piece_orientation == 2):
      if (piece_x == 0):  # can't rotate it against the left wall
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i-1][j+1] == 0) and (matrix[i][j-1] == 0) and (matrix[i+1][j+1] == 0):
        matrix[i][j-1] = 2
        matrix[i+1][j] = 0
        rotated = True
    elif (piece_orientation == 3):
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j] == 0) and (matrix[i-1][j+1] == 0) and (matrix[i+1][j-1] == 0) and (matrix[i+1][j+1] == 0):
        matrix[i-1][j] = 2
        matrix[i][j-1] = 0
        rotated = True
    elif (piece_orientation == 4):
      if (piece_x == 9):  # can't rotate it against the right wall
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i][j+1] == 0) and (matrix[i+1][j-1] == 0) and (matrix[i+1][j+1] == 0):
        matrix[i-1][j] = 0
        matrix[i][j+1] = 2
        rotated = True
    # subtract 1 from orientation; if it hits 0, will go to 4
    piece_orientation -= 1
    if (piece_orientation == 0):
      piece_orientation = 4
  elif (piece_type == 6):
    rotated = True
  elif (piece_type == 7):
    if (piece_orientation == 1):
      if (piece_y == 13) or (piece_y == 12):  # can't rotate it against the bottom 2 rows of the play area
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i-1][j] == 0) and (matrix[i+1][j] == 0) and (matrix[i+1][j+1] == 0) and (matrix[i+1][j+2] == 0) and (matrix[i+2][j] == 0) and (matrix[i+2][j+1] == 0):
        matrix[i-1][j] = 2
        matrix[i][j-1] = 0
        matrix[i][j+1] = 0
        matrix[i][j+2] = 0
        matrix[i+1][j] = 2
        matrix[i+2][j] = 2
        rotated = True
    elif (piece_orientation == 2):
      # can't rotate it against the left wall, or against the right two columns
      if (piece_x == 0) or (piece_x == 8) or (piece_x == 9):
        return piece_orientation
      # if all these conditions met, can rotate piece
      if (matrix[i-1][j-1] == 0) and (matrix[i][j-1] == 0) and (matrix[i][j+1] == 0) and (matrix[i][j+2] == 0) and (matrix[i+1][j+1] == 0) and (matrix[i+1][j+2] == 0) and (matrix[i+2][j+1] == 0):
        matrix[i-1][j] = 0
        matrix[i][j-1] = 2
        matrix[i][j+1] = 2
        matrix[i][j+2] = 2
        matrix[i+1][j] = 0
        matrix[i+2][j] = 0
        rotated = True
    # subtract 1 from orientation; if it hits 0, will go to 2
    piece_orientation -= 1
    if (piece_orientation == 0):
      piece_orientation = 2


  return piece_orientation


# ----------------------------- _____FUNCTIONS_____ ------------------------------


# ----------------------------------- CLASSES ------------------------------------


class Building(pygame.sprite.Sprite):
  """building in game intro"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('INTRObuilding.gif', -1)
    self.rect.bottomleft = (217, 174)
    self.y_change = 0

  def update(self):
    self.rect.move_ip((0, self.y_change))


class Background(pygame.sprite.Sprite):
  """used to load backgrounds (full-screen graphics)"""
  def __init__(self, name):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image(name)
    self.rect.topleft = (0, 0)

  def reset(self, name):
    self.image, junk = load_image(name)


class BlankBlock(pygame.sprite.Sprite):
  """used to blank out blocks when they're moved or rotated"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image = pygame.Surface((80, 80))
    self.image = self.image.convert()
    self.image.fill((40, 170, 130))
    self.rect = self.image.get_rect()


class BlankTime(pygame.sprite.Sprite):
  """used to blank out time before it's redrawn"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('GPblankTime.gif')
    self.rect.topleft = (44, 204)


class Block(pygame.sprite.Sprite):
  """a single block of a game piece, or a placed block"""
  def __init__(self, num):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    if (num == 2):  # normal block in piece
      self.image, self.rect = load_image('GPpshooterBlock.gif')
    elif (num == 3):  # center block in piece
      self.image, self.rect = load_image('GPpshooterBlockBright.gif')
    self.name = "pshooter"
    self.num = num

  def change(self, type):
    self.type = type
    if (self.num == 2):
      self.image, junk = load_image('GP' + self.type + 'Block.gif')
    elif (self.num == 3):
      self.image, junk = load_image('GP' + self.type + 'BlockBright.gif')


class Blocks(pygame.sprite.Sprite):
  """actual blocks corresponding to the block matrix"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image = pygame.Surface((160, 224))
    self.image = self.image.convert()
    self.image.fill((40, 170, 130))
    self.image.set_colorkey((40, 170, 130), RLEACCEL)
    self.rect = self.image.get_rect()
    self.rect.topleft = (144, 0)

  def clear(self):
    self.image.fill((40, 170, 130))


class Character(pygame.sprite.Sprite):
  """creates a character loaded from the game-specific char files"""
  def __init__(self, ch):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    if ((ord(ch) >= 48) and (ord(ch) <= 57)):  # 0-9
      self.image, self.rect = load_image('CHR' + ch + '.gif', -1)
    elif ((ord(ch) >= 65) and (ord(ch) <= 90)):  # A-Z
      self.image, self.rect = load_image('CHR' + ch + '.gif', -1)
    elif (ord(ch) == 32) or (ch == "\n"):  # space
      self.image, self.rect = load_image('CHRspace.gif', -1)
    elif (ch == "~"):  # space without the transparency (a solid black square)
      self.image, self.rect = load_image('CHRblank.gif')
    elif (ord(ch) == 39):  # apostrophe
      self.image, self.rect = load_image('CHRapostrophe.gif', -1)
    elif (ord(ch) == 34):  # double-quote
      self.image, self.rect = load_image('CHRdqR.gif', -1)
    elif (ch == "!"):
      self.image, self.rect = load_image('CHRexclamation.gif', -1)
    elif (ch == "?"):
      self.image, self.rect = load_image('CHRquestion.gif', -1)
    elif (ch == "."):
      self.image, self.rect = load_image('CHRperiod.gif', -1)
    elif (ch == ","):
      self.image, self.rect = load_image('CHRcomma.gif', -1)
    elif (ch == ":"):
      self.image, self.rect = load_image('CHRcolon.gif', -1)
    elif (ch == "-"):  # dash
      self.image, self.rect = load_image('CHRdash.gif', -1)
    else:  # defaults to '0' if character not recognized
      self.image, self.rect = load_image('CHR0.gif', -1)


class City(pygame.sprite.Sprite):
  """city in background of game intro"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('INTROcity.gif')
    self.rect.topleft = (0, -50)
    self.y_change = 0

  def update(self):
    self.rect.move_ip((0, self.y_change))


class CreditsMM(pygame.sprite.Sprite):
  """still of MM for credits"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('CREDITSmm.gif', -1)
    self.rect.topleft = (145, 240)
    self.name = "mega man"

  def move(self):
    self.rect.move_ip((0, -1))


class Copyrights(pygame.sprite.Sprite):
  """copyrights for game intro"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('INTROcopyrights.gif')
    self.rect.topleft = (0, 0)


class EnterName(pygame.sprite.Sprite):
  """ENTER NAME message for best times screen"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('BTenterName.gif')
    self.rect.topleft = (104, 200)


class ENCursor(pygame.sprite.Sprite):
  """cursor for Enter Name state"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('CHRenCursor.gif', -1)
    self.rect.left = (159)
    self.alpha = 255
    self.count = 0

  def move(self, right):
    if (right is True):
      self.rect.move_ip((8, 0))
    else:
      self.rect.move_ip((-8, 0))

  def update(self):
    if (self.count == 6):
      if (self.alpha == 255):
        self.alpha = 0
      else:
        self.alpha = 255
      self.image.set_alpha(self.alpha)
      self.count = 0
    else:
      self.count += 1


class Fade(pygame.sprite.Sprite):
  """sprite as big as the screen, used to fade the screen in / out, or to flash"""
  def __init__(self, r, g, b, screen_x = 320, screen_y = 240):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image = pygame.Surface((screen_x, screen_y))
    self.image = self.image.convert()
    self.image.fill((r, g, b))
    self.rect = self.image.get_rect()
    self.rect.topleft = (0, 0)


class GPbackground(pygame.sprite.Sprite):
  """used to load backgrounds for gameplay"""
  def __init__(self, num):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.frame = 1  # used to animate backgrounds

    if (num == 0):
      self.image, self.rect = load_image('GPbackgroundBubble1.gif')
    elif (num == 1):
      self.image, self.rect = load_image('GPbackgroundAir1.gif')
    elif (num == 2):
      self.image, self.rect = load_image('GPbackgroundQuick.gif')
    elif (num == 3):
      self.image, self.rect = load_image('GPbackgroundHeat1.gif')
    elif (num == 4):
      self.image, self.rect = load_image('GPbackgroundWood.gif')
    elif (num == 5):
      self.image, self.rect = load_image('GPbackgroundMetal1.gif')
    elif (num == 6):
      self.image, self.rect = load_image('GPbackgroundFlash1.gif')
    elif (num == 7):
      self.image, self.rect = load_image('GPbackgroundCrash.gif')
    elif (num == 8):
      self.image, self.rect = load_image('GPbackgroundWily.gif')

    self.rect.topleft = (0, 0)

  def update(self, num):
    if (num == 0):
      self.frame += 1
      if (self.frame == 4):
        self.frame = 1
      self.image, self.rect = load_image('GPbackgroundBubble' + str(self.frame) + '.gif')
    elif (num == 1):
      self.frame += 1
      if (self.frame == 5):
        self.frame = 1
      self.image, self.rect = load_image('GPbackgroundAir' + str(self.frame) + '.gif')
    elif (num == 3):
      self.frame += 1
      if (self.frame == 4):
        self.frame = 1
      self.image, self.rect = load_image('GPbackgroundHeat' + str(self.frame) + '.gif')
    elif (num == 5):
      self.frame += 1
      if (self.frame == 3):
        self.frame = 1
      self.image, self.rect = load_image('GPbackgroundMetal' + str(self.frame) + '.gif')
    elif (num == 6):
      self.frame += 1
      if (self.frame == 4):
        self.frame = 1
      self.image, self.rect = load_image('GPbackgroundFlash' + str(self.frame) + '.gif')


class Highlights(pygame.sprite.Sprite):
  """highlights for stage select"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('SShighlights.gif', -1)
    self.rect.topleft = (138, 86)

  def update(self, x_change, y_change):
    self.rect.move_ip((x_change, y_change))


class Icon(pygame.sprite.Sprite):
  """icon for game window"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('icon.gif')


class IntroMM(pygame.sprite.Sprite):
  """Mega Man on intro / title screen"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('INTROmmHair1.gif', -1)
    self.hair1 = True
    self.blink = False
    self.warp_frame = "none"
    self.rect.bottomleft = (266, -1005)
    self.y_change = 0

  def update(self):
    self.rect.move_ip((0, self.y_change))

  # used to make his hair blow; junk is where the useless rect is placed
  def hair(self, blink):
    if (blink == 1):  # load blinking images
      if (self.hair1 is True):
        self.hair1 = False
        self.image, junk = load_image('INTROmmHair2Blink.gif', -1)
      elif (self.hair1 is False):
        self.hair1 = True
        self.image, junk = load_image('INTROmmHair1Blink.gif', -1)
    elif (blink == 0) or (blink == 2):  # load non-blinking images
      if (self.hair1 is True):
        self.hair1 = False
        self.image, junk = load_image('INTROmmHair2.gif', -1)
      elif (self.hair1 is False):
        self.hair1 = True
        self.image, junk = load_image('INTROmmHair1.gif', -1)

  # used for animation of putting on helmet and warping him off the screen, when the player presses Enter
  def warp(self):
    if (self.warp_frame == "none"):
      self.image, junk = load_image('INTROmmHelm1.gif', -1)
      self.warp_frame = "helm1"
    elif (self.warp_frame == "helm1"):
      self.image, junk = load_image('INTROmmHelm2.gif', -1)
      self.warp_frame = "helm2"
    elif (self.warp_frame == "helm2"):
      self.image, junk = load_image('INTROmmHelm3.gif', -1)
      self.warp_frame = "helm3"
    elif (self.warp_frame == "helm3"):
      self.image, junk = load_image('INTROmmHelm4.gif', -1)
      self.warp_frame = "helm4"
    elif (self.warp_frame == "helm4"):
      self.image, junk = load_image('INTROmmHelm5.gif', -1)
      self.warp_frame = "helm5"
    elif (self.warp_frame == "helm5"):
      self.image, junk = load_image('INTROmmHelm6.gif', -1)
      self.warp_frame = "helm6"
    elif (self.warp_frame == "helm6"):  # after helmet flashes, stands for a second before warping
      self.image, junk = load_image('INTROmmHelm3.gif', -1)
      self.warp_frame = "helm3a"
    elif (self.warp_frame == "helm3a"):  # rect changes on this one
      self.image, self.rect = load_image('INTROmmWarp1.gif', -1)
      self.rect.bottomleft = (266, 145)
      self.warp_frame = "warp1"
    elif (self.warp_frame == "warp1"):  # and on this one
      self.image, self.rect = load_image('INTROmmWarp2.gif', -1)
      self.rect.bottomleft = (266, 145)
      self.warp_frame = "warp2"


class LifeBar(pygame.sprite.Sprite):
  """single life bar for filling up enemy energy during gameplay"""
  def __init__(self, num):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    if (num == 0):
      self.image, self.rect = load_image('GPlifeBubble.gif')
    elif (num == 1):
      self.image, self.rect = load_image('GPlifeAir.gif')
    elif (num == 2):
      self.image, self.rect = load_image('GPlifeQuick.gif')
    elif (num == 3):
      self.image, self.rect = load_image('GPlifeHeat.gif')
    elif (num == 4):
      self.image, self.rect = load_image('GPlifeWood.gif')
    elif (num == 5):
      self.image, self.rect = load_image('GPlifeMetal.gif')
    elif (num == 6):
      self.image, self.rect = load_image('GPlifeFlash.gif')
    elif (num == 7):
      self.image, self.rect = load_image('GPlifeCrash.gif')
    elif (num == 8):
      self.image, self.rect = load_image('GPlifeWily.gif')


class LifeMeter(pygame.sprite.Sprite):
  """empty life meter for enemy energy during gameplay"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('GPlifeMeter.gif')
    self.rect.topleft = (120, 15)


class MegaMan(pygame.sprite.Sprite):
  """Mega Man during gameplay"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('MMpshooterWarp2.gif', -1)
    self.rect.bottomleft = (16, -4)
    self.action = "nothing"
    self.frame = 2  # starts in frame 2 of warp
    self.weapon = "pshooter"

  def animate(self):
    if (self.action == "warping in"):
      if (self.frame == 2):
        self.image, junk = load_image('MM' + self.weapon + 'Warp1.gif', -1)
        self.frame = 1
      elif (self.frame == 1):
        self.image, junk = load_image('MM' + self.weapon + 'Stand.gif', -1)
        self.action = "standing"
        self.frame = -1
    elif (self.action == "standing"):
      self.image, junk = load_image('MM' + self.weapon + 'Blink.gif', -1)
      self.action = "blinking"
    elif (self.action == "blinking"):
      self.image, junk = load_image('MM' + self.weapon + 'Stand.gif', -1)
      self.action = "standing"
    elif (self.action == "warping out"):
      if (self.frame == -1):
        self.image, junk = load_image('MM' + self.weapon + 'Warp1.gif', -1)
        self.frame = 1
      elif (self.frame == 1):
        self.image, junk = load_image('MM' + self.weapon + 'Warp2.gif', -1)
        self.action = "nothing"
        self.frame = 2
    elif (self.action == "nothing"):
      pass
    else:  # helps to find bugs in self.action assignments
      self.image, junk = load_image('MM' + self.weapon + 'Blink.gif', -1)

  def move(self, x_change, y_change):
    self.rect.move_ip((x_change, y_change))


class Paused(pygame.sprite.Sprite):
  """bat with "PAUSED" message that flies around when game paused"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('GPpaused1.gif', -1)
    self.rect.topleft = (201, 100)
    self.frame = 1
    self.x_vel = 0
    self.y_vel = 0

  def animate(self):
    self.frame = mod(self.frame, 4) + 1
    self.image, junk = load_image('GPpaused' + str(self.frame) + '.gif', -1)

  def move(self):
    self.rect.move_ip((self.x_vel, self.y_vel))

    if (self.rect.left <= 144):
      self.rect.left = 144 + (144 - self.rect.left)
      self.x_vel *= -1
      a = random.randint(1, 4)
      if (a == 1):  # change y velocity
        if (self.y_vel > 0):
          sign = 1
        else:
          sign = -1
        self.y_vel = random.randint(2, 4) * sign
    elif (self.rect.right >= 303):
      self.rect.right = 303 - (303 - self.rect.right)
      self.x_vel *= -1
      a = random.randint(1, 4)
      if (a == 1):  # change y velocity
        if (self.y_vel > 0):
          sign = 1
        else:
          sign = -1
        self.y_vel = random.randint(2, 4) * sign

    if (self.rect.top <= 0):
      self.rect.top = 0 + (0 - self.rect.top)
      self.y_vel *= -1
      a = random.randint(1, 4)
      if (a == 1):  # change x velocity
        if (self.x_vel > 0):
          sign = 1
        else:
          sign = -1
        self.x_vel = random.randint(2, 4) * sign
    elif (self.rect.bottom >= 223):
      self.rect.bottom = 223 - (223 - self.rect.bottom)
      self.y_vel *= -1
      a = random.randint(1, 4)
      if (a == 1):  # change x velocity
        if (self.x_vel > 0):
          sign = 1
        else:
          sign = -1
        self.x_vel = random.randint(2, 4) * sign


class PressEnter(pygame.sprite.Sprite):
  """PRESS ENTER message for title screen"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('pressEnter.gif')
    self.rect.topleft = (117, 149)
    self.alpha = 255
    self.slow_fade = 0  # used to fade slow at first
    self.delay = 0  # delay to get the most opaque part to time with the music of the title screen

  def update(self, title):
    if ((title is True) and (self.delay < 15)):
      self.delay += 1
    elif ((title is False) and (self.delay < 6)):
      self.delay += 1
    else:
      if (self.alpha >= 35):
        if (self.slow_fade < 10):
          self.alpha -= 1
          self.image.set_alpha(self.alpha)
          self.slow_fade += 1
        else:
          self.alpha -= 10
          self.image.set_alpha(self.alpha)
      else:
        self.alpha = 255
        self.slow_fade = 0


class Quit(pygame.sprite.Sprite):
  """QUIT message for gameplay"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('GPquit.gif', -1)
    self.rect.topleft = (204, 184)


class Quit2(pygame.sprite.Sprite):
  """QUIT message for stage select"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('SSquit.gif', -1)
    self.rect.topleft = (129, 97)


class Ready(pygame.sprite.Sprite):
  """READY message for gameplay"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('GPready.gif', -1)
    self.rect.topleft = (204, 108)
    self.alpha = 255

  def update(self):
    if (self.alpha == 255):
      self.image.set_alpha(0)
      self.alpha = 0
    elif (self.alpha == 0):
      self.image.set_alpha(255)
      self.alpha = 255


class Robot(pygame.sprite.Sprite):
  """enemy robots (non-Wily) for gameplay"""
  def __init__(self, num):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    if (num == 0):
      self.image, self.rect = load_image('ROBOTbubbleStand.gif', -1)
      self.name = "bubble"
    elif (num == 1):
      self.image, self.rect = load_image('ROBOTairStand.gif', -1)
      self.name = "air"
    elif (num == 2):
      self.image, self.rect = load_image('ROBOTquickStand.gif', -1)
      self.name = "quick"
    elif (num == 3):
      self.image, self.rect = load_image('ROBOTheatClosed.gif', -1)
      self.name = "heat"
    elif (num == 4):
      self.image, self.rect = load_image('ROBOTwoodStand.gif', -1)
      self.name = "wood"
    elif (num == 5):
      self.image, self.rect = load_image('ROBOTmetalStand.gif', -1)
      self.name = "metal"
    elif (num == 6):
      self.image, self.rect = load_image('ROBOTflashStand.gif', -1)
      self.name = "flash"
    elif (num == 7):
      self.image, self.rect = load_image('ROBOTcrashStand.gif', -1)
      self.name = "crash"
    self.rect.bottomleft = (74, 48)
    self.action = "nothing"
    self.frame = -1  # not currently being animated
    self.framecount = 0
    self.hitpoints = 16  # life

  def animate(self):
    self.framecount += 1

    if (self.action == "nothing"):
      self.image, junk = load_image('ROBOT' + self.name + 'Act1.gif', -1)
      self.action = "intro"
      self.frame = 1
    elif (self.action == "intro"):
      if (self.frame == 1):
        self.image, junk = load_image('ROBOT' + self.name + 'Act2.gif', -1)
        self.frame = 2
      elif (self.frame == 2) and (self.name != "flash"):
        if (self.framecount < 12) and ((self.name == "air") or (self.name == "heat") or (self.name == "wood")):
          self.image, junk = load_image('ROBOT' + self.name + 'Act1.gif', -1)
          self.frame = 1
        else:
          self.action = "waiting"
      elif (self.frame == 2) and (self.name == "flash"):
        self.image, junk = load_image('ROBOTflashCrouch.gif', -1)
        self.frame = 3
      elif (self.frame == 3):  # Flash Man only
        self.action = "waiting"

      # rotate fan-mouth in 2 sets, like in MM2, with regular standing between the sets
      if (self.name == "air") and ((self.framecount == 6) or (self.framecount == 7)):
        self.image, junk = load_image('ROBOTairStand.gif', -1)
    elif (self.action == "hit"):  # robot is hit from line completion
      if (self.hitpoints > 0):
        if (self.frame == -1):
          self.image, junk = load_image('ROBOT' + self.name + 'Stand.gif', -1)
          self.frame = 1
        elif (self.frame == 1):
          self.image, junk = load_image('ROBOT' + self.name + 'Hit.gif', -1)
          self.frame = -1
    else:  # default to standing; this will catch "waiting" also
        self.image, junk = load_image('ROBOT' + self.name + 'Stand.gif', -1)
        self.action = "standing"
        self.frame = -1


class RobotDeath(pygame.sprite.Sprite):
  """pulsating orbs for robot death explosion"""
  def __init__(self, num, type):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('GP' + type + 'Death1.gif', -1)
    if (type == "robot"):
      self.rect.topleft = (83, 28)
    elif (type == "pshooterMM"):
      self.rect.topleft = (24, 31)

    if (num == 0):
      self.x_vel = 0
      self.y_vel = -10
    elif (num == 1):
      self.x_vel = 0
      self.y_vel = -20
    elif (num == 2):
      self.x_vel = 15
      self.y_vel = -15
    elif (num == 3):
      self.x_vel = 10
      self.y_vel = 0
    elif (num == 4):
      self.x_vel = 20
      self.y_vel = 0
    elif (num == 5):
      self.x_vel = 15
      self.y_vel = 15
    elif (num == 6):
      self.x_vel = 0
      self.y_vel = 10
    elif (num == 7):
      self.x_vel = 0
      self.y_vel = 20
    elif (num == 8):
      self.x_vel = -15
      self.y_vel = 15
    elif (num == 9):
      self.x_vel = -10
      self.y_vel = 0
    elif (num == 10):
      self.x_vel = -20
      self.y_vel = 0
    elif (num == 11):
      self.x_vel = -15
      self.y_vel = -15
    self.frame = 1
    self.type = type

  def move(self):
    self.rect.move_ip((self.x_vel, self.y_vel))

  def animate(self):
    self.frame += 1
    if (self.frame == 5):
      self.frame = 1
    self.image, junk = load_image('GP' + self.type + 'Death' + str(self.frame) + '.gif', -1)

  def change(self, type):
    self.type = type
    self.image, junk = load_image('GP' + self.type + 'Death' + str(self.frame) + '.gif', -1)


class RobotFace(pygame.sprite.Sprite):
  """robot faces for stage select and gameplay"""
  def __init__(self, screen, num):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    if (screen == 'SS'):
      if (num == 0):
        self.image, self.rect = load_image('SSbubble.gif')
        self.rect.bottomleft = (80, 60)
      elif (num == 1):
        self.image, self.rect = load_image('SSair.gif')
        self.rect.bottomleft = (144, 60)
      elif (num == 2):
        self.image, self.rect = load_image('SSquick.gif')
        self.rect.bottomleft = (208, 60)
      elif (num == 3):
        self.image, self.rect = load_image('SSheat.gif')
        self.rect.bottomleft = (80, 124)
      elif (num == 4):
        self.image, self.rect = load_image('SSwood.gif')
        self.rect.bottomleft = (208, 124)
      elif (num == 5):
        self.image, self.rect = load_image('SSmetal.gif')
        self.rect.bottomleft = (80, 188)
      elif (num == 6):
        self.image, self.rect = load_image('SSflash.gif')
        self.rect.bottomleft = (144, 188)
      elif (num == 7):
        self.image, self.rect = load_image('SScrash.gif')
        self.rect.bottomleft = (208, 188)
      elif (num == 8):  # grayscale image of Wily's stage select box
        self.image, self.rect = load_image('SSwilyNo.gif')
        self.rect.bottomleft = (144, 124)
    elif (screen == 'GP'):
      if (num == 0):
        self.image, self.rect = load_image('GPwpnBubbleNo.gif')
        self.rect.bottomleft = (10, 112)
        self.name = "Bubble"
      elif (num == 1):
        self.image, self.rect = load_image('GPwpnAirNo.gif')
        self.rect.bottomleft = (48, 112)
        self.name = "Air"
      elif (num == 2):
        self.image, self.rect = load_image('GPwpnQuickNo.gif')
        self.rect.bottomleft = (86, 112)
        self.name = "Quick"
      elif (num == 3):
        self.image, self.rect = load_image('GPwpnHeatNo.gif')
        self.rect.bottomleft = (10, 150)
        self.name = "Heat"
      elif (num == 4):
        self.image, self.rect = load_image('GPwpnWoodNo.gif')
        self.rect.bottomleft = (86, 150)
        self.name = "Wood"
      elif (num == 5):
        self.image, self.rect = load_image('GPwpnMetalNo.gif')
        self.rect.bottomleft = (10, 188)
        self.name = "Metal"
      elif (num == 6):
        self.image, self.rect = load_image('GPwpnFlashNo.gif')
        self.rect.bottomleft = (48, 188)
        self.name = "Flash"
      elif (num == 7):
        self.image, self.rect = load_image('GPwpnCrashNo.gif')
        self.rect.bottomleft = (86, 188)
        self.name = "Crash"
      elif (num == -1):  # used for Mega Man's face
        self.image, self.rect = load_image('GPwpnPShooter.gif')
        self.rect.bottomleft = (48, 150)
      self.color = False  # they default to grayscale

  def update(self):  # used for GP faces only
    if (self.color is False):  # face currently gray, so color it
      if (self.name == "Quick"):
        self.image, junk = load_image('GPwpnQuickYes.gif', -1)
      else:
        self.image, junk = load_image('GPwpn' + self.name + 'Yes.gif')
      self.color = True
    else:  # face currently colored, so grayscale it
      if (self.name == "Quick"):
        self.image, junk = load_image('GPwpnQuickNo.gif')
      else:
        self.image, junk = load_image('GPwpn' + self.name + 'No.gif')
      self.color = False


class Rush(pygame.sprite.Sprite):
  """Mega Man's dog Rush (from Mega Man 3), for the Quit prompt"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('RUSHwarp2.gif', -1)
    self.rect.bottomleft = (209, -4)
    self.action = "warping in"
    self.frame = 2  # starts in frame 2 of warp

  def animate(self):
    if (self.action == "warping in"):
      if (self.frame == 2):
        self.image, junk = load_image('RUSHwarp1.gif', -1)
        self.frame = 1
      elif (self.frame == 1):
        self.image, junk = load_image('RUSHstand.gif', -1)
        self.action = "standing"
        self.frame = -1
    elif (self.action == "standing"):
      self.image, junk = load_image('RUSHwag.gif', -1)
      self.action = "wagging"
    elif (self.action == "wagging"):
      self.image, junk = load_image('RUSHstand.gif', -1)
      self.action = "standing"
    elif (self.action == "warping out"):
      if (self.frame == -1):
        self.image, junk = load_image('RUSHwarp1.gif', -1)
        self.frame = 1
      elif (self.frame == 1):
        self.image, junk = load_image('RUSHwarp2.gif', -1)
        self.frame = 2

  def move(self, x_change, y_change):
    self.rect.move_ip((x_change, y_change))


class Ship(pygame.sprite.Sprite):
  """Wily's spaceship"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('WILYship1.gif', -1)
    self.rect.topleft = (25, 64)
    self.x_vel = 1
    self.frame = 1
    self.anim_count = 0

  def move(self):
    self.rect.move_ip((self.x_vel, 0))

  def animate(self):
    self.anim_count += 1
    if (self.anim_count == 5):
      self.frame = mod(self.frame, 3) + 1  # increment frame
      self.image, junk = load_image('WILYship' + str(self.frame) + '.gif', -1)
      self.anim_count = -1


class Star(pygame.sprite.Sprite):
  """stars for starfields"""
  def __init__(self, num, x_pos = 0, y_pos = 0):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    if (num == 1):
      self.image, self.rect = load_image('STARsmall.gif')
      self.x_vel = 1
    elif (num == 2):
      self.image, self.rect = load_image('STARmedium.gif')
      self.x_vel = 2
    elif (num == 3):
      self.image, self.rect = load_image('STARlarge.gif', -1)
      self.x_vel = 3
    self.rect.topleft = (x_pos, y_pos)

  def move(self):
    self.rect.move_ip((self.x_vel, 0))


class Story(pygame.sprite.Sprite):
  """story pages for game intro"""
  def __init__(self, page):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    if (page > 0) and (page < 8):
      self.image, self.rect = load_image('INTROstory' + str(page) + '.gif')
    else:
      self.image, self.rect = load_image('INTROstoryBlank.gif')
    self.rect.topleft = (0, 174)
    self.y_change = 0

  def update(self):
    self.rect.move_ip((0, self.y_change))


class TextLine(pygame.sprite.Sprite):
  """a line of text"""
  def __init__(self, string):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image = pygame.Surface((320, 8))
    self.image = self.image.convert()
    self.image.fill((40, 170, 130))  # transparent color, as set in the next statement
    self.image.set_colorkey((40, 170, 130), RLEACCEL)
    self.rect = self.image.get_rect()
    self.rect.topleft = (0, 240)  # just off the bottom of the screen (only used for credits in this program)
    self.move_count = 1
    self.name = ""

    for i in range(len(string)):
      ch = Character(string[i])
      self.image.blit(ch.image, (i * 8, 0))

    # center the text
    line_width = len(string) * 8
    self.rect.left = 160 - (line_width / 2)

  def move(self):
    self.rect.move_ip((0, -1))


class WeaponBoxSelect(pygame.sprite.Sprite):
  """blue highlight around selected weapon during gameplay"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('GPwpnBoxSel.gif')
    self.rect.topleft = (47, 117)

  def update(self, new_x, new_y):
    self.rect.topleft = (new_x, new_y)


class Wily(pygame.sprite.Sprite):
  """Dr. Wily"""
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('WILYself1.gif', -1)
    self.rect.topleft = (209, 62)
    self.y_vel = -1
    self.action = "coat blowing"
    self.frame = 1
    self.hitpoints = 16  # life

  def animate(self):
    if (self.action == "coat blowing"):
      if (self.frame == 1):
        self.image, junk = load_image('WILYself2.gif', -1)
        self.frame = 2
      else:
        self.image, junk = load_image('WILYself1.gif', -1)
        self.frame = 1
    elif (self.action == "hit"):
      if (self.frame == -1):
        self.breath_out = True
        self.frame = 0

      if (self.frame == 0):
        self.image, junk = load_image('WILYhit.gif', -1)
        if (self.breath_out is True):
          self.frame = 8
          self.breath_out = False
        else:
          self.frame = 9
          self.breath_out = True
      else:  # frame 8 or 9
        self.image, junk = load_image('WILYself' + str(self.frame) + '.gif', -1)
        self.frame = 0
    else:  # all other frame work handled outside of class
      self.image, junk = load_image('WILYself' + str(self.frame) + '.gif', -1)

  def move(self):
    self.rect.move_ip((0, self.y_vel))


class WilyDeath(pygame.sprite.Sprite):
  """pulsating orbs for Wily's death explosion"""
  def __init__(self, num):
    pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
    self.image, self.rect = load_image('GPwilyDeath1.gif', -1)
    self.rect.topleft = (83, 16)

    if (num == 0):
      self.x_vel = 0
      self.y_vel = -10
    elif (num == 1):
      self.x_vel = 0
      self.y_vel = -20
    elif (num == 2):
      self.x_vel = 15
      self.y_vel = -15
    elif (num == 3):
      self.x_vel = 10
      self.y_vel = 0
    elif (num == 4):
      self.x_vel = 20
      self.y_vel = 0
    elif (num == 5):
      self.x_vel = 15
      self.y_vel = 15
    elif (num == 6):
      self.x_vel = 0
      self.y_vel = 10
    elif (num == 7):
      self.x_vel = 0
      self.y_vel = 20
    elif (num == 8):
      self.x_vel = -15
      self.y_vel = 15
    elif (num == 9):
      self.x_vel = -10
      self.y_vel = 0
    elif (num == 10):
      self.x_vel = -20
      self.y_vel = 0
    elif (num == 11):
      self.x_vel = -15
      self.y_vel = -15
    elif (num == 12):
      self.x_vel = 0
      self.y_vel = -5
    elif (num == 13):
      self.x_vel = 11
      self.y_vel = -11
    elif (num == 14):
      self.x_vel = 5
      self.y_vel = 0
    elif (num == 15):
      self.x_vel = 11
      self.y_vel = 11
    elif (num == 16):
      self.x_vel = 0
      self.y_vel = 5
    elif (num == 17):
      self.x_vel = -11
      self.y_vel = 11
    elif (num == 18):
      self.x_vel = -5
      self.y_vel = 0
    elif (num == 19):
      self.x_vel = -11
      self.y_vel = -11
    elif (num == 20):
      self.x_vel = 0
      self.y_vel = -15
    elif (num == 21):
      self.x_vel = 7
      self.y_vel = -7
    elif (num == 22):
      self.x_vel = 15
      self.y_vel = 0
    elif (num == 23):
      self.x_vel = 7
      self.y_vel = 7
    elif (num == 24):
      self.x_vel = 0
      self.y_vel = 15
    elif (num == 25):
      self.x_vel = -7
      self.y_vel = 7
    elif (num == 26):
      self.x_vel = -15
      self.y_vel = 0
    elif (num == 27):
      self.x_vel = -7
      self.y_vel = -7

    self.frame = 1
    self.type = type

  def move(self):
    self.rect.move_ip((self.x_vel, self.y_vel))

  def animate(self):
    self.frame += 1
    if (self.frame == 5):
      self.frame = 1
    self.image, junk = load_image('GPwilyDeath' + str(self.frame) + '.gif', -1)

  def change(self, type):
    self.type = type
    self.image, junk = load_image('GPwilyDeath' + str(self.frame) + '.gif', -1)


# ------------------------------ _____CLASSES_____ -------------------------------


# ------------------------------ *** start MAIN *** ------------------------------


def main():
  # initialize pygame, random seed, and screen mode; set caption; make mouse cursor invisible; set keyboard repeat rate
  pygame.init()
  random.seed()
  screen = pygame.display.set_mode((320, 240), SCALED)
  pygame.display.set_icon(Icon().image)
  pygame.display.set_caption('Mega Man 2: Puzzle Attack')
  pygame.mouse.set_visible(False)
  pygame.key.set_repeat()  # disable key repeat

  # create the backgound
  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill((0, 0, 0))


  # display the background
  screen.blit(background, (0, 0))
  pygame.display.flip()


  # groups that we'll use to reference sprites in different ways
  all_sprites = pygame.sprite.RenderUpdates()

  active_sprites = pygame.sprite.RenderUpdates()
  animated_sprites = pygame.sprite.RenderUpdates()
  fade_sprites = pygame.sprite.RenderUpdates()
  flash_sprites = pygame.sprite.RenderUpdates()
  GP_faces = pygame.sprite.RenderUpdates()
  idle_sprites = pygame.sprite.RenderUpdates()
  starfield = pygame.sprite.RenderUpdates()
  sky = pygame.sprite.RenderUpdates()
  spaceship = pygame.sprite.RenderUpdates()
  wily_sprite = pygame.sprite.RenderUpdates()


  # initialize SFX (sound effects)
  warpout = load_sound('warpout.wav')
  cursor = load_sound('cursor.wav')
  warpin = load_sound('warpin.wav')
  energyfill = load_sound('energyfill.wav')
  shot = []
  shot.append(load_sound('bubbleshot.wav'))
  shot.append(load_sound('airshot.wav'))
  shot.append(load_sound('quickshot.wav'))
  shot.append(load_sound('heatshot.wav'))
  shot.append(load_sound('pshot.wav'))
  shot.append(load_sound('woodshot.wav'))
  shot.append(load_sound('metalshot.wav'))
  shot.append(load_sound('flashshot.wav'))
  shot.append(load_sound('crash2clamp.wav'))
  robothit = load_sound('robothit.wav')
  robotdeath = load_sound('robotdeath.wav')
  shipsound = load_sound('wilyspaceship.wav')


  # clock / timing stuff
  clock = pygame.time.Clock()  # create clock object to use in forcing a certain FPS
  FPS = 48.0  # frames per second to run at; will change later for animation timing, to a minimum of 30.0
  clock_start = pygame.time.get_ticks()  # ref for current time; starts at time since pygame.time called


  # declare globals
  global matrix

  state = "initialize"

  running = True


  # main loop
  while running:
    clock.tick(FPS)  # forces game to run at a certain FPS or less, as defined above
    ct = pygame.time.get_ticks() - clock_start  # current time, in milliseconds

    # clear all sprites from the screen (a feature of the RenderUpdate group)
    active_sprites.clear(screen, background)
    animated_sprites.clear(screen, background)
    fade_sprites.clear(screen, background)
    flash_sprites.clear(screen, background)
    GP_faces.clear(screen, background)
    idle_sprites.clear(screen, background)
    starfield.clear(screen, background)
    sky.clear(screen, background)
    spaceship.clear(screen, background)
    wily_sprite.clear(screen, background)


# ------------------------------------ EVENTS ------------------------------------


    # handle input events
    for event in pygame.event.get():
      if (event.type == KEYDOWN):
        char = event.key
      
      # skip to title screen during intro if Enter pressed
      if (event.type == KEYDOWN) and (state == "intro") and ((event.key == K_RETURN) or (event.key == K_KP_ENTER)):
        initial_delay = False

        state = "title"


      # Enter pressed on title screen
      elif (event.type == KEYDOWN) and (state == "title") and ((event.key == K_RETURN) or (event.key == K_KP_ENTER)):
        title_enter_pressed = True
        pygame.mixer.music.stop()


      # Enter pressed on best times screen
      elif (event.type == KEYDOWN) and (state == "best times") and ((event.key == K_RETURN) or (event.key == K_KP_ENTER)):
        BT_enter_pressed = True
        pygame.mixer.music.stop()


      # handles movement of highlights, pressing Enter, and quitting on stage select
      elif (event.type == KEYDOWN) and (state == "stage select") and (SS_enter_pressed is False):
        if (quit_prompt is False):
          if ((event.key == K_UP) or (event.key == K_KP8) or (event.key == K_w)):
            if (highlight_cell > 3):
              highlight_cell -= 3
              highlights.update(0, -64)
            else:  # 3 or less
              highlight_cell += 6
              highlights.update(0, 128)
            cursor.play()
          elif ((event.key == K_DOWN) or (event.key == K_KP2) or (event.key == K_KP5) or (event.key == K_x) or (event.key == K_s)):
            if (highlight_cell < 7):
              highlight_cell += 3
              highlights.update(0, 64)
            else:  # 7 or higher
              highlight_cell -= 6
              highlights.update(0, -128)
            cursor.play()
          elif ((event.key == K_LEFT) or (event.key == K_KP4) or (event.key == K_a)):
            if (mod(highlight_cell + 2, 3) == 0):  # left-column location
              highlight_cell += 2
              highlights.update(128, 0)
            else:  # middle column or right column
              highlight_cell -= 1
              highlights.update(-64, 0)
            cursor.play()
          elif ((event.key == K_RIGHT) or (event.key == K_KP6) or (event.key == K_d)):
            if (mod(highlight_cell, 3) == 0):  # right-column location
              highlight_cell -= 2
              highlights.update(-128, 0)
            else:  # left column or middle column
              highlight_cell += 1
              highlights.update(64, 0)
            cursor.play()
          elif ((event.key == K_RETURN) or (event.key == K_KP_ENTER)):
            if ((highlight_cell < 5) and (robot_dead[highlight_cell - 1] is False)) or ((highlight_cell > 5) and (robot_dead[highlight_cell - 2] is False)):  # robot player selected is alive
              if (highlight_cell < 5):  # 1-4 maps to 0-3
                selected_robot = highlight_cell - 1
              else:  # 6-9 maps to 4-7
                selected_robot = highlight_cell - 2

              load_music('stageselect-select.mp3')
              pygame.mixer.music.play()
              music_playing = True
              active_pause_count = 0.0
              fade_in_count = 0.0
              fade_out_alpha = 0.0
              flash_sprites.add(whiteFade)
              whiteFade.image.set_alpha(255)
              SS_enter_pressed = True
            elif (highlight_cell == 5) and (robots_dead == 8):  # allowed to fight Wily when other robots dead
              selected_robot = 8

              load_music('stageselect-select.mp3')
              pygame.mixer.music.play()
              music_playing = True
              active_pause_count = 0.0
              fade_in_count = 0.0
              fade_out_alpha = 0.0
              flash_sprites.add(whiteFade)
              whiteFade.image.set_alpha(255)
              SS_enter_pressed = True
          elif ((event.key == K_ESCAPE) or (event.type == QUIT)):
            quit_prompt = True
            quit_init = False
        else:  # (quit_prompt is True)
          if (event.key == K_y):
            running = False
          elif (event.key == K_n) or (event.key == K_ESCAPE):
            blackFade.image.set_alpha(255)
            fade_sprites.remove(blackFade)
            flash_sprites.remove(quit2)
            pygame.mixer.music.set_volume(1.0)
            quit_prompt = False


      # events during gameplay
      elif (state == "gameplay"):
        if (event.type == KEYDOWN):
          if (blocks_moving is True) or ((blocks_moving is False) and (game_paused is True)):
            if ((event.key == K_F1) and (robot_dead[0] is True)):
              selected_weapon = 0
              weapon_box_select.update(9, 79)
              megaman.weapon = "bubble"
              weapon_change_init = False
              weapon_changed = False
              for i in range(12):
                mm_death[i].change("bubbleMM")
              block.change("bubble")
              center_block.change("bubble")
              matrix_update = True
            elif ((event.key == K_F2) and (robot_dead[1] is True)):
              selected_weapon = 1
              weapon_box_select.update(47, 79)
              megaman.weapon = "air"
              weapon_change_init = False
              weapon_changed = False
              for i in range(12):
                mm_death[i].change("airMM")
              block.change("air")
              center_block.change("air")
              matrix_update = True
            elif ((event.key == K_F3) and (robot_dead[2] is True)):
              selected_weapon = 2
              weapon_box_select.update(85, 79)
              megaman.weapon = "quick"
              weapon_change_init = False
              weapon_changed = False
              for i in range(12):
                mm_death[i].change("quickMM")
              block.change("quick")
              center_block.change("quick")
              matrix_update = True
            elif ((event.key == K_F4) and (robot_dead[3] is True)):
              selected_weapon = 3
              weapon_box_select.update(9, 117)
              megaman.weapon = "heat"
              weapon_change_init = False
              weapon_changed = False
              for i in range(12):
                mm_death[i].change("heatMM")
              block.change("heat")
              center_block.change("heat")
              matrix_update = True
            elif (event.key == K_F5):
              selected_weapon = 4
              weapon_box_select.update(47, 117)
              megaman.weapon = "pshooter"
              weapon_change_init = False
              weapon_changed = False
              for i in range(12):
                mm_death[i].change("pshooterMM")
              block.change("pshooter")
              center_block.change("pshooter")
              matrix_update = True
            elif ((event.key == K_F6) and (robot_dead[4] is True)):
              selected_weapon = 5
              weapon_box_select.update(85, 117)
              megaman.weapon = "wood"
              weapon_change_init = False
              weapon_changed = False
              for i in range(12):
                mm_death[i].change("woodMM")
              block.change("wood")
              center_block.change("wood")
              matrix_update = True
            elif ((event.key == K_F7) and (robot_dead[5] is True)):
              selected_weapon = 6
              weapon_box_select.update(9, 155)
              megaman.weapon = "metal"
              weapon_change_init = False
              weapon_changed = False
              for i in range(12):
                mm_death[i].change("metalMM")
              block.change("metal")
              center_block.change("metal")
              matrix_update = True
            elif ((event.key == K_F8) and (robot_dead[6] is True)):
              selected_weapon = 7
              weapon_box_select.update(47, 155)
              megaman.weapon = "flash"
              weapon_change_init = False
              weapon_changed = False
              for i in range(12):
                mm_death[i].change("flashMM")
              block.change("flash")
              center_block.change("flash")
              matrix_update = True
            elif ((event.key == K_F9) and (robot_dead[7] is True)):
              selected_weapon = 8
              weapon_box_select.update(85, 155)
              megaman.weapon = "crash"
              weapon_change_init = False
              weapon_changed = False
              for i in range(12):
                mm_death[i].change("crashMM")
              block.change("crash")
              center_block.change("crash")
              matrix_update = True

          if (blocks_moving is True):
            if ((event.key == K_UP) or (event.key == K_KP8) or (event.key == K_KP9) or (event.key == K_w) or (event.key == K_e)):
              piece_orientation = PieceRotate(piece_type, piece_orientation, piece_x, piece_y)
              matrix_update = True
            elif (event.key == K_KP7) or (event.key == K_q):
              piece_orientation = PieceRotateCCW(piece_type, piece_orientation, piece_x, piece_y)
              matrix_update = True
            elif ((event.key == K_DOWN) or (event.key == K_KP2) or (event.key == K_KP5) or (event.key == K_x) or (event.key == K_s)):
              if (quick_move is False):
                block_speed = block_speed / 4  # make piece drop 4 times as fast
                quick_move = True
            elif ((event.key == K_LEFT) or (event.key == K_KP4) or (event.key == K_a)):
              piece_x = PieceMove("left", piece_x)
              matrix_update = True
            elif ((event.key == K_RIGHT) or (event.key == K_KP6) or (event.key == K_d)):
              piece_x = PieceMove("right", piece_x)
              matrix_update = True
            elif ((event.key == K_KP0) or (event.key == K_SPACE)):  # make piece instantaneously fall as far as it can...
              piece_old_x = piece_x
              piece_old_y = piece_y
              for i in range(14):  # ... by calling PieceDrop a bunch of times
                dropped, lines_completed, piece_y = PieceDrop(piece_y)
                if (dropped is False):  # hit something, so cancel rest of calls to PieceDrop by breaking out of for-loop
                  break
              piece_placed = True
              shot[selected_weapon].play()  # play sound effect of shot for selected weapon
              if (lines_completed > 0):
                # figure out damage multiplier based on weapon selected and robot being damaged
                dmg_multiplier = Multiplier(selected_robot, selected_weapon)
                # if damage greater than 0, blank-out and redraw life meter with new energy
                if (dmg_multiplier > 0):
                  life_meter.image.fill((0, 0, 0))
                  if (selected_robot < 8):
                    robot.hitpoints -= (lines_completed * dmg_multiplier)
                    for i in range(robot.hitpoints):
                      life_meter.image.blit(life_bar.image, (1, (29 - ((i - 1) * 2))))
                    robot.action = "hit"
                    robot.frame = -1
                  else:
                    wily.hitpoints -= (lines_completed * dmg_multiplier)
                    for i in range(wily.hitpoints):
                      life_meter.image.blit(life_bar.image, (1, (29 - ((i - 1) * 2))))
                    wily.action = "hit"
                    wily.frame = -1
                  robothit.play()
                  robot_hit = True
                  robot_hit_count = 0.0
                matrix_update = True
              else:
                x_offset = 2
                y_offset = 2

                # clear the area around the piece (5x5 in the matrix), and re-draw that part of the matrix
                blocks.image.blit(blank_block.image, ((piece_x - x_offset) * 16, (piece_y - y_offset) * 16))
                for i in range(5):
                  row = i + piece_y - y_offset
                  if (row >= 0) and (row <= 13):
                    for j in range(5):
                      col = j + piece_x - x_offset
                      if (col >= 0) and (col <= 9):
                        if (matrix[row][col] == 3):  # 3 is center block of an active piece
                          blocks.image.blit(center_block.image, (col * 16, row * 16))
                        elif (matrix[row][col] != 0):  # 0 is no block; otherwise, there's a block (1 = inactive, 2 = active)
                          blocks.image.blit(block.image, (col * 16, row * 16))

                matrix_update = False

                # update old area where piece used to be
                blocks.image.blit(blank_block.image, ((piece_old_x - x_offset) * 16, (piece_old_y - y_offset) * 16))
                for i in range(5):
                  row = i + piece_old_y - y_offset
                  if (row >= 0) and (row <= 13):
                    for j in range(5):
                      col = j + piece_old_x - x_offset
                      if (col >= 0) and (col <= 9):
                        if (matrix[row][col] == 3):  # 3 is center block of an active piece
                          blocks.image.blit(center_block.image, (col * 16, row * 16))
                        elif (matrix[row][col] != 0):  # 0 is no block; otherwise, there's a block (1 = inactive, 2 = active)
                          blocks.image.blit(block.image, (col * 16, row * 16))

                matrix_update = True
            elif ((event.key == K_RETURN) or (event.key == K_KP_ENTER)):
              paused.rect.topleft = (201, 100)

              sign = 0
              while (sign == 0):
                sign = random.randint(-1, 1)
              paused.x_vel = random.randint(2, 4) * sign

              sign = 0
              while (sign == 0):
                sign = random.randint(-1, 1)
              paused.y_vel = random.randint(2, 4) * sign

              paused.image, junk = load_image('GPpaused1.gif', -1)
              paused.frame = 1
              game_paused = True
              paused_init = False
            elif ((event.key == K_ESCAPE) or (event.type == QUIT)):
              quit_prompt = True
              quit_init = False

          elif (blocks_moving is False):
            if (game_paused is True):
              if (event.key == K_F1) or (event.key == K_F2) or (event.key == K_F3) or (event.key == K_F4) or (event.key == K_F5) or (event.key == K_F6) or (event.key == K_F7) or (event.key == K_F8) or (event.key == K_F9):
                pass
              else:
                game_paused = False
                flash_sprites.remove(paused)
                blocks_moving = True
                pygame.mixer.music.set_volume(1.0)
                matrix_update = True
            elif (rush.rect.bottom == 224):  # doing quit prompt
              if (event.key == K_y):
                running = False
              elif (((event.key == K_n) or (event.key == K_ESCAPE)) and (rush.rect.bottom == 224)):
                rush.action = "warping out"
                rush.animate()  # now in warp1, and about to go off top of screen; rest is handled in state "gameplay"

        elif (event.type == KEYUP) and (blocks_moving is True):
          if ((event.key == K_DOWN) or (event.key == K_KP2) or (event.key == K_KP5) or (event.key == K_x) or (event.key == K_s)):
            if (quick_move is True):
              block_speed = block_speed * 4  # return speed of piece drop to normal
              quick_move = False


      # events during credits
      elif (state == "credits"):
        if (event.type == KEYDOWN) and (fade_alpha == 0):
          done_early = True


      # events during enter name
      elif (state == "enter name"):
        if (event.type == KEYDOWN):
          if (event.key == K_LSHIFT) or (event.key == K_RSHIFT):
            shift_pressed = True
          elif (inputting_name is False) and ((event.key == K_RETURN) or (event.key == K_KP_ENTER)):
            EN_enter_pressed = True
          else:
            EN_key_pressed = True
        elif (event.type == KEYUP):
          if (event.key == K_LSHIFT) or (event.key == K_RSHIFT):
            shift_pressed = False


# ------------------------------- _____EVENTS_____ -------------------------------


# ----------------------------- *** start STATES *** -----------------------------


# ---------------------------------- INITIALIZE ----------------------------------


    if (state == "initialize"):
      # global variables
      music_playing = False
      music_intro_playing = False
      intro_music_restarted = False

      title_enter_pressed = False

      scores_loaded = False
      BT_alphas_loaded = False
      BT_enter_pressed = False

      SS_robot_faces_drawn = False
      highlights_shown = True
      SS_enter_pressed = False

      blocks_moving = False
      piece_placed = False
      quick_move = False
      robot_hit = False
      megaman_dead = False
      weapon_change_init = True
      weapon_changed = True
      game_paused = False
      paused_init = False
      quit_prompt = False
      quit_init = False
      add_line = False
      matrix_update = False

      fading_out = False
      done_early = False
      inputting_name = False
      char = 0
      EN_key_pressed = False
      shift_pressed = False
      EN_enter_pressed = False

      highlight_cell = 5  # Wily's cell highlighted by default (stage select screen)
      selected_robot = -1  # robot selected (for gameplay); none by default
      selected_weapon = 4  # weapon being used during gameplay, 0-8; P-Shooter by default

      robot_dead = []
      for i in range(8):
        robot_dead.append(False)
      robots_dead = 0  # count how many bit the dust

      wily_dead = False

      # matrix for blocks
      row = arange(10)
      matrix = array((row, row, row, row, row, row, row, row, row, row, row, row, row, row))
      for i in range(14):  # 14 rows
        for j in range(10):  # 10 columns
          matrix[i][j] = 0  # 0 = no block, 1 = set block, 2 = active block

      piece_type = 0  # type of piece currently falling; valid values are 1 through 7
      piece_orientation = 0  # direction piece is "facing"; valid values are 1 through 4
      piece_x = -1  # x of center of piece in matrix
      piece_y = -1  # y of center of piece in matrix
      piece_old_x = -1
      piece_old_y = -1

      fade_in_alpha = 0.0
      fade_in_count = 0.0
      fade_out_alpha = 0.0
      fade_out_count = 0.0
      active_pause_count = 0.0
      timing_count = 0.0
      game_time = 0  # in milliseconds
      block_speed = 1000.0  # number of milliseconds that will pass before active blocks drop 1 level
      block_count = 0.0  # incremented at the appropriate times; when it hits block_speed, the current active piece will drop
      robot_hit_count = 0.0  # used for when a line is completed, and when enemy is animated being hit
      lines_completed = 0  # num of lines completed on last piece placement
      music_count = 0

      initial_delay = False

      state = "intro"



# ----------------------------- _____INITIALIZE_____ -----------------------------


# ------------------------------------ INTRO -------------------------------------


    if (state == "intro"):
      if (initial_delay is False):
        copyrights = Copyrights()
        city = City()
        building = Building()

        story1 = Story(1)  # one of the earliest things I programmed for this; pardon the ugliness
        story2 = Story(2)
        story3 = Story(3)
        story4 = Story(4)
        story5 = Story(5)
        story6 = Story(6)
        story7 = Story(7)
        storyBlank = Story(0)

        introMM = IntroMM()

        hair_count = 0.0  # used for making MM's hair blow
        eyes_open_count = 0.0  # used to count time eyes are open
        eyes_shut_count = 0.0  # used to count time eyes are shut (for blinking)

        initial_delay = True


      # 1000 ms: screen black

      # 5000 ms: copyright screen
      if (ct >= 1000) and (ct < 6000):
        if (active_sprites.has(copyrights) is False):
          active_sprites.add(copyrights)
          all_sprites.add(copyrights)
          load_music('intro.mp3')  # get music ready to be played
        active_sprites.draw(screen)

      # 1000 ms: screen black

      # 51300 ms: story sequence (city in background, building in foreground on right)
      if (ct >= 7000) and (ct < 58300):
        # play intro music
        if (music_playing is False):
          pygame.mixer.music.play()
          music_playing = True

        # need to play first 25.55 seconds of intro music twice, due to length of story
        if (pygame.mixer.music.get_pos() >= 25550) and (intro_music_restarted is False):
          pygame.mixer.music.play()
          intro_music_restarted = True

        if (active_sprites.has(copyrights)):
          copyrights.kill()

        if (idle_sprites.has(city) is False):
          idle_sprites.add(city)
          all_sprites.add(city)
        if (idle_sprites.has(building) is False):
          idle_sprites.add(building)
          all_sprites.add(building)

        # story 1
        if (ct >= 8194) and (ct < 14164):
          if (active_sprites.has(story1) is False):
            active_sprites.add(story1)
            all_sprites.add(story1)

        # between pages
        if (ct >= 14164) and (ct < 15358):
          if (active_sprites.has(story1)):
            story1.kill()

        # story 2
        if (ct >= 15358) and (ct < 21328):
          if (active_sprites.has(story2) is False):
            active_sprites.add(story2)
            all_sprites.add(story2)

        # between pages
        if (ct >= 21328) and (ct < 22522):
          if (active_sprites.has(story2)):
            story2.kill()

        # story 3
        if (ct >= 22522) and (ct < 28492):
          if (active_sprites.has(story3) is False):
            active_sprites.add(story3)
            all_sprites.add(story3)

        # between pages
        if (ct >= 28492) and (ct < 29686):
          if (active_sprites.has(story3)):
            story3.kill()

        # story 4
        if (ct >= 29686) and (ct < 35656):
          if (active_sprites.has(story4) is False):
            active_sprites.add(story4)
            all_sprites.add(story4)

        # between pages
        if (ct >= 35656) and (ct < 36850):
          if (active_sprites.has(story4)):
            story4.kill()

        # story 5
        if (ct >= 36850) and (ct < 42820):
          if (active_sprites.has(story5) is False):
            active_sprites.add(story5)
            all_sprites.add(story5)

        # between pages
        if (ct >= 42820) and (ct < 44014):
          if (active_sprites.has(story5)):
            story5.kill()

        # story 6
        if (ct >= 44014) and (ct < 49984):
          if (active_sprites.has(story6) is False):
            active_sprites.add(story6)
            all_sprites.add(story6)

        # between pages
        if (ct >= 49984) and (ct < 51178):
          if (active_sprites.has(story6)):
            story6.kill()

        # story 7
        if (ct >= 51178) and (ct < 57148):
          if (active_sprites.has(story7) is False):
            active_sprites.add(story7)
            all_sprites.add(story7)

        # after last page, before story sequence over
        if (ct >= 57148) and (ct < 58300):
          if (active_sprites.has(story7)):
            story7.kill()

        idle_sprites.draw(screen)
        active_sprites.draw(screen)

      # 13740 ms: scroll building and city down; building scrolls twice as fast as city
      if (ct >= 58300) and (building.rect.top < 113):

        if (idle_sprites.has(city)):
          active_sprites = idle_sprites.copy()
          idle_sprites.empty()
          active_sprites.add(storyBlank)
          all_sprites.add(storyBlank)
          animated_sprites.add(introMM)
          all_sprites.add(introMM)

        # 1150 pixels to scroll / 12.74 seconds to scroll = 97.956 pixels per second
        # 90.267 PPS / 45.133 FPS = 2 pixels per frame
        building.y_change = introMM.y_change = 2
        city.y_change = storyBlank.y_change = 1  # only 1 pixel per frame, to scroll half as fast

        hair_count += 1.0

        if (introMM.blink is False):
          eyes_open_count += 1.0  # increment if not blinking
        elif (introMM.blink is True):
          eyes_shut_count += 1.0  # increment if blinking

        # make his hair change animation frames 8 times a second
        if (hair_count >= (FPS / 8)):
          hair_count = 0.0
          if (eyes_open_count >= (FPS * 4)):
            introMM.blink = True
            introMM.hair(1)
            eyes_open_count = 0.0
          elif (eyes_shut_count >= FPS):
            introMM.blink = False
            introMM.hair(0)
            eyes_shut_count = 0.0
          else:  # need this so that hair is handled normally when one of the above doesn't occur
            introMM.hair(2)

        active_sprites.update()
        animated_sprites.update()

        active_sprites.draw(screen)
        animated_sprites.draw(screen)

      # 1000 ms: no animation for last second before title screen comes up
      if (building.rect.top >= 113) and (pygame.mixer.music.get_busy()):
        hair_count += 1.0

        if (introMM.blink is False):
          eyes_open_count += 1.0  # increment if not blinking
        elif (introMM.blink is True):
          eyes_shut_count += 1.0  # increment if blinking

        # make his hair change animation frames 8 times a second
        if (hair_count >= (FPS / 8)):
          hair_count = 0.0
          if (eyes_open_count >= (FPS * 4)):
            introMM.blink = True
            introMM.hair(1)
            eyes_open_count = 0.0
          elif (eyes_shut_count >= FPS):
            introMM.blink = False
            introMM.hair(0)
            eyes_shut_count = 0.0
          else:  # need this so that hair is handled normally when one of the above doesn't occur
            introMM.hair(2)

        active_sprites.draw(screen)
        animated_sprites.draw(screen)

      # music not playing (using get_busy() to test False doesn't seem to work); intro state done
      elif (building.rect.top >= 113):
        city.kill()
        storyBlank.kill()

        initial_delay = False

        state = "title"


# ------------------------------ ______INTRO_____ --------------------------------


# ------------------------------------ TITLE -------------------------------------


    elif (state == "title"):
      if (initial_delay is False):
        # clean out sprites from intro, if any
        for sprite in all_sprites.sprites():
          sprite.kill()

        FPS = 48.0  # will make it easy to time the flashing "PRESS ENTER" with the music for the title screen
        warp_count = 0.0  # used after player presses Enter on title screen

        load_music('title.mp3')
        pygame.mixer.music.play()

        title = Background('INTROtitle.gif')
        idle_sprites.add(title)

        building = Building()
        building.rect.top = 113
        idle_sprites.add(building)

        introMM = IntroMM()
        introMM.rect.top = 121
        animated_sprites.add(introMM)

        pressEnter = PressEnter()
        animated_sprites.add(pressEnter)

        initial_delay = True

      if (title_enter_pressed is False):
        hair_count += 1.0

        if (introMM.blink is False):
          eyes_open_count += 1.0  # increment if not blinking
        elif (introMM.blink is True):
          eyes_shut_count += 1.0  # increment if blinking

        # make his hair change animation frames 8 times a second
        if (hair_count >= (FPS / 8)):
          hair_count = 0.0
          if (eyes_open_count >= (FPS * 4)):
            introMM.blink = True
            introMM.hair(1)
            eyes_open_count = 0.0
          elif (eyes_shut_count >= FPS):
            introMM.blink = False
            introMM.hair(0)
            eyes_shut_count = 0.0
          else:  # need this so that hair is handled normally when one of the above doesn't occur
            introMM.hair(2)

        # flash "PRESS ENTER" in, and quickly fade it out
        pressEnter.update(True)
      else:  # player pressed Enter
        pressEnter.image.set_alpha(255)  # make "PRESS ENTER" fully opaque

        # MM's helmet comes on, light flashes across it, he stands for a moment, and then warps up and off the screen
        warp_count += 1.0

        if (warp_count >= (FPS / 8)) and (introMM.warp_frame == "none"):  # do helm1
          introMM.warp()
        elif (warp_count >= (FPS / 8) * 2) and (introMM.warp_frame == "helm1"):  # do helm2
          introMM.warp()
        elif (warp_count >= (FPS / 8) * 3) and (introMM.warp_frame == "helm2"):  # do helm3 (slightly longer)
          introMM.warp()
        elif (warp_count >= (FPS / 8) * 5) and (introMM.warp_frame == "helm3"):  # do helm4
          introMM.warp()
        elif (warp_count >= (FPS / 8) * 6) and (introMM.warp_frame == "helm4"):  # do helm5
          introMM.warp()
        elif (warp_count >= (FPS / 8) * 7) and (introMM.warp_frame == "helm5"):  # do helm6
          introMM.warp()
        elif (warp_count >= (FPS / 8) * 8) and (introMM.warp_frame == "helm6"):  # do helm3 again (1 second)
          introMM.warp()
        elif (warp_count >= FPS * 2) and (introMM.warp_frame == "helm3a"):  # do warp1
          introMM.warp()
        elif (warp_count >= (FPS * 2) + (FPS / 8)) and (introMM.warp_frame == "warp1"):  # do warp2
          introMM.warp()
          warpout.play()
        elif (warp_count >= (FPS * 2) + (FPS / 8)):
          introMM.y_change = -10
          introMM.update()

      idle_sprites.draw(screen)
      active_sprites.draw(screen)
      animated_sprites.draw(screen)

      if (introMM.rect.bottom < -10):  # all done with title screen, since MM has warped out
        introMM.kill()
        building.kill()
        title.kill()

        pressEnter.rect.topleft = (115, 208)  # still need this for best times

        initial_delay = False

        state = "best times"


# ------------------------------- _____TITLE_____ --------------------------------


# ---------------------------------- BEST TIMES ----------------------------------


    elif (state == "best times"):
      if (initial_delay is False):
        pygame.time.delay(2000)

        load_music('scores.mp3')
        music_playing = False

        FPS = 41.0  # music is timed differently for best times
        clock_start = pygame.time.get_ticks()  # will reset ct to 0 for start of "best times" state

        btBackground = Background('BTbackground.gif')
        idle_sprites.add(btBackground)

        initial_delay = True

      if (music_playing is False):
        pygame.mixer.music.play(-1)
        music_playing = True

      # load scores from the file
      if (scores_loaded is False):
        try:
          fullname = os.path.join('data', 'scores.dat')
          file = open(fullname)
        except:  # if the file's not there, we'll make one
          file = open(fullname, 'w')
          file.write('03\n')
          file.write('59\n')
          file.write('PROTO MAN\n')
          file.write('05\n')
          file.write('59\n')
          file.write('ROLL\n')
          file.write('07\n')
          file.write('59\n')
          file.write('DR. LIGHT\n')
          file.write('09\n')
          file.write('59\n')
          file.write('GUTS MAN\n')
          file.write('11\n')
          file.write('59\n')
          file.write('SHADOW MAN\n')
          file.write('13\n')
          file.write('59\n')
          file.write('SKULL MAN\n')
          file.write('15\n')
          file.write('59\n')
          file.write('GRAVITY MAN\n')
          file.write('17\n')
          file.write('59\n')
          file.write('KNIGHT MAN\n')
          file.write('19\n')
          file.write('59\n')
          file.write('SLASH MAN\n')
          file.write('21\n')
          file.write('59\n')
          file.write('SWORD MAN\n')
          file.close
          file = open(fullname)

        # initialize score lists, and read the scores from the file
        scores_min = []
        scores_sec = []
        scores_name = []
        for i in range(10):
          scores_min.append(str(file.readline())[:-1])  # the "[:-1]" keeps all but that last character; (con't)
          scores_sec.append(str(file.readline())[:-1])  # in these cases, the '\n' newline char's from the file
          scores_name.append(str(file.readline())[:-1])
        scores_loaded = True

        # add the scores to the screen
        for i in range(10):
          BTtext(btBackground.image, scores_min[i], 95, (51 + i * 12))
          BTtext(btBackground.image, scores_sec[i], 119, (51 + i * 12))
          BTtext(btBackground.image, scores_name[i], 159, (51 + i * 12))

      if (BT_enter_pressed is False):
        # flash "PRESS ENTER" in, and fade it out (slower than for title screen, due to FPS change)
        pressEnter.update(False)
      else:  # player pressed Enter
        btBackground.kill()
        pressEnter.kill()

        initial_delay = False
        
        state = "stage select"

      idle_sprites.draw(screen)
      active_sprites.draw(screen)
      animated_sprites.draw(screen)


# ----------------------------- _____BEST TIMES_____ -----------------------------


# --------------------------------- STAGE SELECT ---------------------------------


    elif (state == "stage select"):
      if (initial_delay is False):
        load_music('stageselect-intro.mp3')
        music_playing = False
        music_intro_playing = False

        highlight_count = 0.0  # used for making stage select highlights flash

        FPS = 48.0  # helps with timing highlights and flashes / fades for stage select

        ssBackground = Background('SSbackground.gif')
        idle_sprites.add(ssBackground)

        SS_robot_face = []
        for i in range(9):
          SS_robot_face.append(RobotFace('SS', i))

        highlights = Highlights()
        animated_sprites.add(highlights)

        quit2 = Quit2()

        whiteFade = Fade(254, 254, 254)
        blackFade = Fade(0, 0, 0)

        initial_delay = True


      if ((music_intro_playing is False) and (music_playing is False) and (SS_enter_pressed is False)):
        pygame.mixer.music.play()
        music_intro_playing = True


      # end intro, and play loop
      if ((music_intro_playing is True) and (pygame.mixer.music.get_pos() >= 1350)):
        pygame.time.delay(50)  # it sounds better with a slight pause
        load_music('stageselect-loop.mp3')
        pygame.mixer.music.play()
        music_intro_playing = False
        music_playing = True


      # calling .play(-1) for infinite looping pauses noticeably with this song, so we'll do this instead
      if ((music_playing is True) and (pygame.mixer.music.get_pos() >= 31990)):
        pygame.mixer.music.play()

      if (SS_robot_faces_drawn is False):  # blit robot faces to background, so we don't have to draw them in every loop
        for i in range(8):
          if (robot_dead[i] is False):
            obj = SS_robot_face[i]
            ssBackground.image.blit(obj.image, (obj.rect.left, obj.rect.top))
        if (robots_dead < 8):
          obj = SS_robot_face[8]  # Wily's grayscale graphic for ss
          ssBackground.image.blit(obj.image, (obj.rect.left, obj.rect.top))
        SS_robot_faces_drawn = True

      highlight_count += 1.0


      # handle quit prompt
      if (quit_prompt is True):
        if (quit_init is False):
          blackFade.image.set_alpha(128)
          fade_sprites.add(blackFade)
          flash_sprites.add(quit2)
          pygame.mixer.music.set_volume(0.5)
          quit_init = True


      # blink highlights in and out
      if (highlight_count >= (FPS / 8)):
        if (highlights_shown is True):
          animated_sprites.remove(highlights)
          highlights_shown = False
        elif (highlights_shown is False):
          animated_sprites.add(highlights)
          highlights_shown = True
        highlight_count = 0


      # player has selected a stage (verified in input event handler)
      if (SS_enter_pressed is True):
        if (pygame.mixer.music.get_pos() >= 850):
          if (whiteFade.image.get_alpha() == 255):  # will use whiteFade for flashing
            whiteFade.image.set_alpha(0)
          music_playing = False
          fade_sprites.add(blackFade)

        # continue to blink highlights ("active pause" means counting something while still animating as before)
        if (music_playing is False):
          active_pause_count += 1.0

          fade_out_alpha += ((256 / (FPS / 4)) - 1)  # fade out in a quarter-second
          blackFade.image.set_alpha(fade_out_alpha)

          if (active_pause_count >= (FPS / 4) + (FPS / 8)):  # when fading done, move on to stage selected
            ssBackground.kill()
            highlights.kill()
            whiteFade.kill()
            blackFade.kill()

            quit2.kill()

            initial_delay = False

            state = "gameplay"

        else:  # flash the screen white before fading
          fade_in_count += 1.0

          if (mod(fade_in_count, (FPS / 12)) == 0):
            if (whiteFade.image.get_alpha() == 0):
              whiteFade.image.set_alpha(255)
            elif (whiteFade.image.get_alpha() == 255):
              whiteFade.image.set_alpha(0)

      idle_sprites.draw(screen)
      active_sprites.draw(screen)
      animated_sprites.draw(screen)
      fade_sprites.draw(screen)
      flash_sprites.draw(screen)


# ---------------------------- _____STAGE SELECT_____ ----------------------------


# ----------------------------------- GAMEPLAY -----------------------------------


    elif (state == "gameplay"):
      if (initial_delay is False):
        pygame.time.delay(500)

        a = selected_robot

        GP_background = GPbackground(a)
        active_sprites.add(GP_background)

        # remove stragglers from last stage, if any
        for sprite in GP_faces.sprites():
          sprite.kill()

        robot_face = []
        for i in range(8):
          robot_face.append(RobotFace('GP', i))
          if (robot_dead[i] is True):
            robot_face[i].update()
          GP_faces.add(robot_face[i])

        GP_MM_face = RobotFace('GP', -1)
        GP_faces.add(GP_MM_face)

        life_bar = LifeBar(a)
        life_meter = LifeMeter()

        megaman = MegaMan()
        animated_sprites.add(megaman)

        ready = Ready()
        animated_sprites.add(ready)

        blank_time = BlankTime()

        weapon_box_select = WeaponBoxSelect()
        animated_sprites.add(weapon_box_select)

        blank_block = BlankBlock()
        block = Block(2)
        center_block = Block(3)
        blocks = Blocks()
        animated_sprites.add(blocks)

        mm_death = []
        for i in range(12):  # explosion graphics for deaths
          mm_death.append(RobotDeath(i, "pshooterMM"))

        paused = Paused()

        rush = Rush()

        quit = Quit()

        if (a == 8):  # Wily
          starfield_count = 0

          darkSky = Fade(24, 60, 92)
          darkSky.image.set_alpha(255)
          sky.add(darkSky)

          ship = Ship()
          spaceship.add(ship)

          wily = Wily()

          wily_death = []
          for i in range(28):  # explosion graphics for Wily's death
            wily_death.append(WilyDeath(i))

        else:
          robot = Robot(a)
          animated_sprites.add(robot)

          robot_death = []
          for i in range(12):  # explosion graphics for deaths
            robot_death.append(RobotDeath(i, "robot"))


        selected_weapon = 4
        weapon_change_init = True
        weapon_changed = True

        music_intro_playing = False
        music_playing = False

        megaman_dead = False
        megaman_ready = False

        robot_intro_done = False
        energy_filling = False
        energy_filled = False

        # get things started off
        piece_placed = True
        matrix_update = True

        energy = 0  # max of 16

        timing_count = 0.0

        initial_delay = True

      if (music_intro_playing is False):
        if (a == 0):
          load_music('bubbleman-intro.mp3')
        elif (a == 1):
          load_music('airman.mp3')
          music_playing = True  # those without intros can just play forever
        elif (a == 2):
          load_music('quickman.mp3')
          music_playing = True
        elif (a == 3):
          load_music('heatman.mp3')
          music_playing = True
        elif (a == 4):
          load_music('woodman-intro.mp3')
        elif (a == 5):
          load_music('metalman.mp3')
          music_playing = True
        elif (a == 6):
          load_music('flashman-intro.mp3')
        elif (a == 7):
          load_music('crashman-intro.mp3')
        elif (a == 8):
          load_music('wily1-2.mp3')
          music_playing = True

        pygame.mixer.music.play(-1)
        music_intro_playing = True

      if (a < 8):
        if (music_intro_playing is True) and (music_playing is False) and (robot_dead[a] is False) and (megaman_dead is False):
          if (a == 0) and (pygame.mixer.music.get_pos() >= 10700):
            load_music('bubbleman-loop.mp3')
            pygame.mixer.music.play(-1)
            music_playing = True
          elif (a == 4) and (pygame.mixer.music.get_pos() >= 7740):
            load_music('woodman-loop.mp3')
            pygame.mixer.music.play(-1)
            music_playing = True
          elif (a == 6) and (pygame.mixer.music.get_pos() >= 25600):
            load_music('flashman-loop.mp3')
            pygame.mixer.music.play(-1)
            music_playing = True
          elif (a == 7) and (pygame.mixer.music.get_pos() >= 12860):
            load_music('crashman-loop.mp3')
            pygame.mixer.music.play(-1)
            music_playing = True

      timing_count += 1.0


      # animate background; change frame of background 8 times a second
      if (a == 0) or (a == 3) or (a == 5):
        if (mod(timing_count, (FPS / 8)) == 0):
          GP_background.update(a)
      elif (a == 1):  # 4 times a second
        if (mod(timing_count, (FPS / 4)) == 0):
          GP_background.update(a)
      elif (a == 6):  # twice a second
        if (mod(timing_count, (FPS / 2)) == 0):
          GP_background.update(a)
      else:  # Quick, Wood, Crash, and Wily each have only 1 background frame
        pass


      # weapon changed; animate Mega Man
      if (weapon_change_init is False):
        weapon_change_count = 0.0
        megaman.image, junk = load_image('MM' + megaman.weapon + 'Warp2.gif', -1)
        weapon_change_init = True
        warpin.play()

      if (weapon_changed is False):
        weapon_change_count += 1.0
        if (weapon_change_count >= (FPS / 8)) and (weapon_change_count < (FPS / 8) * 2):
          megaman.image, junk = load_image('MM' + megaman.weapon + 'Warp1.gif', -1)
        elif (weapon_change_count >= (FPS / 8) * 2):
          megaman.image, junk = load_image('MM' + megaman.weapon + 'Stand.gif', -1)
          weapon_changed = True


      # game paused
      if (game_paused is True):
        if (paused_init is False):
          flash_sprites.add(paused)
          blocks.clear()
          blocks_moving = False
          pygame.mixer.music.set_volume(0.5)
          paused_count = 0.0
          paused_init = True

        paused_count += 1.0

        if (mod(paused_count, (FPS / 16)) == 0):
          paused.move()
        if (mod(paused_count, (FPS / 16)) == 0):
          paused.animate()


      # quit prompt brought up from player hitting Esc or clicking X button on window (?... clicking doesn't seem to work)
      if (quit_prompt is True):
        if (quit_init is False):
          flash_sprites.add(rush)
          rush.action = "warping in"
          blocks.clear()
          blocks_moving = False
          pygame.mixer.music.set_volume(0.5)
          temp_count_rush1 = 0
          temp_count_rush2 = 0
          temp_count_rush3 = 0
          temp_count_rush4 = 0
          quit_count = 0.0
          quit_init = True

        quit_count += 1.0

        if (rush.action == "warping in") and (rush.rect.bottom < 224):
          if (mod(quit_count, (FPS / 24)) == 0):
            rush.move(0, 20)

        if (rush.rect.bottom >= 224) and (temp_count_rush1 == 0):
          rush.rect.bottom = 224
          warpin.play()
          temp_count_rush1 = ct

        if (rush.rect.bottom == 224) and (ct - temp_count_rush1 >= 64) and (rush.action == "warping in") and (rush.frame == 2):
          rush.animate()  # now in warp1
          temp_count_rush2 = ct
        elif (rush.rect.bottom == 224) and (ct - temp_count_rush2 >= 64) and (rush.action == "warping in") and (rush.frame == 1):
          rush.animate()  # now standing
          flash_sprites.add(quit)  # add quit message, now that Rush is in place

        if (rush.action == "standing") and (mod(quit_count, (FPS / 8)) == 0):
          rush.animate()  #now wagging (tail at a 45)
        elif (rush.action == "wagging") and (mod(quit_count, (FPS / 8)) == 0):
          rush.animate()  #now standing (tail straight up)

        if (rush.action == "warping out") and (temp_count_rush3 == 0):
          warpout.play()
          temp_count_rush3 = ct
          flash_sprites.remove(quit)  # remove quit message, so Rush doesn't warp out through it

        if (rush.action == "warping out") and (ct - temp_count_rush3 >= 64):
          rush.animate()  # now in warp2

        if (rush.action == "warping out") and (rush.frame == 2) and (mod(quit_count, (FPS / 24)) == 0):
          rush.move(0, -20)

        if (rush.action == "warping out") and (rush.rect.bottom < 0):
          flash_sprites.remove(rush)
          quit_prompt = False
          blocks_moving = True
          pygame.mixer.music.set_volume(1.0)
          matrix_update = True


      # if enemy dead, do death animation and end level
      if (a < 8):
        if (robot.hitpoints <= 0):
          if (robot_dead[a] is False):
            # print updated block matrix one last time
            blocks.clear()
            for i in range(14):
              for j in range(10):
                if (matrix[i][j] != 0):  # 0 is no block; otherwise, there's a block (1 = inactive, 2 = active)
                  blocks.image.blit(block.image, (j * 16, i * 16))

            robot_dead[a] = True
            robots_dead += 1
            blocks_moving = False  # will also stop timer
            pygame.mixer.music.stop()
            music_playing = False
            robotdeath.play()
            animated_sprites.remove(robot)

            for i in range(12):
              flash_sprites.add(robot_death[i])  # sprites in this container drawn over all others in gameplay

            explosion_count = 0.0

          explosion_count += 1.0

          if (mod(explosion_count, (FPS / 4)) == 0):
            for i in range(12):
              robot_death[i].move()

          if (mod(explosion_count, (FPS / 16)) == 0):
            for i in range(12):
              robot_death[i].animate()

          # once right-most explosion orb thingy is off screen, play victory music
          if (robot_death[4].rect.left > 320):
            if (music_playing is False):
              load_music('robotvictory.mp3')
              pygame.mixer.music.play()
              music_playing = True
              SFX_played = False
              temp_count3 = ct
            else:
              # 1 second after victory music done (5.5 seconds), warp Mega Man out
              if (ct - temp_count3 >= 6500) and (ct - temp_count3 < 6625):
                if (SFX_played is False):
                  warpout.play()
                  SFX_played = True
                  megaman.action = "warping out"
                  megaman.frame = -1
                  temp_count4 = 0
                  megaman.animate()
              elif (ct - temp_count3 >= 6625) and (megaman.frame == 1):
                megaman.animate()
              elif (ct - temp_count3 >= 6675) and (megaman.frame == 2) and (mod(explosion_count, (FPS / 24)) == 0) and (megaman.rect.bottom >= 0):
                megaman.move(0, -20)

            if (megaman.rect.bottom < 0) and (temp_count4 == 0):
              temp_count4 = ct
              face_flash_done = False
              flash_increment = (FPS / 2)
              flash_count = 0.0
              flash_final = 1.0

            # when Mega man off top of screen, pause for a second, flash face of robot weapon acquired, wait, and return to stage select
            if (megaman.rect.bottom < 0) and (ct - temp_count4 >= 1000):
              if (face_flash_done is False):
                if (flash_count == flash_increment):
                  robot_face[a].update()
                  flash_count = 0.0
                  if (flash_increment > 2.0):
                    flash_increment -= 2.0
                  if (flash_increment == 2.0):
                    flash_final += 1.0
                    if (flash_final == 30.0):
                      face_flash_done = True
                      temp_count5 = ct

                flash_count += 1.0

              else:
                if (ct - temp_count5 >= 1500):
                  GP_background.kill()
                  GP_MM_face.kill()
                  life_bar.kill()
                  life_meter.kill()
                  megaman.kill()
                  ready.kill()
                  blank_time.kill()
                  weapon_box_select.kill()
                  blank_block.kill()
                  block.kill()
                  center_block.kill()
                  blocks.kill()
                  paused.kill()
                  rush.kill()
                  quit.kill()

                  robot.kill()


                  # put it back to Wily's cell highlighted
                  highlight_count = 0.0
                  highlight_cell = 5

                  SS_robot_faces_drawn = False
                  SS_enter_pressed = False

                  block_speed -= 50.0

                  for i in range(14):  # 14 rows
                    for j in range(10):  # 10 columns
                      matrix[i][j] = 0  # 0 = no block, 1 = set block, 2 = active block

                  initial_delay = False

                  state = "stage select"
      else:  # Wily dead
        if (wily.hitpoints <= 0):
          if (wily_dead is False):
            # print updated block matrix one last time
            blocks.clear()
            for i in range(14):
              for j in range(10):
                if (matrix[i][j] != 0):  # 0 is no block; otherwise, there's a block (1 = inactive, 2 = active)
                  blocks.image.blit(block.image, (j * 16, i * 16))

            wily_dead = True
            blocks_moving = False  # will also stop timer
            pygame.mixer.music.stop()
            music_playing = False
            robotdeath.play()
            wily.kill()

            for i in range(28):
              flash_sprites.add(wily_death[i])  # sprites in this container drawn over all others in gameplay

            explosion_count = 0.0

          explosion_count += 1.0

          if (mod(explosion_count, (FPS / 4)) == 0):
            for i in range(28):
              wily_death[i].move()

          if (mod(explosion_count, (FPS / 16)) == 0):
            for i in range(28):
              wily_death[i].animate()

          # once lower-right explosion orb thingy is off screen, play victory music
          if (wily_death[5].rect.bottom > 239):
            if (music_playing is False):
              load_music('wilyvictory.mp3')
              pygame.mixer.music.play()
              music_playing = True
              SFX_played = False
              temp_count3 = ct
            else:
              # 1 second after victory music done (9.0 seconds), warp Mega Man out
              if (ct - temp_count3 >= 10000) and (ct - temp_count3 < 10125):
                if (SFX_played is False):
                  warpout.play()
                  SFX_played = True
                  megaman.action = "warping out"
                  megaman.frame = -1
                  temp_count4 = 0
                  megaman.animate()
              elif (ct - temp_count3 >= 10125) and (megaman.frame == 1):
                megaman.animate()
              elif (ct - temp_count3 >= 10175) and (megaman.frame == 2) and (mod(explosion_count, (FPS / 24)) == 0) and (megaman.rect.bottom >= 0):
                megaman.move(0, -20)

            if (megaman.rect.bottom < 0) and (temp_count4 == 0):
              temp_count4 = ct

              # make sure sprites have alpha values set, so we can fade them at the start of the credits

              for sprite in idle_sprites.sprites():
                sprite.image.set_alpha(255)
              for sprite in active_sprites.sprites():
                sprite.image.set_alpha(255)
              animated_sprites.remove(ready)
              for sprite in animated_sprites.sprites():
                sprite.image.set_alpha(255)
              for sprite in GP_faces.sprites():
                sprite.image.set_alpha(255)
              for sprite in fade_sprites.sprites():
                sprite.image.set_alpha(255)
              for sprite in flash_sprites.sprites():
                sprite.image.set_alpha(255)
              fade_alpha = 255

            # when Mega man off top of screen, pause for a second, and go to credits
            if (megaman.rect.bottom < 0) and (ct - temp_count4 >= 1000):
              initial_delay = False

              state = "credits"


      # if Mega Man dead, do death animation and end level
      if (megaman_dead is True):
        if (animated_sprites.has(megaman)):
          # print updated block matrix one last time
          blocks.clear()
          for i in range(14):
            for j in range(10):
              if (matrix[i][j] != 0):  # 0 is no block; otherwise, there's a block (1 = inactive, 2 = active)
                blocks.image.blit(block.image, (j * 16, i * 16))

          blocks_moving = False  # will also stop timer
          pygame.mixer.music.stop()
          music_playing = False
          robotdeath.play()
          megaman.kill()

          # make sure that the blocks aren't falling at quad speed when the player starts the next level
          if (quick_move is True):
            block_speed = block_speed * 4.0
            quick_move = False

          for i in range(12):
            flash_sprites.add(mm_death[i])  # sprites in this container drawn over all others in gameplay

          explosion_count = 0.0

        explosion_count += 1.0

        if (mod(explosion_count, (FPS / 4)) == 0):
          for i in range(12):
            mm_death[i].move()

        if (mod(explosion_count, (FPS / 16)) == 0):
          for i in range(12):
            mm_death[i].animate()

        # once right-most explosion orb thingy is off screen, play game over music
        if (mm_death[4].rect.left > 320):
          if (music_playing is False):
            load_music('gameover.mp3')
            pygame.mixer.music.play()
            music_playing = True
            temp_count5 = ct
          else:
            # 2 seconds after game over music done (3.0 seconds), clear screen and return to stage select
            if (ct - temp_count5 >= 5000):
              GP_background.kill()
              GP_MM_face.kill()
              life_bar.kill()
              life_meter.kill()
              megaman.kill()
              ready.kill()
              blank_time.kill()
              weapon_box_select.kill()
              blank_block.kill()
              block.kill()
              center_block.kill()
              blocks.kill()
              paused.kill()
              rush.kill()
              quit.kill()

              if (a < 8):
                robot.kill()
              else:
                wily.kill()
                ship.kill()
                darkSky.kill()
                for star in starfield.sprites():
                  star.kill()

              # put it back to Wily's cell highlighted
              highlight_count = 0.0
              highlight_cell = 5

              SS_robot_faces_drawn = False
              SS_enter_pressed = False

              block_speed -= 50.0

              initial_delay = False

              for i in range(14):  # 14 rows
                for j in range(10):  # 10 columns
                  matrix[i][j] = 0  # 0 = no block, 1 = set block, 2 = active block

              state = "stage select"


      # animate READY message, Mega Man warping in, enemy trying to intimidate him, and enemy life meter filling up
      if (megaman.action == "nothing") and (timing_count <= (FPS * 3)):  # flash READY for 3 seconds
        if (mod(timing_count, (FPS / 8)) == 0):
          ready.update()
      elif (a < 8):
        if (megaman.action == "nothing") and (timing_count > (FPS * 3)) and (robot_dead[a] is False) and (megaman_dead is False):
          ready.image.set_alpha(0)
          megaman.action = "warping in"
      elif (a == 8):
        if (megaman.action == "nothing") and (timing_count > (FPS * 3)) and (wily_dead is False) and (megaman_dead is False):
          ready.image.set_alpha(0)
          megaman.action = "warping in"

      # stop MM from warping down too far, and change animation frame when he gets to the right spot
      if (megaman.action == "warping in") and (mod(timing_count, (FPS / 24)) == 0) and (megaman.rect.bottom < 48):
        megaman.move(0, 20)
        if (megaman.rect.bottom >= 48):
          megaman.rect.bottom = 48
          warpin.play()
          megaman.animate()
          temp_count = timing_count

      # change from last warp-in frame to standing frame
      if (megaman.action == "warping in") and (megaman.frame == 1) and (timing_count - temp_count >= (FPS / 8)):
        megaman.animate()
        megaman_ready = True
        temp_count = timing_count
        robot_intro_count = 0.0

      # have MM blink every 4 seconds, for 0.25 seconds, when standing
      if (megaman_dead is False) and (weapon_changed is True) and (megaman.action == "standing") and (timing_count - temp_count >= (FPS * 4)):
        megaman.animate()
        temp_count = timing_count
      elif (megaman_dead is False) and (weapon_changed is True) and (megaman.action == "blinking") and (timing_count - temp_count >= (FPS / 8)):
        megaman.animate()
        temp_count = timing_count

      # update starfield and have Wily breathe, if in Wily's stage
      if (a == 8):
        # add a star
        size = random.randint(1, 3)
        y = random.randint(-2, 239)
        starfield.add(Star(size, -2, y))

        for star in starfield.sprites():
          star.move()
          if (star.rect.left > 319):
            star.kill()

        if (wily.action == "breathing") and (robot_intro_done is True):
          if (mod(timing_count, (FPS / 8)) == 0):  # have Wily breathing during energy fill
            if (wily.frame == 9):
              wily.frame = 8
            else:
              wily.frame = 9
            wily.animate()


      # do robot intro animation and life meter filling up
      if (a < 8):
        if (megaman_ready is True) and (robot_intro_done is False):
          robot_intro_count += 1.0

          if (robot_intro_count >= (FPS / 4)):  # pause slightly before robot reacts
            if (energy_filled is False) and (energy_filling is False):
              # go through the 2 or 3 frames of their intro (some are faster than others)
              if (mod(robot_intro_count, (FPS / 16)) == 0) and ((robot.name == "air") or (robot.name == "heat")):
                robot.animate()
              elif (mod(robot_intro_count, (FPS / 12)) == 0) and (robot.name == "wood"):
                robot.animate()
              elif (mod(robot_intro_count, (FPS / 8)) == 0) and (robot.name == "flash"):
                robot.animate()
              elif (mod(robot_intro_count, (FPS / 4)) == 0):
                robot.animate()

              if (robot.action == "waiting"):
                if (robot.name != "flash"):
                  animated_sprites.add(life_meter)
                  energyfill.play()
                  energy_filling = True
                  robot.action = "standing"
                elif (robot.name == "flash"):
                  animated_sprites.add(life_meter)
                  energyfill.play()
                  energy_filling = True
            elif (energy_filled is False) and (energy_filling is True):
              if (mod(robot_intro_count, (FPS / 12)) == 0):  # add another bar to the life meter
                energy += 1
                life_meter.image.blit(life_bar.image, (1, (31 - ((energy - 1) * 2))))
                if (energy == 16):
                  energy_filled = True
                  energy_filling = False
                  robot_intro_done = True
                  temp_count2 = timing_count
        # after life meter fills, robot changes to normal standing, and the blocks can start falling
        elif (robot_intro_done is True) and (blocks_moving is False) and (timing_count - temp_count2 >= (FPS / 4)) and (robot_dead[a] is False) and (megaman_dead is False) and (game_paused is False) and (quit_prompt is False):
          robot.animate()
          blocks_moving = True
      else:  # Wily
        if (megaman_ready is True) and (robot_intro_done is False):
          robot_intro_count += 1.0

          if (robot_intro_count >= FPS):  # pause 1 second before ship starts moving
            if (energy_filled is False) and (energy_filling is False):
              # play spaceship sound effect and initialize temp counters
              if (ship.rect.left == 25):
                shipsound.play()
                temp_count2 = 0
                temp_count3 = 0
              elif (ship.rect.left == 200):
                wily_sprite.add(wily)

              # move the ship across the screen to the right, animating as we go
              ship.move()
              ship.animate()

              # animate Wily (even before he can be seen)
              if (wily.action == "coat blowing"):
                if (mod(robot_intro_count, (FPS / 8)) == 0):
                  wily.animate()

              # when ship leaves right side of screen, start moving Wily up
              if (wily.rect.left == 209):
                if (ship.rect.left >= 319):
                  wily.move()

              # when Wily off top of screen, kill the ship, move Wily to above the battle area, and change his velocity
              if (wily.rect.bottom < 0) and (wily.rect.left == 209):
                ship.kill()
                wily.rect.left = 77
                wily.y_vel = 1
                temp_count2 = timing_count

              # 2 seconds later, start moving Wily down
              if (timing_count - temp_count2 >= (FPS * 2)) and (wily.rect.top < 4) and (wily.y_vel == 1):
                wily.move()

              # when Wily hits the designated spot, wait 1 second, then do his morph and fade the music
              if (wily.rect.top == 4) and (wily.rect.left == 77) and (temp_count3 == 0):
                temp_count3 = timing_count
              if (temp_count3 != 0) and (timing_count - temp_count3 >= FPS):
                if (wily.action == "coat blowing"):
                  wily.action = "morphing"
                  wily.frame = 3
                  pygame.mixer.music.fadeout(3000)  # milliseconds

                if (wily.action == "morphing"):
                  if (mod(robot_intro_count, (FPS / 2)) == 0):
                    wily.animate()
                    if (wily.frame == 7):
                      wily.action = "glowing 1"
                      glow_count = 0
                    else:
                      wily.frame += 1
                elif (wily.action == "glowing 1"):
                  if (mod(robot_intro_count, (FPS / 12)) == 0):
                    if (wily.frame == 6):
                      wily.frame = 7
                    else:
                      wily.frame = 6
                    wily.animate()
                    glow_count += 1
                    if (glow_count == 20):
                      wily.action = "glowing 2"
                      glow_count = 0
                elif (wily.action == "glowing 2"):
                  if (mod(robot_intro_count, (FPS / 12)) == 0):
                    if (wily.frame == 6):
                      wily.frame = 8
                    else:
                      wily.frame = 6
                    wily.animate()
                    glow_count += 1
                    if (glow_count == 30):
                      wily.action = "breathing"
                      animated_sprites.add(life_meter)
                      energyfill.play()
                      energy_filling = True

                # during Wily's morph, fade dark sky out so that starfield shows
                if (wily.action == "morphing") or (wily.action == "glowing 1") or (wily.action == "glowing 2"):
                  al = darkSky.image.get_alpha()
                  if (al > 0):
                    al -= 1
                    darkSky.image.set_alpha(al)

            elif (energy_filled is False) and (energy_filling is True):
              if (mod(robot_intro_count, (FPS / 12)) == 0):  # add another bar to the life meter
                energy += 1
                life_meter.image.blit(life_bar.image, (1, (31 - ((energy - 1) * 2))))
                if (energy == 16):
                  energy_filled = True
                  energy_filling = False
                  robot_intro_done = True
                  temp_count4 = timing_count
              if (mod(robot_intro_count, (FPS / 8)) == 0):  # have Wily breathing during energy fill
                if (wily.frame == 9):
                  wily.frame = 8
                else:
                  wily.frame = 9
                wily.animate()

        # after life meter fills, the blocks can start falling
        elif (robot_intro_done is True) and (blocks_moving is False) and (timing_count - temp_count4 >= (FPS / 4)) and (wily_dead is False) and (megaman_dead is False) and (game_paused is False) and (quit_prompt is False):
          load_music('QGM-wily-altered.mp3')
          pygame.mixer.music.play(-1)
          blocks_moving = True


      # if robot hit from line(s) being completed, animate hit flash for 2 seconds
      if (a < 8):
        if (robot_hit is True):
          if(mod(robot_hit_count, (FPS / 12)) == 0):
            robot.animate()
          robot_hit_count += 1.0
          if (robot_hit_count > (FPS * 2)):
            robot_hit = False
      else:
        if (robot_hit is True):
          if(mod(robot_hit_count, (FPS / 12)) == 0):
            wily.animate()
          robot_hit_count += 1.0
          if (robot_hit_count > (FPS * 2)):
            wily.action = "breathing"
            robot_hit = False


      # actually playing now, since player has control of the blocks
      if (blocks_moving is True):
        if (piece_placed is True):  # need a new random piece
          piece = random.randint(1, 100)
          if (piece >= 1) and (piece <= 15):
            # if new piece overlaps any existing blocks, game over
            if (matrix[0][5] != 0) or (matrix[1][3] != 0) or (matrix[1][4] != 0) or (matrix[1][5] != 0):
              megaman_dead = True
            # even if Mega Man is now dead, still need to add new blocks to matrix
            matrix[0][5] = 2  # 2 = active block
            matrix[1][3] = 2
            matrix[1][4] = 3  # 3 = center block
            matrix[1][5] = 2
            piece_type = 1
          elif (piece >= 16) and (piece <= 30):
            if (matrix[0][3] != 0) or (matrix[1][3] != 0) or (matrix[1][4] != 0) or (matrix[1][5] != 0):
              megaman_dead = True
            matrix[0][3] = 2
            matrix[1][3] = 2
            matrix[1][4] = 3
            matrix[1][5] = 2
            piece_type = 2
          elif (piece >= 31) and (piece <= 45):
            if (matrix[0][4] != 0) or (matrix[0][5] != 0) or (matrix[1][3] != 0) or (matrix[1][4] != 0):
              megaman_dead = True
            matrix[0][4] = 2
            matrix[0][5] = 2
            matrix[1][3] = 2
            matrix[1][4] = 3
            piece_type = 3
          elif (piece >= 46) and (piece <= 60):
            if (matrix[0][3] != 0) or (matrix[0][4] != 0) or (matrix[1][4] != 0) or (matrix[1][5] != 0):
              megaman_dead = True
            matrix[0][3] = 2
            matrix[0][4] = 2
            matrix[1][4] = 3
            matrix[1][5] = 2
            piece_type = 4
          elif (piece >= 61) and (piece <= 75):
            if (matrix[0][4] != 0) or (matrix[1][3] != 0) or (matrix[1][4] != 0) or (matrix[1][5] != 0):
              megaman_dead = True
            matrix[0][4] = 2
            matrix[1][3] = 2
            matrix[1][4] = 3
            matrix[1][5] = 2
            piece_type = 5
          elif (piece >= 76) and (piece <= 90):
            if (matrix[0][4] != 0) or (matrix[0][5] != 0) or (matrix[1][4] != 0) or (matrix[1][5] != 0):
              megaman_dead = True
            matrix[0][4] = 2
            matrix[0][5] = 2
            matrix[1][4] = 2
            matrix[1][5] = 2
            piece_type = 6
          else:  # (piece >= 91) and (piece <= 100)
            if (matrix[1][3] != 0) or (matrix[1][4] != 0) or (matrix[1][5] != 0) or (matrix[1][6] != 0):
              megaman_dead = True
            matrix[1][3] = 2
            matrix[1][4] = 3
            matrix[1][5] = 2
            matrix[1][6] = 2
            piece_type = 7

          piece_orientation = 1
          piece_x = 4
          piece_y = 1
          piece_placed = False

        block_count += clock.get_time()  # used to determine when active piece will drop
        if (block_count >= block_speed) and (megaman_dead is False):  # time to drop the active piece
          dropped, lines_completed, piece_y = PieceDrop(piece_y)
          if (dropped is False):  # piece collided with others or hit bottom, instead of dropping
            shot[selected_weapon].play()  # play sound effect of shot for selected weapon
            piece_placed = True

          if (lines_completed > 0):
            # figure out damage multiplier based on weapon selected and robot being damaged
            dmg_multiplier = Multiplier(selected_robot, selected_weapon)

            # if damage greater than 0, blank-out and redraw life meter with new energy
            if (dmg_multiplier > 0):
              life_meter.image.fill((0, 0, 0))
              if (a < 8):
                robot.hitpoints -= (lines_completed * dmg_multiplier)
                for i in range(robot.hitpoints):
                  life_meter.image.blit(life_bar.image, (1, (29 - ((i - 1) * 2))))
                robot.action = "hit"
                robot.frame = -1
              else:
                wily.hitpoints -= (lines_completed * dmg_multiplier)
                for i in range(wily.hitpoints):
                  life_meter.image.blit(life_bar.image, (1, (29 - ((i - 1) * 2))))
                wily.action = "hit"
                wily.frame = -1
              robothit.play()
              robot_hit = True
              robot_hit_count = 0.0
            lines_completed = 0  # don't want the above to keep getting reset

            matrix_update = True
          else:  # no lines completed, but piece did drop
            matrix_update = True

          block_count = 0.0


        # update matrix display, if necessary
        if (matrix_update is True):
          # clear the block sprite, and then draw updated block matrix
          blocks.clear()
          for i in range(14):
            for j in range(10):
              if (matrix[i][j] == 3):  # 3 is center block of an active piece
                blocks.image.blit(center_block.image, (j * 16, i * 16))
              elif (matrix[i][j] != 0):  # 0 is no block; otherwise, there's a block (1 = inactive, 2 = active)
                blocks.image.blit(block.image, (j * 16, i * 16))
          matrix_update = False

        game_time += clock.get_time()  # add time passed since last tick() call to total game time

        # a cheap way of ensuring the 1-hour time limit; really, the player can go forever, but time won't show higher than 59:59
        if (game_time > ((59 * 60 + 59) * 1000)):
          game_time = (59 * 60 + 59) * 1000

      # update game time on the screen
      GameTime(blank_time, GP_background.image, game_time)

      if (a == 8):
        starfield.draw(screen)
        sky.draw(screen)
        wily_sprite.draw(screen)
        spaceship.draw(screen)

      idle_sprites.draw(screen)
      active_sprites.draw(screen)
      animated_sprites.draw(screen)
      GP_faces.draw(screen)
      fade_sprites.draw(screen)
      flash_sprites.draw(screen)


# ------------------------------ _____GAMEPLAY_____ ------------------------------


# ----------------------------------- CREDITS ------------------------------------


    elif (state == "credits"):
      if (initial_delay is False):
        if (fade_alpha > 0):
          for sprite in idle_sprites.sprites():
            sprite.image.set_alpha(fade_alpha)
          for sprite in active_sprites.sprites():
            sprite.image.set_alpha(fade_alpha)
          for sprite in animated_sprites.sprites():
            sprite.image.set_alpha(fade_alpha)
          for sprite in GP_faces.sprites():
            sprite.image.set_alpha(fade_alpha)
          for sprite in fade_sprites.sprites():
            sprite.image.set_alpha(fade_alpha)
          for sprite in flash_sprites.sprites():
            sprite.image.set_alpha(fade_alpha)

          fade_alpha -= 1
        else:
          GP_background.kill()
          GP_MM_face.kill()
          life_bar.kill()
          life_meter.kill()
          megaman.kill()
          ready.kill()
          blank_time.kill()
          weapon_box_select.kill()
          blank_block.kill()
          block.kill()
          center_block.kill()
          blocks.kill()
          paused.kill()
          rush.kill()
          quit.kill()

          darkSky.kill()
          ship.kill()

          creditsMM = CreditsMM()
          blackFade = Fade(0, 0, 0)

          load_music('credits2.mp3')
          music_count = 0
          pygame.mixer.music.play()

          # load the credits from 'credits.dat'
          try:
            fullname = os.path.join('data', 'credits.dat')
            file = open(fullname)
          except:  # if the file's not there, we'll make one
            file = open(fullname, 'w')
            file.write('THESE ARE WHERE THE CREDITS ARE SUPPOSED TO BE...\n')
            file.write('BUT YOU MESSED WITH THE FILE!\n')
            file.write('\n')
            file.write('SEE README.TXT IN THE MAIN GAME DIRECTORY\n')
            file.write('\n')
            file.write('\n')
            file.write('\n')
            file.write('\n')
            file.write('GAME MADE BY MARK PULVER')
            file.write('WITH PERMISSION FROM CAPCOM')
            file.close
            file = open(fullname)

          credits = []
          reading = True

          # read each line from the file
          while (reading is True):
            rl = str(file.readline())

            if (rl == "\n"):
              credits.append(" ")
            elif (rl != ""):
              credits.append(rl)  # the "[:-1]" keeps all but the last character (newline, in this case)
            else:  # end of file
              credits.append("*END*")
              reading = False

          next_line = 0  # used to create the next line of the credits
          add_line = True

          timing_count = 0

          fading_out = False

          initial_delay = True


      timing_count += 1
      music_count += 1


      # keep the starfield moving
      size = random.randint(1, 3)
      y = random.randint(-2, 239)
      starfield.add(Star(size, -2, y))

      for star in starfield.sprites():
        star.move()
        if (star.rect.left > 319):
          star.kill()


      # scroll the credits up the screen
      if (add_line is True):
        if (credits[next_line] != "*END*"):
          animated_sprites.add(TextLine(credits[next_line]))
          next_line += 1
        else:
          animated_sprites.add(creditsMM)

        add_line = False

      if (initial_delay is True):

        curr_line = 0

        for sprite in animated_sprites.sprites():

          if (mod(timing_count, (FPS / 16)) == 0):
            sprite.move()
            scrolling = True
          else:
            scrolling = False  # used to stop the "add_line = True" statement below from overlapping lines of the credits

          if (scrolling is True) and (sprite.rect.bottom == 239):
            add_line = True

          if (sprite.rect.bottom < 0):
            sprite.kill()

          curr_line += 1


      # when credits done (or if key pressed), fade out the starfield, and go to high score / name entry screen
      if (music_count >= (FPS * 67.36)) or (done_early is True):  # song is 65.36 seconds long, though music_count seems to be about a second ahead of the song, so this delay is more like 1 second
        if (fading_out is False):
          if (done_early is True):
            pygame.mixer.music.fadeout(1000)
          else:
            pygame.mixer.music.stop()
          fade_amount = 0
          blackFade.image.set_alpha(0)
          fade_sprites.add(blackFade)

          fading_out = True
        else:
          if (done_early is True):
            fade_amount += 5
          else:
            fade_amount += 1

          if (fade_amount >= 256):
            for star in starfield.sprites():
              star.kill()

            creditsMM.kill()
            blackFade.kill()

            for sprite in animated_sprites.sprites():
              sprite.kill()  # actual credits

            initial_delay = False

            state = "enter name"
          else:
            blackFade.image.set_alpha(fade_amount)


      starfield.draw(screen)
      idle_sprites.draw(screen)
      active_sprites.draw(screen)
      animated_sprites.draw(screen)
      GP_faces.draw(screen)
      fade_sprites.draw(screen)
      flash_sprites.draw(screen)


# ------------------------------ _____CREDITS_____ -------------------------------


# --------------------------------- ENTER NAME -----------------------------------


    elif (state == "enter name"):
      if (initial_delay is False):
        pygame.time.delay(2000)

        btBackground = Background('BTbackground.gif')
        idle_sprites.add(btBackground)

        pressEnter = PressEnter()
        pressEnter.rect.topleft = (115, 207)
        pressEnter.image.set_alpha(255)
        active_sprites.add(pressEnter)

        EN_cursor = ENCursor()
        enterName = EnterName()

        blackFade = Fade(0, 0, 0)
        blackFade.image.set_alpha(0)
        fade_sprites.add(blackFade)

        music_playing = False
        score_tested = False
        high_score = False
        scores_drawn = False
        player_name = ""
        num_chars = 0
        inputting_name = False
        EN_enter_pressed = False

        # convert from ms to sec
        game_time = int(game_time / 1000)

        al = 0
        fading = True

        initial_delay = True

      if (music_playing is False):
        load_music('scores.mp3')
        pygame.mixer.music.play(-1)
        music_playing = True


      # loaded scores are already up-to-date:
      # scores_min[]
      # scores_sec[]
      # scores_name[]

      # test to see if the player has a high score
      if (score_tested is False):
        mins = str(floordiv(game_time, 60))  # gives us player's minutes
        if (len(mins) == 1):
          mins = "0" + mins
        sec = str(mod(game_time, 60))  # gives us player's seconds
        if (len(sec) == 1):
          sec = "0" + sec

        for i in range(10):
          if (mins < scores_min[i]) or ((mins == scores_min[i]) and (sec < scores_sec[i])):
            high_score = True
            score_slot = i
            break

        # if player has high score, shift the other scores down
        if (high_score is True):
          for i in range((10 - score_slot)):
            j = 9 - i  # do them from bottom to top, to prevent them from overwriting each other
            if (j > 0):  # can't shift the first one (it'll be overwritten anyway)
              scores_min[j] = scores_min[j-1]
              scores_sec[j] = scores_sec[j-1]
              scores_name[j] = scores_name[j-1]

          # assign the player's score to the appropriate place, and make sure name entry area is blank
          scores_min[score_slot] = mins
          scores_sec[score_slot] = sec
          scores_name[score_slot] = ""

          inputting_name = True
          EN_cursor.rect.top = 51 + (12 * score_slot)
          animated_sprites.add(EN_cursor)
          animated_sprites.add(enterName)

        score_tested = True


      # add the scores to the screen
      if (scores_drawn is False):
        for i in range(10):
          BTtext(btBackground.image, scores_min[i], 95, (51 + i * 12))
          BTtext(btBackground.image, scores_sec[i], 119, (51 + i * 12))
          BTtext(btBackground.image, scores_name[i], 159, (51 + i * 12))
        scores_drawn = True


      # have the player input their name
      # player_name = ""
      # num_chars = 0
      if (inputting_name is True):
        EN_cursor.update()

        if (EN_key_pressed is True):
          # char set to event.key at top of event loop

          if (char >= 256) and (char <= 265):
            char -= 208  # turn numbers on keypad into numbers above letters, for the chr() statement
          elif (char == 266):
            char == 46  # period on keypad turns into normal period
          elif (char == 269):
            char == 54  # minus on keypad turns into minus above letters
          elif (char == 271):
            char == 13  # Enter on keypad turns into normal Enter

          # change char if shift is being held down
          if (shift_pressed is True):
            if (char == 59):  # ; to :
              char = 58
            elif (char == 39):  # ' to "
              char = 34
            elif (char == 49):  # 1 to !
              char = 33
            elif (char == 47):  # / to ?
              char = 63

          # player input A-Z or 0-9 or ' or : or , or - or " or ! or . or ? or (space)
          if ((char >= 97) and (char <= 122)) or ((char >= 48) and (char <= 57)) or (char == 39) or (char == 58) or (char == 44) or (char == 45) or (char == 34) or (char == 33) or (char == 46) or (char == 63) or (char == 32):
            if (num_chars < 12):
              player_name += str(chr(char)).upper()
              BTtext(btBackground.image, player_name, 159, (51 + score_slot * 12))
              EN_cursor.move(True)  # 'True' makes it move to the right
              num_chars += 1
          elif (char == 8):  # backspace
            if (num_chars > 0):
              player_name = player_name[:-1]  # remove the last character
              # clear out name with 12   (123456789012) - length string of tildes, then print updated name
              BTtext(btBackground.image, "~~~~~~~~~~~~", 159, (51 + score_slot * 12))
              BTtext(btBackground.image, player_name, 159, (51 + score_slot * 12))
              EN_cursor.move(False)  # 'False' makes it move to the left
              num_chars -= 1
          elif (char == 13):  # Enter pressed; done inputting name
            if (num_chars > 0):  # make sure player's name is at least 1 char
              scores_name[score_slot] = player_name

              animated_sprites.remove(EN_cursor)
              animated_sprites.remove(enterName)

              # write updates scores to scores.dat
              fullname = os.path.join('data', 'scores.dat')
              file = open(fullname, 'w')
              for i in range(10):
                file.write(str(scores_min[i] + '\n'))
                file.write(str(scores_sec[i] + '\n'))
                file.write(str(scores_name[i] + '\n'))
              file.close()

              inputting_name = False

          EN_key_pressed = False
      else:  # done inputting name
        if (al == 0):
          enter_init = True

      if (EN_enter_pressed is True):
        if (enter_init is True):
          fading = True
          pygame.mixer.music.fadeout(1000)
          enter_init = False

        if (fading is True):
          blackFade.image.set_alpha(al)
          if (al == 255):
            fading = False
          al += 5
        else:
          pygame.time.delay(2000)

          btBackground.kill()
          pressEnter.kill()
          EN_cursor.kill()
          enterName.kill()
          blackFade.kill()

          # for game to function properly once it's "started over"
          clock_start = pygame.time.get_ticks()  # will reset ct to 0

          state = "initialize"

      idle_sprites.draw(screen)
      active_sprites.draw(screen)
      animated_sprites.draw(screen)
      fade_sprites.draw(screen)


# ----------------------------_____ ENTER NAME _____------------------------------


# ------------------------------ *** end STATES *** ------------------------------


    # flip the newly drawn screen to the display, replacing the old one
    pygame.display.flip()

  # game over; reset display so it's not fullscreen
  if (pygame.mixer.music.get_busy()):
    pygame.mixer.music.stop()
  screen = pygame.display.set_mode((320, 240))


# ------------------------------- *** end MAIN *** -------------------------------


# calls the main function when this script is executed
if __name__ == '__main__': main()
