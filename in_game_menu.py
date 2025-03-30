# -*- coding: utf-8 -*-
"""
Created on Wed May 12 23:50:00 2021

@author: Roel
"""

import pygame
from sys import exit
import col
import mult_ui as mu
import field_setup_ui
import choose_team_v2
import schedule_season as sse
import play_round as pr
import league_table_ui as ltu
import init_players_and_teams as initpat
import schedule_ui
import loading_screen as ls

# only initialize when debugging
# pygame.init()
# pygame.display.set_caption('Manager Madness')
# screen =mu.screen
# scrwid= 1900
# scrhei = 1200

def basic_flip(team,button_list,screen):
    screen.fill(col.blue_dark)
    mu.draw_message('Your team is ' + team.name,0.2*mu.scrwid,0.1*mu.scrhei,col.black,screen)
    mu.draw_message('What do you want to do?',0.2*mu.scrwid,0.2*mu.scrhei,col.black,screen)
    for button in button_list:
        button.draw()
    pygame.display.flip()
    return

def main():
    pygame.init()
    pygame.display.set_caption('Manager Madness')
    screen_1 = mu.screen_setup()
    screen = screen_1.scr 
    scrwid,scrhei = mu.scrwid,mu.scrhei
    
    bf= mu.bf # new font for buttons
    quit_button = mu.quit_button_function(screen)
    play_button = mu.button("Play",bf,(0.2*scrwid,0.3*scrhei),240,40,screen)
    setup_button = mu.button("Setup",bf,(0.2*scrwid,0.3*scrhei+40),240,40,screen)
    table_button = mu.button("League Table",bf,(0.2*scrwid,0.3*scrhei+80),240,40,screen)
    schedule_button = mu.button("Schedule",bf,(0.2*scrwid,0.3*scrhei+120),240,40,screen)
    
    button_list = [quit_button,play_button,setup_button,table_button,schedule_button]
    
    # team = teams[0]
    # for i in teams:
    #     if i.human == 1:
    #         team = i
    teams = [0]*len(initpat.teamsv0)
    for i in range(len(initpat.teamsv0)):
        teams[i] = initpat.create_basic_team(initpat.teamsv0[i])
        
    team_number= choose_team_v2.main(teams)
    team = teams[team_number]
    team.human = 1
    
    schedule = sse.make_schedule(teams)
    week_nr = 0
    
    clock = pygame.time.Clock()
    main_loop = 1
    runtime=0
    basic_flip(team,button_list,screen)
    
    while main_loop == True:
        # print(clock.tick())
        runtime += 1
        reflip =0 
        rectangle_update_list = []
        
        for button in button_list:
            if button.draw_check():
                button.draw()
                rectangle_update_list.append(button.rect)
        
        for event in pygame.event.get():
            main_loop  = mu.quit_game(event,quit_button) 
            if main_loop == False:
                pygame.quit()
                exit(0)
            
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                
                if setup_button.rect.collidepoint(event.pos):
                     team,placeholder = field_setup_ui.main(team,-1,col.blue_cyan)
                     reflip = 1
                
                if table_button.rect.collidepoint(event.pos):
                    ltu.main(teams)
                    reflip = 1
                
                if play_button.rect.collidepoint(event.pos):
                    ls.main()
                    pr.play_competition(schedule,len(teams),week_nr)
                    week_nr +=1
                    reflip = 1
                
                if schedule_button.rect.collidepoint(event.pos):
                    schedule_ui.main(teams,schedule,week_nr)
                    reflip = 1
                    
                if reflip == 1:
                    basic_flip(team,button_list,screen)
                    reflip = 0
                    
        pygame.display.update(rectangle_update_list)
                        
# main('Zwaluwen')
main()