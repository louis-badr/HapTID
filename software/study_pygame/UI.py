import pygame

color_bg = pygame.Color("#04071B")
color_text = pygame.Color("#F4EFDC")
color_accent = pygame.Color("#2E45ED")
color_red = pygame.Color("#E34D55")
color_green = pygame.Color("#318F48")

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
    pygame.draw.rect(surface, color_accent, (textrect.left-10, textrect.top-10, textrect.width+20, textrect.height+20), 2)
    return textrect