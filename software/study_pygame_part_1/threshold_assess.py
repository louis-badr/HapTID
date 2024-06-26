from datetime import datetime

import config
import csv
import numpy
import os
import pygame
import random
import serial
import sys
import UI


class Threshold_assess:
    def __init__(self, stim_type, max_vib_lvl, max_nb_trials, max_chg_points, desc_start_step, staircase_coeff):
        # pygame things
        pygame.display.set_caption("Threshold assessment - HapTID")
        self.screen = pygame.display.get_surface()
        self.screen_w = pygame.display.Info().current_w
        self.screen_h = pygame.display.Info().current_h
        self.font = pygame.font.SysFont(None, 48)
        self.clock = pygame.time.Clock()
        self.file_path = f'./participants_data/P{config.id}/P{config.id}-data.csv'

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

        config.ser_haptid.write('0'.encode())
        if config.current_assess > 3 and config.current_assess < 7:
        #if config.current_assess == 2:
            self.sr_on = True
            self.noise_lvl = round(config.wrist_threshold * config.sr_coeff * 1000)
            print(f'Noise_lvl: {round(config.wrist_threshold * config.sr_coeff, 3)}%')
            pygame.time.wait(50)
            config.ser_haptid.write(f'{self.noise_lvl}'.encode())
            print(f'Sending {self.noise_lvl} to MCU')

    def run(self):
        # waiting screen
        self.screen.fill('black')
        UI.draw_text('Cliquez n\'importe où pour commencer', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2)
        UI.draw_text(f'{config.current_assess+1}/{len(config.stim_order_params)}', self.font, UI.color_text, self.screen, self.screen_w-100, 50)
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
            self.screen.fill('black')
            # UI.draw_text('Avez-vous senti une stimulation à votre poignet ?' if config.current_assess == 0 else 'Avez-vous senti une stimulation à votre index ?', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2)
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
            #! reactive the white noise if needed
            if self.sr_on:
                pygame.time.wait(50)
                config.ser_haptid.write(f'{self.noise_lvl}'.encode())
                print(f'Sending {self.noise_lvl} to MCU')
            # wait a bit
            pygame.time.wait(random.randint(1000, 2000))
            # display the buttons
            self.screen.fill('black')
            UI.draw_text('Avez-vous senti une stimulation à votre poignet ?' if config.current_assess == 0 else 'Avez-vous senti une stimulation à votre index ?', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2)
            no_button = UI.draw_button('Non', self.font, UI.color_text, UI.color_red, self.screen, self.screen_w/2-100, self.screen_h/2+100)
            yes_button = UI.draw_button('Oui', self.font, UI.color_text, UI.color_green, self.screen, self.screen_w/2+100, self.screen_h/2+100)
            pygame.display.update()
            print(self.desc_answers_history)
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
        # save the results in a csv file
        # Participant #; Age; Gender (M/F/O); Dominant hand (L/R); Assess #; Assess type (Desc/Asc); Noise PT coeff; Start; End; Stim type; Calculated PT; Vibration history
        data = [config.id, config.age, config.gender, config.dominant_hand, config.current_assess + 1, 'Desc', config.sr_coeff if self.sr_on else 0, start_date, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.stim_type, self.desc_threshold]
        data += self.desc_vib_lvl_history
        with open(self.file_path, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(data)
        print('Starting the ascending assessment...')
        start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.asc_step = self.desc_threshold * 0.4 # starting ascending step in %
        # ends when the maximum number of trials has been reached or when the value has stabilized
        while len(self.asc_vib_lvl_history) < self.max_nb_trials and len(self.asc_changing_points) < self.max_chg_points:
            # display a black screen
            self.screen.fill('black')
            # UI.draw_text('Avez-vous senti une stimulation à votre poignet ?' if config.current_assess == 0 else 'Avez-vous senti une stimulation à votre index ?', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2)
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
            #! reactive the white noise if needed
            if self.sr_on:
                pygame.time.wait(50)
                config.ser_haptid.write(f'{self.noise_lvl}'.encode())
                print(f'Sending {self.noise_lvl} to MCU')
            # wait a bit
            pygame.time.wait(random.randint(1000, 2000))
            # display the buttons
            self.screen.fill('black')
            UI.draw_text('Avez-vous senti une stimulation à votre poignet ?' if config.current_assess == 0 else 'Avez-vous senti une stimulation à votre index ?', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2)
            no_button = UI.draw_button('Non', self.font, UI.color_text, UI.color_red, self.screen, self.screen_w/2-100, self.screen_h/2+100)
            yes_button = UI.draw_button('Oui', self.font, UI.color_text, UI.color_green, self.screen, self.screen_w/2+100, self.screen_h/2+100)
            pygame.display.update()
            print(self.asc_answers_history)
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
        # save the results
        # Participant #; Age; Gender (M/F/O); Dominant hand (L/R); Assess #; Assess type (Desc/Asc); Noise PT coeff; Start; End; Stim type; Calculated PT; Vibration history
        data = [config.id, config.age, config.gender, config.dominant_hand, config.current_assess + 1, 'Asc',config.sr_coeff if self.sr_on else 0, start_date, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.stim_type, self.asc_threshold]
        data += self.asc_vib_lvl_history
        with open(self.file_path, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(data)
        if config.current_assess == 0:
            config.wrist_threshold = round((self.desc_threshold + self.asc_threshold) / 2, 3)
        if config.current_assess >=9:
            self.screen.fill('black')
            UI.draw_text('Fin de l\'expérience', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2)
            pygame.display.update()
            # stay on the screen indefinitely
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        config.ser_haptid.write('0'.encode())
                        config.ser_haptid.close()
                        pygame.quit()
                        sys.exit()
        else:
            config.current_assess += 1
            app = Threshold_assess(*config.stim_order_params[config.current_assess])
            app.run()