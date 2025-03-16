import pygame
import numpy as np
from ball_system import BallSystem

# Constants
WIDTH, HEIGHT = 640, 480
BALL_RADIUS = 15
FPS = 60
BACKGROUND_COLOR = (30, 30, 30)
BALL_COLOR = (200, 50, 50)
HOVER_BALL_COLOR = (50, 200, 50)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Collision Simulation")
clock = pygame.time.Clock()

# Initialize ball system with 5 fixed balls
ball_system = BallSystem(num_fixed_balls=5)

def draw_balls():
    """Draws balls on the screen."""
    for i, pos in enumerate(ball_system.positions):
        color = BALL_COLOR if ball_system.fixed[i] else HOVER_BALL_COLOR
        pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), BALL_RADIUS)

# Main loop
running = True
while running:
    screen.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if not any(np.linalg.norm(ball_system.positions - np.array([x, y]), axis=1) < 2 * BALL_RADIUS):
                ball_system.add_balls(
                    np.array([[x, y]]),
                    np.array([[0, 0]]),
                    np.array([False])
                )

    ball_system.move_balls()
    ball_system.resolve_collisions()
    draw_balls()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
