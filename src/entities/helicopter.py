# src/entities/helicopter.py
import pygame
import random

class Helicopter:
    def __init__(self, screen_width, body_color=(190, 190, 70), rotor_color=(30, 30, 30)):
        self.x = random.randint(0, screen_width - 60)
        self.y = 10
        self.speed = random.choice([-2, 2])  # left or right
        self.width = 60
        self.height = 30
        self.spawned_men = []
        self.spawn_cooldown = 0
        self.body_color = (random.randint(100, 255), random.randint(100, 255), 0)  # yellowish
        self.rotor_color = (random.randint(20, 50), random.randint(20, 50), random.randint(20, 50))  # dark

    def draw(self, surf):
        pygame.draw.ellipse(surf, self.body_color, (self.x, self.y + 6, self.width, 18))
        pygame.draw.rect(surf, self.rotor_color, (self.x + 10, self.y - 8, 40, 6))

    def move(self):
        self.x += self.speed
        # Bounce off screen edges
        if self.x < 0 or self.x > 800 - self.width:
            self.speed *= -1

    def draw(self, surf):
        # Body
        pygame.draw.ellipse(surf, (190, 190, 70), (self.x, self.y + 6, self.width, 18))  # Elliptical body

        # Cockpit (front bubble)
        pygame.draw.ellipse(surf, (120, 160, 240), (self.x + self.width - 16, self.y + 8, 14, 12))

        # Tail boom
        pygame.draw.rect(surf, (120, 120, 80), (self.x - 28, self.y + 12, 28, 6))
        # Tail fin vertical
        pygame.draw.polygon(surf, (120,160,240), [(self.x - 28, self.y + 12), (self.x - 16, self.y + 6), (self.x - 16, self.y + 18)])
        # Tail rotor
        pygame.draw.circle(surf, (30, 30, 30), (self.x - 30, int(self.y + 15)), 6, 2)
        pygame.draw.line(surf, (30,30,30), (self.x - 30, self.y + 15), (self.x - 30, self.y + 7), 2)
        pygame.draw.line(surf, (30,30,30), (self.x - 30, self.y + 15), (self.x - 36, self.y + 15), 2)
        pygame.draw.line(surf, (30,30,30), (self.x - 30, self.y + 15), (self.x - 30, self.y + 23), 2)
        pygame.draw.line(surf, (30,30,30), (self.x - 30, self.y + 15), (self.x - 24, self.y + 15), 2)

        # Main rotor
        pygame.draw.line(surf, (30, 30, 30), (self.x + self.width//2, self.y), (self.x + self.width//2 - 35, self.y - 12), 4)
        pygame.draw.line(surf, (30, 30, 30), (self.x + self.width//2, self.y), (self.x + self.width//2 + 35, self.y - 12), 4)
        pygame.draw.circle(surf, (30,30,30), (self.x + self.width//2, self.y), 6, 0)

    def drop_parachute(self):
        from entities.parachute import MilitaryMan
        if random.random() < 0.01:  # 1% chance per frame to drop
            man = MilitaryMan(self.x + self.width // 2, self.y + self.height)
            self.spawned_men.append(man)
            return man
        return None
    

    def maybe_drop(self):
        # Control drop rate (every 80+ frames)
        if self.spawn_cooldown > 0:
            self.spawn_cooldown -= 1
            return None
        if random.random() < 0.01:
            self.spawn_cooldown = 80
            return (self.x + self.width//2, self.y + self.height)
        return None