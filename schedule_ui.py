# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 00:30:11 2021

@author: Gebruiker
"""

import pygame
import sys
import col
import mult_ui as mu

pygame.init()

# pygame.display.set_caption('Manager Madness')
# screen =mu.screen
scrwid,scrhei = mu.scrwid,mu.scrhei

bf = mu.bf # the new button font


def draw_screen(schedule,week_nr,screen,button_list):
    screen.fill(col.blue_dark)
    for i in range(len(schedule.weeks[week_nr])):
       mu.draw_message(str(schedule.weeks[week_nr][i].home_team.name),0.2*scrwid,0.1*scrhei+40*i,col.black,screen)
       mu.draw_message(str(schedule.weeks[week_nr][i].home_team_score),0.2*scrwid+240,0.1*scrhei+40*i,col.black,screen)
       mu.draw_message("-",0.2*scrwid+260,0.1*scrhei+40*i,col.black,screen)
       mu.draw_message(str(schedule.weeks[week_nr][i].away_team_score),0.2*scrwid+280,0.1*scrhei+40*i,col.black,screen)
       mu.draw_message(str(schedule.weeks[week_nr][i].away_team.name),0.2*scrwid+360,0.1*scrhei+40*i,col.black,screen)
       mu.draw_message("Week: " + str(week_nr+1),0.05*scrwid+40,0.05*scrhei,col.black,screen)
     
    for button in button_list:
        if not ((button.text =="Previous" and week_nr == 0) or (button.text =="Next" and week_nr == len(schedule.weeks)-1)):
            button.draw()
    pygame.display.flip()            
    return 

def main(teams,schedule,week_nr):
    screen_1 = mu.screen_setup()
    screen = screen_1.scr 
    # scrwid,scrhei = mu.scrwid,mu.scrhei
    
    previous_button = mu.button("Previous",bf,(1900-960,0),240,40,screen)
    next_button = mu.button("Next",bf,(1900-720,0),240,40,screen)
    quit_button = mu.quit_button_function(screen)
    back_button = mu.back_button_function(screen)
    button_list = [quit_button,back_button,previous_button,next_button]
    
    main_loop = 1
    runtime=0
    
    draw_screen(schedule,week_nr,screen,button_list)
    while main_loop == True:
        runtime += 1
        rectangle_update_list = []
        for button in button_list:
            if button.draw_check() and not ((button.text =="Previous" and week_nr == 0) or (button.text =="Next" and week_nr == len(schedule.weeks)-1)):
                button.draw()
                rectangle_update_list.append(button.rect)
        
        for event in pygame.event.get():
            main_loop  = mu.quit_game(event,quit_button) 
            if main_loop == False:
                pygame.quit()
                sys.exit(0)
            
            if event.type == pygame.MOUSEBUTTONUP:
                if back_button.rect.collidepoint(event.pos):
                    return()
                if next_button.rect.collidepoint(event.pos) and week_nr != len(schedule.weeks)-1:
                    week_nr +=1
                    draw_screen(schedule,week_nr,screen,button_list)
                if previous_button.rect.collidepoint(event.pos) and week_nr != 0:
                    week_nr -=1
                    draw_screen(schedule,week_nr,screen,button_list)
                    
                
        pygame.display.update(rectangle_update_list)
    return
                        
# main()