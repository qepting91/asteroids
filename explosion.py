import pygame
import random

class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__(self.containers)
        self.position = position
        self.lifetime = 0.5
        self.particles = [(pygame.Vector2(0, 1).rotate(angle * (360/8)) * random.uniform(50, 100), 
                          random.uniform(0.3, 0.5)) for angle in range(8)]

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

    def draw(self, screen):
        for particle, size in self.particles:
            end_pos = self.position + particle * (1 - self.lifetime/0.5)
            pygame.draw.line(screen, "white", self.position, end_pos, 1)