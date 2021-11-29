# This is the main file for my game jam project Squash The Bug

# Import and Initiation

import pygame
import random

from pygame import cursors

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
            return True

class Level():

    def __init__(self, window, tl_point, number):
        # Setting it up
        self.window = window
        self.tl_point = tl_point
        # Position
        self.width = 100
        self.height = 100
        # Showing
        self.number = str(number)
        self.colour = (4, 118, 208)
        self.lvl_rect = pygame.Rect(self.tl_point.x, self.tl_point.y, self.width, self.height)
        self.won_stat = False
    
    def render(self, window):
        pygame.draw.rect(window, self.colour, self.lvl_rect, border_radius = 4)
        render_text(self.window, self.number, Point(self.tl_point.x+50, self.tl_point.y+50), 50, (255,255,255))
        if self.won_stat == True:
            render_text(self.window, "Level " + self.number + " Completed", Point(400, 680+int(self.number)*20), 25, (0,0,0))

    
    def if_won(self, new_won_stat):
        if new_won_stat:
            self.won_stat = True
            self.colour = (13, 152, 186)

    
    def on_click(self, event):
        if self.won_stat == False:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.lvl_rect.collidepoint(event.pos):
                    # Write code in the main event loop if the button.on_click(event) is true
                    return True

    def off_click(self, event):
        if self.won_stat == False:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.lvl_rect.collidepoint(event.pos):
                    return True



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
credits_button = Button(300, 80, Point(250, 800), (244, 236, 93))
pygame.mixer.music.load("bread.wav")  # Add music
pygame.mixer.music.play(-1)

# Back Buttons
htp_back_button = Button(150, 75, Point(25, 850), (244, 236, 93))
ls_back_button = Button(150, 75, Point(25, 850), (244, 236, 93))
l1_back_button = Button(150, 75, Point(25, 725), (244, 236, 93))
l2_back_button = Button(150, 75, Point(25, 725), (244, 236, 93))
l3_back_button = Button(150, 75, Point(25, 725), (244, 236, 93))
l4_back_button = Button(150, 75, Point(25, 725), (244, 236, 93))
l5_back_button = Button(150, 75, Point(25, 725), (244, 236, 93))
l6_back_button = Button(150, 75, Point(25, 725), (244, 236, 93))
# Level 1
level1_button = Level(window, Point(100,100), 1)
level1_goal = Goal(borderx, bordery, height, width, border_color, text_color, 35, "Goal: Print Out Hello World")
level1_code = Text_Box(window, Point(25,420), """print("Hello World')""")
# Level 2
level2_button = Level(window, Point(250,100), 2)
level2_goal = Goal(borderx, bordery, height, width, border_color, text_color, 35, "Goal: Store your input in spam then print it out")
level2_code_1 = Text_Box(window, Point(25,350), "spam = Input()")
level2_code_2 = Text_Box(window, Point(25,400), "print(spam)")
# Level 3
level3_button = Level(window, Point(400,100), 3)
level3_goal = Goal(borderx, bordery, height, width, border_color, text_color, 35, "Goal: Add variables a and b together and print out an integer")
level3_code_1 = Text_Box(window, Point(25,350), """a = input("Insert Number: ")""")
level3_code_2 = Text_Box(window, Point(25,400), """b = input("Insert Number: ")""")
level3_code_3 = Text_Box(window, Point(25,500), """print(a + b)""")
# Level 4
level4_button = Level(window, Point(550,100), 4)
level4_goal = Goal(borderx, bordery, height, width, border_color, text_color, 35, "Goal: Print Made Function using the Foo Function")
level4_code_1 = Text_Box(window, Point(25,350), """def foo()""")
level4_code_2 = Text_Box(window, Point(75,400), """print("Made Function")""")
level4_code_3 = Text_Box(window, Point(25,500), """foo()""")
# Level 5
level5_button = Level(window, Point(100,250), 5)
level5_goal = Goal(borderx, bordery, height, width, border_color, text_color, 35, "Goal: Using the if statment, find if x is less than 5 or more and print out the result, using the least amount of characters")
level5_code_1 = Text_Box(window, Point(25,250), """x = 5""")
level5_code_2 = Text_Box(window, Point(25,350), """if x < 5:""")
level5_code_3 = Text_Box(window, Point(75,400), """print("Less than 5")""")
level5_code_4 = Text_Box(window, Point(25,450), """else x >= 5:""")
level5_code_5 = Text_Box(window, Point(75,500), """print("At least 5")""")
# Level 6
level6_button = Level(window, Point(250,250), 6)
level6_goal = Goal(borderx, bordery, height, width, border_color, text_color, 35, "Goal: print out all values of i from 0 - 3 using the for loop")
level6_code_1 = Text_Box(window, Point(25,400), """for i in range(0, 3):""")
level6_code_2 = Text_Box(window, Point(75,450), """print(i, "so far, final i should be 3")""")

run = True
button_clicked = False
current_screen = 1

# Main Loop

while run:

    

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if current_screen == 4:
            level1_code.check_event(event)

        if current_screen == 5:
            level2_code_1.check_event(event)
            level2_code_2.check_event(event)

        if current_screen == 6:
            level3_code_1.check_event(event)
            level3_code_2.check_event(event)
            level3_code_3.check_event(event)

        if current_screen == 7:
            level4_code_1.check_event(event)
            level4_code_2.check_event(event)
            level4_code_3.check_event(event)

        if current_screen == 8:
            level5_code_1.check_event(event)
            level5_code_2.check_event(event)
            level5_code_3.check_event(event)
            level5_code_4.check_event(event)
            level5_code_5.check_event(event)
        
        if current_screen == 9:
            level6_code_1.check_event(event)
            level6_code_2.check_event(event)

        

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
        credits_button.render(window)
        render_text(window, "Credits", Point(400, 840), 40, (0,0,0))


        if play_button.on_click(event) == True and button_clicked == False:
            button_clicked = True
            
        if play_button.off_click(event) == True:
            button_clicked = False
            current_screen = 3

        if how_to_play_button.on_click(event) == True and button_clicked == False:
            button_clicked = True
        
        if how_to_play_button.off_click(event) == True:
            button_clicked = False
            current_screen = 2
        
        if credits_button.on_click(event) == True and button_clicked == False:
            button_clicked = True
            
        if credits_button.off_click(event) == True:
            button_clicked = False
            current_screen = 10

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

    # Level Selection Screen
    if current_screen == 3:
        level1_button.render(window)
        level2_button.render(window)
        level3_button.render(window)
        level4_button.render(window)
        level5_button.render(window)
        level6_button.render(window)
        ls_back_button.render(window)
        render_text(window, "< Back", Point(75, 880), 30, (0,0,0))

        if level1_button.on_click(event) == True and button_clicked == False:
            button_clicked = True

        if level1_button.off_click(event) == True:
            button_clicked = False
            current_screen = 4

        if level2_button.on_click(event) == True and button_clicked == False:
            button_clicked = True

        if level2_button.off_click(event) == True:
            button_clicked = False
            current_screen = 5

        if level3_button.on_click(event) == True and button_clicked == False:
            button_clicked = True

        if level3_button.off_click(event) == True:
            button_clicked = False
            current_screen = 6

        if level4_button.on_click(event) == True and button_clicked == False:
            button_clicked = True

        if level4_button.off_click(event) == True:
            button_clicked = False
            current_screen = 7
        
        if level5_button.on_click(event) == True and button_clicked == False:
            button_clicked = True

        if level5_button.off_click(event) == True:
            button_clicked = False
            current_screen = 8
        
        if level6_button.on_click(event) == True and button_clicked == False:
            button_clicked = True

        if level6_button.off_click(event) == True:
            button_clicked = False
            current_screen = 9
        
        if ls_back_button.on_click(event) == True:
            current_screen = 1



    # Level 1 test
    if current_screen == 4:

        level1_goal.render_goal(window)
        render_text(window, "1.", Point(12,18), 40, (255,255,255))
        level1_code.render(window)
        #level1_code.check_event(event)

        l1_back_button.render(window)
        render_text(window, "< Back", Point(75, 760), 30, (0,0,0))

        if level1_code.check_win("""print("Hello World")"""):
            level1_button.if_won(True)
            current_screen = 3
        
        if l1_back_button.on_click(event) == True:
            current_screen = 3

    # Level 2
    if current_screen == 5:

        level2_goal.render_goal(window)
        render_text(window, "2.", Point(18,21), 40, (255,255,255))
        level2_code_1.render(window)
        #level2_code_1.check_event(event)
        level2_code_2.render(window)
        #level2_code_2.check_event(event)

        l2_back_button.render(window)
        render_text(window, "< Back", Point(75, 760), 30, (0,0,0))


        if level2_code_1.check_win("""spam = input()""") and level2_code_2.check_win("""print(spam)"""):
            level2_button.if_won(True)
            current_screen = 3

        if l2_back_button.on_click(event) == True:
            current_screen = 3

    # Level 3
    if current_screen == 6:
        level3_goal.render_goal(window)
        render_text(window, "3.", Point(18,21), 40, (255,255,255))
        level3_code_1.render(window)
        level3_code_2.render(window)
        level3_code_3.render(window)
        # level3_code_1.check_event(window)
        # level3_code_2.check_event(window)
        # level3_code_3.check_event(window)

        l3_back_button.render(window)
        render_text(window, "< Back", Point(75, 760), 30, (0,0,0))
        if level3_code_1.check_win("""a = int(input("Insert Number: "))""") and level3_code_2.check_win("""b = int(input("Insert Number: "))""") and level3_code_3.check_win("""print(a + b)"""):
            level3_button.if_won(True)
            current_screen = 3

        if l3_back_button.on_click(event) == True:
            current_screen = 3
    # Level 4
    if current_screen == 7:
        level4_goal.render_goal(window)
        render_text(window, "4.", Point(18,21), 40, (255,255,255))
        level4_code_1.render(window)
        level4_code_2.render(window)
        level4_code_3.render(window)

        l4_back_button.render(window)
        render_text(window, "< Back", Point(75, 760), 30, (0,0,0))
        if level4_code_1.check_win("""def foo():""") and level4_code_2.check_win("""print("Made Function")""") and level4_code_3.check_win("""foo()"""):
            level4_button.if_won(True)
            current_screen = 3

        if l4_back_button.on_click(event) == True:
            current_screen = 3

    # level 5
    if current_screen == 8:
        level5_goal.render_goal(window)
        render_text(window, "5.", Point(18,21), 40, (255,255,255))
        level5_code_1.render(window)
        level5_code_2.render(window)
        level5_code_3.render(window)
        level5_code_4.render(window)
        level5_code_5.render(window)

        l5_back_button.render(window)
        render_text(window, "< Back", Point(75, 760), 30, (0,0,0))

        if level5_code_1.check_win("x = 5") and level5_code_2.check_win("if x < 5:") and level5_code_3.check_win("""print("Less than 5")""") and level5_code_4.check_win("else:") and level5_code_5.check_win("""print("At least 5")"""):
            level5_button.if_won(True)
            current_screen = 3

        if l5_back_button.on_click(event) == True:
            current_screen = 3

    if current_screen == 9:
        

        l6_back_button.render(window)
        render_text(window, "< Back", Point(75, 760), 30, (0,0,0))

        if level6_code_1.check_win("for i in range(0, 4):") and level6_code_2.check_win("""print(i, "so far, final i should be 3")"""):
            level6_button.if_won(True)
            current_screen = 3
        
        level6_goal.render_goal(window)
        render_text(window, "6.", Point(18,21), 40, (255,255,255))
        level6_code_1.render(window)
        level6_code_2.render(window)

    if current_screen == 10:
        render_text(window, 'Created By: Sean Yang', Point(400, 100), 60, (207, 222, 255))
        render_text(window, "Special Thanks To", Point(400, 275), 60, ((207, 222, 255)))
        render_text(window, "Rico Zhu", Point(400, 375), 60, (207, 222, 255))



    # Time to do this

    # Update the screen display
    pygame.display.flip()
    # Update frames; necessary for the textbox to work
    clock.tick(60)

pygame.quit()