import pygame
import math

class Cannon:
    def __init__(self, x, y):
        self.x = x      # Base center x
        self.y = y      # Base top y (ground level)
        self.angle = 90  # Angle in degrees (90 vertical)
        self.length = 80  # Length of barrel lines
        self.width = 4   # Thickness (distance between two lines)

    def move_left(self):
        self.angle = min(self.angle + 5, 270)

    def move_right(self):
        self.angle = max(self.angle - 5, 0)

    def get_position(self):
        return self.x, self.y

    def get_angle(self):
        return self.angle

    def draw(self, surf):
        # Draw base as rectangle
        base_rect = pygame.Rect(self.x - 40, self.y, 80, 30)
        pygame.draw.rect(surf, (100, 100, 100), base_rect)

        # Calculate rotated end points for the two lines forming barrel
        angle_rad = math.radians(90 - self.angle)  # rotation to match visual

        # Calculate the offset vector for the lines (perpendicular to barrel)
        perp_x = math.cos(angle_rad + math.pi / 2) * (self.width / 2)
        perp_y = math.sin(angle_rad + math.pi / 2) * (self.width / 2)

        # Calculate the barrel tip point
        tip_x = self.x + math.cos(angle_rad) * self.length
        tip_y = self.y + math.sin(angle_rad) * self.length

        # Left line start and end points
        start1 = (self.x + perp_x, self.y + perp_y)
        end1 = (tip_x + perp_x, tip_y + perp_y)

        # Right line start and end points
        start2 = (self.x - perp_x, self.y - perp_y)
        end2 = (tip_x - perp_x, tip_y - perp_y)

        # Draw the two lines as barrel
        pygame.draw.line(surf, (80, 80, 80), start1, end1, 4)
        pygame.draw.line(surf, (80, 80, 80), start2, end2, 4)

        # Debug: draw a small circle at barrel center (midpoint of the barrel)
        mid_x = self.x + math.cos(angle_rad) * (self.length / 2)
        mid_y = self.y + math.sin(angle_rad) * (self.length / 2)
        pygame.draw.circle(surf, (255, 0, 0), (int(mid_x), int(mid_y)), 5)

    def get_barrel_center(self):
        # Center point along barrel axis (for bullet origin)
        angle_rad = math.radians(90 - self.angle)
        center_x = self.x + math.cos(angle_rad) * (self.length / 2)
        center_y = self.y + math.sin(angle_rad) * (self.length / 2)
        return center_x, center_y

    def get_bullet_velocity(self, speed):
        angle_rad = math.radians(90 - self.angle)
        vx = math.cos(angle_rad) * speed
        vy = math.sin(angle_rad) * speed
        return vx, vy
