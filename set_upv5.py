# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 22:30:37 2019

@author: Gebruiker
"""
import sys
from tabulate import tabulate

def check_input(inputted,minimal,maximal):
    if inputted == 'exit':
        sys.exit()
    try:
        inputted = int(inputted)
    except ValueError:
        if inputted != "back":  print("This is no valid input.")
        return(inputted,0)
    inputted = int(inputted)
    if inputted < minimal or inputted > maximal:
        print("This is out of range.")
        return(inputted,2)
    else:
        return(inputted,1)
        
def check_input_float(inputted,minimal,maximal):
    if inputted == 'exit':
        sys.exit()
    try:
        inputted = float(inputted)
    except ValueError:
        if inputted != "back":  print("This is no valid input.")
        return(inputted,0)
    inputted = float(inputted)
    if inputted < minimal or inputted > maximal:
        print("This is out of range.")
        return(inputted,0)
    else:
        return(inputted,1)
        
#def index_number(team,text): #find index of certain number of player
#    success =0 
#    while success == 0:
#        number = input(text)
#        [number,success]= check_input(number,0,100)
#    for i in range(len(team.players)):
#        if team.players[i].back_number == number:
#            return [i,1]
#    print('The given number does not correspond to one the players in your squad.')
#    return[number,0]

def index_number(team,text): #find index of certain number of player
    number = input(text)
    [number,success]= check_input(number,0,100)
    if success ==0:
        return number,0
    for i in range(len(team.players)):
        if team.players[i].back_number == number:
            return [i,1]
    print('The given number does not correspond to one the players in your squad.')
    return number,0

        
def show_first(team): 
    show_table= []
    for j in range(len(team.players)):
        t=team.players[j]
        show_table.append([t.back_number,t.first_name,t.second_name,t.playing,t.goals[1],
                           t.yellow_cards[1],t.red_cards[1],t.goals[2],t.yellow_cards[2],t.red_cards[2],
                           t.is_keeper,t.takes_freekick,t.takes_corner,t.takes_penalty,t.injured] ) 
    print(tabulate(show_table, headers=["Number","First name", "Surname","Playing","Curgoals", "Cur yc","Cur rc", "Tot goals", "Tot yc", "Tot rc", 
                                        "keeper", "fk", "cor", "pen", "inj"],tablefmt="grid"))
    return

def show_second(team):
    show_table= []
    for j in range(len(team.players)):
        t=team.players[j]
        show_table.append([t.back_number,t.first_name,t.second_name, str(round(t.shooting[0],3)) +"/" + str(round(t.shooting[1],3)),
                           str(round(t.heading[0],3))+"/" +str(round(t.heading[1],3)),str(round(t.long_pass[0],3))+"/" +str(round(t.long_pass[1],3)),
                               str(round(t.short_pass[0],3))+"/" + str(round(t.short_pass[1],3)),str(round(t.interception[0],3))+"/" +str(round(t.interception[1],3)),
                               str(round(t.goal_keeping[0],3))+"/" +str(round(t.goal_keeping[1],3)),str(round(t.stamina[0],3))+"/" +str(round(t.stamina[1],3)),
                               str(round(t.opportunism[0],3))+"/" +str(round(t.opportunism[1],3)) ]) 
    print(tabulate(show_table,headers=["Number", "First name", "Second name","Shooting","Heading", "Long Pass",
                                       "Short Pass","Interception","Goal Keeping", "Stamina","Opportunism"],tablefmt="grid"))
    return

def show_third(team):
    show_table= []
    for j in range(len(team.players)):
        t=team.players[j]
        if j < 11:
            t.position = team.set_up[j][1:3]
        else:
            t.position = [0,0]
        show_table.append([t.back_number,t.first_name,t.second_name,
                              str(round(t.aggression[0],3))+"/" +str(round(t.aggression[1],3)),str(round(t.positioning[0],3))+"/" +str(round(t.positioning[1],3)),
                            str(round(t.ball_control[0],3))+"/"+str(round(t.ball_control[1],3)),
                           str(round(t.freekick_accuracy[0],3))+"/"+ str(round(t.freekick_accuracy[1],3)),
                            str(round(t.corner_accuracy[0],3))+"/"+ str(round(t.corner_accuracy[1],3)),
                            str(round(t.penalty_accuracy[0],3))+"/"+ str(round(t.penalty_accuracy[1],3)),round(t.position[0],3),round(t.position[1],3)] ) 
    print(tabulate(show_table,headers=["Number", "First name", "Second name", "Aggression", "Positioning", "Ball Control", "Freekick acc", "Corner acc", "Penalty acc", "x", "y"],tablefmt="grid"))
    return

def show_team(team):
    show_first(team)
    show_second(team)
    show_third(team)
    return

def show_positions(team):
    show_table= []
    for j in range(len(team.players)):
        t=team.players[j]
        if j < 11:
            t.position = team.set_up[j][1:3]
        else:
            t.position = [0,0]
        show_table.append([t.back_number,t.first_name,t.second_name,t.playing,round(t.position[0],3),round(t.position[1],3)] ) 
    print(tabulate(show_table,headers=["Number", "First name", "Second name", "Playing", "x", "y"],tablefmt="grid"))
    return

# change players in squad

def swap(team,substitution):
    success =0 
    while success == 0:
        [first_nr,success1]= index_number(team,'Select number player 1: ')
        [second_nr,success2]= index_number(team,'Select number player 2: ')
        success = success1*success2

    team = swap_players(team,first_nr,second_nr)
    if (team.players[first_nr].playing == 1 and team.players[second_nr].playing == 0) or (team.players[first_nr].playing == 0 and team.players[second_nr].playing == 1) :
        substitution[1]+=1
    return team,substitution

def swap_players(team,first_nr,second_nr):
    team.players[second_nr],team.players[first_nr] = team.players[first_nr],team.players[second_nr]
    team.players[second_nr].playing,team.players[first_nr].playing = team.players[first_nr].playing,team.players[second_nr].playing
    team.players[second_nr].is_keeper,team.players[first_nr].is_keeper = team.players[first_nr].is_keeper,team.players[second_nr].is_keeper
    team.players[second_nr].takes_freekick,team.players[first_nr].takes_freekick = team.players[first_nr].takes_freekick,team.players[second_nr].takes_freekick
    team.players[second_nr].takes_corner,team.players[first_nr].takes_corner = team.players[first_nr].takes_corner,team.players[second_nr].takes_corner
    team.players[second_nr].takes_penalty,team.players[first_nr].takes_penalty = team.players[first_nr].takes_penalty,team.players[second_nr].takes_penalty
    return team   


def select(team):
    success =0 
    while success == 0:
        print('Select which you want to change: ')
        print('1) The goalkeeper')
        print('2) The players who takes the free kicks')
        print('3) The players who takes the corners')
        print('4) The players who takes the penalties')
        print('(Or type back to go back)')
        action_choice = input(' ')
        if action_choice == 'back':
            return team
        [action_choice,success]= check_input(action_choice,0,5)
    success =0 
    while success == 0:
        [piecetaker,success]= index_number(team,'Select the number of the player you want to assign this task (or type back to go back):')
#        print('(Or type back to go back)')
        print(piecetaker)
        if piecetaker == 'back':
            return team
    if team.players[piecetaker].playing == 0:
        print("Choose a player currently on the field.")
        return team
    if action_choice ==1:
        for i in range(len(team.players)):
            team.players[i].is_keeper =0
        team.players[piecetaker].is_keeper = 1
    elif action_choice ==2:
        for i in range(len(team.players)):
            team.players[i].takes_freekick =0
        team.players[piecetaker].takes_freekick = 1
    elif action_choice ==3:
        for i in range(len(team.players)):
            team.players[i].takes_corner =0
        team.players[piecetaker].takes_corner = 1
    elif action_choice ==4:
        for i in range(len(team.players)):
            team.players[i].takes_penalty =0
        team.players[piecetaker].takes_penalty = 1
    return team
        
def positions(team):
    show_positions(team)
    success =0
    while success == 0:
        [player_change,success]= index_number(team,'Select the number of the player of whom you want to change the position (or type back to go back):')
#        print('(Or type back to go back)')
        if player_change == 'back':
            return team
    x_success =0
    while x_success ==0:
        x_position = input('Give the new x position of the player (or type back to go back):')
        [x_position,x_success] = check_input_float(x_position,0,1)
    team.set_up[player_change][1] = x_position
    y_success =0
    while y_success ==0:
        y_position = input('Give the new y position of the player (or type back to go back):')
        [y_position,y_success] = check_input_float(y_position,0,1)
    team.set_up[player_change][2] = y_position            
    print("The player's position is changed.")
    show_positions(team)
    return team

def menu(team,substitution): #subsitution = [in match, nr of used substitutions]
    stay = True
    if substitution[1] >= 3 and substitution[0] == 1:
        print('You have already substituted the maximal amount.')
        return team,substitution
    while stay:
        check_go=input("What do you want to do? (show/swap/select/positions/back)")
        if check_go == "back":
            return team,substitution
        elif check_go == "show":
            show_team(team)
        elif check_go == "swap":
            team,substitution= swap(team,substitution)
        elif check_go == "select":
            team= select(team)
        elif check_go == "positions":
            team=positions(team)
    return team,substitution