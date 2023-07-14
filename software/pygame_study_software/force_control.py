import constants
import pygame
import serial
import sys


class FC:
    def __init__(self):
        self.ser = serial.Serial(constants.com_port, constants.baud_rate, timeout=1)
        self.ser.flush()
        pygame.display.set_caption("Force Control - HapTID")
        self.screen = pygame.display.get_surface()
        self.screen_w = pygame.display.Info().current_w
        self.screen_h = pygame.display.Info().current_h
        self.font = pygame.font.SysFont(None, 48)
        self.clock = pygame.time.Clock()
    def run(self):
        circle_color = 'white'
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.ser.close()
                    pygame.quit()
                    sys.exit()
            self.screen.fill('black')
            circle_size = int(self.ser.readline())
            if circle_size > 52:
                circle_color = 'red'
            elif circle_size < 48:
                circle_color = 'blue'
            else:
                circle_color = 'white'
            pygame.draw.circle(self.screen, circle_color, (self.screen_w/2, self.screen_h/2), circle_size)
            pygame.display.update()
            self.clock.tick(constants.framerate)