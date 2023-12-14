import constants
import json
import menu
import numpy as np
import pygame
import random
import serial
import sys
import UI


class Calibration:
    def __init__(self):
        # arduino things
        self.ser_haptid = serial.Serial(constants.com_port_haptid, 115200, timeout=.1)
        # dirty fix to make sure the arduino is ready to receive data
        self.ser_haptid.close()
        self.ser_haptid.open()    
        # initialize variables
        self.vib_lvl = constants.max_vib_lvl
        self.step = constants.starting_step
        self.vib_lvl_history = []
        self.changing_points = []
        self.answers_history = []

        # pygame things
        pygame.display.set_caption("Calibration - HapTID")
        self.screen = pygame.display.get_surface()
        self.screen_w = pygame.display.Info().current_w
        self.screen_h = pygame.display.Info().current_h
        self.font = pygame.font.SysFont(None, 48)
        self.clock = pygame.time.Clock()
        
    def run(self):

        # self.screen.fill('black')
        # UI.draw_button('Menu', self.font, 'white', self.screen, 75, 50)
        # UI.draw_text('Avez-vous senti une vibration ?', self.font, 'white', self.screen, self.screen_w/2, self.screen_h/2)
        # pygame.display.update()
        # pygame.time.wait(2000)
    
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
                        if len(self.vib_lvl_history) >= constants.nb_trials:
                            threshold_value = np.mean(self.changing_points[-3:])
                            constants.wrist_threshold = threshold_value
                            # save the calibration data
                            data = {
                                "Participant ID": constants.id,
                                "Wrist threshold value": threshold_value,
                                "Vibration level history": self.vib_lvl_history,
                                "Level changing points": self.changing_points,
                                "Participant answers history": self.answers_history
                            }
                            json_object = json.dumps(data, indent=4)
                            with open(f'./P{constants.id}/P{constants.id}-calibration.json', "w") as outfile:
                                outfile.write(json_object)
                            # go back to the menu
                            self.ser_haptid.close()
                            menu_screen = menu.Menu()
                            menu_screen.run()
                        self.screen.fill('black')
                        menu_button = UI.draw_button('Menu', self.font, 'white', self.screen, 75, 50)
                        UI.draw_text('Avez-vous senti une vibration ?', self.font, 'white', self.screen, self.screen_w/2, self.screen_h/2)
                        pygame.display.update()
                        pygame.time.wait(random.randint(1000, 4000))
                        #! vibrate here at max_vib_lvl (we send max_vib_lvl)
                        print(f'{int(self.vib_lvl)}')
                        self.ser_haptid.write(f'{int(float(self.vib_lvl) * 1000)}'.encode())
                        pygame.time.wait(2000)
                        #! stop vibration (send 0)
                        self.ser_haptid.write('0'.encode())
                        pygame.time.wait(500)
                        if yes_button.collidepoint(event.pos):
                            if len(self.answers_history) == 0 or self.answers_history[-1] == 'y':
                                self.vib_lvl_history.append(self.vib_lvl)
                                self.answers_history.append('y')
                                self.vib_lvl -= self.step
                            elif self.answers_history[-1] == 'n':
                                self.vib_lvl_history.append(self.vib_lvl)
                                self.answers_history.append('y')
                                self.changing_points.append(self.vib_lvl)
                                self.step *= constants.coeff
                                self.vib_lvl -= self.step
                            if self.vib_lvl < 0:
                                self.vib_lvl = 0
                        if no_button.collidepoint(event.pos):
                            if len(self.answers_history) > 0 and self.answers_history[-1] == 'n':
                                self.vib_lvl_history.append(self.vib_lvl)
                                self.answers_history.append('n')
                                self.vib_lvl += self.step
                            elif self.answers_history[-1] == 'y':
                                self.vib_lvl_history.append(self.vib_lvl)
                                self.answers_history.append('n')
                                self.changing_points.append(self.vib_lvl)
                                self.step *= constants.coeff
                                self.vib_lvl += self.step
                            if self.vib_lvl > constants.max_vib_lvl:
                                self.vib_lvl = constants.max_vib_lvl
            
            pygame.display.update()
            self.clock.tick(constants.framerate)