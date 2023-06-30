import pygame, sys

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h

# Colors
white = (255,255,255)
black = (0,0,0)

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

def main_menu():
    pygame.display.set_caption("Menu - HapTID")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if calib_button.collidepoint(event.pos):
                    print('Calibration')
                if crt_button.collidepoint(event.pos):
                    print('Choice Reaction Time')
                if fc_button.collidepoint(event.pos):
                    print('Force Control')

        screen.fill((0,0,0))
        draw_text('Main Menu', font, white, screen, screen_width/2, screen_height/2-200)
        calib_button = draw_button('Calibration', font, white, screen, screen_width/2, screen_height/2-100)
        crt_button = draw_button('Choice Reaction Time', font, white, screen, screen_width/2, screen_height/2)
        fc_button = draw_button('Force Control', font, white, screen, screen_width/2, screen_height/2+100)

        pygame.display.update()
        clock.tick(60)

main_menu()