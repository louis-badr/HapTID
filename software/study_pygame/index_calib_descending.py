from datetime import datetime

import config
import index_calib_ascending
import json
import menu
import numpy as np
import os
import pygame
import random
import serial
import sys
import UI


class Calibration_descending:
    def __init__(self):
        # arduino things
        self.ser_haptid = serial.Serial(config.com_port_haptid, 115200, timeout=.1)
        # dirty fix to make sure the arduino is ready to receive data
        self.ser_haptid.close()
        self.ser_haptid.open()    
        # initialize variables
        self.vib_lvl = config.index_max_vib_lvl
        self.step = config.index_descending_starting_step
        self.vib_lvl_history = []
        self.changing_points = []
        self.answers_history = []
        # pygame things
        pygame.display.set_caption("Index calibration - HapTID")
        self.screen = pygame.display.get_surface()
        self.screen_w = pygame.display.Info().current_w
        self.screen_h = pygame.display.Info().current_h
        self.font = pygame.font.SysFont(None, 48)
        self.clock = pygame.time.Clock()
        self.counter = 1
        self.noise_lvl = round(config.wrist_threshold * config.sr_coeff * 1000)
        print(f'Noise_lvl: {round(config.wrist_threshold * config.sr_coeff, 3)}%')
        self.ser_haptid.write(f'{self.noise_lvl}'.encode())
        config.index_calib_done_trials += 1

    def run(self):
        print(f'Starting the index #{config.index_calib_done_trials} descending calibration...')
        # ends when the maximum number of trials has been reached or when the value has stabilized
        while len(self.vib_lvl_history) < config.index_max_nb_trials and len(self.changing_points) < config.index_max_changing_points:
            # display the screen without the buttons yet
            self.screen.fill('black')
            menu_button = UI.draw_button('Menu', self.font, UI.color_text, self.screen, 75, 50)
            UI.draw_text('Avez-vous senti une vibration ?', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2)
            pygame.display.update()
            # wait a bit
            pygame.time.wait(random.randint(1000, 4000))
            print(self.answers_history)
            #! vibrate here during a random time
            if self.vib_lvl > 0:
                if config.dominant_hand == "R":
                    self.ser_haptid.write(f'{round(self.vib_lvl * 1000 + 400000)}'.encode())
                else:
                    self.ser_haptid.write(f'{round(self.vib_lvl * 1000 + 300000)}'.encode())
            print(f'Trial n°{self.counter}: {self.vib_lvl}%')
            self.counter += 1
            # wait a bit
            pygame.time.wait(random.randint(1000, 2500))
            #! stop all vibrations
            self.ser_haptid.write('0'.encode())
            #! reactivate the white noise if it is the second trial
            if config.index_calib_done_trials == 2:
                pygame.time.wait(50)
                self.ser_haptid.write(f'{self.noise_lvl}'.encode())
            pygame.time.wait(random.randint(500, 1000))
            # display the buttons
            self.screen.fill('black')
            menu_button = UI.draw_button('Menu', self.font, UI.color_text, self.screen, 75, 50)
            UI.draw_text('Avez-vous senti une vibration ?', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2)
            no_button = UI.draw_button('Non', self.font, UI.color_text, self.screen, self.screen_w/2-100, self.screen_h/2+100)
            yes_button = UI.draw_button('Oui', self.font, UI.color_text, self.screen, self.screen_w/2+100, self.screen_h/2+100)
            pygame.display.update()
            # wait for the participant's answer
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
                                self.step *= config.index_coeff
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
                                self.step *= config.index_coeff
                                if self.step < 0.001:
                                    self.step = 0.001
                                self.vib_lvl += self.step
                                self.vib_lvl = round(self.vib_lvl, 3)
                            if self.vib_lvl > config.index_max_vib_lvl:
                                self.vib_lvl = config.index_max_vib_lvl
                            running = False
        #! stop all vibrations
        self.ser_haptid.write('0'.encode())
        threshold_value = round(np.mean(self.changing_points[-3:]), 3)    # mean of the last 3 changing points
        config.index_trials_thresholds[config.index_calib_done_trials - 1] = threshold_value
        # save the calibration data
        data = {
            "Participant ID": config.id,
            "Date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Trial": config.index_calib_done_trials,
            "Descending index threshold value": threshold_value,
            "Descending vibration level history": self.vib_lvl_history,
            "Descending level changing points": self.changing_points,
            "Descending participant answers history": self.answers_history,
            "SR": "on" if config.index_calib_done_trials == 2 else "off",
            "SR coefficient": config.sr_coeff,
            "Wrist threshold": config.wrist_threshold
        }
        json_object = json.dumps(data, indent=4)
        file_path = f'./participants_data/P{config.id}/P{config.id}-index-calib.jsonl'
        with open(file_path, "a") as outfile:
            outfile.write(json_object + '\n')
        # go to the ascending calibration
        self.ser_haptid.close()
        index_calib_ascending.Calibration_ascending().run()