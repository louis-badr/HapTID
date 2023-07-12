import menu
import os
import pygame

# ask for participant ID in the format : order + first letters of last and first name
id = input('Enter participant ID (ex:01BL):')
# create folder for participant if it doesn't exist
if not os.path.exists(f'./{id}'):
    os.mkdir(f'./{id}')

# initialize pygame
pygame.init()

screen = pygame.display.set_mode((640,480))

if __name__ == '__main__':
    app = menu.Menu(id)
    app.run()