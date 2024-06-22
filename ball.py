import vector as vector
import color as colors
import uuid

GRAVITY = 9.8
TIME_STEP = 0.1
COEFFICIENT_OF_RESTITUTION = 0.8  # Change this value to make the ball more or less bouncy
COEFFICIENT_OF_FRICTION = 0.1

class Ball:
    def __init__(self, color, position, velocity, radius, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.color = color
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.id = uuid.uuid4()

    def _updateColor(self, magnitude):
        n = 100
        cmap = colors.generate_color_map(n)
        color = colors.map_number_to_color(magnitude, cmap, n)
        
        newColor = []
        newColor.append(int(color[0] * 255))
        newColor.append(int(color[1] * 255))
        newColor.append(int(color[2] * 255))
        
        self.color = newColor

        print(newColor)

    def movement(self):
        self.velocity.y += GRAVITY * TIME_STEP

        # Check if the ball is on the ground
        if self.position.y >= self.SCREEN_HEIGHT - self.radius and self.velocity.y >= 0:
            if self.velocity.x > 0:
                self.velocity.x -= COEFFICIENT_OF_FRICTION * GRAVITY * TIME_STEP
                if self.velocity.x < 0:
                    self.velocity.x = 0
            elif self.velocity.x < 0:
                self.velocity.x += COEFFICIENT_OF_FRICTION * GRAVITY * TIME_STEP
                if self.velocity.x > 0:
                    self.velocity.x = 0

        self._updateColor(vector.magnitude(self.velocity))

    def updatePosition(self):
        new_position = vector.add(self.position, vector.multiply(self.velocity, TIME_STEP))

        # Ensure the new position is within the screen bounds
        if new_position.x + self.radius > self.SCREEN_WIDTH:
            new_position.x = self.SCREEN_WIDTH - self.radius
            self.velocity.x = -self.velocity.x * COEFFICIENT_OF_RESTITUTION
        if new_position.x - self.radius < 0:
            new_position.x = self.radius
            self.velocity.x = -self.velocity.x * COEFFICIENT_OF_RESTITUTION
        if new_position.y + self.radius > self.SCREEN_HEIGHT:
            new_position.y = self.SCREEN_HEIGHT - self.radius
            self.velocity.y = -self.velocity.y * COEFFICIENT_OF_RESTITUTION
        if new_position.y - self.radius < 0:
            new_position.y = self.radius
            self.velocity.y = -self.velocity.y * COEFFICIENT_OF_RESTITUTION

        self.position = new_position

    def collides(self, ball):
        if vector.magnitude(vector.subtract(self.position, ball.position)) < self.radius + ball.radius:
            return True