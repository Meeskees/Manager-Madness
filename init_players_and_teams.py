# -*- coding: utf-8 -*-
"""
Created on Thu May 13 00:30:36 2021

@author: Roel
"""

import random
import first_names_men
import surnames2 as surnames

first_names= first_names_men.first_names_men_list
second_names = surnames.surnames_list
teamsv0= ["Victorie", "Fc Knudde", "FC de Kampioenen", "Swift Boys", "Lazio Roma", "FC Emmen","Top Oss",
          "SVO Oosterend", "Full Speed", "All Stars","Lions", "Triomftankers","Puntertjes", "Fortuna Sittard", "PSV", "FC Barcelona", "Hoezee!","Zegeridders"]

class player:
    """ PLAYER CLASS WIL GRAAG EEN DOCSTRING HEBBEN """
    def __init__(self):
        self.first_name = random.choice(first_names)
        self.second_name = random.choice(second_names)
        self.id_number =0
        self.back_number = 0
        self.age = random.randrange(17,36)
        self.goals = [0]*3 #current,season and total
        self.yellow_cards = [0]*3 #current,season and total
        self.red_cards = [0]*3 #current,season and total
        self.injured =0
        self.suspended =0
#        self.shooting = random.random()
        self.shooting = [random.random()]*2
        self.heading = [random.random()]*2
        self.long_pass = [random.random()]*2
        self.short_pass = [random.random()]*2
        self.interception = [random.random()]*2
        self.goal_keeping = [random.random()]*2
        self.stamina = [random.random()]*2
        self.opportunism = [random.random()]*2
        self.aggression = [random.random()]*2
        self.positioning = [random.random()]*2
        self.freekick_accuracy = [random.random()]*2        
        self.corner_accuracy = [random.random()]*2
        self.penalty_accuracy = [random.random()]*2
        self.ball_control = [random.random()]*2
#        self.ball_control =[0.999,0.999]
        self.takes_freekick =0
        self.takes_corner =0 
        self.takes_penalty =0
        self.is_keeper =0
        self.playing = 0
        self.position = [0,0] #position on field
        self.possession_count =0#counts how many times the player has had the ball
        self.home_or_away =0 #home or away in matches
        self.teamid =0 # gives id of the team player is in
        self.color =(0,0,0)
        self.keep_val = self.keeper_value()
        self.def_val = defender_value(self)
        self.mid_val = midfielder_value(self)
        self.att_val = attacker_value(self)
        self.is_defender = 0
        self.is_midfielder = 0
        self.is_attacker =0
        
    def renew_vals(self):
        self.keep_val = self.keeper_value()
        self.def_val = defender_value(self)
        self.mid_val = midfielder_value(self)
        self.att_val = attacker_value(self)
        return
    
    def keeper_value(self):
        """ Method to USE MATHEMATHICS TO FIND keeper value based on blablabla 
        Mischa was here """ 
        a=0.7*self.goal_keeping[0]+0.10*self.stamina[0]+0.05*(1-self.opportunism[0])+0.05*(1-self.aggression[0])
        return a+0.03*self.short_pass[0]+0.05*self.long_pass[0]+0.02*self.ball_control[0]

class team:
    def __init__(self,name,players):
        self.name = name
        # self.id_number =id_nr
        self.players=players
        self.set_up = [[0,1/2,0],[1,1/7,3/10],[2,2/5,1/4],[3,3/5,1/4],[4,6/7,3/10],[5,1/6,1/2],[6,1/2,1/2],[7,5/6,1/2],[8,1/6,3/4],[9,1/2,3/4],[10,5/6,3/4]]
        for i in range(len(self.set_up)):
            self.set_up[i][0] = players[i].id_number
        self.wins = [0]*3 #current,season and total
        self.draws = [0]*3 #current,season and total
        self.losses = [0]*3 #current,season and total
        self.goals_for = [0]*3 #current,season and total
        self.goals_against = [0]*3 #current,season and total
        self.human = 0
        self.substitutions =0

players_list = [] #list with all players, unique_id is given by index of player
team_list = [] #list with all teams, unique_id is given by index of player

def keeper_value(player):
    a=0.7*player.goal_keeping[0]+0.10*player.stamina[0]+0.05*(1-player.opportunism[0])+0.05*(1-player.aggression[0])
    return a+0.03*player.short_pass[0]+0.05*player.long_pass[0]+0.02*player.ball_control[0]

def defender_value(player):
    a=0.2*player.short_pass[0]+0.2*player.long_pass[0]+0.2*player.interception[0]+0.05*(1-player.opportunism[0])+0.05*player.aggression[0]
    return a+0.10*player.stamina[0]+0.1*player.heading[0]+0.1*player.ball_control[0]

def midfielder_value(player):
    a=0.2*player.short_pass[0]+0.2*player.long_pass[0]+0.1*player.interception[0]+0.05*player.opportunism[0]+0.1*player.shooting[0]+0.05*player.aggression[0]
    return a+0.10*player.stamina[0]+0.1*player.heading[0]+0.1*player.ball_control[0]+0.1*player.positioning[0]

def attacker_value(player):
    a=0.04*player.short_pass[0]+0.04*player.long_pass[0]+0.19*player.opportunism[0]+0.38*player.shooting[0]
    return a+0.09*player.stamina[0]+0.09*player.heading[0]+0.09*player.ball_control[0]+0.08*player.positioning[0]

def update_vals(player):
    player.keep_val =keeper_value(player)
    player.def_val = defender_value(player)
    player.mid_val = midfielder_value(player)
    player.att_val = attacker_value(player)
    return

def create_basic_player():
    new_player= player()
    players_list.append(new_player)
    return new_player


# for i in range(len(teamsv0)*18):    # number of initialized players
#     playerid[i] = 
#    playerid[i].info()

# kees = create_basic_player()
# print(kees.keep_val)
# kees.goal_keeping[0] = 0
# kees.renew_vals()
# # kees = kees.renew_vals()
# print(kees.keep_val)
def create_basic_team(name):
    players_team = []
    set_up = [[0,1/2,0],[1,1/7,3/10],[2,2/5,1/4],[3,3/5,1/4],[4,6/7,3/10],[5,1/6,1/2],[6,1/2,1/2],[7,5/6,1/2],[8,1/6,3/4],[9,1/2,3/4],[10,5/6,3/4]]
    for i in range(18):
        next_player = create_basic_player()
        next_player.back_number = i+1
        if i < 11:
            next_player.playing =1
            next_player.position=set_up[i][1:3]
        else:
            next_player.position=[1.1,0.05*(i-11)]
        players_team.append(next_player)
    players_team[0].is_keeper = 1
    players_team[8].takes_freekick = 1
    players_team[8].takes_corner = 1
    players_team[10].takes_penalty = 1
    
    # new_team = team(name,players_team,id_nr )
    # for created_player in new_team.players_team:
    #     created_player.teamid = new_team.id_nr
    
    # return new_team
    return team(name,players_team)
    
    
# for i in range(18):
#     teamid[i] = team(teamsv0[i],i,[playerid[j] for j in range(i*18,(i+1)*18)] ) #initialize teams
#     playerid[i*18].is_keeper=1 #set piecetakers
#     playerid[i*18+8].takes_freekick=1
#     playerid[i*18+8].takes_corner =1
#     playerid[i*18+10].takes_penalty =1    

# teamid=[0]*18


# for i in range(len(teamid)):
#     for j in range(len(teamid[i].players)):
#         teamid[i].players[j].back_number = j
#         if j < 11:
#             teamid[i].players[j].playing = 1