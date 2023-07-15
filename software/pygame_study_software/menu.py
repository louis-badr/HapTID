import calibration
import csv
import choice_reaction_time
import force_control
import numpy as np
import os
import plotly.graph_objects as go
import pygame
import constants
import sys
import UI

class Menu:
    def __init__(self):
        pygame.display.set_caption("Start Menu - HapTID")
        self.screen = pygame.display.get_surface()
        self.screen_w = pygame.display.Info().current_w
        self.screen_h = pygame.display.Info().current_h
        self.font = pygame.font.SysFont(None, 48)
        self.clock = pygame.time.Clock()
        self.show_exercices_button = False
        if os.path.exists(f'./{constants.id}/{constants.id}-calibration.csv'):
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
                        calibration.Calibration().run()
                    if self.show_exercices_button:
                        if exercices_button.collidepoint(event.pos):
                            running = False
                            #force_control.FC().run()
                            with open('./running_order_table.csv') as csv_file:
                                csv_reader = csv.reader(csv_file, delimiter=';')
                                rows = list(csv_reader)
                                exercice = rows[int(constants.id[:2])][0].split(',')[1]
                                if exercice == 'CRT':
                                    choice_reaction_time.CRT().run()
                                elif exercice == 'FC':
                                    force_control.FC().run()
            
            self.screen.fill('black')
            UI.draw_text(f'Participant {constants.id}', self.font, 'white', self.screen, self.screen_w/2, self.screen_h/10)
            calib_button = UI.draw_button('Start calibration', self.font, 'white', self.screen, self.screen_w/2, self.screen_h/2-100)
            if self.show_exercices_button:
                exercices_button = UI.draw_button('Start exercices', self.font, 'white', self.screen, self.screen_w/2, self.screen_h/2)
                UI.draw_text('Calibration complete !', self.font, 'green', self.screen, self.screen_w/2, self.screen_h/2+100)

            pygame.display.update()
            self.clock.tick(constants.framerate)