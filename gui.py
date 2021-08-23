import pygame as pg
from settings import *

class Button():
    def __init__(self, game, text, font_name, size, width, height, x, y):
        self.font = pg.font.Font(font_name, size)
        self.text_surface_red = self.font.render(text, True, RED)
        self.text_rect_red = self.text_surface_red.get_rect()
        self.text_rect_red.center = (x, y)
        self.text_surface_white = self.font.render(text, True, WHITE)
        self.text_rect_white = self.text_surface_white.get_rect()
        self.text_rect_white.center = (x, y)
        self.game = game
        self.text = text
        self.font_name = font_name
        self.size = size
        self.width = width
        self.height = height 
        self.x = x
        self.y = y
        self.dark_green_surf = pg.Surface((self.width, self.height))
        self.dark_green_surf.fill(DARK_GREEN)
        self.dark_green_rect = self.dark_green_surf.get_rect()
        self.dark_green_rect.center = (x, y + 10)
        self.blue_surf = pg.Surface((self.width, self.height))
        self.blue_surf.fill(BLUE)
        self.blue_rect = self.blue_surf.get_rect()
        self.blue_rect.center = (x, y + 10)
        self.hovering = False

        
    def update(self):
        mouse_pos = pg.mouse.get_pos()
        collide_red = self.dark_green_rect.collidepoint(mouse_pos)
        collide_blue = self.blue_rect.collidepoint(mouse_pos)

        if collide_red or collide_blue:
            self.hovering = True
            self.game.screen.blit(self.blue_surf, self.blue_rect)
            self.game.screen.blit(self.text_surface_red, self.text_rect_red)
        else:
            self.hovering = False
            self.game.screen.blit(self.dark_green_surf, self.dark_green_rect)
            self.game.screen.blit(self.text_surface_white, self.text_rect_white) 