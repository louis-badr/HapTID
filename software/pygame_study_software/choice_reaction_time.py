import pygame


class CRT:
    def __init__(self):
        pygame.display.set_caption("Choice Reaction Time - HapTID")
        self.screen = pygame.display.get_surface()
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
        self.font = pygame.font.SysFont(None, 48)
        self.clock = pygame.time.Clock()
    def run(self):
        running = True
        while running:
            self.screen.fill('black')
            pygame.display.update()