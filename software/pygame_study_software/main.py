import csv
import numpy as np
import os
import plotly.graph_objects as go
import pygame
import sys

id = input('Enter participant ID (ex:01BL):')

if not os.path.exists(f'./{id}'):
    os.mkdir(f'./{id}')

max_vib_lvl = 5
nb_trials = 5
threshold_value = None

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h

# Colors
white = (255,255,255)
black = (0,0,0)
green = (0,255,0)

# Fonts
font = pygame.font.SysFont(None, 48)
img = font.render('Menu', True, white)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x,y)
    surface.blit(textobj, textrect)

def draw_button(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x,y)
    surface.blit(textobj, textrect)
    pygame.draw.rect(surface, white, (textrect.left-10, textrect.top-10, textrect.width+20, textrect.height+20), 2)
    return textrect

def calib_screen(id):
    pygame.display.set_caption("Calibration - HapTID")
    screen.fill((0,0,0))
    menu_button = draw_button('Menu', font, white, screen, 100, 50)
    draw_text('Avez-vous senti une vibration ?', font, white, screen, screen_width/2, screen_height/2)
    pygame.display.update()
    pygame.time.wait(2000)

    vib_lvl = max_vib_lvl
    vib_lvl_history = []
    changing_points = []
    answers_history = []
    step = 1.5
    coeff = 0.7

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if menu_button.collidepoint(event.pos):
                    running = False
                    main_menu(id)
                if yes_button.collidepoint(event.pos) or no_button.collidepoint(event.pos):
                    print(answers_history)
                    print(vib_lvl_history)
                    if len(vib_lvl_history) >= nb_trials:
                        threshold_value = np.mean(changing_points)
                        with open(f'./{id}/{id}-calibration.csv', 'w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(vib_lvl_history)
                            writer.writerow(answers_history)
                            writer.writerow(changing_points)
                            writer.writerow([threshold_value])
                        running=False
                        main_menu(id)
                    screen.fill((0,0,0))
                    menu_button = draw_button('Menu', font, white, screen, 100, 50)
                    draw_text('Avez-vous senti une vibration ?', font, white, screen, screen_width/2, screen_height/2)
                    pygame.display.update()
                    pygame.time.wait(2000)
                    # vibrate here at vib_lvl
                    pygame.time.wait(250)
                    if yes_button.collidepoint(event.pos):
                        if len(answers_history) == 0 or answers_history[-1] == 'y':
                            vib_lvl_history.append(vib_lvl)
                            answers_history.append('y')
                            vib_lvl -= step
                        elif answers_history[-1] == 'n':
                            vib_lvl_history.append(vib_lvl)
                            answers_history.append('y')
                            changing_points.append(vib_lvl)
                            step *= coeff
                            vib_lvl -= step
                        if vib_lvl < 0:
                            vib_lvl = 0
                    if no_button.collidepoint(event.pos):
                        if answers_history[-1] == 'n':
                            vib_lvl_history.append(vib_lvl)
                            answers_history.append('n')
                            vib_lvl += step
                        elif answers_history[-1] == 'y':
                            vib_lvl_history.append(vib_lvl)
                            answers_history.append('n')
                            changing_points.append(vib_lvl)
                            step *= coeff
                            vib_lvl += step
                        if vib_lvl > max_vib_lvl:
                            vib_lvl = max_vib_lvl

        screen.fill((0,0,0))
        # always displayed
        menu_button = draw_button('Menu', font, white, screen, 100, 50)
        draw_text('Avez-vous senti une vibration ?', font, white, screen, screen_width/2, screen_height/2)
        no_button = draw_button('Non', font, white, screen, screen_width/2-100, screen_height/2+100)
        yes_button = draw_button('Oui', font, white, screen, screen_width/2+100, screen_height/2+100)
        

        pygame.display.update()
        clock.tick(60)

def main_menu(id):
    pygame.display.set_caption("Start Menu - HapTID")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if calib_button.collidepoint(event.pos):
                    running = False
                    calib_screen(id)

        screen.fill((0,0,0))
        draw_text(f'Participant {id}', font, white, screen, screen_width/2, screen_height/10)
        calib_button = draw_button('Start calibration', font, white, screen, screen_width/2, screen_height/2)
        if os.path.exists(f'./{id}/{id}-calibration.csv'):
            exercices_button = draw_button('Start exercices', font, white, screen, screen_width/2, screen_height/2+100)
            draw_text('Calibration complete !', font, green, screen, screen_width/2, screen_height/2+200)

        pygame.display.update()

main_menu(id)