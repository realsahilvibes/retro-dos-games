import pygame, math

class Renderer:
    def __init__(self, width=800, height=600, caption="Retro DOS Game"):
        # create and own the screen surface
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)

    def clear(self):
        # clear the screen (call before drawing)
        self.screen.fill((0, 0, 0))
    
    def draw_burst(surface, x, y):
    # Simple burst using a yellow circle
        pygame.draw.circle(surface, (255, 255, 0), (x, y), 18)


    def draw(self, cannon, bullets=None):
        # draw the cannon in white and render its barrel using angle
        white = (255, 255, 255)
        # base rectangle
        rect = pygame.Rect(int(cannon.x), int(cannon.y), cannon.width, cannon.height)
        pygame.draw.rect(self.screen, white, rect)

        # barrel: compute center and end point from angle (degrees)
        cx = cannon.x + cannon.width / 2
        cy = cannon.y + cannon.height / 2
        angle_deg = cannon.get_angle() if hasattr(cannon, "get_angle") else getattr(cannon, "angle", 0)
        angle_rad = math.radians(angle_deg)
        barrel_length = 40
        # subtract sin component because y increases downward in screen coords
        end_x = cx + barrel_length * math.cos(angle_rad)
        end_y = cy - barrel_length * math.sin(angle_rad)
        pygame.draw.line(self.screen, white, (int(cx), int(cy)), (int(end_x), int(end_y)), 4)

        # draw bullets (white circles)
        if bullets:
            for b in bullets:
                pygame.draw.circle(self.screen, b.color, b.get_pos(), b.radius)


def initialize_rendering(width=800, height=600):
    # return a Renderer instance; assume pygame.init() was called by the caller
    return Renderer(width, height)