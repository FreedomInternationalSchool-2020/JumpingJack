import pygame, random, itertools, sys
from pygame import *

white = (255, 255, 255)
black = (0,0,0)
light_red = (230, 0, 0)
light_green = (0, 240, 0)
light_blue = (51, 153, 255)
gray = (128, 128, 128)
green = (0, 180, 0)
red = (190, 0, 0)
blue = (0, 102, 204)

# Initialize pygame
pygame.init()
pygame.display.set_caption('Jumping Jack')
window = pygame.display.set_mode((900, 700))

# Lets play some tunes
pygame.mixer.music.load('res/music.mp3')
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()

"""
    Function to create a button with text in it and set its colour to its light
    version when mouse is hovered on it. Also returns True when clicked on it.
"""
def button(text, colorname, x, y, w, h, tx, ty):
    color = eval(colorname)

    pygame.draw.rect(window, color, [x, y, w, h])
    display_text(text, (tx, ty), "res/SansPosterBold.ttf", 40)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Detect mouse hover by comparing coordinates of box and mouse point
    for i, j in itertools.product(range(x, x+w+1), range(y, y+h+1)):
        if i == mouse[0] and j == mouse[1]:
            pygame.draw.rect(window, eval("light_"+colorname), [x, y, w, h])
            display_text(text, (tx, ty), "res/SansPosterBold.ttf", 40)

            if click[0]:
                return True

"""
    Function to display text on any surface, provided the co-ordinates,
    font, size etc
"""
def display_text(text, place, font, size):
    font = pygame.font.Font(font, size)
    text_ =  font.render(text, True, black)
    text_rect = text_.get_rect()
    text_rect.center = place
    window.blit(text_, text_rect)

"""
    The main menu. Options: Play, High scores, Quit
"""
def mainmenu():
    run = True
    bg = pygame.image.load("res/bg_mainwindow.png")

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        window.blit(bg, (0, 0))
        play = button('Play', "green", 380, 225, 165, 60, 460, 250)
        highscores = button('High Scores', "blue", 295, 325, 330, 60, 460, 350)
        quitbutton = button('Quit', "red", 380, 425, 165, 60, 460, 450)

        if quitbutton:
            pygame.quit()
            sys.exit()
        elif play:
            gameloop()

        pygame.display.update()
        clock.tick(15)

# Set of coordinates for the platform in (x, y) format
platform_coord = [(291, 567), (463, 504), (572, 453), (739, 443), (409, 377), (206, 328), (61, 273), (257, 189), (405, 180), (567, 122), (636, 252)]

"""
    Function to redraw background & platforms when updating stickman
"""
def redraw():
    bg = pygame.image.load("res/bg_game.png")
    window.blit(bg, (0, 0))
    for coord in platform_coord:
        platform = pygame.image.load("res/platform.png")
        window.blit(platform, (coord[0], coord[1]))

"""
    Function to check whether stickman is on platform
"""
def platformcheck(x, y):
    onplatform=False
    for i in platform_coord:
        if (i[1] in range(y+78, y+94)) and (x in range(i[0]-50, i[0]+80)):
            onplatform=True
            break
    return onplatform

"""
    Main game loop
"""
def gameloop():
    stickman = pygame.image.load("res/stickman_left.png")
    direction = "right"
    x,y=50,530

    redraw()
    pygame.display.update()

    #print(platform_coord)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainmenu()

        key = pygame.key.get_pressed()

        stickman = pygame.image.load("res/stickman_"+direction+".png")
        stickman_right = (pygame.image.load("res/stickman_right.png"), pygame.image.load("res/stickman_running_right.png"), pygame.image.load("res/stickman_jumping_right.png"))
        stickman_left = (pygame.image.load("res/stickman_left.png"), pygame.image.load("res/stickman_running_left.png"), pygame.image.load("res/stickman_jumping_left.png"))

        window.blit(stickman, (x,y))

        # TODO: Collision check (prevent walking throuh platforms)
        collision=False
        """for i in platform_coord:
            if ((x+64 in range(i[0]-11, i[0]+11)) or (x in range(i[0]-11, i[0]+11))) and (i[1] in range(y, y+92)):
                collision=True
                break"""

        if key[K_RIGHT] and not collision:
            if x<=760:
                for i in range(0, 3):
                    x+=8
                    redraw()
                    window.blit(stickman_right[i], (x,y))
                    pygame.display.flip()
                direction="jumping_right"

        elif key[K_LEFT] and not collision:
            if x>=50:
                for i in range(0, 3):
                    x-=8
                    redraw()
                    window.blit(stickman_left[i], (x,y))
                    pygame.display.flip()
                direction="jumping_left"

        elif key[K_UP]:
            velocity=15
            iskeyright=False
            iskeyleft=False

            for i in range(0, 29):
                jumping=True
                velocity-=1
                y-=velocity

                # Check if right/left key is being pressed
                for event in pygame.event.get():
                    if event.type==KEYDOWN:
                        if event.key==K_RIGHT:
                            iskeyright = True
                        elif event.key==K_LEFT:
                            iskeyleft = True

                if x<=760 and iskeyright:
                    x+=8
                elif x>=50 and iskeyleft:
                    direction="jumping_left"
                    x-=8

                redraw()
                window.blit(stickman, (x,y))
                pygame.display.flip()

                if platformcheck(x, y):
                    jumping=False
                    break

        if not platformcheck(x, y):
            downvel=12
            while y<=520:
                falling=True
                y+=downvel
                if platformcheck(x, y): break
                redraw()
                window.blit(stickman, (x,y))
                pygame.display.flip()

        pygame.display.flip()

mainmenu()
pygame.quit()
