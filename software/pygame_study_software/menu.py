import calibration
import numpy as np
import os
import plotly.graph_objects as go
import pygame
import settings
import sys
import UI

class Menu:
    def __init__(self, id):
        pygame.display.set_caption("Start Menu - HapTID")
        self.screen = pygame.display.get_surface()
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
        self.font = pygame.font.SysFont(None, 48)
        self.clock = pygame.time.Clock()
        self.id = id
        self.show_exercices_button = False
        if os.path.exists(f'./{self.id}/{self.id}-calibration.csv'):
            self.show_exercices_button = True

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if calib_button.collidepoint(event.pos):
                        running = False
                        calibration.Calibration(id=self.id).run()
                    if self.show_exercices_button:
                        if exercices_button.collidepoint(event.pos):
                            print('exercices')
                            # follow the order in the CSV file
            
            self.screen.fill('black')
            UI.draw_text(f'Participant {self.id}', self.font, 'white', self.screen, self.screen_width/2, self.screen_height/10)
            calib_button = UI.draw_button('Start calibration', self.font, 'white', self.screen, self.screen_width/2, self.screen_height/2)
            if self.show_exercices_button:
                exercices_button = UI.draw_button('Start exercices', self.font, 'white', self.screen, self.screen_width/2, self.screen_height/2+100)   
                UI.draw_text('Calibration complete !', self.font, 'green', self.screen, self.screen_width/2, self.screen_height/2+200)

            pygame.display.update()

