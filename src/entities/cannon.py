class Cannon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0  # Angle of the cannon
        self.vx = 0
        self.width = 50
        self.height = 20
        self.speed = 5

    def move_left(self):
        self.angle -= 5  # Move the cannon left by 5 degrees

    def move_right(self):
        self.angle += 5  # Move the cannon right by 5 degrees

    def get_position(self):
        return self.x, self.y

    def get_angle(self):
        return self.angle
    

    def update(self):
        """
        Advance cannon position by current velocity, apply simple friction,
        and clamp to the current display width (falls back to 800).
        Called from main.py as cannon.update().
        """
        # get current display width if available
        try:
            import pygame
            surf = pygame.display.get_surface()
            bounds_width = surf.get_width() if surf else 800
        except Exception:
            bounds_width = 800

        # apply velocity
        self.x += self.vx

        # simple friction so the cannon slows when not being pressed
        self.vx *= 0.8
        if abs(self.vx) < 0.01:
            self.vx = 0

        # clamp to screen
        max_x = bounds_width - getattr(self, "width", 50)
        if self.x < 0:
            self.x = 0
            self.vx = 0
        elif self.x > max_x:
            self.x = max_x
            self.vx = 0