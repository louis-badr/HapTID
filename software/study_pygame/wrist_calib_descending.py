from datetime import datetime

import config
import json
import menu
import numpy as np
import os
import pygame
import random
import serial
import sys
import UI
import wrist_calib_ascending


class Calibration_descending:
    def __init__(self):
        # arduino things
        self.ser_haptid = serial.Serial(config.com_port_haptid, 115200, timeout=.1)
        # dirty fix to make sure the arduino is ready to receive data
        self.ser_haptid.close()
        self.ser_haptid.open()    
        # initialize variables
        self.vib_lvl = config.wrist_max_vib_lvl
        self.step = config.wrist_descending_starting_step
        self.vib_lvl_history = []
        self.changing_points = []
        self.answers_history = []
        # pygame things
        pygame.display.set_caption("Wrist calibration - HapTID")
        self.screen = pygame.display.get_surface()
        self.screen_w = pygame.display.Info().current_w
        self.screen_h = pygame.display.Info().current_h
        self.font = pygame.font.SysFont(None, 48)
        self.clock = pygame.time.Clock()
        self.counter = 1
    def run(self):
        print('Starting the wrist descending calibration...')
        # ends when the maximum number of trials has been reached or when the value has stabilized
        while len(self.vib_lvl_history) < config.wrist_max_nb_trials and len(self.changing_points) < config.wrist_max_changing_points:
            # display the screen without the buttons yet
            self.screen.fill('black')
            menu_button = UI.draw_button('Menu', self.font, UI.color_text, self.screen, 75, 50)
            UI.draw_text('Avez-vous senti une vibration ?', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2)
            pygame.display.update()
            # wait a bit
            pygame.time.wait(random.randint(1000, 4000))
            #! vibrate here during a random time
            print(self.answers_history)
            self.ser_haptid.write(f'{round(self.vib_lvl * 1000)}'.encode())
            print(f'Trial n°{self.counter} : {self.vib_lvl}%')
            self.counter += 1
            pygame.time.wait(random.randint(1000, 2500))
            #! stop vibrating
            self.ser_haptid.write('0'.encode())
            # wait a bit
            pygame.time.wait(random.randint(500, 1000))
            # display the buttons
            self.screen.fill('black')
            menu_button = UI.draw_button('Menu', self.font, UI.color_text, self.screen, 75, 50)
            UI.draw_text('Avez-vous senti une vibration ?', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2)
            no_button = UI.draw_button('Non', self.font, UI.color_text, self.screen, self.screen_w/2-100, self.screen_h/2+100)
            yes_button = UI.draw_button('Oui', self.font, UI.color_text, self.screen, self.screen_w/2+100, self.screen_h/2+100)
            pygame.display.update()
            # wait for the participant's to answer
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.ser_haptid.close()
                        pygame.quit()
                        sys.exit()
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        if menu_button.collidepoint(event.pos):
                            self.ser_haptid.close()
                            menu_screen = menu.Menu()
                            menu_screen.run()
                        if yes_button.collidepoint(event.pos):
                            if len(self.answers_history) == 0 or self.answers_history[-1] == 'y':
                                self.vib_lvl_history.append(self.vib_lvl)
                                self.answers_history.append('y')
                                self.vib_lvl -= self.step
                                self.vib_lvl = round(self.vib_lvl, 3)
                            elif self.answers_history[-1] == 'n':
                                self.vib_lvl_history.append(self.vib_lvl)
                                self.answers_history.append('y')
                                self.changing_points.append(self.vib_lvl)
                                self.step *= config.wrist_coeff
                                if self.step < 0.001:
                                    self.step = 0.001
                                self.vib_lvl -= self.step
                                self.vib_lvl = round(self.vib_lvl, 3)
                            if self.vib_lvl < 0:
                                self.vib_lvl = 0
                            running = False
                        if no_button.collidepoint(event.pos):
                            if len(self.answers_history) > 0 and self.answers_history[-1] == 'n':
                                self.vib_lvl_history.append(self.vib_lvl)
                                self.answers_history.append('n')
                                self.vib_lvl += self.step
                                self.vib_lvl = round(self.vib_lvl, 3)
                            elif self.answers_history[-1] == 'y':
                                self.vib_lvl_history.append(self.vib_lvl)
                                self.answers_history.append('n')
                                self.changing_points.append(self.vib_lvl)
                                self.step *= config.wrist_coeff
                                if self.step < 0.001:
                                    self.step = 0.001
                                self.vib_lvl += self.step
                                self.vib_lvl = round(self.vib_lvl, 3)
                            if self.vib_lvl > config.wrist_max_vib_lvl:
                                self.vib_lvl = config.wrist_max_vib_lvl
                            running = False
        threshold_value = round(np.mean(self.changing_points[-3:]), 3)    # mean of the last 3 changing points
        config.wrist_threshold = threshold_value
        # save the calibration data
        data = {
            "Participant ID": config.id,
            "Date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Descending wrist threshold value": threshold_value,
            "Descending vibration level history": self.vib_lvl_history,
            "Descending level changing points": self.changing_points,
            "Descending participant answers history": self.answers_history
        }
        json_object = json.dumps(data, indent=4)
        file_path = f'./participants_data/P{config.id}/P{config.id}-wrist-calib.jsonl'
        with open(file_path, "a") as outfile:
            outfile.write(json_object + '\n')
        # go to the ascending calibration
        self.ser_haptid.close()
        wrist_calib_ascending.Calibration_ascending().run()