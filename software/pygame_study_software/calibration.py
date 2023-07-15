import csv
import menu
import numpy as np
import pygame
import constants
import sys
import UI


class Calibration:
    def __init__(self):
        
        # initialize variables
        self.vib_lvl = constants.max_vib_lvl
        self.step = constants.starting_step
        self.vib_lvl_history = []
        self.changing_points = []
        self.answers_history = []    
        # initialize pygame
        pygame.display.set_caption("Calibration - HapTID")
        self.screen = pygame.display.get_surface()
        self.screen_w = pygame.display.Info().current_w
        self.screen_h = pygame.display.Info().current_h
        self.font = pygame.font.SysFont(None, 48)
        self.clock = pygame.time.Clock()
        
    def run(self):
        self.screen.fill('black')
        UI.draw_button('Menu', self.font, 'white', self.screen, 100, 50)
        UI.draw_text('Avez-vous senti une vibration ?', self.font, 'white', self.screen, self.screen_w/2, self.screen_h/2)
        pygame.display.update()
        pygame.time.wait(2000)
    
        running = True
        while running:
            self.screen.fill('black')
            # always displayed
            menu_button = UI.draw_button('Menu', self.font, 'white', self.screen, 100, 50)
            UI.draw_text('Avez-vous senti une vibration ?', self.font, 'white', self.screen, self.screen_w/2, self.screen_h/2)
            no_button = UI.draw_button('Non', self.font, 'white', self.screen, self.screen_w/2-100, self.screen_h/2+100)
            yes_button = UI.draw_button('Oui', self.font, 'white', self.screen, self.screen_w/2+100, self.screen_h/2+100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if menu_button.collidepoint(event.pos):
                        menu_screen = menu.Menu()
                        menu_screen.run()
                    # if the participant has answered yes or no
                    if yes_button.collidepoint(event.pos) or no_button.collidepoint(event.pos):
                        # ends when the maximum number of trials has been reached
                        if len(self.vib_lvl_history) >= constants.nb_trials:
                            threshold_value = np.mean(self.changing_points)
                            with open(f'./{constants.id}/{constants.id}-calibration.csv', 'w', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(self.vib_lvl_history)
                                writer.writerow(self.answers_history)
                                writer.writerow(self.changing_points)
                                writer.writerow([threshold_value])
                            menu_screen = menu.Menu()
                            menu_screen.run()
                        self.screen.fill('black')
                        menu_button = UI.draw_button('Menu', self.font, 'white', self.screen, 75, 50)
                        UI.draw_text('Avez-vous senti une vibration ?', self.font, 'white', self.screen, self.screen_w/2, self.screen_h/2)
                        pygame.display.update()
                        pygame.time.wait(2000)
                        # vibrate here at vib_lvl
                        pygame.time.wait(250)
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
                            if self.answers_history[-1] == 'n':
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