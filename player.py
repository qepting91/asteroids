import pygame
import math
from constants import (PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, 
                      PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN, 
                      PLAYER_STARTING_LIVES, PLAYER_RESPAWN_TIME,
                      SCREEN_WIDTH, SCREEN_HEIGHT,
                      PLAYER_ACCELERATION, PLAYER_FRICTION)
from circleshape import CircleShape
from shot import Shot
from bomb import Bomb

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.lives = PLAYER_STARTING_LIVES
        self.invulnerable = False
        self.respawn_timer = 0
        self.shield_active = False
        self.shield_timer = 0
        self.speed_boost = 1.0
        self.speed_timer = 0
        self.bombs = 3
        self.bomb_cooldown = 0

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def accelerate(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_ACCELERATION * dt * self.speed_boost
        
        # Apply speed limit
        max_speed = PLAYER_SPEED * self.speed_boost
        if self.velocity.length() > max_speed:
            self.velocity.scale_to_length(max_speed)

    def activate_power_up(self, type):
        if type == "shield":
            self.shield_active = True
            self.shield_timer = 5.0
        elif type == "speed":
            self.speed_boost = 2.0
            self.speed_timer = 5.0

    def drop_bomb(self):
        if self.bomb_cooldown <= 0 and self.bombs > 0:
            self.bombs -= 1
            self.bomb_cooldown = 2.0  # 2 second cooldown between bombs
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            return Bomb(self.position.x, self.position.y, forward)
        return None

    def shoot(self):
        if self.shoot_timer <= 0:
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN
            return shot

    def respawn(self):
        self.position = pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.invulnerable = True
        self.respawn_timer = PLAYER_RESPAWN_TIME

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw_shield(self):
        shield_points = []
        num_points = 8
        outer_radius = self.radius * 1.8
        inner_radius = self.radius * 1.4
        
        for i in range(num_points * 2):
            angle = (i * 2 * math.pi) / (num_points * 2)
            radius = outer_radius if i % 2 == 0 else inner_radius
            x = self.position.x + math.cos(angle) * radius
            y = self.position.y + math.sin(angle) * radius
            shield_points.append((x, y))
            
        return shield_points

    def collides_with(self, other):
        if self.shield_active:
            return False
        points = self.triangle()
        for point in points:
            distance = point.distance_to(other.position)
            if distance <= other.radius:
                return True
        return False

    def draw(self, screen):
        if not self.invulnerable or (self.respawn_timer * 4) % 1 > 0.5:
            points = self.triangle()
            # Draw gray interior
            pygame.draw.polygon(screen, (128, 128, 128), points, 0)  # Solid gray fill
            # Draw white outline
            pygame.draw.polygon(screen, (255, 255, 255), points, 2)  # White border
            
            if self.shield_active:
                shield_points = self.draw_shield()
                pygame.draw.polygon(screen, "blue", shield_points, 2)
        if not self.invulnerable or (self.respawn_timer * 4) % 1 > 0.5:
            pygame.draw.polygon(screen, "white", self.triangle(), 2)
            if self.shield_active:
                shield_points = self.draw_shield()
                pygame.draw.polygon(screen, "blue", shield_points, 2)

    def update(self, dt):
        if self.velocity.length() > 0:
            self.velocity *= (1 - PLAYER_FRICTION * dt)
            
        self.position += self.velocity * dt
        self.wrap_position()
        
        if self.shield_timer > 0:
            self.shield_timer -= dt
            if self.shield_timer <= 0:
                self.shield_active = False
                
        if self.speed_timer > 0:
            self.speed_timer -= dt
            if self.speed_timer <= 0:
                self.speed_boost = 1.0
        
        if self.invulnerable:
            self.respawn_timer -= dt
            if self.respawn_timer <= 0:
                self.invulnerable = False

        if self.shoot_timer > 0:
            self.shoot_timer -= dt
            
        if self.bomb_cooldown > 0:
            self.bomb_cooldown -= dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.accelerate(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.accelerate(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_b]:
            self.drop_bomb()