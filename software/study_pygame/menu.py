import choice_reaction_time
import config
import csv
import force_control
import index_calib_descending
import json
import numpy as np
import os
import plotly.graph_objects as go
import pygame
import sys
import UI
import wrist_calib_descending

class Menu:
    def __init__(self):
        pygame.display.set_caption("Start Menu - HapTID")
        self.screen = pygame.display.get_surface()
        self.screen_w = pygame.display.Info().current_w
        self.screen_h = pygame.display.Info().current_h
        self.font = pygame.font.SysFont(None, 48)
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    if wrist_calib_button.collidepoint(event.pos):
                        running = False
                        wrist_calib_descending.Calibration_descending().run()
                    if config.wrist_threshold is not None and index_calib_button.collidepoint(event.pos):
                        running = False
                        index_calib_descending.Calibration_descending().run()
                    if config.wrist_threshold is not None and config.finger_threshold is not None and exercices_button.collidepoint(event.pos):
                        running = False
                        # check what the next task is
                        if config.tasks[0][1] == 'CRT':
                            choice_reaction_time.CRT().run()
                        elif config.tasks[0][1] == 'FC':
                            force_control.FC().run()
            
            self.screen.fill('black')
            UI.draw_text(f'Participant #{config.id}', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/10)
            quit_button = UI.draw_button('Quit', self.font, UI.color_red, self.screen, 75, 50)
            wrist_calib_button = UI.draw_button('Start wrist calibration', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2-100)
            if config.wrist_threshold is not None:
                index_calib_button = UI.draw_button('Start index calibration', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2)
            if config.wrist_threshold is not None and config.finger_threshold is not None:
                exercices_button = UI.draw_button('Start exercices', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2)
                UI.draw_text('Calibration complete !', self.font, UI.color_green, self.screen, self.screen_w/2, self.screen_h/2+100)

            pygame.display.update()
            self.clock.tick(config.framerate)