# game.py

import pygame
from entities.cannon import Cannon
from input import InputHandler
from render import Renderer

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Retro DOS Game")
        self.clock = pygame.time.Clock()
        self.cannon = Cannon(400, 500)  # Start cannon in the middle of the screen
        self.input_handler = InputHandler()
        self.renderer = Renderer(self.screen)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.input_handler.handle_input(self.cannon)
            self.renderer.render(self.cannon)
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()