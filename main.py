import pygame
import random
from constants import *
from circleshape import CircleShape
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from powerup import PowerUp
from bomb import Bomb
from explosion import Explosion

def draw_start_screen(screen, font):
    # Create container surface
    container = pygame.Surface((600, 500))
    container.fill((0, 0, 0))
    container.set_alpha(128)  # Semi-transparent
    container_rect = container.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(container, container_rect)
    
    title_font = pygame.font.Font(None, 74)
    title = title_font.render("Space Havoc", True, (255, 255, 255))
    title_rect = title.get_rect(center=(SCREEN_WIDTH/2, container_rect.top + 50))
    
    instructions = [
        "Select Difficulty:",
        "1 - EASY",
        "2 - MEDIUM",
        "3 - HARD",
        "",
        "Arrow Keys or WASD to move",
        "SPACE to shoot",
        "B to drop bombs",
        "Press 1, 2, or 3 to start"
    ]
    
    for i, line in enumerate(instructions):
        text = font.render(line, True, (255, 255, 255))
        rect = text.get_rect(center=(SCREEN_WIDTH/2, container_rect.top + 120 + i * 40))
        screen.blit(text, rect)
    
    screen.blit(title, title_rect)

def draw_game_over_screen(screen, font, final_score):
    container = pygame.Surface((600, 400))
    container.fill((0, 0, 0))
    container.set_alpha(128)
    container_rect = container.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    screen.blit(container, container_rect)
    
    title_font = pygame.font.Font(None, 74)
    title = title_font.render("FATALITY!!!", True, (255, 255, 255))
    title_rect = title.get_rect(center=(SCREEN_WIDTH/2, container_rect.top + 50))
    
    score_text = font.render(f"Final Score: {final_score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH/2, container_rect.top + 150))
    
    replay_text = font.render("Press SPACE to play again or ESC to quit", True, (255, 255, 255))
    replay_rect = replay_text.get_rect(center=(SCREEN_WIDTH/2, container_rect.top + 250))
    
    screen.blit(title, title_rect) 
    screen.blit(score_text, score_rect)
    screen.blit(replay_text, replay_rect)

def main():
    print("Starting Space Havoc!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 36)
    
    # Load and scale background
    background = pygame.image.load("images/space.jpg")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    pygame.display.set_caption("Space Havoc")
    
    while True:  # Main game loop
        # Start screen and difficulty selection
        difficulty = None
        while difficulty is None:
            screen.blit(background, (0, 0))
            draw_start_screen(screen, font)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_KP1]:
                        difficulty = DIFFICULTY_EASY
                    elif event.key in [pygame.K_2, pygame.K_KP2]:
                        difficulty = DIFFICULTY_MEDIUM
                    elif event.key in [pygame.K_3, pygame.K_KP3]:
                        difficulty = DIFFICULTY_HARD
        
        clock = pygame.time.Clock()
        dt = 0
        score = 0
        
        updatable = pygame.sprite.Group()
        drawable = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        shots = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        bombs = pygame.sprite.Group()
        
        Player.containers = (updatable, drawable)
        Asteroid.containers = (asteroids, updatable, drawable)
        AsteroidField.containers = (updatable,)
        Shot.containers = (shots, updatable, drawable)
        PowerUp.containers = (powerups, updatable, drawable)
        Bomb.containers = (bombs, updatable, drawable)
        Explosion.containers = (updatable, drawable)
        
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        asteroid_field = AsteroidField(difficulty)
        
        powerup_timer = 0
        POWERUP_SPAWN_RATE = 15.0
        
        def draw_hud(screen, score, lives):
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
            lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
            screen.blit(lives_text, (10, 50))
            difficulty_text = font.render(f"Difficulty: {difficulty['NAME']}", True, (255, 255, 255))
            screen.blit(difficulty_text, (10, 90))
        
        game_running = True
        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            screen.blit(background, (0, 0))
            
            powerup_timer += dt
            if powerup_timer >= POWERUP_SPAWN_RATE:
                powerup_timer = 0
                type = random.choice(["shield", "speed"])
                PowerUp(random.randint(0, SCREEN_WIDTH), 
                       random.randint(0, SCREEN_HEIGHT), type)
            
            for sprite in updatable:
                sprite.update(dt)
                
            for powerup in powerups:
                if player.collides_with(powerup):
                    player.activate_power_up(powerup.type)
                    powerup.kill()
                
            for asteroid in asteroids:
                if player.collides_with(asteroid) and not player.invulnerable:
                    player.lives -= 1
                    if player.lives <= 0:
                        waiting = True
                        while waiting:
                            screen.blit(background, (0, 0))
                            draw_game_over_screen(screen, font, score)
                            pygame.display.flip()
                            
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    return
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_SPACE:
                                        game_running = False
                                        waiting = False
                                    elif event.key == pygame.K_ESCAPE:
                                        return
                    player.respawn()
                    
                for shot in shots:
                    if asteroid.collides_with(shot):
                        if asteroid.radius == ASTEROID_MAX_RADIUS:
                            score += SCORE_LARGE_ASTEROID
                        elif asteroid.radius == ASTEROID_MAX_RADIUS - ASTEROID_MIN_RADIUS:
                            score += SCORE_MEDIUM_ASTEROID
                        else:
                            score += SCORE_SMALL_ASTEROID
                        asteroid.split()
                        shot.kill()
            
            for sprite in drawable:
                sprite.draw(screen)
                
            draw_hud(screen, score, player.lives)
            
            pygame.display.flip()
            
            dt = clock.tick(60) / 1000
    
    pygame.quit()

if __name__ == "__main__":
    main()