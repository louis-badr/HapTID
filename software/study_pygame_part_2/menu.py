import config
import crt
import pygame
import threshold_assess
import UI

class Menu:
    def __init__(self):
        # pygame things
        pygame.display.set_caption('Menu - HapTID')
        self.screen = pygame.display.get_surface()
        self.screen_w = pygame.display.Info().current_w
        self.screen_h = pygame.display.Info().current_h
        self.font = pygame.font.SysFont(None, 48)
        self.clock = pygame.time.Clock()
    def run(self):
        running = True
        while running:
            self.screen.fill(UI.color_bg)
            UI.draw_text(f'Participant #{config.id}', self.font, UI.color_text, self.screen, self.screen_w//2, 50)
            if config.state == 'calib-wrist' or config.state == 'calib-finger-click' or config.state == 'calib-finger-vib':
                calib_button = UI.draw_button('Commencer la calibration', self.font, UI.color_text, UI.color_accent, self.screen, self.screen_w//2, self.screen_h//2 - 100)
            if config.state == 'training' or config.state == 'experiment':
                train_button = UI.draw_button('Commencer l\'entraînement', self.font, UI.color_text, UI.color_accent, self.screen, self.screen_w//2, self.screen_h//2)
            if config.state == 'experiment':
                expe_button = UI.draw_button('Commencer l\'expérience', self.font, UI.color_text, UI.color_accent, self.screen, self.screen_w//2, self.screen_h//2 + 100)
            pygame.display.flip()
            self.clock.tick(config.framerate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    config.ser_haptid.write('0'.encode()) 
                    running = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if config.state == 'calib-wrist' or config.state == 'calib-finger-click' or config.state == 'calib-finger-vib' and calib_button.collidepoint(event.pos):
                        print('Start calibration')
                        threshold_assess.Threshold_assess('noise', config.wrist_max_vib_lvl, config.max_nb_trials, config.max_chg_points, config.wrist_desc_start_step, config.wrist_staircase_coeff, True).run()
                    if config.state == 'training' or config.state == 'experiment' and train_button.collidepoint(event.pos):
                        print('Start training')
                        crt.CRT(config.train_tasks).run()
                    if config.state == 'experiment' and expe_button.collidepoint(event.pos):
                        print('Start experiment')
                        config.state = 'experiment'
                        crt.CRT(config.expe_tasks).run()