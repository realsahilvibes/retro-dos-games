import math

class Bullet:
    def __init__(self, x, y, angle_deg, speed=10, radius=4, color=(255,255,255)):
        self.x = float(x)
        self.y = float(y)
        self.angle = angle_deg
        angle_rad = math.radians(angle_deg)
        self.vx = math.cos(angle_rad) * speed
        self.vy = -math.sin(angle_rad) * speed  # screen y grows downward
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