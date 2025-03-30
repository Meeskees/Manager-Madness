# -*- coding: utf-8 -*-
"""
Created on Wed May 12 22:08:31 2021

@author: Roel
"""

import pygame
import sys
import mult_ui as mu
import col
# only initialize when debugging
# pygame.init()
# pygame.display.set_caption('Manager Madness')
# screen =mu.screen
# scrwid= 1900
# scrhei = 1200

# bf = mu.bf

# clubbuttonlist = []
# quit_button = mu.quit_button

def main(teams):
    screen_1 = mu.screen_setup()
    screen = screen_1.scr 
    scrwid,scrhei = mu.scrwid,mu.scrhei

    bf = mu.bf

    clubbuttonlist = []
    quit_button = mu.quit_button_function(screen)
    
    
    main_loop = 1
    runtime=0
    for i in range(len(teams)):
        clubbuttonlist.append(mu.button(teams[i].name,bf,(0.2*scrwid,0.25*scrhei+40*i),240,40,screen))
    screen.fill(col.blue_dark)
        
    mu.draw_message('Welcome to Manager Madness! Pick a team: ',0.2*scrwid,0.1*scrhei,col.black,screen)
    for button in clubbuttonlist+[quit_button]:
        button.draw()
    pygame.display.flip()
    
    while main_loop == True:
        runtime += 1
        rectangle_update_list = []
        
        for button in clubbuttonlist+[quit_button]:
            if button.draw_check():
                button.draw()
                rectangle_update_list.append(button.rect)
        
        for event in pygame.event.get():
            main_loop  = mu.quit_game(event,quit_button) 
            if main_loop == False:
                pygame.quit()
                sys.exit(0)
            
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for check_club in clubbuttonlist:
                    if check_club.rect.collidepoint(event.pos):
                        check_club.clicked = 1
                        return(clubbuttonlist.index(check_club))
                    
        pygame.display.update(rectangle_update_list)
    return
                        
# main(teams)