# -*- coding: utf-8 -*-
"""
Created on Thu May 13 00:18:35 2021

@author: Roel
"""

import pygame
import sys
import col
import mult_ui as mu

# pygame.init()

# pygame.display.set_caption('Manager Madness')
# screen =mu.screen
# scrwid= 1900
# scrhei = 1200

# bf = mu.bf # the new button font



def make_sorted_table(teams):
    table = []
    for i in range(len(teams)):
        table.append([0,teams[i].name,teams[i].wins[1],teams[i].draws[1],teams[i].losses[1], 3*teams[i].wins[1]+1*teams[i].draws[1]
                     ,teams[i].goals_for[1]-teams[i].goals_against[1],teams[i].goals_for[1],teams[i].goals_against[1]])
    table=sorted(table, key=lambda tup: (-tup[5],-tup[6],-tup[7],-tup[2],tup[1]))
    for i in range(len(teams)):
       table[i][0]=i+1
    return(table)

def main(teams):
    screen_1 = mu.screen_setup()
    screen = screen_1.scr 
    scrwid,scrhei = mu.scrwid,mu.scrhei
    
    quit_button = mu.quit_button_function(screen)
    back_button = mu.back_button_function(screen)
    button_list = [quit_button,back_button]
    
    main_loop = 1
    runtime=0
    table = make_sorted_table(teams)
    
    screen.fill(col.blue_dark)
    for i in range(len(teams)):
            mu.draw_message(str(table[i][0]),0.2*scrwid,0.1*scrhei+40*i,col.black,screen)
            mu.draw_message(str(table[i][1]),0.2*scrwid+80,0.1*scrhei+40*i,col.black,screen)
            for j in range(2,9):
                mu.draw_message(str(table[i][j]),0.2*scrwid+320+80*j,0.1*scrhei+40*i,col.black,screen)
                
    for button in button_list:
        button.draw()
    pygame.display.flip()
    
    while main_loop == True:
        runtime += 1
        rectangle_update_list = []
        for button in button_list:
            if button.draw_check():
                button.draw()
                rectangle_update_list.append(button.rect)
        
        for event in pygame.event.get():
            main_loop  = mu.quit_game(event,quit_button) 
            if main_loop == False:
                pygame.quit()
                sys.exit(0)
            
            if event.type == pygame.MOUSEBUTTONUP:
                if back_button.rect.collidepoint(event.pos):
                    print('Back')
                    return()
        pygame.display.update(rectangle_update_list)
                        
# main()