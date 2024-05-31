from datetime import datetime

import config
import csv
import menu
import numpy
import os
import pygame
import random
import serial
import sys
import UI


class Threshold_assess:
    def __init__(self, stim_type, max_vib_lvl, max_nb_trials, max_chg_points, desc_start_step, staircase_coeff, asc_assess):
        # pygame things
        pygame.display.set_caption("Threshold assessment - HapTID")
        self.screen = pygame.display.get_surface()
        self.screen_w = pygame.display.Info().current_w
        self.screen_h = pygame.display.Info().current_h
        self.font = pygame.font.SysFont(None, 48)
        self.clock = pygame.time.Clock()
        self.file_path = f'./participants_data/P{config.id}/P{config.id}-PT.csv'

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
        self.noise_lvl = 0
        self.sr_on = False

        self.asc_assess = asc_assess

        config.ser_haptid.write('0'.encode())

    def run(self):
        # waiting screen
        self.screen.fill(UI.color_bg)
        UI.draw_text('Cliquez n\'importe où pour commencer', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2)
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    config.ser_haptid.write('0'.encode())
                    config.ser_haptid.close()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    running = False
        print('Starting the descending assessment...')
        start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # ends when the maximum number of trials has been reached or when the value has stabilized
        while len(self.desc_vib_lvl_history) < self.max_nb_trials and len(self.desc_changing_points) < self.max_chg_points:
            # display a black screen
            self.screen.fill(UI.color_bg)
            pygame.display.update()
            # wait a bit
            pygame.time.wait(random.randint(1000, 2000))
            #! vibrate here
            print(f'Trial n°{self.desc_counter} : {self.desc_vib_lvl}%')
            val_to_send = round(self.desc_vib_lvl * 1000)
            if self.desc_vib_lvl > 0:
                if self.stim_type == 'noise':
                    config.ser_haptid.write(f'{val_to_send}'.encode())
                    print(f'Sending {val_to_send} to MCU')
                    pygame.time.wait(random.randint(1000, 2000))
                elif self.stim_type == '80':
                    if config.dominant_hand == "R":
                        val_to_send += 200000
                    else:
                        val_to_send += 100000
                    config.ser_haptid.write(f'{val_to_send}'.encode())
                    print(f'Sending {val_to_send} to MCU')
                    pygame.time.wait(random.randint(1000, 2000))
                elif self.stim_type == '250':
                    if config.dominant_hand == "R":
                        val_to_send += 400000
                    else:
                        val_to_send += 300000
                    config.ser_haptid.write(f'{val_to_send}'.encode())
                    print(f'Sending {val_to_send} to MCU')
                    pygame.time.wait(random.randint(1000, 2000))
                elif self.stim_type == 'click':
                    if config.dominant_hand == "R":
                        val_to_send  += 400000
                    else:
                        val_to_send += 200000
                    val_to_send *= -1
                    # two clicks
                    config.ser_haptid.write(f'{val_to_send}'.encode())
                    print(f'Sending {val_to_send} to MCU')
                    pygame.time.wait(random.randint(1000, 2000))
                    config.ser_haptid.write(f'{val_to_send}'.encode())
                    print(f'Sending {val_to_send} to MCU')
                    pygame.time.wait(random.randint(1000, 2000))
                    
            self.desc_counter += 1
            #! stop all vibrations
            config.ser_haptid.write('0'.encode())
            print('Sending 0 to MCU')
            # wait a bit
            pygame.time.wait(random.randint(1000, 2000))
            # display the buttons
            self.screen.fill(UI.color_bg)
            UI.draw_text('Avez-vous senti une stimulation à votre poignet ?' if self.stim_type == 'noise' else 'Avez-vous senti une stimulation à votre index ?', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2)
            no_button = UI.draw_button('Non', self.font, UI.color_text, UI.color_red, self.screen, self.screen_w/2-100, self.screen_h/2+100)
            yes_button = UI.draw_button('Oui', self.font, UI.color_text, UI.color_green, self.screen, self.screen_w/2+100, self.screen_h/2+100)
            pygame.display.update()
            # wait for the participant to answer
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        config.ser_haptid.write('0'.encode())
                        config.ser_haptid.close()
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
                                if self.desc_step < config.min_step:
                                    self.desc_step = config.min_step
                                self.desc_vib_lvl -= self.desc_step
                                self.desc_vib_lvl = round(self.desc_vib_lvl, 3)
                            if self.desc_vib_lvl < 0:
                                self.desc_vib_lvl = 0.01
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
                                if self.desc_step < config.min_step:
                                    self.desc_step = config.min_step
                                self.desc_vib_lvl += self.desc_step
                                self.desc_vib_lvl = round(self.desc_vib_lvl, 3)
                            if self.desc_vib_lvl > self.max_vib_lvl:
                                self.desc_vib_lvl = self.max_vib_lvl
                            running = False
        print('Descending assessment done.')
        self.desc_threshold = round(numpy.mean(self.desc_changing_points[-3:]), 3)
        if config.state == 'calib-finger-vib':
            config.finger_vib_threshold = self.desc_threshold
            print('PT for finger vibration:', config.finger_vib_threshold)
        elif config.state == 'calib-finger-click':
            config.finger_click_threshold = self.desc_threshold
            print('PT for finger click:', config.finger_click_threshold)
        # save the results in a csv file
        # Participant #; Age; Gender (M/F/O); Dominant hand (L/R); Assess type (Desc/Asc); Start; End; Stim type; Calculated PT; Vibration history
        data = [config.id, config.age, config.gender, config.dominant_hand, 'Desc', start_date, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.stim_type, self.desc_threshold]
        data += self.desc_vib_lvl_history
        with open(self.file_path, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(data)
        if self.asc_assess:
            print('Starting the ascending assessment...')
            start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.asc_step = self.desc_threshold * 0.4 # starting ascending step in %
            # ends when the maximum number of trials has been reached or when the value has stabilized
            while len(self.asc_vib_lvl_history) < self.max_nb_trials and len(self.asc_changing_points) < self.max_chg_points:
                # display a black screen
                self.screen.fill(UI.color_bg)
                pygame.display.update()
                # wait a bit
                pygame.time.wait(random.randint(1000, 2000))
                #! vibrate here
                print(f'Trial n°{self.asc_counter} : {self.asc_vib_lvl}%')
                val_to_send = round(self.asc_vib_lvl * 1000)
                if self.asc_vib_lvl > 0:
                    if self.stim_type == 'noise':
                        config.ser_haptid.write(f'{val_to_send}'.encode())
                        print(f'Sending {val_to_send} to MCU')
                        pygame.time.wait(random.randint(1000, 2000))
                    elif self.stim_type == '80':
                        if config.dominant_hand == "R":
                            val_to_send += 200000
                        else:
                            val_to_send += 100000
                        config.ser_haptid.write(f'{val_to_send}'.encode())
                        print(f'Sending {val_to_send} to MCU')
                        pygame.time.wait(random.randint(1000, 2000))
                    elif self.stim_type == '250':
                        if config.dominant_hand == "R":
                            val_to_send += 400000
                        else:
                            val_to_send += 300000
                        config.ser_haptid.write(f'{val_to_send}'.encode())
                        print(f'Sending {val_to_send} to MCU')
                        pygame.time.wait(random.randint(1000, 2000))
                    elif self.stim_type == 'click':
                        if config.dominant_hand == "R":
                            val_to_send  += 400000
                        else:
                            val_to_send += 200000
                        val_to_send *= -1 
                        # two clicks
                        config.ser_haptid.write(f'{val_to_send}'.encode())
                        print(f'Sending {val_to_send} to MCU')
                        pygame.time.wait(random.randint(1000, 2000))
                        config.ser_haptid.write(f'{val_to_send}'.encode())
                        print(f'Sending {val_to_send} to MCU')
                        pygame.time.wait(random.randint(1000, 2000))
                self.asc_counter += 1
                #! stop all vibrations
                config.ser_haptid.write('0'.encode())
                print('Sending 0 to MCU')
                # wait a bit
                pygame.time.wait(random.randint(1000, 2000))
                # display the buttons
                self.screen.fill(UI.color_bg)
                UI.draw_text('Avez-vous senti une stimulation à votre poignet ?' if self.stim_type == 'noise' else 'Avez-vous senti une stimulation à votre index ?', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2)
                no_button = UI.draw_button('Non', self.font, UI.color_text, UI.color_red, self.screen, self.screen_w/2-100, self.screen_h/2+100)
                yes_button = UI.draw_button('Oui', self.font, UI.color_text, UI.color_green, self.screen, self.screen_w/2+100, self.screen_h/2+100)
                pygame.display.update()
                # wait for the participant to answer
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            config.ser_haptid.write('0'.encode())
                            config.ser_haptid.close()
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
                                        if self.asc_step < config.min_step:
                                            self.asc_step = config.min_step
                                        self.asc_vib_lvl -= self.asc_step
                                        self.asc_vib_lvl = round(self.asc_vib_lvl, 3)
                                if self.asc_vib_lvl < 0:
                                    self.asc_vib_lvl = 0.01
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
                                    if self.asc_step < config.min_step:
                                        self.asc_step = config.min_step
                                    self.asc_vib_lvl += self.asc_step
                                    self.asc_vib_lvl = round(self.asc_vib_lvl, 3)
                                if self.asc_vib_lvl > self.max_vib_lvl:
                                    self.asc_vib_lvl = self.max_vib_lvl
                                running = False
            print('Ascending assessment done.')
            self.asc_threshold = round(numpy.mean(self.asc_changing_points[-3:]), 3)
            if config.state == 'calib-wrist':
                config.wrist_threshold = round((self.desc_threshold + self.asc_threshold) / 2, 3)
                print('PT for wrist vibration:', config.wrist_threshold)
            # save the results
            # Participant #; Age; Gender (M/F/O); Dominant hand (L/R); Assess type (Desc/Asc); Start; End; Stim type; Calculated PT; Vibration history
            data = [config.id, config.age, config.gender, config.dominant_hand, 'Asc', start_date, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.stim_type, self.asc_threshold]
            data += self.asc_vib_lvl_history
            with open(self.file_path, 'a', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(data)
        if config.state == 'calib-wrist':
            config.state = 'calib-finger-vib'
            Threshold_assess('250', config.index_max_vib_lvl, config.max_nb_trials, config.max_chg_points, config.index_vib_desc_start_step, config.finger_staircase_coeff, False).run()
        elif config.state == 'calib-finger-vib':
            config.state = 'calib-finger-click'
            Threshold_assess('click', config.index_max_click_lvl, config.max_nb_trials, config.max_chg_points, config.index_click_desc_start_step, config.finger_staircase_coeff, False).run()
        elif config.state == 'calib-finger-click':
            config.state = 'training'
            # print all the thresholds
            print('\n--- Thresholds ---')
            print('Wrist threshold:', config.wrist_threshold)
            print('Finger vibration threshold:', config.finger_vib_threshold)
            print('Finger click threshold:', config.finger_click_threshold)
            print('-------------------\n')
            # go back to the menu
            menu.Menu().run()