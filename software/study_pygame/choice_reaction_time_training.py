import config
import csv
import menu
import os
import pygame
import random
import serial
import sys
import time
import UI


class CRT:
    def __init__(self):
        # arduino things
        self.ser_mega = serial.Serial(config.com_port_keyboard, 115200, timeout=.1)
        self.ser_haptid = serial.Serial(config.com_port_haptid, 115200, timeout=.1)
        # dirty fix to make sure the arduino is ready to receive data
        self.ser_mega.close()
        self.ser_mega.open()
        self.ser_haptid.close()
        self.ser_haptid.open()
        # pygame things
        pygame.display.set_caption("Choice Reaction Time Training - HapTID")
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
        # we flip everything if the participant is left-handed
        if config.dominant_hand == 'L':
            hand_img = pygame.transform.flip(hand_img, True, False)
            self.circles_pos_x = [1-i for i in self.circles_pos_x]
        # scale the image to the screen size
        hand_img_w, hand_img_h = hand_img.get_rect().size
        ratio = hand_img_w/hand_img_h
        self.hand_img = pygame.transform.smoothscale(hand_img, (int(ratio*self.screen_h*0.8), int(self.screen_h*0.8)))
        # get the training list of tasks

    def run(self):
        while True:
            # on récupère les infos de la prochaine tâche
            next_task = config.tasks[0]
            # si c'est une pause on loop sur l'écran d'attente jusqu'à ce que l'utilisateur appuie sur espace
            if next_task[0] == 'break':
                running = True
                while running:
                    self.screen.fill('black')
                    menu_button = UI.draw_button('Menu', self.font, 'white', self.screen, 75, 50)
                    UI.draw_text('Appuyez sur espace pour continuer', self.font, 'white', self.screen, self.screen_w/2, self.screen_h/2)
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.ser_mega.close()
                            self.ser_haptid.close()
                            pygame.quit()
                            sys.exit()
                        if event.type==pygame.MOUSEBUTTONDOWN:
                            if menu_button.collidepoint(event.pos):
                                self.ser_mega.close()
                                self.ser_haptid.close()
                                menu_screen = menu.Menu()
                                menu_screen.run()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                running = False
                    self.clock.tick(config.framerate)
                # on ajoute l'exercice à la liste des exercices faits
                config.completed_crt_tasks.append(config.tasks.pop(0))
                next_task = config.tasks[0]
            # si la prochaine tâche n'est pas un CRT on retourne au menu
            if next_task[1] != 'CRT':
                self.ser_mega.close()
                self.ser_haptid.close()
                menu_screen = menu.Menu()
                menu_screen.run()
            # on récupère les infos de l'exercice
            wrist_vibration = bool(next_task[2])
            ws_type = next_task[4]
            is_type = next_task[5]
            # on fait correspondre le doigt à la position du cercle
            match next_task[3]:
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
                case other:
                    finger = 0
            # on lance la vibration du poignet si nécessaire
            if wrist_vibration:
                #! vibrate here
                print(f'Start wrist vibration at {self.wrist_vib_lvl}')
                self.ser_haptid.write(f'{int(self.wrist_vib_lvl * 1000)}'.encode())
                print(f'Sent to serial : {int(self.wrist_vib_lvl * 1000)}')
            # on affiche la main puis on attend un temps aléatoire
            self.screen.fill('black')
            self.screen.blit(self.hand_img, (self.screen_w/2-self.hand_img.get_rect().size[0]/2, self.screen_h/2-self.hand_img.get_rect().size[1]/2))
            # draw a little cross in the middle of the screen
            pygame.draw.line(self.screen, 'white', (self.screen_w/2-10, self.screen_h/2), (self.screen_w/2+10, self.screen_h/2), 5)
            pygame.draw.line(self.screen, 'white', (self.screen_w/2, self.screen_h/2-10), (self.screen_w/2, self.screen_h/2+10), 5)
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
                    #! click on all fingers
                    self.ser_haptid.write(b'-7')
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
                #! vibrate here
                self.ser_haptid.write(str(finger-2).encode())


            # on demande au mega de lancer la fonction de record
            self.ser_mega.write(b'C')
            # on attend d'avoir un retour du mega
            running = True
            while running:
                data = self.ser_mega.readline().decode().strip()
                if data:
                    print(data)
                    # parse data - fsr pressed ; reaction time
                    data = data.split(';')
                    # on fait correspondre le numéro du fsr au doigt
                    # si le participant est gaucher on inverse
                    if config.dominant_hand == 'L':
                        data[0] = 4 - data[0]
                    match data[0]:
                        case '0':
                            finger_pressed = 'little'
                        case '1':
                            finger_pressed = 'ring'
                        case '2':
                            finger_pressed = 'middle'
                        case '3':
                            finger_pressed = 'index'
                        case '4':
                            finger_pressed = 'thumb'
                        case other:
                            finger_pressed = 'error'
                    # save to csv here
                    with open(self.results_filepath, 'a', newline='') as csv_file:
                        csv_writer = csv.writer(csv_file, delimiter=';')
                        csv_writer.writerow(config.tasks[0]+[finger_pressed,data[1]])
                    running = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.ser_mega.close()
                        self.ser_haptid.close()
                        pygame.quit()
                        sys.exit()
                self.clock.tick(config.framerate)
            #! on arrête la vibration du poignet si nécessaire
            if wrist_vibration:
                print('Stop wrist vibration')
                self.ser_haptid.write(b'0')
            # on ajoute l'exercice à la liste des exercices faits
            config.completed_crt_tasks.append(config.tasks.pop(0))
            print(config.completed_crt_tasks)