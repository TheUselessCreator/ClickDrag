import pygame
import sys
import tkinter as tk
from tkinter import colorchooser, filedialog
import webbrowser

# Initialize pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Click and Drag Highlight")

# Set up colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BUTTON_COLOR = (100, 200, 100)
BUTTON_HOVER_COLOR = (150, 250, 150)
DISCORD_BUTTON_COLOR = (114, 137, 218)
DISCORD_BUTTON_HOVER_COLOR = (83, 100, 151)
highlight_color = BLUE  # Default color for the highlight
DISCORD_TEXT_COLOR = (255, 255, 255)

# Button setup
button_width, button_height = 150, 50
button_rect = pygame.Rect(10, 10, button_width, button_height)  # "Change Color" button
bg_button_rect = pygame.Rect(170, 10, button_width, button_height)  # "Set Background" button

# Join Discord button setup
discord_button_width, discord_button_height = 150, 50
discord_button_rect = pygame.Rect(screen_width - discord_button_width - 10, 10, discord_button_width, discord_button_height)  # Button location

# Variables for dragging
dragging = False
start_pos = (0, 0)
current_pos = (0, 0)
rect_width = 0
rect_height = 0
background_image = None  # Variable to store the background image

# Function to draw a rectangular button with text
def draw_button(color, rect, text):
    pygame.draw.rect(screen, color, rect)  # Rectangular button
    font_size = min(rect.width, rect.height) // 3  # Scale font size to button size
    font = pygame.font.SysFont(None, font_size)  # Set font size
    
    # Render the text
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)  # Center the text
    screen.blit(text_surface, text_rect)

# Function to open a color picker dialog
def open_color_picker():
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    chosen_color = colorchooser.askcolor()[0]  # Open color picker dialog
    if chosen_color:  # If a color is selected
        return (int(chosen_color[0]), int(chosen_color[1]), int(chosen_color[2]))
    return highlight_color  # Return the chosen color or the current one if canceled

# Function to open a file dialog and set the background image
def open_image():
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    file_path = filedialog.askopenfilename()  # Open file dialog
    if file_path:
        try:
            image = pygame.image.load(file_path)
            return pygame.transform.scale(image, (screen_width, screen_height))  # Resize to fit screen
        except pygame.error:
            print("Unable to load image.")
    return None

# Function to open the Discord server URL
def open_discord():
    url = "https://discord.gg/TGTaXgA2yr"  # Replace with your Discord server invite URL
    webbrowser.open(url)

# Game loop
while True:
    screen.fill(WHITE)  # Clear the screen with white background

    # Draw the background image if one is set
    if background_image:
        screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Check for button clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                highlight_color = open_color_picker()  # Change color button
            elif bg_button_rect.collidepoint(event.pos):
                background_image = open_image()  # Set background button
            elif discord_button_rect.collidepoint(event.pos):
                open_discord()  # Join Discord button
            else:
                start_pos = event.pos  # Save start position for drag
                current_pos = event.pos  # Initialize current_pos when clicking
                dragging = True

        # When mouse button is released
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        # While mouse is being dragged
        if event.type == pygame.MOUSEMOTION and dragging:
            current_pos = event.pos
            rect_width = current_pos[0] - start_pos[0]
            rect_height = current_pos[1] - start_pos[1]

    # Draw the rectangle while dragging
    if dragging:
        # Handle negative width/height to allow dragging in any direction
        rect = pygame.Rect(min(start_pos[0], current_pos[0]),
                           min(start_pos[1], current_pos[1]),
                           abs(rect_width), abs(rect_height))
        pygame.draw.rect(screen, highlight_color, rect, 2)

    # Handle button hover effect
    draw_button(BUTTON_COLOR if not button_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_HOVER_COLOR, button_rect, "Change Color")
    draw_button(BUTTON_COLOR if not bg_button_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_HOVER_COLOR, bg_button_rect, "Set Background")

    # Draw the Discord button with text
    draw_button(DISCORD_BUTTON_COLOR if not discord_button_rect.collidepoint(pygame.mouse.get_pos()) else DISCORD_BUTTON_HOVER_COLOR, discord_button_rect, "Join Discord")

    pygame.display.update()
