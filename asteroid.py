import random
from logger import log_event
from constants import ASTEROID_MIN_RADIUS
from constants import LINE_WIDTH
import pygame
from circleshape import CircleShape
from shockwave import Shockwave


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt
        w, h = pygame.display.get_surface().get_size()
        self.position.x %= w
        self.position.y %= h

    def split(self):
        Shockwave(self.position.x, self.position.y, self.radius)
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        vec1 = self.velocity.rotate(angle)
        vec2 = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = vec1 * 1.2
        asteroid2.velocity = vec2 * 1.2
