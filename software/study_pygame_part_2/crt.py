from datetime import datetime

import config
import csv
import menu
import pygame
import random
import UI


class CRT:
    def __init__(self, tasks_list):
        # pygame things
        pygame.display.set_caption('Menu - HapTID')
        self.screen = pygame.display.get_surface()
        self.screen_w = pygame.display.Info().current_w
        self.screen_h = pygame.display.Info().current_h
        self.font = pygame.font.SysFont(None, 48)
        self.clock = pygame.time.Clock()
        # hand image
        # positions of the circles for each finger
        self.circles_pos_x = [0.673, 0.582, 0.496, 0.412, 0.33]
        self.circles_pos_y = [0.498, 0.19, 0.151, 0.189, 0.34]
        hand_img = pygame.image.load('hand_drawing.png').convert_alpha()
        hand_img_green = pygame.image.load('hand_drawing_green.png').convert_alpha()
        # we study the non-dominant hand, the image is of a left hand
        # we flip it as well as the circles if the participant is left-handed
        if config.dominant_hand == 'L':
            hand_img = pygame.transform.flip(hand_img, True, False)
            hand_img_green = pygame.transform.flip(hand_img_green, True, False)
            self.circles_pos_x = [1-i for i in self.circles_pos_x]
        # scale the image to the screen size
        hand_img_w, hand_img_h = hand_img.get_rect().size
        ratio = hand_img_w/hand_img_h
        self.hand_img = pygame.transform.smoothscale(hand_img, (int(ratio*self.screen_h*0.8), int(self.screen_h*0.8)))
        self.hand_img_green = pygame.transform.smoothscale(hand_img_green, (int(ratio*self.screen_h*0.8), int(self.screen_h*0.8)))

        self.tasks_list = tasks_list
        self.file_path = f'./participants_data/P{config.id}/P{config.id}-CRT.csv'
        self.nb_sessions = 1
        self.current_session = 0
        # count the number of sessions
        for task in self.tasks_list:
            if task[2] == 'break':
                self.nb_sessions += 1

        self.noise_lvl = 0

    def run(self):
        # the csv file is structured as follows:
        # Participant #; Exercise type; Task #; Noise PT coeff; Finger; Warning signal type; Imperative signal type
        for i in range(len(self.tasks_list)):
            if self.tasks_list[i][0] == 'break' or i == 0:
                self.current_session += 1
                ws_type = self.tasks_list[i+1][5] if i != 0 else self.tasks_list[i][5]
                is_type = self.tasks_list[i+1][6] if i != 0 else self.tasks_list[i][6]
                self.screen.fill(UI.color_bg)
                match ws_type:
                    case 'visual':
                        ws_type = 'Avertissement visuel'
                    case 'tactile-click':
                        ws_type = 'Avertissement tactile'
                    # case 'tactile-vibration':
                    #     ws_type = 'Avertissement tactile'
                    case 'none':
                        ws_type = 'Pas d\'avertissement'
                    case other:
                        print(f'Error: unknown warning signal type: {ws_type}')
                        pass
                match is_type:
                    case 'visual':
                        is_type = 'Signal visuel'
                    case 'tactile-click':
                        is_type = 'Signal tactile'
                    case 'tactile-vibration':
                        is_type = 'Signal tactile'
                    case other:
                        print(f'Error: unknown imperative signal type: {is_type}')
                UI.draw_text(f'{self.current_session}/{self.nb_sessions}', self.font, UI.color_text, self.screen, self.screen_w-100, 50)
                UI.draw_text(ws_type, self.font, UI.color_text, self.screen, self.screen_w//2, self.screen_h//2 - 50)
                UI.draw_text(is_type, self.font, UI.color_text, self.screen, self.screen_w//2, self.screen_h//2 + 50)
                UI.draw_text('Cliquez n\'importe où pour commencer', self.font, UI.color_text, self.screen, self.screen_w//2, self.screen_h - 50)
                pygame.display.flip()
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            running = False
            if self.tasks_list[i][0] != 'break':
                # get the info for the task
                task_no = self.tasks_list[i][2]
                noise_coeff = float(self.tasks_list[i][3])
                finger = self.tasks_list[i][4]
                ws_type = self.tasks_list[i][5]
                is_type = self.tasks_list[i][6]
                match finger:
                    case 'thumb':
                        finger_no = 0
                    case 'index':
                        finger_no = 1
                    case 'middle':
                        finger_no = 2
                    case 'ring':
                        finger_no = 3
                    case 'little':
                        finger_no = 4
                    case other:
                        print(f'Error: unknown finger: {finger}')
                # values to send to the MCU computed here to avoid delays
                finger_vib_volume = config.finger_vib_threshold * 16
                finger_click_volume = config.finger_click_threshold * 16
                if finger_vib_volume > 99.999:
                    finger_vib_volume = 99.999
                if finger_click_volume > 99.999:
                    finger_click_volume = 99.999
                val_click_all = round(-(600000 + finger_click_volume * 1000))
                if config.dominant_hand == 'L':
                    val_tactile_click = round(-((finger_no + 1) * 100000 + finger_click_volume * 1000))
                    val_tactile_vibration = round(-((finger_no + 8) * 100000 + finger_vib_volume * 1000))
                else:
                    val_tactile_click = round(-((5 - finger_no) * 100000 + finger_click_volume * 1000))
                    val_tactile_vibration = round(-((12 - finger_no) * 100000 + finger_vib_volume * 1000))
                if noise_coeff != 0:
                    # start the noise
                    self.noise_lvl = round(config.wrist_threshold * noise_coeff * 1000)
                    config.ser_haptid.write(f'{self.noise_lvl}'.encode())
                    print(f'Sent {self.noise_lvl} to MCU')
                # display the hand and the crosshair
                self.screen.fill(UI.color_bg)
                self.screen.blit(self.hand_img, (self.screen_w/2-self.hand_img.get_rect().size[0]/2, self.screen_h/2-self.hand_img.get_rect().size[1]/2))
                pygame.draw.line(self.screen, 'white', (self.screen_w/2-20, self.screen_h/2), (self.screen_w/2+20, self.screen_h/2), 4)
                pygame.draw.line(self.screen, 'white', (self.screen_w/2, self.screen_h/2-20), (self.screen_w/2, self.screen_h/2+20), 4)
                pygame.display.flip()
                pygame.time.wait(random.randint(2000, 3000))
                # warning signal (or not)
                match ws_type:
                    case 'visual':
                        # add the dots
                        for i in range(5):
                            pygame.draw.circle(self.screen, 'white', (self.screen_w*self.circles_pos_x[i], self.screen_h*self.circles_pos_y[i]), 20)
                        pygame.display.flip()
                        pygame.time.wait(config.visual_signal_duration)
                        self.screen.fill(UI.color_bg)
                        self.screen.blit(self.hand_img, (self.screen_w/2-self.hand_img.get_rect().size[0]/2, self.screen_h/2-self.hand_img.get_rect().size[1]/2))
                        pygame.draw.line(self.screen, 'white', (self.screen_w/2-20, self.screen_h/2), (self.screen_w/2+20, self.screen_h/2), 4)
                        pygame.draw.line(self.screen, 'white', (self.screen_w/2, self.screen_h/2-20), (self.screen_w/2, self.screen_h/2+20), 4)
                        pygame.display.flip()
                        pygame.time.wait(500)
                    case 'tactile-click':
                        # click on all fingers
                        config.ser_haptid.write(f'{val_click_all}'.encode())
                        print(f'Sent {val_click_all} to MCU')
                        pygame.time.wait(500)
                    case 'none':
                        pass
                    case other:
                        print(f'Error: unknown warning signal type: {ws_type}')
                # imperative signal
                match is_type:
                    case 'visual':
                        pygame.draw.circle(self.screen, 'green', (self.screen_w*self.circles_pos_x[finger_no], self.screen_h*self.circles_pos_y[finger_no]), 20)
                        pygame.display.flip()
                        pygame.time.wait(config.visual_signal_duration)
                        self.screen.fill(UI.color_bg)
                        self.screen.blit(self.hand_img, (self.screen_w/2-self.hand_img.get_rect().size[0]/2, self.screen_h/2-self.hand_img.get_rect().size[1]/2))
                        pygame.draw.line(self.screen, 'white', (self.screen_w/2-20, self.screen_h/2), (self.screen_w/2+20, self.screen_h/2), 4)
                        pygame.draw.line(self.screen, 'white', (self.screen_w/2, self.screen_h/2-20), (self.screen_w/2, self.screen_h/2+20), 4)
                        pygame.display.flip()
                    case 'tactile-click':
                        # click on the finger
                        config.ser_haptid.write(f'{val_tactile_click}'.encode())
                        print(f'Sent {val_tactile_click} to MCU')
                    case 'tactile-vibration':
                        # sine click on the finger
                        config.ser_haptid.write(f'{val_tactile_vibration}'.encode())
                        print(f'Sent {val_tactile_vibration} to MCU')
                    case other:
                        print(f'Error: unknown imperative signal type: {is_type}')
                # set the keyboard in listening mode
                config.ser_keyboard.write(b'C')
                # start a timer
                start_time = pygame.time.get_ticks()
                # wait for the participant's response
                running = True
                while running:
                    data = config.ser_keyboard.readline().decode().strip()
                    if data:
                        print(f'Received {data} from MCU')
                        running = False
                        self.screen.fill(UI.color_bg)
                        self.screen.blit(self.hand_img_green, (self.screen_w/2-self.hand_img.get_rect().size[0]/2, self.screen_h/2-self.hand_img.get_rect().size[1]/2))
                        pygame.draw.line(self.screen, 'white', (self.screen_w/2-20, self.screen_h/2), (self.screen_w/2+20, self.screen_h/2), 4)
                        pygame.draw.line(self.screen, 'white', (self.screen_w/2, self.screen_h/2-20), (self.screen_w/2, self.screen_h/2+20), 4)
                        pygame.display.flip()
                        pygame.time.wait(500)
                        self.screen.fill(UI.color_bg)
                        pygame.display.flip()
                        pygame.time.wait(1000)
                    elif pygame.time.get_ticks() - start_time >= config.max_reaction_time:
                        print('Timeout')
                        data = None
                        running = False
                        self.screen.fill(UI.color_bg)
                        pygame.display.flip()
                        pygame.time.wait(3000)
                config.ser_haptid.write('0'.encode()) # stop the noise
                # save the data
                if data is None:
                    finger_pressed = 'timeout'
                    data = ['timeout', 'timeout']
                else:
                    data = data.split(';')
                    if config.dominant_hand == 'R':
                        data[0] = str(4 - int(data[0]))
                    match data[0]:
                        case '0':
                            finger_pressed = 'thumb'
                        case '1':
                            finger_pressed = 'index'
                        case '2':
                            finger_pressed = 'middle'
                        case '3':
                            finger_pressed = 'ring'
                        case '4':
                            finger_pressed = 'little'
                        case other:
                            print(f'Error: unknown finger pressed: {data[0]}')
                with open(self.file_path, mode='a', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    # Participant #; Age; Gender (M/F/O); Dominant hand (L/R); Wrist PT; Exercise type; Date; Task #; Noise PT coeff; Finger to press; Warning signal type; Imperative signal type; Finger pressed; Reaction time
                    writer.writerow([config.id, config.age, config.gender, config.dominant_hand, config.wrist_threshold, 'CRT', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), task_no, noise_coeff, finger, ws_type, is_type, finger_pressed, data[1]])
                    print(f'Task {task_no} saved')
        if config.state == 'experiment' and task_no != '-1':
            config.state = None
            # end screen
            self.screen.fill(UI.color_bg)
            UI.draw_text('Fin de l\'expérience', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2)
            UI.draw_text('Merci d\'appeler l\'expérimentateur avant de retirer le matériel', self.font, UI.color_text, self.screen, self.screen_w/2, self.screen_h/2 + 50)
            pygame.display.update()
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        config.ser_haptid.write('0'.encode())
                        config.ser_haptid.close()
                        config.ser_keyboard.close()
                        pygame.quit()
        else:
            config.state = 'experiment'
            # back to the menu
            menu.Menu().run()