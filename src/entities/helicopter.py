# src/entities/helicopter.py
import pygame
import random, os

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
        # Load all frames
        self.frames = []
        frame_count = 0
        while os.path.exists(f"assets/heli_frames/frame_{frame_count}.png"):
            frame = pygame.image.load(f"assets/heli_frames/frame_{frame_count}.png")
            self.frames.append(frame)
            frame_count += 1
        
        self.current_frame = 0
        self.frame_counter = 0
        self.frame_delay = 5  # Adjust animation speed


    def draw(self, surf):
        if self.frames:
            surf.blit(self.frames[self.current_frame], (self.x, self.y))
            
            # Animate
            self.frame_counter += 1
            if self.frame_counter >= self.frame_delay:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.frame_counter = 0

    def move(self):
        self.x += self.speed
        # Bounce off screen edges
        if self.x < 0 or self.x > 800 - self.width:
            self.speed *= -1

    

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