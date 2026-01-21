import pygame
from constants import SHOCKWAVE_GROWTH_SPEED, SHOCKWAVE_DURATION, LINE_WIDTH


class Shockwave(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.position = pygame.Vector2(x, y)
        self.radius = radius
        self.timer = SHOCKWAVE_DURATION

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.kill()
            return
        self.radius += SHOCKWAVE_GROWTH_SPEED * dt

    def draw(self, screen):
        pygame.draw.circle(screen, "yellow", self.position, self.radius, LINE_WIDTH)
