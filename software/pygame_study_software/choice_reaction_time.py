import constants
import csv
import menu
import os
import pygame
import random
import sys
import time
import UI


class CRT:
    def __init__(self):

        # pygame things
        pygame.display.set_caption("Choice Reaction Time - HapTID")
        self.screen = pygame.display.get_surface()
        self.screen_w = pygame.display.Info().current_w
        self.screen_h = pygame.display.Info().current_h
        self.font = pygame.font.SysFont(None, 48)
        self.clock = pygame.time.Clock()

        # positions of the circles for each finger
        self.circles_pos_x = [0.673, 0.582, 0.496, 0.412, 0.33]
        self.circles_pos_y = [0.498, 0.19, 0.151, 0.189, 0.34]

        # load the hand image
        hand_img = pygame.image.load('assets/hand_drawing.png').convert_alpha()

        # we study the non-dominant hand, the image is of a left hand
        # we flip it as well as the circles if the participant is left-handed
        if constants.dominant_hand == 'L':
            hand_img = pygame.transform.flip(hand_img, True, False)
            self.circles_pos_x = [1-i for i in self.circles_pos_x]

        # scale the image to the screen size
        hand_img_w, hand_img_h = hand_img.get_rect().size
        ratio = hand_img_w/hand_img_h
        self.hand_img = pygame.transform.smoothscale(hand_img, (int(ratio*self.screen_h*0.8), int(self.screen_h*0.8)))
        
        # load the results or create the file if it doesn't exist
        self.results_filepath = f'./P{constants.id}/P{constants.id}-crt-results.csv'
        if not os.path.exists(self.results_filepath):
            with open(self.results_filepath, 'w', newline='') as csv_file:
                pass
        with open(self.results_filepath) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            print(len(list(csv_reader)))
            if len(list(csv_reader)) != 0:
                self.done_exercices = list(csv_reader)[0]
            else:
                self.done_exercices = []
            print(self.done_exercices)

    def run(self):
        while True:

            # on récupère les infos de la prochaine tâche
            next_task = constants.tasks[0]
            # si la prochaine tâche n'est pas un CRT on retourne au menu
            if next_task[1] != 'CRT':
                menu_screen = menu.Menu()
                menu_screen.run()
            # on récupère les infos de l'exercice
            ws_type = next_task[4]
            is_type = next_task[5]
            match next_task[2]:
                case 'thumb':
                    finger = 0
                case 'index':
                    finger = 1
                case 'middle':
                    finger = 2
                case 'ring':
                    finger = 3
                case 'little':
                    finger = 4
            # si le participant est gaucher
            if constants.dominant_hand == 'L':
                finger = abs(4 - finger)

            # on loop sur l'écran d'attente jusqu'à ce que l'utilisateur appuie sur espace
            running = True
            while running:
                self.screen.fill('black')
                menu_button = UI.draw_button('Menu', self.font, 'white', self.screen, 75, 50)
                UI.draw_text('Appuyez sur espace pour continuer', self.font, 'white', self.screen, self.screen_w/2, self.screen_h/2)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        if menu_button.collidepoint(event.pos):
                            menu_screen = menu.Menu()
                            menu_screen.run()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            running = False
                self.clock.tick(constants.framerate)
            # on affiche la main puis on attend un temps aléatoire
            self.screen.fill('black')
            self.screen.blit(self.hand_img, (self.screen_w/2-self.hand_img.get_rect().size[0]/2, self.screen_h/2-self.hand_img.get_rect().size[1]/2))
            pygame.display.update()
            pygame.time.wait(random.randint(3000, 8000))
            # on lance le warning signal
            if ws_type != 'None':
                if ws_type == 'visual':
                    print('WS Type : Visual')
                    for i in range(5):
                        pygame.draw.circle(self.screen, 'white', (self.screen_w*self.circles_pos_x[i], self.screen_h*self.circles_pos_y[i]), 20)
                    pygame.display.update()
                elif ws_type == 'tactile':
                    print('WS Type : Tactile')
                    # vibrate here
                pygame.time.wait(500)
                self.screen.fill('black')
                self.screen.blit(self.hand_img, (self.screen_w/2-self.hand_img.get_rect().size[0]/2, self.screen_h/2-self.hand_img.get_rect().size[1]/2))
                pygame.display.update()
            # on lance l'imperative signal
            if is_type == 'visual':
                pygame.draw.circle(self.screen, 'green', (self.screen_w*self.circles_pos_x[finger], self.screen_h*self.circles_pos_y[finger]), 20)
                pygame.display.update()
            elif is_type == 'tactile':
                print('IS Type : Tactile')
                # vibrate here
            start = time.time()
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            end = time.time()
                            print(end-start)
                            running = False
                self.clock.tick(constants.framerate)
            # on enregistre les résultats dans le fichier csv
            with open(self.results_filepath, 'a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=';')
                csv_writer.writerow([next_exercice, finger, end-start])
            # on ajoute l'exercice à la liste des exercices faits
            self.done_exercices.append(next_exercice)