from importlib import reload

import pygame
import os
from random import *
import time
global blink
blink = False

# Initialize pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("sounds\song.mp3")
pygame.mixer.music.play(-1)
global eatsound,bwomp
eatsound = pygame.mixer.Sound("sounds/food.mp3")
bwomp = pygame.mixer.Sound("sounds/bwoarp.mp3")
fatmode = 2

# Screen dimensions and settings
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Food Movement with Player Collision")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Button class to create and manage button actions
class Button:
    def __init__(self, x, y, width, height, text,image):
        self.rect = pygame.Rect(x-width//2, y-height//2, width, height)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('sprites', image)), (width, height))
        self.text = text
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        #pygame.draw.rect(surface, GRAY, self.rect)
        surface.blit(self.image,self.rect)
        #pygame.draw.rect(surface, BLACK, self.rect, 2)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, mouse_x, mouse_y):
        return self.rect.collidepoint(mouse_x, mouse_y)


# Player class (same as your existing Player class)
class Player:
    def __init__(self):
        self.eating = 0
        self.size = 1
        self.eaten=0
        self.players = ['PUSSY!!','frog','fatkapi']
        self.poo=0
        self.player = 'PUSSY!!'
        #self.player = 'frog'
        folder = f'sprites/{self.player}/size {self.size}'
        self.left = Button(50, 300, 50, 50, "",'button.png')
        self.right = Button(width-50, 300, 50, 50, "", 'button.png')
        self.body = pygame.image.load(os.path.join(folder, "body.png"))
        self.eyes = pygame.image.load(os.path.join(folder, "face/eyesopen.png"))
        self.blink = pygame.image.load(os.path.join(folder, "face/eyesclosed.png"))
        self.smile = pygame.image.load(os.path.join(folder, "face/smile.png"))
        self.open = pygame.image.load(os.path.join(folder, "face/mouthopen.png"))
        self.table = pygame.image.load('sprites/PUSSY!!/table.PNG')

        # Resize images to fit within a max size while maintaining aspect ratio
        self.max_width = 800
        self.max_height = 800
        self.body = self.scale_and_center(self.body)
        self.eyes = self.scale_and_center(self.eyes)
        self.blink = self.scale_and_center(self.blink)
        self.smile = self.scale_and_center(self.smile)
        self.open = self.scale_and_center(self.open)
        self.table = self.scale_and_center(self.table)

        # Green box inside the player to catch the food
        self.green_box = pygame.Rect(width // 2 - 50, 250, 100, 10)
        self.blue_box = pygame.Rect(width // 2 - 100, 150, 200, 200)

    def reset(self):
        # Reset player variables to defaults
        self.eating = 0
        self.size = 1
        self.eaten = 0
        self.poo = 0
        self.player = self.players[self.poo]  # Reset to default player character
        self.reload()  # Reload the initial images and setup
        self.left = Button(50, 300, 50, 50, "", 'button.png')
        self.right = Button(width - 50, 300, 50, 50, "", 'button.png')

    def scale_and_center(self, image):
        # Scale the image while preserving the aspect ratio
        image_rect = image.get_rect()
        scale_factor = min(self.max_width / image_rect.width, self.max_height / image_rect.height)
        new_size = (int(image_rect.width * scale_factor), int(image_rect.height * scale_factor))
        scaled_image = pygame.transform.scale(image, new_size)

        # Center the image on the screen
        centered_rect = scaled_image.get_rect(center=(width // 2, height // 2))
        return scaled_image, centered_rect
    def reload(self):
        self.player = self.players[self.poo]
        folder = f'sprites/{self.player}/size {self.size}'
        self.body = pygame.image.load(os.path.join(folder, "body.png"))
        self.eyes = pygame.image.load(os.path.join(folder, "face/eyesopen.png"))
        self.blink = pygame.image.load(os.path.join(folder, "face/eyesclosed.png"))
        self.smile = pygame.image.load(os.path.join(folder, "face/smile.png"))
        self.open = pygame.image.load(os.path.join(folder, "face/mouthopen.png"))
        self.table = pygame.image.load('sprites/PUSSY!!/table.PNG')

        # Resize images to fit within a max size while maintaining aspect ratio
        self.body = self.scale_and_center(self.body)
        self.eyes = self.scale_and_center(self.eyes)
        self.blink = self.scale_and_center(self.blink)
        self.smile = self.scale_and_center(self.smile)
        self.open = self.scale_and_center(self.open)
        self.table = self.scale_and_center(self.table)
        if self.size==6:
            pygame.mixer.Sound.play(bwomp)
            screen.blit(self.table[0], self.table[1])
            screen.blit(self.body[0], self.body[1])
            screen.blit(self.blink[0], self.blink[1]) if blink else screen.blit(self.eyes[0], self.eyes[1])
            screen.blit(self.open[0], self.open[1])
            screen.blit(self.smile[0], self.smile[1])
            pygame.display.flip()
            time.sleep(3)

    def draw(self, surface):
        global blink
        if blink:
            blink = not blink if randint(0, 3) == 1 else blink
        else:
            blink = not blink if randint(0, 100) == 4 else blink
        if not self.eaten:
            self.left.draw(screen)
            self.right.draw(screen)
        if self.eating>0:
            self.eating-=1
            if self.eating ==0:
                pygame.mixer.Sound.play(eatsound)
                self.eaten+=1
                if fatmode and self.size<1+self.eaten//1 and self.size<6:
                    self.size+=1
                    if fatmode == 1:self.size=max(self.size,4)
                    self.reload()

        #print(self.eating)
        # Draw images centered
        surface.blit(self.table[0], self.table[1])
        surface.blit(self.body[0], self.body[1])
        surface.blit(self.blink[0], self.blink[1]) if blink else surface.blit(self.eyes[0], self.eyes[1])
        surface.blit(self.open[0], self.open[1]) if self.eating else ''
        surface.blit(self.smile[0], self.smile[1])
        if self.size<6: surface.blit(self.table[0], self.table[1])
        #pygame.draw.rect(surface, BLUE, self.blue_box)
        #pygame.draw.rect(surface, GREEN, self.green_box)  # Draw the green box


# Food class to create a clickable, moving, and disappearing item
class Food:
    def __init__(self):
        # Set initial random position and color
        self.x = randint(50, width - 50)
        self.y = 0
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.size = 100
        self.is_visible = True
        self.holyfucklouisimcumming=False
        self.moving = False
        self.hide_timer = 0  # Time to keep the food hidden
        self.dragging = False  # Whether the food is being dragged
        image_folder = "sprites/foods"
        shits = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, choice(shits))), (self.size, self.size))

    def draw(self, surface):
        if self.is_visible:
            #pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))
            surface.blit(self.image,(self.x, self.y, self.size, self.size))

    def check_click(self, mouse_x, mouse_y):
        # Check if the food item was clicked
        if self.is_visible and self.x <= mouse_x <= self.x + self.size and self.y <= mouse_y <= self.y + self.size:
            self.dragging = True  # Start dragging
            return True
        return False

    def stop_dragging(self):
        self.dragging = False

    def move_with_mouse(self, mouse_x, mouse_y):
        if self.dragging:
            self.x = mouse_x - self.size // 2  # Center the food with the mouse
            self.y = mouse_y - self.size // 2

    def check_collision(self, green_box):
        if not self.holyfucklouisimcumming:
            if self.y<height-randint(0, 255):
                self.y+=15
            else:
                self.holyfucklouisimcumming = True
        else:
            # Check if the food collides with the green box
            food_rect = pygame.Rect(self.x, self.y, self.size, self.size)
            return food_rect.colliderect(green_box)

    def reset(self):
        del self


def title_screen():
    title_font = pygame.font.Font(None, 80)
    info_font = pygame.font.Font(None, 40)

    # Text
    title_text = title_font.render("Eat! Eat! Eat!!", True, BLACK)
    info_text = info_font.render("Press Any Key to Start", True, BLACK)

    # Position the text
    title_rect = title_text.get_rect(center=(width // 2, height // 3))
    info_rect = info_text.get_rect(center=(width // 2, height // 1.5))

    # Title screen loop
    title_screen = True
    while title_screen:
        screen.fill(WHITE)  # Background color for the title screen
        screen.blit(title_text, title_rect)
        screen.blit(info_text, info_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                title_screen = False  # Exit the title screen

        pygame.display.flip()  # Update the display

def settings_menu():
    global fatmode
    fattext=['Off','On','Super Fat Mode']
    # Fonts
    title_font = pygame.font.Font(None, 60)
    option_font = pygame.font.Font(None, 40)

    # Text
    title_text = title_font.render("Settings", True, BLACK)

    # Buttons for settings options
    music_button = Button(width // 2, height // 2 - 50, 200, 50, "Toggle Music", 'button.png')
    fat_button = Button(width // 2, height // 2 - 150, 200, 50, f"Fat Mode:{fattext[fatmode]}", 'button.png')
    back_button = Button(width // 2, height // 2 + 100, 150, 50, "Back", 'button.png')

    # Menu loop
    settings_active = True
    while settings_active:
        screen.fill(WHITE)
        title_rect = title_text.get_rect(center=(width // 2, height // 4))
        screen.blit(title_text, title_rect)

        # Draw options
        fat_button.draw(screen)
        music_button.draw(screen)
        back_button.draw(screen)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if music_button.is_clicked(mouse_x, mouse_y):
                    # Toggle music on/off
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1)
                elif fat_button.is_clicked(mouse_x, mouse_y):
                    fatmode=(fatmode+1)%len(fattext)
                    fat_button = Button(width // 2, height // 2 - 150, 200, 50, f"Fat Mode:{fattext[fatmode]}",
                                        'button.png')
                elif back_button.is_clicked(mouse_x, mouse_y):
                    settings_active = False  # Exit settings menu

        pygame.display.flip()

# Call the title screen function
title_screen()


# Initialize player, food list, and button
player = Player()
food = []
add_food_button = Button(width-75, 75, 100, 100, "",'button.png')  # Button positioned at (50, 50)
reset_button = Button(width // 2, 50, 150, 50, "Reset", 'button.png')
settings_button = Button(75, 75, 100, 100, "", 'button.png')

# Main game loop
running = True
while running:
    screen.fill(WHITE)  # Fill the screen with white

    # Draw and handle button clicks
    add_food_button.draw(screen)
    reset_button.draw(screen)
    settings_button.draw(screen)

    for poo in food:
        # Move the food with the mouse if dragging
        if poo.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            poo.move_with_mouse(mouse_x, mouse_y)

    # Draw the player and the food items
    player.draw(screen)
    [poo.draw(screen) for poo in food]

    for poo in food:
        if poo.check_collision(player.blue_box):
            player.eating = 2

        if poo.check_collision(player.green_box):
            poo.is_visible = False  # Hide the food
            food.remove(poo)

    pygame.display.flip()  # Update the display

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Check if the add_food_button was clicked
            if add_food_button.is_clicked(mouse_x, mouse_y):
                food.append(Food())  # Add a new Food item
            if reset_button.is_clicked(mouse_x, mouse_y):
                player.reset()  # Reset player variables
                food.clear()  # Clear the list of food items
            if settings_button.is_clicked(mouse_x, mouse_y):
                settings_menu()
            if not player.eaten:
                if player.left.is_clicked(mouse_x,mouse_y):
                    player.poo=(player.poo-1)%len(player.players)
                    player.reload()
                if player.right.is_clicked(mouse_x,mouse_y):
                    player.poo=(player.poo+1)%len(player.players)
                    player.reload()
            for poo in food:
                if poo.check_click(mouse_x, mouse_y): break
        elif event.type == pygame.MOUSEBUTTONUP:
            [poo.stop_dragging() for poo in food]

# Quit pygame
pygame.quit()
