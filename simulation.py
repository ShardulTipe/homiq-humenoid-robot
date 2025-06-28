import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Humanoid Robot Simulation')

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Robot settings
robot_size = 20
robot_pos = [width // 2, height // 2]
cleaned_areas = []

# Clock to control frame rate
clock = pygame.time.Clock()

# Font for text
font = pygame.font.SysFont("Arial", 24)

def draw_robot(pos):
    pygame.draw.circle(screen, BLUE, pos, robot_size)

def clean_area(pos):
    if pos not in cleaned_areas:
        cleaned_areas.append(pos)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the robot randomly
    robot_pos[0] += random.choice([-1, 1])
    robot_pos[1] += random.choice([-1, 1])

    # Ensure robot stays within bounds
    robot_pos[0] = max(robot_size, min(width - robot_size, robot_pos[0]))
    robot_pos[1] = max(robot_size, min(height - robot_size, robot_pos[1]))

    # Clean the area where the robot is located
    clean_area(tuple(robot_pos))

    # Draw everything
    screen.fill(WHITE)
    for area in cleaned_areas:
        pygame.draw.circle(screen, (200, 200, 200), area, robot_size)
    draw_robot(robot_pos)

    # Display status
    text = font.render("Cleaning in progress...", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    # Update the display
    pygame.display.flip()
    clock.tick(30)  # Frame rate

# Quit Pygame
pygame.quit()
sys.exit()
