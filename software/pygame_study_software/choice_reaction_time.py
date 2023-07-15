import constants
import menu
import pygame
import sys
import UI


class CRT:
    def __init__(self):
        pygame.display.set_caption("Choice Reaction Time - HapTID")
        self.screen = pygame.display.get_surface()
        self.screen_w = pygame.display.Info().current_w
        self.screen_h = pygame.display.Info().current_h
        self.font = pygame.font.SysFont(None, 48)
        self.clock = pygame.time.Clock()
        self.circles_pos_x = [0.673, 0.582, 0.496, 0.412, 0.33]
        self.circles_pos_y = [0.498, 0.19, 0.151, 0.189, 0.34]
        hand_img = pygame.image.load('assets/hand_drawing.png').convert_alpha()
        if constants.dominant_hand == 'L':
            hand_img = pygame.transform.flip(hand_img, True, False)
            self.circles_pos_x = [1-i for i in self.circles_pos_x]
        hand_img_w, hand_img_h = hand_img.get_rect().size
        ratio = hand_img_w/hand_img_h
        self.hand_img = pygame.transform.smoothscale(hand_img, (int(ratio*self.screen_h*0.8), int(self.screen_h*0.8)))


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if menu_button.collidepoint(event.pos):
                        menu_screen = menu.Menu()
                        menu_screen.run()
            self.screen.fill('black')
            menu_button = UI.draw_button('Menu', self.font, 'white', self.screen, 100, 50)
            self.screen.blit(self.hand_img, (self.screen_w/2-self.hand_img.get_rect().size[0]/2, self.screen_h/2-self.hand_img.get_rect().size[1]/2))
            for i in range(5):
                pygame.draw.circle(self.screen, 'white', (self.screen_w*self.circles_pos_x[i], self.screen_h*self.circles_pos_y[i]), 20)
            pygame.display.update()
            self.clock.tick(constants.framerate)