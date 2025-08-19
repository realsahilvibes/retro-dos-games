# ...existing code...
class InputHandler:
    def __init__(self, cannon):
        self.cannon = cannon
        self.shoot_sound = None
        # Try to initialize mixer and load a shot sound. Fallback to synth via numpy if no file.
        try:
            import pygame, os
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            here = os.path.dirname(__file__)
            asset_path = os.path.normpath(os.path.join(here, "..", "assets", "shoot.wav"))
            if os.path.exists(asset_path):
                self.shoot_sound = pygame.mixer.Sound(asset_path)
            else:
                # synth a short beep if numpy is available
                try:
                    import numpy as np
                    sr = 44100
                    duration = 0.12
                    freq = 880.0
                    t = np.linspace(0, duration, int(sr * duration), False)
                    wave = 0.5 * np.sin(2 * np.pi * freq * t)
                    audio = np.int16(wave * 32767)
                    self.shoot_sound = pygame.sndarray.make_sound(audio)
                except Exception:
                    self.shoot_sound = None
        except Exception:
            self.shoot_sound = None

    def handle_input(self, events):
        """
        Process events. Returns a list of newly created Bullet instances (may be empty).
        """
        import pygame, math
        from pygame.locals import KEYDOWN, K_LEFT, K_RIGHT, K_SPACE
        from entities.bullet import Bullet

        new_bullets = []

        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.cannon.move_left()
                elif event.key == K_RIGHT:
                    self.cannon.move_right()
                elif event.key == K_SPACE:
                    # compute barrel end as bullet spawn point (match renderer)
                    cx = self.cannon.x + self.cannon.width / 2
                    cy = self.cannon.y + self.cannon.height / 2
                    angle_deg = self.cannon.get_angle() if hasattr(self.cannon, "get_angle") else getattr(self.cannon, "angle", 0)
                    barrel_length = 40
                    start_x = cx + barrel_length * math.cos(math.radians(angle_deg))
                    start_y = cy - barrel_length * math.sin(math.radians(angle_deg))
                    new_bullets.append(Bullet(start_x, start_y, angle_deg))
                    # play shot sound if available
                    try:
                        if self.shoot_sound:
                            self.shoot_sound.play()
                    except Exception:
                        pass

        return new_bullets
# ...existing code...