from constants import PLAYER_SHOOT_COOLDOWN_SECONDS
from constants import PLAYER_SHOOT_SPEED
import pygame
from constants import (
    SHOT_RADIUS,
    PLAYER_SPEED,
    PLAYER_RADIUS,
    LINE_WIDTH,
    PLAYER_TURN_SPEED,
    PLAYER_INVULNERABILITY_DURATION,
    PLAYER_LIVES,
)
from shot import Shot
from circleshape import CircleShape


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown_timer = 0
        self.invulnerability_timer = 0
        self.lives = PLAYER_LIVES

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        color = "white"
        if self.invulnerability_timer > 0:
            color = "red"
        pygame.draw.polygon(screen, color, self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        self.shot_cooldown_timer -= dt
        if self.invulnerability_timer > 0:
            self.invulnerability_timer -= dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
        w, h = pygame.display.get_surface().get_size()
        self.position.x %= w
        self.position.y %= h

    def shoot(self):
        if self.shot_cooldown_timer > 0:
            return
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.shot_cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS

    def respawn(self):
        self.lives -= 1
        self.invulnerability_timer = PLAYER_INVULNERABILITY_DURATION

    def is_invulnerable(self):
        return self.invulnerability_timer > 0
