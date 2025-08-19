# src/entities/parachute.py
import pygame, random

class MilitaryMan:
    
    def __init__(self, x, y, man_color=(0, 120, 0), rope_color=(120, 120, 120)):
        self.x = x
        self.y = y
        self.speed = 2
        self.size = 16
        self.alive = True
        self.man_color = man_color
        self.rope_color = rope_color

    def draw(self, surf):
        pygame.draw.ellipse(surf, (255, 255, 255), (self.x-12, self.y-16, 24, 12))  # parachute white
        pygame.draw.line(surf, self.rope_color, (self.x-8, self.y-10), (self.x, self.y), 2)
        pygame.draw.line(surf, self.rope_color, (self.x+8, self.y-10), (self.x, self.y), 2)
        pygame.draw.circle(surf, self.man_color, (self.x, self.y), 6)
        pygame.draw.rect(surf, (max(self.man_color[0]-20,0), max(self.man_color[1]-50,0), 0), (self.x-4, self.y, 8, 10))

   
    def move(self):
        self.y += self.speed

    def draw(self, surface):
        # Draw parachute
        pygame.draw.ellipse(surface, (255,255,255), (self.x-12, self.y-16, 24, 12))
        # Draw man
        pygame.draw.circle(surface, (0, 255, 0), (self.x, self.y), self.size//4)
        pygame.draw.rect(surface, (0, 100, 0), (self.x-4, self.y, 8, 12))
