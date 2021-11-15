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
    def __init__(self, x, y, height, width, border_color):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.border_color = border_color

    def render(self, window, text):
        pygame.draw.rect(window, border_color, (self.x, self.y, self.width, self.height), 5)
        render_text(window, text, )
        


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
run = True

# Main Loop

while run:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
        
    window.fill(background_color)

    # Level 1 test

     # width border = 5

    render_text(window, "test", Point(700, 525))

    # Update the screen display
    pygame.display.flip()
    # Update frames; necessary for the textbox to work
    clock.tick(60)

pygame.quit()