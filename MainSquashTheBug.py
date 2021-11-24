# This is the main file for my game jam project Squash The Bug

# Import and Initiation

import pygame
import random

pygame.init()

# Functions and class

# Adding Image

def render_image(window, img_path, point, size):
    img = pygame.image.load(img_path)
    img = pygame.transform.scale(img, size)
    window.blit(img, (point.x, point.y))

# Adding Text
class Point():
    
    def __init__(self, x, y):
        self.x = x
        self.y = y


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
    def __init__(self, x, y, height, width, border_color, font_colour, font_size, text):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.border_color = border_color
        self.text = text
        self.font_colour = font_colour
        self.font_size = font_size

    def render_goal(self, window):
        rect = pygame.draw.rect(window, self.border_color, (self.x, self.y, self.width, self.height), 5)
        WrapText(window, self.text, self.font_colour, rect, pygame.font.SysFont("arial", self.font_size))

def WrapText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top + 5
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < (rect.width) and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left+8, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text


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

    def off_click(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                return True

# Sticky Note Class
class Text_Box():
    
    def __init__(self, window, tl_point, user_text):
        # Positioning
        self.tl_point = tl_point
        self.input_rect = pygame.Rect(self.tl_point.x, self.tl_point.y, 140, 32)
        # Render colors
        self.surface = pygame.Surface((140, 32))
        self.surface.set_alpha(0)
        self.surface.fill((255,255,255))
        self.color_active = pygame.Color('darkgray')
        self.color_passive = pygame.Color('lightgray')
        self.color = self.color_passive
        self.window = window
        self.active = False
        self.backspaced = False
        # Render text
        self.user_text = user_text
        self.base_font = pygame.font.Font(None, 45)

    def check_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active and event.key == pygame.K_BACKSPACE and self.backspaced == False:
                # Get text input from 0 to -1 i.e. end
                self.user_text = self.user_text[:-1]
                self.backspaced = True
            else:
                if self.active == True:
                    self.user_text += event.unicode
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                self.backspaced = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.active = True
                self.color = self.color_active
            elif not self.input_rect.collidepoint(event.pos):
                self.active = False
                self.color = self.color_passive

    def render(self, window):
        # pygame.draw.rect(window, self.color, self.input_rect)
        self.window.blit(self.surface, (self.input_rect.left, self.input_rect.top))
        text_surface = self.base_font.render(self.user_text, True, (255, 255, 255))
        self.window.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(100, text_surface.get_width() + 10)

    def get_current_text(self):
        return self.user_text

    def update_position(self, n_point):
        self.tl_point = n_point
        self.input_rect = pygame.Rect(self.tl_point.x, self.tl_point.y, 140, 32)

    def check_win(self, win_text):
        if self.user_text == win_text:
            render_text(self.window, "YOU WIN", Point(400,400), 30, (255,255,0))


# Setting up Main Loop

window = pygame.display.set_mode((800, 950))
clock = pygame.time.Clock()
background_color = (31, 31, 36)
border_color = (156, 141, 140)
text_color = (15, 185, 191)
borderx = 10 
bordery = 820
width = 780
height = 120
play_button = Button(300, 80, Point(250, 600), (244, 236, 93))
how_to_play_button = Button(300, 80, Point(250, 700), (244, 236, 93))
htp_back_button = Button(150, 75, Point(25, 850), (244, 236, 93))
level1_goal = Goal(borderx, bordery, height, width, border_color, text_color, 35, "Goal: Print Out Hello World")
level1_code = Text_Box(window, Point(25,420), """print("Hello World')""")
run = True
button_clicked = False
current_screen = 1

# Main Loop

while run:

    

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if current_screen == 3:
            level1_code.check_event(event)
        

    window.fill(background_color)
    
    # Menu Screen

    if current_screen == 1:
        render_image(window, "menu-background.jpg", Point(0,0), (800, 950))
        render_image(window, "fly-swatter.png", Point(150,270), (200, 300))
        render_text(window, "Squash The Bug", Point(400, 100), 100, (189, 207, 59))
        play_button.render(window)
        render_text(window, "Play", Point(400, 635), 40, (0,0,0))
        how_to_play_button.render(window)
        render_text(window, "How To Play", Point(400, 740), 30, (0,0,0))

        if play_button.on_click(event) == True and button_clicked == False:
            button_clicked = True
            
        
        if play_button.off_click(event) == True:
            button_clicked = False
            current_screen = 3

        if how_to_play_button.on_click(event) == True and button_clicked == False:
            button_clicked = True
            print(button_clicked)
        
        if how_to_play_button.off_click(event) == True:
            button_clicked = False
            current_screen = 2
            print(button_clicked)

    # How to play Screen

    if current_screen == 2:
        render_text(window, "In order to play this game, you have to click on the textbox shown in every level.", Point(400, 50), 25, (0,255,0))
        render_text(window, "You can use your keyboard to delete and type in words. The goal of the game", Point(400, 80), 25, (0,255,0))
        render_text(window, "is to find the bug in the code and fix it to the correct one that completes the goal,", Point(400, 110), 25, (0,255,0))
        render_text(window, "if it is correct, you win and move on to the next level", Point(400, 140), 25, (0,255,0))
        render_text(window, "WARNING: I am a very bad game designer,", Point(400, 300), 35, (255,0,0))
        render_text(window, "so there might be multiple solutions to each problem,", Point(400, 340), 35, (255,0,0))
        render_text(window, "but just find the one that requires the least amount", Point(400, 380), 35, (255,0,0))   
        render_text(window, "of tweaking and you would usually get it right!", Point(400, 420), 35, (255,0,0))
        render_image(window, "how-to-play.png", Point(200, 500), (400, 300))
        htp_back_button.render(window)
        render_text(window, "< Back", Point(75, 880), 30, (0,0,0))

        if htp_back_button.on_click(event) == True:
            current_screen = 1
            print(button_clicked)


    # Level 1 test
    if current_screen == 3:

        level1_goal.render_goal(window)
        render_text(window, "1.", Point(12,18), 40, (255,255,255))
        level1_code.render(window)
        level1_code.check_win("""print("Hello World")""")
        level1_code.check_event(event)

    # Time to do this

    # Update the screen display
    pygame.display.flip()
    # Update frames; necessary for the textbox to work
    clock.tick(60)

pygame.quit()