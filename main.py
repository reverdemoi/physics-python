import pygame
import sys
import asyncio
from colorama import Fore
import numpy as np

import vector as vector
import ball as ballClass

pygame.init()
font = pygame.font.SysFont("Arial", 18, bold=True)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]

SCREEN_CENTER = vector.Vector(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

def genBalls(balls):
    mousePos = vector.Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    print(f"Mouse position: {mousePos.x}, {mousePos.y}")

    subtracted = vector.subtract(mousePos, SCREEN_CENTER)
    normalized = vector.normalize(subtracted)

    balls.append(ballClass.Ball(WHITE, SCREEN_CENTER, vector.multiply(normalized, 50), 10, SCREEN_WIDTH, SCREEN_HEIGHT))

def renderText(window, text, position):
    text_surface = font.render(text, True, pygame.Color("RED"))
    window.blit(text_surface, position)

async def gen(balls):
    while True:
        genBalls(balls)
        await asyncio.sleep(0.2)

def compute_collision_velocity(m1, v1, m2, v2, r1, r2):
    """
    Computes the velocities of two colliding balls.
    
    Parameters:
    m1, m2: masses of the balls
    v1, v2: Vector objects representing the initial velocities of the balls
    r1, r2: Vector objects representing the positions of the balls
    
    Returns:
    v1_new, v2_new: Vector objects representing the new velocities of the balls
    """
    
    # Relative position and velocity
    r = vector.subtract(r2, r1)
    v = vector.subtract(v2, v1)
    
    # Normal vector
    n = vector.normalize(r)

    # Relative velocity in the direction of the normal
    v_rel_n = vector.dotProduct(v, n)

    # If the balls are not moving towards each other, return the original velocities
    if v_rel_n > 0:
        return v1, v2
    
    # Compute the new velocities
    # v1_new = v1 + n * (2 * m2 / (m1 + m2) * v_rel_n)
    # v2_new = v2 - n * (2 * m1 / (m1 + m2) * v_rel_n)
    # Convert the two lines above to use the vector methods instead
    v1_new = vector.add(v1, vector.multiply(n, 2 * m2 / (m1 + m2) * v_rel_n))
    v2_new = vector.subtract(v2, vector.multiply(n, 2 * m1 / (m1 + m2) * v_rel_n))
    
    return v1_new, v2_new

def collision(checkBall, balls):
    for ball in balls:
        if ball.id == checkBall.id:
            continue

        if checkBall.collides(ball):
            v1_new, v2_new = compute_collision_velocity(checkBall.radius, checkBall.velocity, ball.radius, ball.velocity, checkBall.position, ball.position)
            checkBall.velocity = v1_new
            ball.velocity = v2_new

async def main(clock):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    balls = []
    asyncio.create_task(gen(balls))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     genBalls(balls)

        # Cap at 60 FPS
        clock.tick(0)

        # Clear screen
        screen.fill(BLACK)

        if len(balls) > 0:
            fps = int(clock.get_fps())
            renderText(screen, f"FPS: {fps}", (10, 10))
            renderText(screen, f"Number of balls: {len(balls)}", (10, 30))
            renderText(screen, f"FPS/BALLS ratio: {round((fps / len(balls) * 100000)) / 100000}", (10, 50))

            for ball in balls:
                collision(ball, balls)
                ball.movement()
                ball.updatePosition()
                pygame.draw.circle(screen, ball.color, [int(ball.position.x), int(ball.position.y)], ball.radius)
        
        # Update screen
        pygame.display.flip()
        
        await asyncio.sleep(0)

async def init():
    clock = pygame.time.Clock()
    await main(clock)

if __name__ == "__main__":
    asyncio.run(init())
