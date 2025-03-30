# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:08:22 2019

@author: Gebruiker
"""

import init_players_and_teams as initpat

def send_message(matchdata, str_message):
    matchdata.message.append([str(matchdata.minute),str(matchdata.second),str_message])
    return matchdata

def swap_attr(object1,object2,attr):
    reserve = getattr(object1,attr)
    setattr(object1, attr , getattr(object2,attr))
    setattr(object2, attr , reserve)
    return (object1,object2)

def swap_players(player1,player2):
    player1,player2=player2,player1
    #change some values to other player (like position)
    change_var = ["playing","is_keeper","is_defender", "is_midfielder", "is_attacker", "takes_freekick","takes_corner","takes_penalty", "position"]
    for i in range(len(change_var)):
       player1,player2 = swap_attr(player1,player2,change_var[i])
    return player1,player2

def initial_setup_players(team,crit_val,task,start_nr,end_nr):
    for i in range(start_nr,end_nr):
        player_nr = i
        setattr(team.players[i],task,1)
        for j in range(i,len(team.players)):
            if getattr(team.players[j],crit_val)  > getattr(team.players[player_nr],crit_val) and team.players[j].suspended == 0:
                    player_nr = j
        team.players[i],team.players[player_nr]=swap_players(team.players[i],team.players[player_nr])
    # best players central:
    for k in range(3,6):
        if end_nr - start_nr == k:
            team.players[start_nr],team.players[start_nr+k-2]=swap_players(team.players[start_nr],team.players[start_nr+k-2])
    if end_nr - start_nr == 5:
        team.players[start_nr],team.players[start_nr+4]=swap_players(team.players[start_nr],team.players[start_nr+4])
    return team

def set_piecetaker(team,set_piece,crit_val):
    piecetaker = 0 
    for player in team.players:
        setattr(player,set_piece,0)
        if piecetaker ==0:
            piecetaker = player
        if getattr(player,crit_val)[0] > getattr(piecetaker,crit_val)[0] and player.playing ==1:
            piecetaker =player
    setattr(piecetaker,set_piece,1)
    return team

def initial_setup(team,strat):
    tasks = ["is_keeper","is_defender","is_midfielder","is_attacker"]
    for player in team.players:
        for task in tasks:
            setattr(player,task,0)
    for [a,b,c,d] in [["keep_val","is_keeper",0,1],["def_val","is_defender",1,strat[0]+1],
                    ["mid_val","is_midfielder",strat[0]+1,strat[0]+strat[1]+1],
                    ["att_val","is_attacker",strat[0]+strat[1]+1,strat[0]+strat[1]+strat[2]+1]]:
        team = initial_setup_players(team,a,b,c,d)
    for [a,b] in [["takes_freekick","freekick_accuracy"],["takes_corner","corner_accuracy"],
                  ["takes_penalty","penalty_accuracy"]]:
        team = set_piecetaker(team,a,b)
    return team            

def find_player(team,player):
    for i in range(len(team.players)):
        if team.players[i] == player:
            return i
    return 0

def substitute_picked_player(team,picked_player):
    pos_skills={"is_keeper":"keep_val","is_defender":"def_val","is_midfielder":"mid_val","is_attacker":"att_val"}
    # i= find_player(team,picked_player)
    possible_substitutes =[]
    for player in team.players:
        initpat.update_vals(player)
        if player.playing ==0 and player.suspended ==0:
            possible_substitutes.append(player)
    for task in pos_skills:
        if getattr(player,task) == 1:
            possible_substitutes = sorted(possible_substitutes,key=lambda pos_sub: getattr(pos_sub,pos_skills[task]))  
            if getattr(possible_substitutes[0],pos_skills[task]) > getattr(picked_player,pos_skills[task]):
                i = find_player(team,picked_player)
                j = find_player(team,possible_substitutes[0])
                team.players[i],team.players[j] = swap_players(team.players[i],team.players[j])
                return(1)
    return(0)

def get_player_task(player):
    pos_skills={"is_keeper":"keep_val","is_defender":"def_val","is_midfielder":"mid_val","is_attacker":"att_val"}
    for task in pos_skills:
        if getattr(player,task) == 1:
            return task
    return 0
    

def player_match_val(player,skill,time_to_play):
    pos_skills={"is_keeper":"keep_val","is_defender":"def_val","is_midfielder":"mid_val","is_attacker":"att_val"}
    current_val = getattr(player, pos_skills[skill])
    
    inj_fac = 3/(player.injured+3)
    end_val = current_val-time_to_play[0]*inj_fac*(1-player.stamina[0])*current_val/(4*time_to_play[1])
    
    return current_val+end_val
    

def worst_best_playing_players(team,time_to_play):
    worst_to_best_on_field = []
    for player in team.players:
        if player.playing == 1:
            initpat.update_vals(player)
            worst_to_best_on_field.append(player)
    return sorted( worst_to_best_on_field, key=lambda player: player_match_val(player,get_player_task(player),time_to_play))
   

def find_best_substitute(team,player,time_to_play):
    best_not_on_field = player
    for substitute in team.players:
        initpat.update_vals(substitute)
        if substitute.playing ==0:
            # print("Player: " + str(player_match_val(best_not_on_field, get_player_task(player), time_to_play)))
            # print("Substitute: " + str(player_match_val(substitute, get_player_task(player), time_to_play)))
            # if average (in time) and start of substitute is better than current player, replace current player
            if (player_match_val(best_not_on_field, get_player_task(player),time_to_play) < player_match_val(substitute, get_player_task(player),time_to_play) and
                player_match_val(best_not_on_field, get_player_task(player),(0,1)) < player_match_val(substitute, get_player_task(player),(0,1))):
                best_not_on_field = substitute
    return best_not_on_field

def substition_check(team,time_to_play,nr_subs,matchdata):
    worst_to_best_on_field =  worst_best_playing_players(team,time_to_play)
    for player in worst_to_best_on_field:
        best_substitute=find_best_substitute(team,player,time_to_play)
        if player != best_substitute and nr_subs >0:
            i = find_player(team,player)
            j = find_player(team,best_substitute)
            matchdata = send_message(matchdata, str(team.players[j].first_name) + " " + str(team.players[j].second_name) + " replaces " +str(team.players[i].first_name) + " " + str(team.players[i].second_name) + " (" + str(team.name) +")")
            team.players[i],team.players[j] = swap_players(team.players[i],team.players[j])
            nr_subs -=1
            
    return(nr_subs,matchdata)
    


def print_team(team):
    for player in  team.players:
        print(player.first_name,player.second_name,"("+ str(player.back_number) + ")", player.playing,"|",player.is_keeper,player.is_defender,player.is_midfielder,player.is_attacker)
    return



# test_team=initpat.create_basic_team("Hopentjes")  
# test_team = initial_setup(test_team,(3,3,4))
# print_team(test_team)
# for player in worst_best_playing_players(test_team,(30,90)):
#     print(player.first_name,player.second_name,player_match_val(player,(30,90)))
# test_team = initial_setup(test_team,(3,3,4))
# print(test_team.players[3].first_name)
# substitute_injured_player(test_team, test_team.players[3])
       