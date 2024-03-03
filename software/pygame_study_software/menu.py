import calibration_descending
import csv
import choice_reaction_time
import force_control
import json
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
        jsonl_file = f'./P{constants.id}/P{constants.id}-calibration.jsonl'
        if os.path.exists(jsonl_file):
            # data = json.load(open(jsonl_file))
            # with open(jsonl_file, 'r') as file:
            #     for line in file:
            #         line = line.strip()  # Remove leading/trailing whitespace
            #         if line:
            #             try:
            #                 data = json.loads(line)
            #                 if "Wrist threshold value" in data:
            #                     constants.wrist_threshold = int(data["Wrist threshold value"])
            #             except json.JSONDecodeError:
            #                 # Skip lines that don't contain valid JSON
            #                 continue
            self.show_exercices_button = True

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
                    if calib_button.collidepoint(event.pos):
                        running = False
                        calibration_descending.Calibration_descending().run()
                    if self.show_exercices_button:
                        if exercices_button.collidepoint(event.pos):
                            running = False
                            # check what the next task is
                            if constants.tasks[0][1] == 'CRT':
                                choice_reaction_time.CRT().run()
                            elif constants.tasks[0][1] == 'FC':
                                force_control.FC().run()
            
            self.screen.fill('black')
            UI.draw_text(f'Participant #{constants.id}', self.font, 'white', self.screen, self.screen_w/2, self.screen_h/10)
            quit_button = UI.draw_button('Quit', self.font, 'red', self.screen, 75, 50)
            calib_button = UI.draw_button('Start calibration', self.font, 'white', self.screen, self.screen_w/2, self.screen_h/2-100)
            if self.show_exercices_button:
                exercices_button = UI.draw_button('Start exercices', self.font, 'white', self.screen, self.screen_w/2, self.screen_h/2)
                UI.draw_text('Calibration complete !', self.font, 'green', self.screen, self.screen_w/2, self.screen_h/2+100)

            pygame.display.update()
            self.clock.tick(constants.framerate)