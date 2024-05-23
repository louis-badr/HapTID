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
            calib_button = UI.draw_button('Calibration', self.font, UI.color_text, self.screen, self.screen_w//2, self.screen_h//2 - 100)
            train_button = UI.draw_button('Entraînement - Temps de réaction', self.font, UI.color_text, self.screen, self.screen_w//2, self.screen_h//2)
            expe_button = UI.draw_button('Commencer - Temps de réaction', self.font, UI.color_text, self.screen, self.screen_w//2, self.screen_h//2 + 100)
            pygame.display.flip()
            self.clock.tick(config.framerate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    config.ser_haptid.write('0'.encode()) 
                    running = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if calib_button.collidepoint(event.pos):
                        print('Start calibration')
                        threshold_assess.ThresholdAssessment(config.assess_params[0]).run()
                    if train_button.collidepoint(event.pos):
                        print('Start training')
                        crt.CRT(config.train_tasks).run()
                    if expe_button.collidepoint(event.pos):
                        print('Start experiment')
                        crt.CRT(config.expe_tasks).run()