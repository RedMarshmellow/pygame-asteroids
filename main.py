from shot import Shot
import pygame
import sys
from asteroid import Asteroid
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, SCORE_BASE, FONT
from logger import log_state, log_event
from player import Player
from asteroidfield import AsteroidField


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)
    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    AsteroidField()
    score = 0
    font_path = "fonts/" + FONT + ".ttf"
    try:
        font = pygame.font.Font(font_path, 24)
    except FileNotFoundError:
        print(f"Font file not found at {font_path}, using default font.")
        font = pygame.font.SysFont("monospace", 24, bold=True)

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
        for asteroid in asteroids:
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    score += SCORE_BASE // asteroid.radius
                    asteroid.split()
        screen.fill("black")
        for obj in drawable:
            obj.draw(screen)

        score_text = font.render(f"Score: {score}", True, "yellow")
        screen.blit(score_text, (20, 20))

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
