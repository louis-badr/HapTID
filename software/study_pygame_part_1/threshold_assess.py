from datetime import datetime

import config
import json
import numpy
import os
import pygame
import random
import serial
import sys
import UI


class Threshold_assess:
    def __init__(self, stim_type, max_vib_lvl, max_nb_trials, max_chg_points, desc_start_step, staircase_coeff):
        # arduino things
        self.ser_haptid = serial.Serial(config.com_port_haptid, 115200, timeout=.1)
        # dirty fix to make sure the arduino is ready to receive data
        self.ser_haptid.close()
        self.ser_haptid.open()    

        # pygame things
        pygame.display.set_caption("Threshold assessment - HapTID")
        self.screen = pygame.display.get_surface()
        self.screen_w = pygame.display.Info().current_w
        self.screen_h = pygame.display.Info().current_h
        self.font = pygame.font.SysFont(None, 48)
        self.clock = pygame.time.Clock()
        self.file_path = f'./participants_data/P{config.id}/P{config.id}-data.jsonl'

        # initializations
        self.desc_vib_lvl_history = []
        self.asc_vib_lvl_history = []
        self.desc_changing_points = []
        self.asc_changing_points = []
        self.desc_answers_history = []
        self.asc_answers_history = []
        self.desc_counter = 1
        self.asc_counter = 1

        self.stim_type = stim_type
        self.max_vib_lvl = max_vib_lvl
        self.desc_vib_lvl = max_vib_lvl
        self.asc_vib_lvl = 0
        self.max_nb_trials = max_nb_trials
        self.max_chg_points = max_chg_points
        self.desc_step = desc_start_step
        self.asc_step = None
        self.staircase_coeff = staircase_coeff

        self.desc_threshold = None
        self.asc_threshold = None
        self.noise_lvl = round(config.wrist_threshold * config.sr_coeff * 1000)
        print(f'Noise_lvl: {round(config.wrist_threshold * config.sr_coeff, 3)}%')
        self.ser_haptid.write(f'{self.noise_lvl}'.encode())

    def run(self):
        # waiting screen
        self.screen.fill('black')
        UI.draw_text('Cliquez n\'importe où pour commencer', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2)
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    running = False
        print('Starting the descending assessment...')
        # ends when the maximum number of trials has been reached or when the value has stabilized
        while len(self.desc_vib_lvl_history) < self.max_nb_trials and len(self.desc_changing_points) < self.max_chg_points:
            # display the screen without the buttons yet
            self.screen.fill('black')
            UI.draw_text('Avez-vous senti une stimulation à votre poignet ?' if config.current_assess == 0 else 'Avez-vous senti une stimulation à votre index ?', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2)
            pygame.display.update()
            # wait a bit
            pygame.time.wait(random.randint(1000, 4000))
            #! vibrate here during a random time
            print(self.desc_answers_history)
            val_to_send = round(self.desc_vib_lvl * 1000)
            if config.current_assess > 0 and self.desc_vib_lvl > 0:
                if self.stim_type == '80':
                    if config.dominant_hand == "R":
                        val_to_send += 200000
                    else:
                        val_to_send += 100000
                elif self.stim_type == '250':
                    if config.dominant_hand == "R":
                        val_to_send += 400000
                    else:
                        val_to_send += 300000
                elif self.stim_type == 'click':
                    if config.dominant_hand == "R":
                        val_to_send  += 400000
                    else:
                        val_to_send += 200000
                    val_to_send *= -1 
            self.ser_haptid.write(f'{val_to_send}'.encode())
            print(f'Trial n°{self.desc_counter} : {self.desc_vib_lvl}%')
            self.desc_counter += 1
            pygame.time.wait(random.randint(1000, 2500))
            #! stop all vibrations
            self.ser_haptid.write('0'.encode())
            #! reactive the white noise if needed
            if config.current_assess > 4 and config.current_assess < 8:
                pygame.time.wait(50)
                self.ser_haptid.write(f'{self.noise_lvl}'.encode())
            # wait a bit
            pygame.time.wait(random.randint(500, 1000))
            # display the buttons
            self.screen.fill('black')
            UI.draw_text('Avez-vous senti une stimulation à votre poignet ?' if config.current_assess == 0 else 'Avez-vous senti une stimulation à votre index ?', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2)
            no_button = UI.draw_button('Non', self.font, UI.color_text, self.screen, self.screen_w/2-100, self.screen_h/2+100)
            yes_button = UI.draw_button('Oui', self.font, UI.color_text, self.screen, self.screen_w/2+100, self.screen_h/2+100)
            pygame.display.update()
            # wait for the participant to answer
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if yes_button.collidepoint(event.pos):
                            if len(self.desc_answers_history) == 0 or self.desc_answers_history[-1] == 'y':
                                self.desc_vib_lvl_history.append(self.desc_vib_lvl)
                                self.desc_answers_history.append('y')
                                self.desc_vib_lvl -= self.desc_step
                                self.desc_vib_lvl = round(self.desc_vib_lvl, 3)
                            elif self.desc_answers_history[-1] == 'n':
                                self.desc_vib_lvl_history.append(self.desc_vib_lvl)
                                self.desc_answers_history.append('y')
                                self.desc_changing_points.append(self.desc_vib_lvl)
                                self.desc_step *= self.staircase_coeff
                                if self.desc_step < 0.001:
                                    self.desc_step = 0.001
                                self.desc_vib_lvl -= self.desc_step
                                self.desc_vib_lvl = round(self.desc_vib_lvl, 3)
                            if self.desc_vib_lvl < 0:
                                self.desc_vib_lvl = 0
                            running = False
                        if no_button.collidepoint(event.pos):
                            if len(self.desc_answers_history) > 0 and self.desc_answers_history[-1] == 'n':
                                self.desc_vib_lvl_history.append(self.desc_vib_lvl)
                                self.desc_answers_history.append('n')
                                self.desc_vib_lvl += self.desc_step
                                self.desc_vib_lvl = round(self.desc_vib_lvl, 3)
                            elif self.desc_answers_history[-1] == 'y':
                                self.desc_vib_lvl_history.append(self.desc_vib_lvl)
                                self.desc_answers_history.append('n')
                                self.desc_changing_points.append(self.desc_vib_lvl)
                                self.desc_step *= self.staircase_coeff
                                if self.desc_step < 0.001:
                                    self.desc_step = 0.001
                                self.desc_vib_lvl += self.desc_step
                                self.desc_vib_lvl = round(self.desc_vib_lvl, 3)
                            if self.desc_vib_lvl > self.max_vib_lvl:
                                self.desc_vib_lvl = self.max_vib_lvl
                            running = False
        print('Descending assessment done.')
        # save the results
        self.desc_threshold = round(numpy.mean(self.desc_changing_points[-3:]), 3)
        data = {
            "Participant": config.id,
            "Dominant hand": config.dominant_hand,
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Assessment type": self.stim_type,
            "Location": "wrist" if config.current_assess == 0 else "index",
            "SR": "on" if config.current_assess > 4 and config.current_assess < 8 else "off",
            "Descending threshold": self.desc_threshold,
            "Descending stim level history": self.desc_vib_lvl_history,
            "Descending level changing points": self.desc_changing_points,
            "Descending participant answers history": self.desc_answers_history
        }
        json_object = json.dumps(data, indent=4)
        with open(self.file_path, 'a') as file:
            file.write(json_object + '\n')
        print('Starting the ascending assessment...')
        self.asc_step = self.desc_threshold / 5
        # ends when the maximum number of trials has been reached or when the value has stabilized
        while len(self.asc_vib_lvl_history) < self.max_nb_trials and len(self.asc_changing_points) < self.max_chg_points:
            # display the screen without the buttons yet
            self.screen.fill('black')
            UI.draw_text('Avez-vous senti une stimulation à votre poignet ?' if config.current_assess == 0 else 'Avez-vous senti une stimulation à votre index ?', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2)
            pygame.display.update()
            # wait a bit
            pygame.time.wait(random.randint(1000, 4000))
            #! vibrate here during a random time
            print(self.asc_answers_history)
            val_to_send = round(self.desc_vib_lvl * 1000)
            if config.current_assess > 1 and self.desc_vib_lvl > 0:
                if self.stim_type == '80':
                    if config.dominant_hand == "R":
                        val_to_send += 200000
                    else:
                        val_to_send += 100000
                elif self.stim_type == '250':
                    if config.dominant_hand == "R":
                        val_to_send += 400000
                    else:
                        val_to_send += 300000
                elif self.stim_type == 'click':
                    if config.dominant_hand == "R":
                        val_to_send  += 400000
                    else:
                        val_to_send += 200000
                    val_to_send *= -1 
            self.ser_haptid.write(f'{val_to_send}'.encode())
            print(f'Trial n°{self.asc_counter} : {self.asc_vib_lvl}%')
            self.asc_counter += 1
            pygame.time.wait(random.randint(1000, 2500))
            #! stop vibrating
            self.ser_haptid.write('0'.encode())
            # wait a bit
            pygame.time.wait(random.randint(500, 1000))
            # display the buttons
            self.screen.fill('black')
            UI.draw_text('Avez-vous senti une stimulation à votre poignet ?' if config.current_assess == 0 else 'Avez-vous senti une stimulation à votre index ?', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2)
            no_button = UI.draw_button('Non', self.font, UI.color_text, self.screen, self.screen_w/2-100, self.screen_h/2+100)
            yes_button = UI.draw_button('Oui', self.font, UI.color_text, self.screen, self.screen_w/2+100, self.screen_h/2+100)
            pygame.display.update()
            # wait for the participant to answer
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if yes_button.collidepoint(event.pos):
                            if len(self.asc_answers_history) > 0:
                                if self.asc_answers_history[-1] == 'y':
                                    self.asc_vib_lvl_history.append(self.asc_vib_lvl)
                                    self.asc_answers_history.append('y')
                                    self.asc_vib_lvl -= self.asc_step
                                    self.asc_vib_lvl = round(self.asc_vib_lvl, 3)
                                elif self.asc_answers_history[-1] == 'n':
                                    self.asc_vib_lvl_history.append(self.asc_vib_lvl)
                                    self.asc_answers_history.append('y')
                                    self.asc_changing_points.append(self.asc_vib_lvl)
                                    self.asc_step *= self.staircase_coeff
                                    if self.asc_step < 0.001:
                                        self.asc_step = 0.001
                                    self.asc_vib_lvl -= self.asc_step
                                    self.asc_vib_lvl = round(self.asc_vib_lvl, 3)
                            if self.asc_vib_lvl < 0:
                                self.asc_vib_lvl = 0
                            running = False
                        if no_button.collidepoint(event.pos):
                            if len(self.asc_answers_history) == 0 or self.asc_answers_history[-1] == 'n':
                                self.asc_vib_lvl_history.append(self.asc_vib_lvl)
                                self.asc_answers_history.append('n')
                                self.asc_vib_lvl += self.asc_step
                                self.asc_vib_lvl = round(self.asc_vib_lvl, 3)
                            elif self.asc_answers_history[-1] == 'y':
                                self.asc_vib_lvl_history.append(self.asc_vib_lvl)
                                self.asc_answers_history.append('n')
                                self.asc_changing_points.append(self.asc_vib_lvl)
                                self.asc_step *= self.staircase_coeff
                                if self.asc_step < 0.001:
                                    self.asc_step = 0.001
                                self.asc_vib_lvl += self.asc_step
                                self.asc_vib_lvl = round(self.asc_vib_lvl, 3)
                            if self.asc_vib_lvl > self.max_vib_lvl:
                                self.asc_vib_lvl = self.max_vib_lvl
                            running = False
        print('Ascending assessment done.')
        # save the results
        self.asc_threshold = round(numpy.mean(self.asc_changing_points[-3:]), 3)
        data = {
            "Participant": config.id,
            "Dominant hand": config.dominant_hand,
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Assessment type": self.stim_type,
            "Location": "wrist" if config.current_assess == 0 else "index",
            "SR": "on" if config.current_assess > 4 and config.current_assess < 8 else "off",
            "Ascending threshold": self.asc_threshold,
            "Ascending stim level history": self.asc_vib_lvl_history,
            "Ascending level changing points": self.asc_changing_points,
            "Ascending participant answers history": self.asc_answers_history
        }
        json_object = json.dumps(data, indent=4)
        with open(self.file_path, 'a') as file:
            file.write(json_object + '\n')
        # save the final threshold
        final_threshold = round((self.desc_threshold + self.asc_threshold) / 2, 3)
        data = {
            "Participant": config.id,
            "Dominant hand": config.dominant_hand,
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Assessment type": self.stim_type,
            "Location": "wrist" if config.current_assess == 0 else "index",
            "SR": "on" if config.current_assess > 4 and config.current_assess < 8 else "off",
            "Final threshold": final_threshold
        }
        json_object = json.dumps(data, indent=4)
        with open(self.file_path, 'a') as file:
            file.write(json_object + '\n')
        if config.current_assess == 0:
            config.wrist_threshold = final_threshold
        if config.current_assess == 10:
            self.screen.fill('black')
            UI.draw_text('Fin de l\'expérience', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2)
            pygame.display.update()
        else:
            config.current_assess += 1
            app = Threshold_assess(*config.stim_order_params[config.current_assess])
            app.run()