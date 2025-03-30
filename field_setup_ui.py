# -*- coding: utf-8 -*-
"""
Created on Fri May 21 23:48:07 2021

@author: Roel
"""

import pygame
# import first_names_men
# import surnames2 as surnames
import ai_formation as ai_for
import init_players_and_teams as initpat
import copy
import show_player_ui
import mult_ui as mu
import col
import sys

# pygame.init()
# screen =mu.screen
pitch,pitchx,pitchy = mu.pitch,mu.pitchx,mu.pitchy
# real_pitch  =mu.real_pitch
# scrwid =1900
# scrhei= 1200
scrwid,scrhei=mu.scrwid,mu.scrhei
bf = mu.bf # new font for buttons

# swap_button = mu.button("Swap",bf,(scrwid-720,0),240,40,screen)
# freekick_button = mu.button("Freekick",bf,(scrwid-1200,40),240,40,screen)
# corner_button = mu.button("Corner",bf,(scrwid-960,40),240,40,screen)
# penalty_button = mu.button("Penalty",bf,(scrwid-720,40),240,40,screen)

# button_list = [mu.quit_button,mu.back_button,swap_button,freekick_button,corner_button,penalty_button]
# for button in  button_list[2:]:
#     button.color2 = col.blue_purple
# first_names= first_names_men.first_names_men_list
# second_names = surnames.surnames_list

test_team = initpat.create_basic_team("Huizenhoog")
    
def swap_attr(object1,object2,attr):
    reserve = getattr(object1,attr)
    setattr(object1, attr , getattr(object2,attr))
    setattr(object2, attr , reserve)
    return (object1,object2)

def draw_rem_subs(nr_rem_subs,old_subs,rectangle_update_list,screen):
    if old_subs != nr_rem_subs and nr_rem_subs >= 0:
        sub_rect=pygame.Rect(mu.xrtf(0.05*1900+40),mu.yrtf(0.05*1200),mu.xrtf(320),mu.yrtf(40))
        pygame.draw.rect(screen,col.blue_dark,sub_rect) 
        mu.draw_message("Remaining substitutions: " + str(nr_rem_subs),0.05*scrwid+40,0.05*scrhei,col.black,screen)
        rectangle_update_list.append(sub_rect)
        old_subs= nr_rem_subs
    return  old_subs,rectangle_update_list
    
#Do we actually still use this function, or can we remove it?
def draw_variables(shlis,button_names,rectangle_update_list,color_circles,screen,real_pitch):
    text_line_1 = ["Age", "Nr", "Goal", "YC", "RC", "Inj", "Sus", "Keep","Def", "Mid", "Att","GK","FK","CK","Pen"]
    var_rect =pygame.Rect(0.05*scrwid+240,0.1*scrhei,50*(len(text_line_1)+1),30+30*len(shlis))
    pygame.draw.rect(screen,col.blue_dark,var_rect) 
    for k in range(len(shlis)): 
        name_txt = str(shlis[k].first_name) + " " + str(shlis[k].second_name)
        button_names.append(mu.button(name_txt, bf,(0.05*scrwid,0.1*scrhei+30*k+30), 240, 30, screen))
              
        
        mu.draw_message("Name", 0.05*scrwid, 0.1*scrhei,col.black,screen)    
    
    for i in range(len(text_line_1)):
        mu.draw_message(text_line_1[i], 0.05*scrwid+240+50*(i+1),0.1*scrhei,col.black,screen)     
    for i in range(len(text_line_1)):
        mu.draw_message(text_line_1[i], 0.05*scrwid+240+50*(i+1),0.1*scrhei,col.black,screen) 
    
    for j in range(len(shlis)):
         var_line_1 = [shlis[j].age,
              shlis[j].back_number, shlis[j].goals[1],shlis[j].yellow_cards[1],
              shlis[j].red_cards[1], shlis[j].injured,shlis[j].suspended,
              shlis[j].keep_val,shlis[j].def_val,
              shlis[j].mid_val,shlis[j].att_val,
              shlis[j].is_keeper,
              shlis[j].takes_freekick,shlis[j].takes_corner,shlis[j].takes_penalty]
         
         mu.number_circle(shlis[j],color_circles,screen,real_pitch) #add circles with number on pitch
         
         
         for i in range(len(text_line_1)):
             if not (i >= 7 and i <= 10):
                 mu.draw_message(str(var_line_1[i]),0.05*scrwid+240+50*(i+1),0.1*scrhei+30*j+30,col.black,screen)
             else:
                 mu.draw_message(mu.stint(var_line_1[i]), 0.05*scrwid+240+50*(i+1),0.1*scrhei+30*j+30,mu.red_green_line(var_line_1[i]*1000),screen) 
    rectangle_update_list.append(var_rect)
    return rectangle_update_list

def initial_draw(shlis,color_circles,text_line_1,screen,button_list,real_pitch):
    screen.fill(col.blue_dark) # draw background
    screen.blit(pitch,[pitchx,pitchy])# draw soccer pitch on right side
    button_names =[]
    # for button in button_list: # draw initial buttons
        # button.draw()
    for k in range(len(shlis)): 
        name_txt = str(shlis[k].first_name) + " " + str(shlis[k].second_name)
        button_names.append(mu.button(name_txt, bf,(0.05*scrwid,0.1*scrhei+30*k+30), 240, 30, screen))
        button_names[k].color2 = col.blue_purple  
        
        mu.draw_message("Name", 0.05*scrwid, 0.1*scrhei,col.black,screen)      
    
    for i in range(len(text_line_1)):
        mu.draw_message(text_line_1[i], 0.05*scrwid+240+50*(i+1),0.1*scrhei,col.black,screen)     
    for i in range(len(text_line_1)):
        mu.draw_message(text_line_1[i], 0.05*scrwid+240+50*(i+1),0.1*scrhei,col.black,screen) 
    
    for j in range(len(shlis)):
         var_line_1 = [shlis[j].age,
              shlis[j].back_number, shlis[j].goals[1],shlis[j].yellow_cards[1],
              shlis[j].red_cards[1], shlis[j].injured,shlis[j].suspended,
              shlis[j].keep_val,shlis[j].def_val,
              shlis[j].mid_val,shlis[j].att_val,
              shlis[j].is_keeper,
              shlis[j].takes_freekick,shlis[j].takes_corner,shlis[j].takes_penalty]
         
         mu.number_circle(shlis[j],color_circles,screen,real_pitch) #add circles with number on pitch
         
         
         for i in range(len(text_line_1)):
             if not (i >= 7 and i <= 10):
                 mu.draw_message(str(var_line_1[i]),0.05*scrwid+240+50*(i+1),0.1*scrhei+30*j+30,col.black,screen)
             else:
                 mu.draw_message(mu.stint(var_line_1[i]), 0.05*scrwid+240+50*(i+1),0.1*scrhei+30*j+30,mu.red_green_line(var_line_1[i]*1000),screen) 
    for button in button_list+button_names:
         button.draw()
         
    pygame.display.flip()
    return button_names

def main(showed_team,nr_rem_subs,color_circles):
    screen_1 = mu.screen_setup()
    screen = screen_1.scr 
    # scrwid,scrhei = mu.scrwid,mu.scrhei
    
    
    
    quit_button = mu.quit_button_function(screen)
    back_button = mu.back_button_function(screen)

    button_list = [quit_button,back_button]
    
    if showed_team.human == True:
        swap_button = mu.button("Swap",bf,(scrwid-720,0),240,40,screen)
        freekick_button = mu.button("Freekick",bf,(scrwid-1200,40),240,40,screen)
        corner_button = mu.button("Corner",bf,(scrwid-960,40),240,40,screen)
        penalty_button = mu.button("Penalty",bf,(scrwid-720,40),240,40,screen)
    
        button_list += [swap_button,freekick_button,corner_button,penalty_button]
        
    for button in  button_list[2:]:
        button.color2 = col.blue_purple
    
    # pitch,pitchx,pitchy = mu.pitch,mu.pitchx,mu.pitchy
    real_pitch = mu.draw_real_pitch(screen)
    
    clock = pygame.time.Clock()
    main_loop = 1
    runtime=0
    
    # time =0
    old_subs = 0
    shlis=showed_team.players #abbreviation for shorter notation
    # button_names = []
    cnb=[]
    var_line_1_list = [0]*(len(shlis))
    halo_or_not = [0]*len(shlis)
    released_circle = 1
    text_line_1 = ["Age", "Nr", "Goal", "YC", "RC", "Inj", "Sus", "Keep","Def", "Mid", "Att","GK","FK","CK","Pen"]
    
    button_names=initial_draw(shlis,color_circles,text_line_1,screen,button_list,real_pitch)
    # ai_for.print_team(showed_team)
    while main_loop == True:
        # print(clock.tick())
        runtime += 1
       
        rectangle_update_list=[]
        cnb = []
        
        var_line_1_list_old = copy.deepcopy(var_line_1_list)
        
        # draw section starts here
        
        for button in button_list+button_names:
            if button.draw_check():
                button.draw()
                rectangle_update_list.append(button.rect)
                
        for j in range(len(shlis)): # create list of variables per player to be displayed
            var_line_1_list[j] = [shlis[j].age,
                  shlis[j].back_number, shlis[j].goals[1],shlis[j].yellow_cards[1],
                  shlis[j].red_cards[1], shlis[j].injured,shlis[j].suspended,
                  shlis[j].keep_val,shlis[j].def_val,
                  shlis[j].mid_val,shlis[j].att_val,
                  shlis[j].is_keeper,
                  shlis[j].takes_freekick,shlis[j].takes_corner,shlis[j].takes_penalty]
             

             
            if var_line_1_list[j] != var_line_1_list_old[j] and var_line_1_list_old[j] != 0:
                reck_change= pygame.Rect(mu.xrtf(0.05*scrwid+240+40),mu.yrtf(0.1*scrhei+30*(j+1)),mu.xrtf(50*len(text_line_1)),mu.yrtf(30))
                pygame.draw.rect(screen,col.blue_dark,reck_change)
                rectangle_update_list.append(reck_change) 
                for i in range(len(text_line_1)):
                    if not (i >= 7 and i <= 10):
                        mu.draw_message(str(var_line_1_list[j][i]),0.05*scrwid+240+50*(i+1),0.1*scrhei+30*j+30,col.black,screen)
                    else:
                        mu.draw_message(mu.stint(var_line_1_list[j][i]), 0.05*scrwid+240+50*(i+1),0.1*scrhei+30*j+30,mu.red_green_line(var_line_1_list[j][i]*1000),screen)      
                rectangle_update_list.append(reck_change) 

        
        for event in pygame.event.get():

            main_loop  = mu.quit_game(event,quit_button) 
            if main_loop == False:
                pygame.quit()
                sys.exit(0)
            
            if event.type == pygame.MOUSEBUTTONUP:
                released_circle = 1
                if back_button.rect.collidepoint(event.pos):
                   main_loop = False
                
                if  showed_team.human == False:
                     for k in range(len(shlis)):
                         if button_names[k].rect.collidepoint(event.pos):
                             show_player_ui.main(shlis[k])
                             initial_draw(shlis, color_circles, text_line_1,screen,button_list,real_pitch)
                             # rectangle_update_list = draw_variables(shlis,button_names,rectangle_update_list,color_circles)
                             
                if showed_team.human == True:   #allow only teams coached by humans to be changed by humans
                
                    if  (swap_button.clicked,freekick_button.clicked,corner_button.clicked,penalty_button.clicked)==(0,0,0,0):
                         for k in range(len(shlis)):
                             if button_names[k].rect.collidepoint(event.pos):
                                 show_player_ui.main(shlis[k])
                                 initial_draw(shlis, color_circles, text_line_1,screen,button_list,real_pitch)
                                 # rectangle_update_list = draw_variables(shlis,button_names,rectangle_update_list,color_circles)
                                 
                 
                    if swap_button.rect.collidepoint(event.pos):
                        swap_button.clicked = 1 - swap_button.clicked
                        if swap_button.clicked == 0 and any([o.clicked for o in button_names]): 
                        #buttons of players not purple if no swapping is going on
                            for k in range(len(shlis)):
                                    button_names[k].clicked = 0
                    
                    if swap_button.clicked == 1: #swapping the buttons does not seem to work as intended
                        
                        cnb = [] #clicked_name_buttons abbreviated
                        for k in range(len(shlis)):
                            if button_names[k].rect.collidepoint(event.pos) and button_names[k].clicked ==0:
                                button_names[k].clicked =1
                            if button_names[k].clicked ==1:
                                cnb.append(k)
                        if len(cnb) == 2:
                            for l in cnb:
                                button_names[l].clicked =0
                            swap_button.clicked =0    
                            if (nr_rem_subs != 0 or shlis[cnb[0]].playing == shlis[cnb[1]].playing):
                                # associate buttons to players and swap them in the list in the team object
                                shlis[cnb[0]],shlis[cnb[1]]=ai_for.swap_players(shlis[cnb[0]],shlis[cnb[1]])
                                
                                
                                button_names=initial_draw(shlis,color_circles,text_line_1,screen,button_list,real_pitch)
                                
                                if shlis[cnb[0]].playing != shlis[cnb[1]].playing:
                                    nr_rem_subs -= 1
                        """
                        cnb = [] #clicked_name_buttons abbreviated
                        for k in range(len(shlis)):
                            if button_names[k].rect.collidepoint(event.pos) and button_names[k].clicked ==0:
                                button_names[k].clicked =1
                            if button_names[k].clicked ==1:
                                cnb.append(k)
                        if len(cnb) == 2:
                            for l in cnb:
                                button_names[l].clicked =0
                            swap_button.clicked =0    
                            if (nr_rem_subs != 0 or shlis[cnb[0]].playing == shlis[cnb[1]].playing):
                                # associate buttons to players and swap them in the list in the team object
                                shlis[cnb[0]],shlis[cnb[1]]=ai_for.swap_players(shlis[cnb[0]],shlis[cnb[1]])
                                button_names[cnb[0]].rend,button_names[cnb[1]].rend = button_names[cnb[1]].rend,button_names[cnb[0]].rend
                                for p in range(2):
                                    mu.number_circle(shlis[cnb[p]],color_circles,screen,real_pitch)
                                    new_rect = pygame.Rect(mu.xrtf(0),mu.yrtf(0),mu.xrtf(40),mu.yrtf(40))
                                    new_rect.center= (shlis[cnb[p]].position[0]*real_pitch.width+real_pitch.x,
                                               shlis[cnb[p]].position[1]*real_pitch.height+real_pitch.y-2)
                                    rectangle_update_list.append(new_rect)
                                    
                                if shlis[cnb[0]].playing != shlis[cnb[1]].playing:
                                    nr_rem_subs -= 1
                                screen.blit(pitch,[pitchx,pitchy]) # draw soccer pitch on right side
                                for j in range(len(shlis)):
                                    mu.number_circle(shlis[j],color_circles,screen,real_pitch) #add circles with number on pitch
                                for i in range(2):
                                    button_names[cnb[i]].draw()
                                    rectangle_update_list.append(button_names[cnb[i]].rect)
                                ai_for.print_team(showed_team)
                          """         
                               
                                
                                    
                    for btn in [[freekick_button,"takes_freekick"],[corner_button,"takes_corner"],
                                [penalty_button,"takes_penalty"]]:
                        if btn[0].rect.collidepoint(event.pos):
                            btn[0].clicked = 1 - btn[0].clicked
                        
                        if btn[0].clicked == 1:
                            for k in range(len(shlis)):       
                                if button_names[k].rect.collidepoint(event.pos) and shlis[k].playing ==1:
                                    for l in range(len(shlis)):  
                                        setattr(shlis[l],btn[1],0)
                                    setattr(shlis[k],btn[1],1)
                                    btn[0].clicked =0
                            
                                
                            
            old_subs,rectangle_update_list =draw_rem_subs(nr_rem_subs,old_subs,rectangle_update_list,screen)
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                for k in range(len(shlis)):   
                    bound_circle = pygame.draw.circle(screen, color_circles , (int(shlis[k].position[0]*real_pitch.width+real_pitch.x), 
                                            int(shlis[k].position[1]*real_pitch.height+real_pitch.y)), 15, 0)
                    if bound_circle.collidepoint(event.pos) and shlis[k].playing ==1:
                        released_circle = 0
                        moved_circle_index = k
            
            if not real_pitch.collidepoint(pygame.mouse.get_pos()):
                   released_circle = 1                        
            
            if released_circle ==0:
                (x,y) = pygame.mouse.get_pos()
                shlis[moved_circle_index].position = ((x-real_pitch.x)/real_pitch.width,(y-real_pitch.y)/real_pitch.height)
                screen.blit(pitch,[pitchx,pitchy])# draw soccer pitch on right side
                for j in range(len(shlis)):
                    mu.number_circle(shlis[j],color_circles,screen,real_pitch) #add circles with number on pitch
                rectangle_update_list.append(pygame.Rect(mu.pitchx,mu.pitchy,mu.pitch_width,mu.pitch_height)) 
        
            if event.type == pygame.MOUSEMOTION: #halo for player when their button is hovered over
                for k in range(len(shlis)):
                    if halo_or_not[k] != mu.hovers_mouse_over_rect(button_names[k].rect,event.pos):
                        mu.number_circle(shlis[k],color_circles,screen,real_pitch)
                        halo_or_not[k] = mu.hovers_mouse_over_rect(button_names[k].rect,event.pos)
                        if halo_or_not[k] == 1:
                            mu.halo(shlis[k],screen,real_pitch)
                        new_rect = pygame.Rect(0,0,40,40)
                        new_rect.center= (shlis[k].position[0]*real_pitch.width+real_pitch.x,shlis[k].position[1]*real_pitch.height+real_pitch.y-2)
                        rectangle_update_list.append(new_rect) 

        pygame.display.update(rectangle_update_list)

                
                                
    return(showed_team,nr_rem_subs)                            
                            
# test_team = ai_for.initial_setup(test_team, (4,3,3))                        
# a,b=main(test_team,1,col.blue_cyan)