# -*- coding: utf-8 -*-
"""
Created on Wed May 12 21:44:30 2021

@author: Roel
"""

import pygame
import col

pygame.init()

# "Colors"
# black = (23,23,23)
# white = (254,254,254)
# green = (31,122,20)


button_font = pygame.font.SysFont("calisto", 18) #the used font (currently for everything)


def hovers_mouse_over_rect(rectangle,mouse_pos):#checks if the mouse is on the rectangle
    if mouse_pos[0] >= rectangle.x and mouse_pos[0] <= rectangle.x+rectangle.width:
        if mouse_pos[1] >= rectangle.y and mouse_pos[1] <= rectangle.y+rectangle.height:
            return True        
    return False

def draw_transparent_rect(rectangle,color,alpha_level,screen):#draws a transparent rectangle
    new_rectangle= pygame.Surface((rectangle.width,rectangle.height))
    new_rectangle.set_alpha(alpha_level)
    new_rectangle.fill(color)
    screen.blit(new_rectangle,(rectangle.x,rectangle.y))
    return

class button: #class for all buttons; changes color when hovered over
    
    def __init__(self,text,font,pos,width,height,screen):
        # self.rendered_text=rendered_text
        self.text = text
        self.pos = pos
        self.width=width
        self.height = height
        self.screen = screen
        # self.set_rect()
        # self.draw()
        self.clicked = 0
        self.click_status = 0
        self.hover_status =0 
        self.color1 = col.black
        self.color2 = col.black
        # self.change_rect_color()
        self.font = font
        self.rend = self.font.render(self.text, True, col.white)
        self.rect = pygame.Rect(self.pos[0],self.pos[1],self.width,self.height)
        
    def draw(self):
        # self.set_rend()
        if self.clicked == 0:
            pygame.draw.rect(self.screen,self.color1,self.rect)
            # self.click_status = 0
        # if self.clicked == 1 != self.click_status:
        if self.clicked == 1:
            pygame.draw.rect(self.screen,self.color2,self.rect)     
        self.screen.blit(self.rend,(self.rect.x+0.2*self.width,self.rect.y+0.2*self.height))
        mouse_pos=pygame.mouse.get_pos()
        if hovers_mouse_over_rect(self.rect,mouse_pos) == True and self.hover_status ==0:
            draw_transparent_rect(self.rect,col.white,128,self.screen)
            # self.hover_status = 1
        # else:
            # self.hover_status = 0
        
        if (self.click_status,self.hover_status) == (self.clicked,hovers_mouse_over_rect(self.rect,mouse_pos)):
            return 0 # the rectangle does not need to be updated
        else:
            self.click_status,self.hover_status = self.clicked,hovers_mouse_over_rect(self.rect,mouse_pos)
            return 1 # the rectangle needs to be updated
    # def set_rend(self):
    #     
        
    # def set_rect(self):
        # self.set_rend()
        
        

                
            
        

