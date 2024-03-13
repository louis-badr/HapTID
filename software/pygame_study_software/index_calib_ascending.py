from datetime import datetime

import constants
import index_calib_descending
import json
import menu
import numpy as np
import os
import pygame
import random
import serial
import sys
import UI


class Calibration_ascending:
    def __init__(self):
        # arduino things
        self.ser_haptid = serial.Serial(constants.com_port_haptid, 115200, timeout=.1)
        # dirty fix to make sure the arduino is ready to receive data
        self.ser_haptid.close()
        self.ser_haptid.open()    
        # initialize variables
        self.vib_lvl = 0
        self.step = constants.index_ascending_starting_step
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
        
    def run(self):

        self.screen.fill('black')
        UI.draw_button('Menu', self.font, 'white', self.screen, 75, 50)
        UI.draw_text('Avez-vous senti une vibration ?', self.font, 'white', self.screen, self.screen_w/2, self.screen_h/2)
        pygame.display.update()
        pygame.time.wait(2000)
        print('calibration ascending')
        running = True
        while running:

            self.screen.fill('black')
            menu_button = UI.draw_button('Menu', self.font, 'white', self.screen, 75, 50)
            UI.draw_text('Avez-vous senti une vibration ?', self.font, 'white', self.screen, self.screen_w/2, self.screen_h/2)
            no_button = UI.draw_button('Non', self.font, 'white', self.screen, self.screen_w/2-100, self.screen_h/2+100)
            yes_button = UI.draw_button('Oui', self.font, 'white', self.screen, self.screen_w/2+100, self.screen_h/2+100)

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
                    # if the participant has answered yes or no
                    if yes_button.collidepoint(event.pos) or no_button.collidepoint(event.pos):
                        # ends when the maximum number of trials has been reached
                        if len(self.vib_lvl_history) >= constants.index_nb_trials:
                            threshold_value = np.mean(self.changing_points[-3:])    # mean of the last 3 changing points
                            constants.finger_threshold += threshold_value
                            # save the calibration data
                            data = {
                                "Participant ID": constants.id,
                                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "Trial": constants.index_calib_done_trials,
                                "Ascending index threshold value": threshold_value,
                                "Ascending vibration level history": self.vib_lvl_history,
                                "Ascending level changing points": self.changing_points,
                                "Ascending participant answers history": self.answers_history
                            }
                            json_object = json.dumps(data, indent=4)
                            file_path = f'./P{constants.id}/P{constants.id}-index-calib.jsonl'
                            with open(file_path, "a") as outfile:
                                outfile.write(json_object + '\n')
                            # save the threshold value
                            data = {
                                "Participant ID": constants.id,
                                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "Trial": constants.index_calib_done_trials,
                                "Index threshold value": constants.wrist_threshold
                            }
                            json_object = json.dumps(data, indent=4)
                            with open(file_path, "a") as outfile:
                                outfile.write(json_object + '\n')

                            if constants.index_calib_done_trials == 3:
                                constants.finger_threshold /= 3
                                # save the threshold value
                                data = {
                                    "Participant ID": constants.id,
                                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "Mean index threshold value": constants.finger_threshold
                                }
                                json_object = json.dumps(data, indent=4)
                                with open(file_path, "a") as outfile:
                                    outfile.write(json_object + '\n')
                                # go back to the menu
                                self.ser_haptid.close()
                                menu_screen = menu.Menu()
                                menu_screen.run()
                            else:
                                # go to the descending calibration
                                self.ser_haptid.close()
                                index_calib_descending.Calibration_descending().run()


                        
                        self.screen.fill('black')
                        menu_button = UI.draw_button('Menu', self.font, 'white', self.screen, 75, 50)
                        UI.draw_text('Avez-vous senti une vibration ?', self.font, 'white', self.screen, self.screen_w/2, self.screen_h/2)
                        pygame.display.update()
                        #! white noise if it is the second trial
                        if constants.index_calib_done_trials == 2:
                            noise_lvl = int(constants.wrist_threshold * constants.sr_coeff * 1000)
                            self.ser_haptid.write(f'{int(noise_lvl)}'.encode())
                            print(f'noise_lvl: {noise_lvl}')
                        pygame.time.wait(random.randint(1000, 4000))
                        #! vibrate here
                        print(self.vib_lvl)
                        if self.vib_lvl > 0:
                            if constants.dominant_hand == "R":
                                self.ser_haptid.write(f'{int(float(self.vib_lvl) * 1000 + 400000)}'.encode())
                            else:
                                self.ser_haptid.write(f'{int(float(self.vib_lvl) * 1000 + 300000)}'.encode())
                        pygame.time.wait(random.randint(1000, 2500))
                        #! stop vibration (send 0)
                        self.ser_haptid.write('0'.encode())
                        pygame.time.wait(random.randint(500, 1000))



                        if yes_button.collidepoint(event.pos):
                            if len(self.answers_history) > 0:
                                # if the answer was yes and the previous answer was yes -> decrease the vibration level
                                if self.answers_history[-1] == 'y':
                                    self.vib_lvl_history.append(self.vib_lvl)
                                    self.answers_history.append('y')
                                    self.vib_lvl -= self.step
                                # if the answer was yes and the previous answer was no -> decrease the vibration level by a smaller step
                                elif self.answers_history[-1] == 'n':
                                    self.vib_lvl_history.append(self.vib_lvl)
                                    self.answers_history.append('y')
                                    self.changing_points.append(self.vib_lvl)
                                    self.step *= constants.index_coeff
                                    self.vib_lvl -= self.step
                                if self.vib_lvl < 0:
                                    self.vib_lvl = 0
                        if no_button.collidepoint(event.pos):
                            # if the answer was no and the previous answer was no -> increase the vibration level
                            if len(self.answers_history) == 0 or self.answers_history[-1] == 'n':
                                self.vib_lvl_history.append(self.vib_lvl)
                                self.answers_history.append('n')
                                self.vib_lvl += self.step
                            # if the answer was no and the previous answer was yes -> increase the vibration level by a smaller step
                            elif self.answers_history[-1] == 'y':
                                self.vib_lvl_history.append(self.vib_lvl)
                                self.answers_history.append('n')
                                self.changing_points.append(self.vib_lvl)
                                self.step *= constants.index_coeff
                                self.vib_lvl += self.step
                            if self.vib_lvl > constants.index_max_vib_lvl:
                                self.vib_lvl = constants.index_max_vib_lvl
            
            pygame.display.update()
            self.clock.tick(constants.framerate)