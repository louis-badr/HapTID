import constants
import csv
import menu
import os
import pygame
import serial
import sys
import UI


class FC:
    def __init__(self):
        # arduino things
        self.ser_mega = serial.Serial(constants.com_port_keyboard, 115200)
        # dirty fix to make sure the arduino is ready to receive data
        self.ser_mega.close()
        self.ser_mega.open()

        # pygame things
        pygame.display.set_caption("Force Control - HapTID")
        self.screen = pygame.display.get_surface()
        self.screen_w = pygame.display.Info().current_w
        self.screen_h = pygame.display.Info().current_h
        self.font = pygame.font.SysFont(None, 48)
        self.clock = pygame.time.Clock()

        # load the results or create the file if it doesn't exist
        self.results_filepath = f'./P{constants.id}/P{constants.id}-fc-results.csv'
        if not os.path.exists(self.results_filepath):
            with open(self.results_filepath, 'w', newline='') as csv_file:
                # write the header
                csv_writer = csv.writer(csv_file, delimiter=';')
                csv_writer.writerow(['Task #', 'Task type', 'Wrist vibration', 'Force target(N)', 'Force applied(N)'])
        with open(self.results_filepath) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            print(len(list(csv_reader)))
            if len(list(csv_reader)) > 1:
                constants.completed_fc_tasks = list(csv_reader)[0]
            print(constants.completed_fc_tasks)

    def run(self):
        while True:
            # on récupère les infos de la prochaine tâche
            next_task = constants.tasks[0]
            # si la prochaine tâche n'est pas un FC on retourne au menu
            if next_task[1] != 'FC':
                self.ser_mega.close()
                menu_screen = menu.Menu()
                menu_screen.run()
            wrist_vibration = bool(next_task[2])
            force_target = int(next_task[3])
            circle_size_coeff = constants.target_circle_size/force_target

            # on loop sur l'écran d'attente jusqu'à ce que l'utilisateur appuie sur espace
            running = True
            while running:
                self.screen.fill('black')
                menu_button = UI.draw_button('Menu', self.font, 'white', self.screen, 75, 50)
                UI.draw_text('Positionnez votre index sur la touche, appuyez sur espace pour continuer', self.font, 'white', self.screen, self.screen_w/2, self.screen_h/2)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.ser_mega.close()
                        pygame.quit()
                        sys.exit()
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        if menu_button.collidepoint(event.pos):
                            self.ser_mega.close()
                            menu_screen = menu.Menu()
                            menu_screen.run()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            running = False
                self.clock.tick(constants.framerate)

            # on lance la vibration du poignet si nécessaire
            if wrist_vibration:
                print('Start wrist vibration')
            # on attend un peu
            self.screen.fill('black')
            pygame.display.update()
            pygame.time.wait(3000)
            circle_color = 'white'
            circle_size = constants.target_circle_size
            # flush du port série
            self.ser_mega.reset_input_buffer()
            # on demande au mega de lancer la fonction de lecture
            self.ser_mega.write(b'F')
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.ser_mega.close()
                        pygame.quit()
                        sys.exit()
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        if menu_button.collidepoint(event.pos):
                            self.ser_mega.close()
                            menu_screen = menu.Menu()
                            menu_screen.run()
                self.screen.fill('black')
                menu_button = UI.draw_button('Menu', self.font, 'white', self.screen, 75, 50)
                # on lit le port série
                if self.ser_mega.in_waiting > 0:
                    data = self.ser_mega.readline().decode().strip()
                    print(data)
                    # on adapte la taille du cercle en fonction de la force
                    circle_size = float(data) * circle_size_coeff
                    # le cercle devient rouge si la force est trop élevée, bleu si elle est trop faible et blanc sinon
                    if circle_size > constants.target_circle_size + 2:
                        circle_color = 'red'
                    elif circle_size < constants.target_circle_size - 2:
                        circle_color = 'blue'
                    else:
                        circle_color = 'white'
                    pygame.draw.circle(self.screen, circle_color, (self.screen_w/2, self.screen_h/2), circle_size)
                    pygame.display.update()
                self.clock.tick(constants.framerate)