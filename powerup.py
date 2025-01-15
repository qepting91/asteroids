import pygame
import random
from circleshape import CircleShape

class PowerUp(CircleShape):
    def __init__(self, x, y, type):
        super().__init__(x, y, 15)
        self.type = type  # 'shield' or 'speed'
        self.lifetime = 10.0  # Disappears after 10 seconds
        
    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
        self.wrap_position()
        
    def draw(self, screen):
        color = "blue" if self.type == "shield" else "yellow"
        pygame.draw.circle(screen, color, self.position, self.radius, 2)