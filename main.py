import pygame
from constants import *
from circleshape import CircleShape
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Add clock for FPS control
    clock = pygame.time.Clock()
    dt = 0
    
    # Create sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    # Set up containers
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    
    # Create game objects
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        screen.fill("black")
        
        # Update and draw all sprites using groups
        for sprite in updatable:
            sprite.update(dt)
            
        # Check for player-asteroid collisions
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                print("Game over!")
                return
                
            # Check for bullet-asteroid collisions
            for shot in shots:
                if asteroid.collides_with(shot):
                    asteroid.split()
                    shot.kill()
        
        for sprite in drawable:
            sprite.draw(screen)
            
        pygame.display.flip()
        
        # Control FPS and get delta time
        dt = clock.tick(60) / 1000
    
    pygame.quit()

if __name__ == "__main__":
    main()