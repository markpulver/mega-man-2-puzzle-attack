# mega-man-2-puzzle-attack
Mega Man 2: Puzzle Attack is a mashup with Tetris where you defeat bosses by completing lines — dealing bonus damage with their weapon weaknesses! How quickly can you finish the game?



Mega Man 2: Puzzle Attack
=========================

by Mark Pulver

version 1.1: 04/12/2025

version 1.0: 01/16/2005


Legal Disclaimer
================

This game was made with permission from Capcom, the creators of the Mega Man
game series. All elements (graphics, music, and sound effects (SFX)) from this
game are copyrighted by Capcom, and were used with permission from Capcom. The
exception to this rule is the second song in the final battle, which was created
by Quickshot Game Metal, and is a remake of the music from stages 1 and 2 of
Wily's Castle in Mega Man 2 on the NES. At the time of the composition of this
song, Joey Ellis was the sole member of Quickshot Game Metal. (See "Credit
Where Credit is Due" for more information.)

This is the email I was sent by Capcom concerning this game:

    "As long as you are not profiting from this project or attacking Capcom
    employees in it, you're welcome to use Mega Man material for your game."

For obvious reasons, I cannot share the name of the employee that emailed this
response to me, nor can I share his or her email address.

Those wishing to create Mega Man games for distribution on the Internet should
contact Capcom, whether they are using elements straight from a Mega Man game,
or are using elements from this game, or are using elements from any other game
that were taken from a Mega Man game.

Tetris copyright 1987 V/O Electronorgtechnica (Elorg). All rights reserved.
Tetris is a trademark of Elorg. Tetris copyright and trademark licensed to
Sphere, Inc. Original concept by Alexei Pazhitnov. Original design and program
by Vadim Gerasimov. This game is a Tetris-clone, or a reasonable facsimile
thereof. Note that this game is distributed as FREEWARE, and may never be used
to obtain profit of any sort, directly or indirectly. It may also never be
combined with any other software package that is used to obtain profit of any
sort, directly or indirectly. This applies to myself, and to any other person
who distributes, or makes access available to, copies of this program.

The source code for this game is included for instructional purposes. Compil-
ation of the source code by anyone but me may violate the permission given by
Capcom. Alteration of the source code or any data files (graphics, music, SFX,
or the "credits.dat" file), may violate the permission given by Capcom. This
game may be distributed to others, provided that it has not been altered in any
way, and that all the files that I packaged with it are included (see "What
Comes With This Game"). Distributing altered copies of this game may violate
Capcom copyrights and will not be recognized as valid copies of the game.

I cannot and will not be held responsible for any damages, liabilities, or
otherwise negative occurrences resulting from the use, misuse, or abuse of this
software, or of anything mentioned in this Legal Disclaimer. This game is
intended to be distributed free of viruses or harmful effects to the user.
Should any viruses or harmful effects occur from the use of this program, I will
not be held responsible. This program may have been altered by a third party
to contain viruses or harmful effects, in which case, I also cannot be held
responsible. This program is intended to be distributed "as-is", and users
should run it at their own risk. I have not knowingly implanted any viruses or
harmful effects into this program, and any user of this program acknowledges my
freedom from liability of any kind by installing or running this program. I am
also not responsible for alterations to this Legal Disclaimer by any person but
myself, even should those alterations violate the terms of the permission given
me by Capcom to create this game, or if it should violate the original Legal
Disclaimer in any other fashion.

Anyone using this program for any means agrees to everything herein, even if
this Legal Disclaimer is missing, in part or in whole, and even if they have
not read this Legal Disclaimer. They also agree that I have the final say on
what this Legal Disclaimer does and does not say, and which version is correct,
should such disputes occur.



What Comes With This Game
=========================

In the directory into which this game is installed, the following files should
be found. If they are not, it may be an altered version of the game, and may
violate the Legal Disclaimer above. They should be:

    - controls.txt: The file explaining the game controls
    - MM2PA.exe: The executable game file; run this to play the game
    - readme.txt: This file

    - data/MM2PA.py: The Python source code file for the game



Why I Made This Game
====================

I made this game because:

    1. I wanted to learn a new programming language
    2. I love Mega Man games

I wanted to make something different from the standard Tetris-clone and decided
to take the opportunity to pay homage to Mega Man 2, my favorite in the
standard Mega Man series.



How I Made This Game
====================

I made this game using:

    For version 1.1:
        Python 3.13.2
        Pygame 2.6

    For version 1.0:
        Python 2.3.4
        Pygame 1.6

Pygame is a wrapper, or a set of classes and functions, that was created to be
used with Python. It simplifies the interactions between Python and SDL, the
Simple Directmedia Library. SDL is a cross-platform multimedia library, similar
to DirectX. By using Pygame, no direct programming in SDL was necessary.

I learned Python via the excellent tutorial that it comes with. I learned
Pygame via the extremely helpful tutorials and examples that it comes with. For
most problems that I encountered while programming, I was able to refer to the
documentation for Python and/or Pygame for a solution. When that failed, I was
usually able to find a solution online.

All of the logic for this game was developed and implemented by me. Most of the
code for this game was developed and implemented by me, although some of the
more basic functions in the game, such as "load_image", were taken directly from
the examples included with Pygame.



What I Would Have Done Differently
==================================

I've learned a lot by making this game: a lot about Python, a lot about Pygame,
and a lot about programming in general. That is, arguably, the point of making
a practice game with a new language. That being said, there are things I would
have done differently. I've learned from those mistakes but do not feel the
need to go back and change them. The code is reasonably commented, but it seems
a waste of time. However, I will list them here, so that hopefully anyone who
wishes to learn (for the first time / more about) Python and/or Pygame can avoid
those mistakes. Note that anything that affected the performance of this
program was corrected, but I will still list it here:

    NAMING CONVENTIONS: This is easily the item I most wish I had implemented.
    By naming conventions, I mean not only consistency, but an explicit nature
    that immediately identifies anything in the program. By this, I mean that
    all function names would have started with "FN_", all sprites names would
    have started with "SPR_", all classes would have started with "CLS_", all
    group (a means of looking at sprites in categories) names would have started
    with "GRP_", etc. When I was making the program, it was somewhat easy to
    remember that "press_enter" is a sprite instead of a Boolean variable (True
    or False, that is). However, such a thing could be forgotten in the future,
    if I were to return to the code and look at a random spot. A name such as
    "SPR_press_enter", though, is unmistakable.

    A SMALLER NUMBER OF CLASSES: There are many classes that I created just to
    load one particular graphic. This should have been replaced by some super
    class (e.g., "CLS_graphic"), that takes many arguments to specify filename,
    transparent color, the coordinates of the top-left pixel where the image
    will default to, etc.

    STORY SEQUENCE: In the intro, the text for the story sequence is, I'm
    afraid to say, comprised of graphics instead of actual text. This could
    have been done, as the credits are read from the "data\credits.dat" file;
    however, when I first created the game, I had not yet implemented the code
    that can translate normal text into the Mega Man 2 font. I guess the lesson
    here is that in my excitement to see a certain thing on the screen, I would
    sometimes take a shortcut, when I should have taken a more logical approach.
    Such times when I -did- take a more logical approach, the results were
    always more satisfying, for I knew I had done them right. Or at least,
    "right" as I would define it for myself.

    STARTING THE GAME OVER AGAIN AFTER THE PLAYER HAS BEATEN IT: This turned
    out to be a chore, as I had at first initialized almost everything before
    the main() function, including loading all the graphics. :-/ I ended up
    encapsulating all of the loading (and unloading, via the kill() statement)
    to each individual state ("title", "intro", etc.). I also created an
    "initialize" state, which gives values to many variables that are
    needed for the entire game. Once the game is done, I just set the "state"
    variable back to "initialize", and everything is reset. I definitely
    recommend this kind of section encapsulation/independence for any program.

    DRAWING TETRIS BLOCKS: At first, I programmed the game to clear out the
    entire block area, and redraw each block, -every time- through the main game
    loop. Needless to say, this was grossly inefficient, and caused slowdown in
    the last level, which has a more CPU-intensive background. I ended up
    changing the program so that the entire block area is updated only when one
    or more lines are completed; otherwise, just the area around the piece is
    updated (when a piece is moved, rotated, or dropped). The lesson here is
    that it pays to only redraw the things that need to be redrawn, and only
    when they need to be redrawn. VERSION 1.1 UPDATE: To fix a bug that showed
    up as I was converting to the current versions of Python and Pygame, I
    actually went back to clearing/redrawing the entire block area. Computers
    have gotten so much faster in 20 years that this is no longer an issue!



Credit Where Credit is Due
==========================

There are various companies and individuals to whom I would like to extend my
thanks:

    - The creators of Tetris. Without it, this game would not exist.
    - Capcom, for the Mega Man games. Without them, this game would not exist.
    - The creators of Pygame. Without them, this game might not exist.
    - The creators of Python and SDL. Without them, Pygame would not exist.
    - Brian Kerr. Without him, I wouldn't have started using Python/Pygame.
    - Isaac Wyatt. For his playtesting of the game, and for his constant
      realism, even if it bordered on pessimism. ^_^
    - Mark Brooks. For waiting so patiently for this game.
    - Joey Ellis. Last, and most certainly not least. Joey Ellis, as I
      mentioned in the Legal Disclaimer, created the remake of the music from
      stages 1 and 2 of Wily's Castle in Mega Man 2, which I have used in the
      final battle of this game. His band, Quickshot Game Metal, creates great
      remakes of music from many old NES games, and can be found at
      (http://www.nintendometal.tk). I would also like to thank him for helping
      me figure out how to acquire the music from Mega Man 2, which was done
      via an NSF (Nintendo Sound File) reader plugin for Winamp. Many thanks.



Questions Players may Have
==========================

Q. Can I play this full-screen?

A. Unfortunately, no, as Python does not have a quick solution for running a
   game in 320x240 pixels (NES resolution) and taking up most of the screen.
   I was able to turn on scaling, so it will multiply pixels to 2x, 3x, etc.
   and take up as much of your screen as possible.

Q. How do I control this game?

A. See the file "controls.txt" for full details.

Q. When I complete a line, the robot doesn't take damage. Why?

A. This is because some robots are immune to some weapons. Change the weapon
   you are using (F1-F9, for colored robot faces) to try to find what the
   robot is weak against. If all else fails, use the P-Shooter (F5), as it
   will do at least 1 damage to any standard robot.

Q. How do I get more weapons?

A. When you defeat a robot, its face will become colored in the display in
   the bottom-left of the gameplay screen. On subsequent levels, pressing
   the function key shown by that robot's face will change Mega Man's selected
   weapon to that of the corresponding robot.

Q. I messed around with the "data\scores.dat" file, and now the program
   crashes when it tries to load the scores. What should I do?
   
A. Just delete the file, and the program will create a new one the next time
   you run it. Note that this is why the game is not distributed with a
  "scores.dat" file in the first place.

Q. I can't seem to quit the program, and end up forcing the program to close
   instead. How can I quit?

A. Pressing Esc at the stage select screen, or while the blocks are falling
   during gameplay, will bring up a quit prompt. If you're in a hurry, close
   the Command Prompt window that should be behind MM2PA's window.

Q. Can I play this game on any platform?

A. Python and Pygame are intended to be platform-independent programming
   tools. However, this was developed on a Windows platform, and remains
   untested on any Mac OS, on UNIX, etc. Feel free to try it out.

Q. Can I contact you about this game?

A. Sure! markpulver@gmail.com
