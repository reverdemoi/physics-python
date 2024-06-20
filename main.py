import pygame
import sys
import math
import time
import matplotlib.colors as mcolors
from colorama import Fore

pygame.init()
font = pygame.font.SysFont("Arial" , 18 , bold = True)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]

GRAVITY = 9.8
TIME_STEP = 0.1
COEFFICIENT_OF_RESTITUTION = 0.8  # Change this value to make the ball more or less bouncy
COEFFICIENT_OF_FRICTION = 0.1

def generate_color_map(n=100):
    """
    Generate a colormap that transitions smoothly through the colors of the rainbow.
    """
    # Define the colors of the rainbow
    colors = ["green", "blue", "red"]
    # Create a colormap from these colors
    cmap = mcolors.LinearSegmentedColormap.from_list('rainbow', colors, N=n)
    return cmap

def map_number_to_color(number, cmap, n=100):
    """
    Map a number in the range 1 to n to a color using the provided colormap.
    """
    # Normalize the number to the range 0 to 1
    norm = mcolors.Normalize(vmin=1, vmax=n)
    # Get the color from the colormap
    color = cmap(norm(number))
    return color

def subtract(vector1, vector2):
    return Vector(vector1.x - vector2.x, vector1.y - vector2.y)

def normalize(vector):
    length = math.sqrt(vector.x ** 2 + vector.y ** 2)
    if length == 0:
        return Vector(0, 0)
    return Vector(vector.x / length, vector.y / length)

def multiply(vector, scalar):
    return Vector(vector.x * scalar, vector.y * scalar)

def magnitude(vector):
    return math.sqrt(vector.x ** 2 + vector.y ** 2)

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

SCREEN_CENTER = Vector(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

class Ball:
    def __init__(self, color, position, velocity, radius):
        self.color = color
        self.position = position
        self.velocity = velocity
        self.radius = radius

    def _updateColor(self, magnitude):
        n = 100
        cmap = generate_color_map(n)
        color = map_number_to_color(magnitude, cmap, n)
        
        newColor = []
        newColor.append(int(color[0] * 255))
        newColor.append(int(color[1] * 255))
        newColor.append(int(color[2] * 255))
        
        self.color = newColor

        print(newColor)

    def movement(self):
        self.velocity.y += GRAVITY * TIME_STEP

        # Check if the ball is on the ground
        if self.position.y >= SCREEN_HEIGHT - self.radius and self.velocity.y >= 0:
            if self.velocity.x > 0:
                self.velocity.x -= COEFFICIENT_OF_FRICTION * GRAVITY * TIME_STEP
                if self.velocity.x < 0:
                    self.velocity.x = 0
            elif self.velocity.x < 0:
                self.velocity.x += COEFFICIENT_OF_FRICTION * GRAVITY * TIME_STEP
                if self.velocity.x > 0:
                    self.velocity.x = 0

        self._updateColor(magnitude(self.velocity))

    def updatePosition(self):
        new_position = self._add(self._multiply(TIME_STEP))

        # Ensure the new position is within the screen bounds
        if new_position.x + self.radius > SCREEN_WIDTH:
            new_position.x = SCREEN_WIDTH - self.radius
            self.velocity.x = -self.velocity.x * COEFFICIENT_OF_RESTITUTION
        if new_position.x - self.radius < 0:
            new_position.x = self.radius
            self.velocity.x = -self.velocity.x * COEFFICIENT_OF_RESTITUTION
        if new_position.y + self.radius > SCREEN_HEIGHT:
            new_position.y = SCREEN_HEIGHT - self.radius
            self.velocity.y = -self.velocity.y * COEFFICIENT_OF_RESTITUTION
        if new_position.y - self.radius < 0:
            new_position.y = self.radius
            self.velocity.y = -self.velocity.y * COEFFICIENT_OF_RESTITUTION

        self.position = new_position

    def _add(self, vector):
        return Vector(self.position.x + vector.x, self.position.y + vector.y)

    def _multiply(self, scalar):
        return Vector(self.velocity.x * scalar, self.velocity.y * scalar)
    
def genBalls(balls):
    mousePos = Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    print(f"Mouse position: {mousePos.x}, {mousePos.y}")

    subtracted = subtract(mousePos, SCREEN_CENTER)
    normalized = normalize(subtracted)

    balls.append(Ball(WHITE, SCREEN_CENTER, multiply(normalized, 50), 10))

def renderText(window, text, position):
    text = font.render(text, 1, pygame.Color("RED"))
    window.blit(text, position)
    
def main(clock):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    balls = []
    ball = Ball(WHITE, Vector(SCREEN_WIDTH / 2 - 7.5, SCREEN_HEIGHT / 2 - 7.5), Vector(5, 1), 15)

    prev = time.time()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        # Cap at 60 FPS
        clock.tick(60)

        # Clear screen
        screen.fill(BLACK)

        # Not overwhelmingly many balls
        now = time.time()
        print(prev, now)
        if round(prev) != round(now):
            genBalls(balls)
            prev = now

        if len(balls) == 0: continue

        fps = int(clock.get_fps())
        renderText(screen, f"FPS: {fps}", (10,10))
        renderText(screen, f"Number of balls: {len(balls)}", (10,30))
        renderText(screen, f"FPS/BALLS ratio: {round((fps / len(balls) * 100000)) / 100000}", (10,50))

        # now = time.localtime()
        # print(prevSec, now.tm_sec)
        # if prevSec != now.tm_sec:
        #     genBalls(balls)
        #     prevSec = now.tm_sec


        for ball in balls:  
            # Calculate movement
            ball.movement()

            # Move ball
            ball.updatePosition()

            print(f"Magnitude of ball velocity: {magnitude(ball.velocity)}")

            # print(f"Ball position: {ball.position.x}, {ball.position.y}, ball velocity: {ball.velocity.x}, {ball.velocity.y}")

            # Draw ball
            pygame.draw.circle(screen, ball.color, [int(ball.position.x), int(ball.position.y)], ball.radius)
        
        # Update screen
        pygame.display.flip()
        
        # pygame.time.delay(16) # 16ms = 60fps

def init():
    clock = pygame.time.Clock()

    main(clock)

if __name__ == "__main__":
    init()
