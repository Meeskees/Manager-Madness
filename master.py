# -*- coding: utf-8 -*-
"""
Created on Thu May 13 00:20:54 2021

@author: Roel
"""
from sys import exit
import pygame
import choose_team_v2
import in_game_menu
# import schedule_season as sse
# import play_round as pr
# import league_table_ui as ltu
import init_players_and_teams as initpat
# import loading_screen


pygame.init()
teams = [0]*len(initpat.teamsv0)
for i in range(len(initpat.teamsv0)):
    teams[i] = initpat.create_basic_team(initpat.teamsv0[i])
    
team_number= choose_team_v2.main(teams)
teams[team_number].human = 1

# schedule = sse.make_schedule(teams)
week_nr = 0
menu_screen = 1
# print(menu_screen)
play = 0
while menu_screen != 0:
    # print(menu_screen)
    if menu_screen ==1:
        menu_screen = in_game_menu.main(teams)
    
    # if menu_screen == 3:
    #     pr.play_competition(schedule,len(teams),week_nr)
    #     week_nr +=1
    #     # choice =0
    #     menu_screen =1
        
    # if menu_screen ==2:
    #     menu_screen=ltu.main(teams)




pygame.quit() 
exit()