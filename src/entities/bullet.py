import math
import pygame

class Bullet:
    def __init__(self, x, y, vx, vy, radius=4, color=(255,255,255)):
        self.x = float(x)
        self.y = float(y)
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def is_offscreen(self, width, height):
        return (
            self.x < -self.radius or
            self.x > width + self.radius or
            self.y < -self.radius or
            self.y > height + self.radius
        )

    def get_pos(self):
        return int(self.x), int(self.y)
    
    def get_rect(self):
        # Return a pygame.Rect around the bullet's position based on radius
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2
        )
