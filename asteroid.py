import pygame
import random
import math
from constants import ASTEROID_MIN_RADIUS
from circleshape import CircleShape
from explosion import Explosion

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        # Create random variations for the asteroid's shape
        self.variations = []
        num_points = 12  # Number of points that make up the asteroid
        for i in range(num_points):
            variation = random.uniform(0.8, 1.2)  # Random radius multiplier
            self.variations.append(variation)

    def get_points(self):
        points = []
        num_points = len(self.variations)
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            variation = self.variations[i]
            radius = self.radius * variation
            x = self.position.x + math.cos(angle) * radius
            y = self.position.y + math.sin(angle) * radius
            points.append((x, y))
        return points

    def draw(self, screen):
        points = self.get_points()
        pygame.draw.polygon(screen, "white", points, 2)

    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap_position()

    def split(self):
        Explosion(self.position)
        self.kill()
        
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
            
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        random_angle = random.uniform(20, 50)
        
        vel1 = self.velocity.rotate(random_angle) * 1.2
        vel2 = self.velocity.rotate(-random_angle) * 1.2
        
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = vel1
        
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = vel2