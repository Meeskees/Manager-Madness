# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 21:16:50 2021

@author: Gebruiker
"""
import pygame
import col
from win32api import GetSystemMetrics

pygame.init()
scrwid = 1900
scrhei = 1200

class screen_setup:
    def __init__(self):
        self.scr = pygame.display.set_mode([GetSystemMetrics(0),GetSystemMetrics(1)])
        pygame.display.set_caption('Manager Madness')



def xrtf(x): #gives the right horizontal position wrt 1900:full
    scrwid_real = GetSystemMetrics(0)
    return int(x*scrwid_real/scrwid)

def yrtf(y): #gives the right vertical position wrt 1200:full
    scrhei_real = GetSystemMetrics(1)
    return int(y*scrhei_real/scrhei)

def quit_game(event,quit_button):
    if (event.type == pygame.QUIT or #close when escape or quit button is pressed 
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or 
                (event.type == pygame.MOUSEBUTTONUP and quit_button.rect.collidepoint(event.pos))):
        pygame.quit(); 
        return(False)
    return(True)

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
        self.text = text
        self.pos = [xrtf(pos[0]),yrtf(pos[1])]
        self.width= xrtf(width)
        self.height = yrtf(height)
        self.screen = screen
        self.clicked = 0
        self.click_status = 0
        self.hover_status =0 
        self.color1 = col.black
        self.color2 = col.black
        self.font = font
        self.rend = self.font.render(self.text, True, col.white)
        self.rect = pygame.Rect(self.pos[0],self.pos[1],self.width,self.height)
        
    def draw(self):
        if self.clicked == 0:
            pygame.draw.rect(self.screen,self.color1,self.rect)
        if self.clicked == 1:
            pygame.draw.rect(self.screen,self.color2,self.rect)     
        self.screen.blit(self.rend,(self.rect.x+0.2*self.width,self.rect.y+0.2*self.height))
        mouse_pos=pygame.mouse.get_pos()
        # if hovers_mouse_over_rect(self.rect,mouse_pos) == True and self.hover_status ==0:
        if hovers_mouse_over_rect(self.rect,mouse_pos) == True:
            draw_transparent_rect(self.rect,col.white,128,self.screen)
        return
    
    def draw_check(self):
        mouse_pos=pygame.mouse.get_pos()
        if (self.click_status,self.hover_status) == (self.clicked,hovers_mouse_over_rect(self.rect,mouse_pos)):
            return 0 # the rectangle does not need to be updated
        else:
            self.click_status,self.hover_status = self.clicked,hovers_mouse_over_rect(self.rect,mouse_pos)
            return 1 # the rectangle needs to be updated   
        
        

pitch = pygame.image.load("soccerpitch.jpg")
pitchx = xrtf(0.2*1900+800)
pitchy = yrtf(0.1*1200+30)
(pitch_width,pitch_height) = pitch.get_size()
pitch = pygame.transform.scale(pitch,(xrtf(pitch_width),yrtf(pitch_height)))
(pitch_width,pitch_height) = pitch.get_size()
def draw_real_pitch(screen):
    return pygame.draw.rect(screen, col.black, (pitchx+xrtf(24),pitchy+yrtf(30),pitch_width-xrtf(54),pitch_height-yrtf(52)),1)

bf = pygame.font.SysFont("calisto", xrtf(18)) #new font size buttons
def quit_button_function(screen):
    return button("Quit",bf,(1900-240,0),240,40,screen)

def back_button_function(screen):
    return button("Back",bf,(1900-480,0),240,40,screen)

def draw_message(message, x,y,color,screen):#draw_message in color
    font = pygame.font.SysFont("Georgia", xrtf(20),True)
    message_0 = font.render(message,1,color)
    screen.blit(message_0, (xrtf(x),yrtf(y)))
    return

def number_circle(player,color_circles,screen,real_pitch):
    pygame.draw.circle(screen, color_circles , (int(player.position[0]*real_pitch.width+real_pitch.x), 
                             int(player.position[1]*real_pitch.height+real_pitch.y)), 15, 0)
    font= pygame.font.SysFont("Georgia",xrtf(22),True)
    numbertext = font.render(str(player.back_number),1,col.white)
    screen.blit(numbertext,numbertext.get_rect(
        center=(int(player.position[0]*real_pitch.width+real_pitch.x),
                int(player.position[1]*real_pitch.height+real_pitch.y-2))))
    return

def stint(number): #turns number between 0 and 1 into one string between 0 and 1000
    return(str(int(1000*number)))

def halo(player,screen,real_pitch):
    pygame.draw.circle(screen, col.yellow , (int(player.position[0]*real_pitch.width+real_pitch.x), 
                                            int(player.position[1]*real_pitch.height+real_pitch.y)), 15, 5)
    font= pygame.font.SysFont("Georgia",xrtf(22),True)
    numbertext = font.render(str(player.back_number),1,col.white)
    screen.blit(numbertext,numbertext.get_rect(
        center=(player.position[0]*real_pitch.width+real_pitch.x,
                player.position[1]*real_pitch.height+real_pitch.y-2)))
    return

def red_green_line(slidenr):# 0 is red, 1000 is green
    if slidenr < 500:
        return ( 204,int(204*slidenr/500),0)
    else:
        return ( int(204*(1000-slidenr)/500),204,0)