# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 23:57:08 2021

@author: Roel
"""

import pygame
import sys
# import first_names_men
# import surnames2 as surnames
import ai_formation as ai_for
import init_players_and_teams as initpat
import mult_ui as mu
import match_markov_v2 as match
import field_setup_ui
import col
import loading_screen as ls

pygame.init()
# pygame.display.set_caption('Manager Madness')
# screen =mu.screen
pitch,pitchx,pitchy = mu.pitch,mu.pitchx,mu.pitchy
# real_pitch  =mu.real_pitch
scrwid,scrhei=mu.scrwid,mu.scrhei
# scrwid =1900
# scrhei= 1200

bf = mu.bf # new font for buttons

time_per_match_second = 20 #time in ms

MATCHSECOND = pygame.USEREVENT + 1
pygame.time.set_timer(MATCHSECOND,time_per_match_second)

# first_names= first_names_men.first_names_men_list
# second_names = surnames.surnames_list

test_team = initpat.create_basic_team("Huizenhoog")
test_team2= initpat.create_basic_team("Bomenbeukers")

test_team= ai_for.initial_setup(test_team,(4,3,3))
test_team2= ai_for.initial_setup(test_team2,(4,3,3))

# continue_button = mu.button("Continue",bf,(1900-480,0),240,40,screen)
# for player in test_team2.players:
#     print(player.is_keeper,player.is_defender,player.is_midfielder,player.is_attacker)

def string_double_digits(digit):
    if digit < 10 and digit >=0:
        return "0"+str(digit)
    else:
        return str(digit)
        

def draw_time(matchdata, rectangle_update_list,screen):
    time_rect=pygame.Rect(mu.xrtf(0.05*scrwid+120),mu.yrtf(0.1*scrhei+30),mu.xrtf(80),mu.yrtf(40))
    pygame.draw.rect(screen,col.blue_dark,time_rect) 
    mu.draw_message(str(matchdata.minute) +" : " + string_double_digits(matchdata.second),0.05*scrwid+120,0.1*scrhei+30,col.black,screen)
    rectangle_update_list.append(time_rect)
    return  rectangle_update_list

def draw_match_messages(matchdata, old_message,nr_messages_shown,rectangle_update_list,forced,screen):
    if matchdata.message[nr_messages_shown:] != old_message or matchdata.message[nr_messages_shown:] ==[] or forced == 1: 
        message_rect=pygame.Rect(mu.xrtf(0.05*scrwid+120),mu.yrtf(0.1*scrhei+30+80),mu.xrtf(800),mu.yrtf(40*nr_messages_shown))
        pygame.draw.rect(screen,col.blue_dark,message_rect) 
        for k in range(min(len(matchdata.message),nr_messages_shown)):
            mu.draw_message(str(matchdata.message[-1-k][0]) +" : " 
                         + string_double_digits(int(matchdata.message[-1-k][1])) + "   " 
                         + str(matchdata.message[-1-k][2]),0.05*scrwid+120,0.1*scrhei+30+80+40*k,col.black,screen)
        rectangle_update_list.append(message_rect)
        old_message = matchdata.message[nr_messages_shown:]
    
    return old_message,rectangle_update_list
    
def draw_scores(matchdata,old_score,rectangle_update_list,screen):
    if old_score != matchdata.score:
        score_rect=pygame.Rect(mu.xrtf(0.05*scrwid+400),mu.yrtf(0.1*scrhei+30),mu.xrtf(80),mu.yrtf(40))
        pygame.draw.rect(screen,col.blue_dark,score_rect) 
        mu.draw_message(str( matchdata.score[0]) +" - " + str( matchdata.score[1]),0.05*scrwid+400,0.1*scrhei+30,col.black,screen)
        rectangle_update_list.append(score_rect)
        old_score= matchdata.score.copy()
    return  old_score,rectangle_update_list

def draw_pitch(homelist,awaylist,rectangle_update_list,screen,real_pitch):
    pitch_rect = pygame.Rect(mu.xrtf(0.2*scrwid+800-54), mu.yrtf(0.1*scrhei+30), mu.xrtf(mu.pitch_width+108), mu.yrtf(mu.pitch_height) )
    pygame.draw.rect(screen,col.blue_dark,pitch_rect)
    screen.blit(pitch,[pitchx,pitchy])# draw soccer pitch on right side
    for j in range(len(homelist)):
        mu.number_circle(homelist[j],col.blue_cyan,screen,real_pitch) #add circles with number on pitch
    for j in range(len(awaylist)):
        mu.number_circle(awaylist[j],col.red,screen,real_pitch) #add circles with number on pitch
    
    rectangle_update_list.append(pitch_rect)
    return rectangle_update_list

def main(matchdata):
    screen_1 = mu.screen_setup()
    screen = screen_1.scr 
    scrwid,scrhei = mu.scrwid,mu.scrhei
    
    real_pitch = mu.draw_real_pitch(screen)
    
    clock = pygame.time.Clock()
    main_loop = 1
    runtime=0
    secpermin =60
    minpermatch = 90
    match_over = 0
    nr_messages_shown =10
    # matchdata = match.class_matchdata(home_team,away_team)
    # time =0
    home_team = matchdata.home_team
    away_team = matchdata.away_team
    homelist=home_team.players #abbreviation for shorter notation
    awaylist=away_team.players #abbreviation for shorter notation
    home_team,away_team = match.setup_start(home_team,away_team)
    home_team = match.stats_begin(home_team)
    away_team = match.stats_begin(away_team)

    home_team_button = mu.button(str(home_team.name),bf,(scrwid-960,0),240,40,screen)
    away_team_button = mu.button(str(away_team.name),bf,(scrwid-720,0),240,40,screen)
    
    continue_button = mu.button("Continue",bf,(1900-480,0),240,40,screen)
    
    quit_button = mu.quit_button_function(screen)
    button_list = [quit_button,home_team_button,away_team_button]
    for button in  button_list[2:]:
        button.color2 = col.blue_purple
    
    screen.fill(col.blue_dark) # draw background
    screen.blit(pitch,[pitchx,pitchy])
    for button in button_list: # draw initial buttons
        button.draw()
        
    mu.draw_message(home_team.name, 0.05*scrwid+240,0.1*scrhei+30,col.black,screen)   
    mu.draw_message(away_team.name, 0.05*scrwid+480,0.1*scrhei+30,col.black,screen)
    mu.draw_message(str(0) +" - " + str(0),0.05*scrwid+400,0.1*scrhei+30,col.black,screen)
    rectangle_update_list= draw_pitch(homelist, awaylist,[],screen,real_pitch)
    
    old_score = [0,0]
    old_possession = matchdata.possession
    old_message = matchdata.message

    pygame.display.flip()
    while main_loop == True:
        # print(clock.tick())
        runtime += 1  
        rectangle_update_list=[]
        
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
                
                if continue_button.rect.collidepoint(event.pos):
                    main_loop = False
                    ls.main()
                # if mu.back_button.rect.collidepoint(event.pos):
                #     return matchdata
                    # print("Home team:")
                    # for i in home_team.players[:11]:
                    #     print(i.first_name+ " " + i.second_name)
                    # print("Away team:")
                    # for i in away_team.players[:11]:
                    #     print(i.first_name+ " " + i.second_name)
                    # print("Back!")
                
                for tsuc in [[home_team,home_team_button,0,matchdata.home_team,col.blue_cyan],[away_team,away_team_button,1,matchdata.away_team,col.red]]: # tsuc stands for team_set_up_clicking
                    if tsuc[1].rect.collidepoint(event.pos): #go to home team setup screen
                        tsuc[0],matchdata.substitutions[tsuc[2]] = field_setup_ui.main(tsuc[3],tsuc[0].substitutions,tsuc[4])
                        screen.fill(col.blue_dark)
                        mu.draw_message(home_team.name, 0.05*scrwid+240,0.1*scrhei+30,col.black,screen)   
                        mu.draw_message(away_team.name, 0.05*scrwid+480,0.1*scrhei+30,col.black,screen)
                        mu.draw_message(str(matchdata.score[0]) +" - " + str(matchdata.score[1]),0.05*scrwid+400,0.1*scrhei+30,col.black,screen)
                        for button in button_list: # draw initial buttons
                            button.draw()
                        old_message,rectangle_update_list=draw_match_messages(matchdata, old_message
                                                                          ,nr_messages_shown,rectangle_update_list,1,screen)
                        rectangle_update_list= draw_pitch(homelist, awaylist,rectangle_update_list,screen,real_pitch)
                        pygame.display.flip()
                
            if event.type == MATCHSECOND: 
                if matchdata.second == secpermin-1:
                    matchdata.minute +=1
                    matchdata.second =0
                    for team in [matchdata.home_team,matchdata.away_team]: #stamina calculations once per game minute
                        team= match.stats_after_stamina(team,minpermatch)
                        if team.human ==0:
                            team.substitutions,matchdata=ai_for.substition_check(team,(matchdata.minute,minpermatch),team.substitutions,matchdata)
                    # do here the substitution stuff
                    
                if matchdata.minute != minpermatch:
                    matchdata=match.match_second(matchdata)
                    matchdata.second +=1
                elif match_over == 0: # things to do when the match is over
                    home_team =match.stats_begin(home_team)
                    away_team =match.stats_begin(away_team)
                    home_team =match.injuries_passing(home_team)
                    away_team =match.injuries_passing(away_team)
                    for player in away_team.players:
                        player.position = [1-player.position[0],1-player.position[1]]
                    continue_button.draw()
                    button_list.append(continue_button)
                    rectangle_update_list.append(continue_button.rect)
                    match_over =1
                
                rectangle_update_list=draw_time(matchdata, rectangle_update_list,screen)
                old_message,rectangle_update_list=draw_match_messages(matchdata, old_message
                                                                      ,nr_messages_shown,rectangle_update_list,0,screen)
                old_score,rectangle_update_list = draw_scores(matchdata,old_score,rectangle_update_list,screen)
                
              
                for shlis in [home_team.players,away_team.players]:
                    if old_possession != matchdata.possession:
                        mu.number_circle(old_possession,old_possession.color,screen,real_pitch)
                        mu.number_circle(matchdata.possession,matchdata.possession.color,screen,real_pitch)
                        mu.halo(matchdata.possession,screen,real_pitch)
                        # new_rect1 = pygame.Rect(mu.xrtf(0),mu.yrtf(0),mu.xrtf(40),mu.yrtf(40))
                        new_rect1 = pygame.Rect(mu.xrtf(0),mu.yrtf(0),mu.xrtf(60),mu.yrtf(60))
                        new_rect1.center= (old_possession.position[0]*real_pitch.width+real_pitch.x,
                                           old_possession.position[1]*real_pitch.height+real_pitch.y-2)
                        # new_rect2 = pygame.Rect(mu.xrtf(0),mu.yrtf(0),mu.xrtf(40),mu.yrtf(40))
                        new_rect2 = pygame.Rect(mu.xrtf(0),mu.yrtf(0),mu.xrtf(60),mu.yrtf(60))
                        new_rect2.center= (matchdata.possession.position[0]*real_pitch.width+real_pitch.x,
                                           matchdata.possession.position[1]*real_pitch.height+real_pitch.y-2)
                        rectangle_update_list.append(new_rect1) 
                        rectangle_update_list.append(new_rect2)
                        old_possession = matchdata.possession

        pygame.display.update(rectangle_update_list)
        clock.tick(60)                
                            
    return matchdata                            

# test_team.human = 1                            
# matchdata = match.class_matchdata(test_team,test_team2)                        
# main(matchdata)