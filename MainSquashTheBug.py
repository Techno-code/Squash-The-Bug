# This is the main file for my game jam project Squash The Bug

# Import and Initiation

import pygame
import random

pygame.init()

# Functions and class

# Adding Image

def render_image(window, img_path, point):
    img = pygame.image.load(img_path)
    window.blit(img, (point.x, point.y))

# Adding Text

def render_text(window, text, point, font_size, font_colour):
    
    font = pygame.font.SysFont("arial", font_size)
    text = font.render(text, True, font_colour)

    text_rect = text.get_rect()
    text_rect.center = (point.x, point.y)

    window.blit(text, text_rect)

# A point class


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Goal():
    def __init__(self, x, y, height, width, border_color, font_colour, text):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.border_color = border_color
        self.text = text
        self.font_colour = font_colour
        self.font = "arial"
        self.font_size = 15

    def render_goal(self, window):
        rect = pygame.draw.rect(window, self.border_color, (self.x, self.y, self.width, self.height), 5)
        y = rect.top
        lineSpacing = -2
        aa=False
        bkg=None
        font = pygame.font.SysFont("arial", self.font_size)

        # get the height of the font
        fontHeight = font.size("Tg")[1]

        while self.text:
            i = 1

            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break

            # determine maximum width of line
            while font.size(self.text[:i])[0] < rect.width and i < len(self.text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word      
            if i < len(self.text): 
                i = self.text.rfind(" ", 0, i) + 1

            # render the line and blit it to the surface
            if bkg:
                image = font.render(self.text[:i], 1, self.font_colour, bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(self.text[:i], aa, self.font_colour)

            window.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing

            # remove the text we just blitted
            self.text = self.text[i:]

        render_text(window, self.text, Point(self.x, self.y), self.font_size, self.font_colour)
        


# Button Class

class Button():

    def __init__(self, len, wid, position, color):
        self.len = len
        self.wid = wid
        self.position = position
        self.rect = pygame.Rect(position.x, position.y, len, wid)
        self.color = color

    def render(self, window):
        # (window, color, (tlx, tly, len, wid))
        pygame.draw.rect(window, self.color, self.rect)

    def on_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # Write code in the main event loop if the button.on_click(event) is true
                return True

# Setting up Main Loop

window = pygame.display.set_mode((800, 950))
clock = pygame.time.Clock()
background_color = (31, 31, 36)
border_color = (156, 141, 140)
border_coords = (10, 820, 780, 120)
test_goal = Goal(100, 100, 400, 80, (0,0,0), (0,0,0), "Testing Idk if this can work but here we go")
run = True

# Main Loop

while run:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
        
    window.fill(background_color)

    # Level 1 test

     # width border = 5

    
    test_goal.render_goal(window)

    # Update the screen display
    pygame.display.flip()
    # Update frames; necessary for the textbox to work
    clock.tick(60)

pygame.quit()