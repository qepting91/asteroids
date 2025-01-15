import pygame
from circleshape import CircleShape
from asteroid import Asteroid
from explosion import Explosion

class Bomb(CircleShape):
    def __init__(self, x, y, direction):
        super().__init__(x, y, 5)  # Smaller radius for rocket appearance
        self.velocity = direction * 300  # Slower than normal shots
        self.explosion_radius = 150  # Larger blast radius
        self.explosion_timer = 1.5  # Longer fuse
        
    def update(self, dt):
        self.position += self.velocity * dt
        self.explosion_timer -= dt
        if self.explosion_timer <= 0:
            self.explode()
        self.wrap_position()
            
    def explode(self):
        # Create explosion effect
        Explosion(self.position)
        # Affect asteroids in blast radius
        for sprite in self.groups()[0]:
            if isinstance(sprite, Asteroid):
                if self.position.distance_to(sprite.position) <= self.explosion_radius:
                    sprite.split()
        self.kill()
        
    def draw(self, screen):
        # Draw as small red rocket
        pygame.draw.line(screen, "red", self.position, 
                        self.position - self.velocity.normalize() * 10, 2)