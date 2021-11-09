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

def render_text(window, text, point):

    font = pygame.font.SysFont("arial", 20)
    text = font.render(text, True, (0, 0, 0))

    text_rect = text.get_rect()
    text_rect.center = (point.x, point.y)

    window.blit(text, text_rect)

# A point class

class Point():

    def __init__(self, x, y):
        self.x = x
        self.y = y

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

