import pygame

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
    pygame.draw.rect(surface, 'white', (textrect.left-10, textrect.top-10, textrect.width+20, textrect.height+20), 2)
    return textrect