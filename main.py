from shot import Shot
import pygame
from asteroid import Asteroid
from shockwave import Shockwave
from constants import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SCORE_BASE,
    FONT,
    SCORE_PER_LIFE,
    PLAYER_LIVES,
    PLAYER_INVULNERABILITY_DURATION,
)
from logger import log_state, log_event
from player import Player
from asteroidfield import AsteroidField


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)
    Shockwave.containers = (updatable, drawable)
    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    AsteroidField()
    score = 0
    last_life_score = 0
    is_game_over = False
    font_path = "fonts/" + FONT + ".ttf"
    try:
        font = pygame.font.Font(font_path, 24)
    except FileNotFoundError:
        print(f"Font file not found at {font_path}, using default font.")
        font = pygame.font.SysFont("monospace", 24, bold=True)

    loaded_background_img = pygame.image.load("assets/background.png").convert()

    def get_scaled_background(w, h):
        return pygame.transform.smoothscale(loaded_background_img, (w, h))

    curr_w, curr_h = screen.get_size()
    background_img = get_scaled_background(curr_w, curr_h)

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.VIDEORESIZE:
                curr_w, curr_h = event.w, event.h
                screen = pygame.display.set_mode((curr_w, curr_h), pygame.RESIZABLE)
                background_img = get_scaled_background(curr_w, curr_h)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and is_game_over:
                    score = 0
                    last_life_score = 0
                    player.lives = PLAYER_LIVES
                    player.position = pygame.Vector2(curr_w / 2, curr_h / 2)
                    player.rotation = 0
                    player.velocity = pygame.Vector2(0, 0)
                    player.invulnerability_timer = PLAYER_INVULNERABILITY_DURATION
                    for asteroid in asteroids:
                        asteroid.kill()
                    for shot in shots:
                        shot.kill()
                    is_game_over = False

        if not is_game_over:
            updatable.update(dt)
        if not is_game_over:
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    if not player.is_invulnerable():
                        log_event("player_hit")
                        Shockwave(
                            asteroid.position.x, asteroid.position.y, asteroid.radius
                        )
                        asteroid.kill()
                        player.respawn()
                        if player.lives <= 0:
                            is_game_over = True
            for asteroid in asteroids:
                for shot in shots:
                    if shot.collides_with(asteroid):
                        log_event("asteroid_shot")
                        shot.kill()
                        score += SCORE_BASE // asteroid.radius
                        asteroid.split()
                        while score - last_life_score >= SCORE_PER_LIFE:
                            player.lives += 1
                            last_life_score += SCORE_PER_LIFE
        screen.blit(background_img, (0, 0))
        for obj in drawable:
            obj.draw(screen)

        score_text = font.render(f"Score: {score}", True, "yellow")
        screen.blit(score_text, (20, 20))

        lives_text = font.render(f"Lives: {player.lives}", True, "red")
        screen.blit(lives_text, (curr_w - 250, 20))

        if is_game_over:
            game_over_text = font.render("GAME OVER", True, "white")
            restart_text = font.render("Press R to Restart", True, "white")

            go_rect = game_over_text.get_rect(center=(curr_w / 2, curr_h / 2 - 20))
            re_rect = restart_text.get_rect(center=(curr_w / 2, curr_h / 2 + 40))

            screen.blit(game_over_text, go_rect)
            screen.blit(restart_text, re_rect)

        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
