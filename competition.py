# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 23:11:31 2018

@author: Gebruiker
"""

#import match
import numpy as np
import matchve as match
import sys
from tabulate import tabulate


teamsv0= ["Victorie", "Fc Knudde", "FC de Kampioenen", "Swift Boys", "Lazio Roma", "FC Emmen","Top Oss","SVO Oosterend", "Full Speed", "All Stars","Lions", "Triomftankers","Puntertjes", "Fortuna Sittard", "PSV", "FC Barcelona", "Hoezee!","Zegeridders"]

def check_input(inputted,minimal,maximal):
    if inputted == 'exit':
        sys.exit()
    try:
        inputted = int(inputted)
    except ValueError:
        print("This is no valid input.")
        return(inputted,0)
    inputted = int(inputted)
    if inputted < minimal or inputted > maximal:
        print("This is no valid input.")
        return(inputted,0)
    else:
        return(inputted,1)

def welcome(teams):
    print('Welcome to Manager Madness! Pick a team: ')
    for i in range(len(teams)):
        print(i,') ', teams[i])
    success =0
    while success == 0:
        clubnr = input('Give the number of the desired club. ')
        [clubnr,success]= check_input(clubnr,0,len(teams))
    teams[0],teams[clubnr] = teams[clubnr],teams[0] 
    return(teams)
    
teams = welcome(teamsv0)

piecetakers = [[0,0],[8,8],[10,10]]
setup_a = np.array([[1/2,0],[1/5,1/4],[2/5,1/4],[3/5,1/4],[4/5,1/4],[1/6,1/2],[1/2,1/2],[5/6,1/2],[1/6,3/4],[1/2,3/4],[5/6,3/4]])
setup_b = np.zeros([11,2])
setups=[setup_a,setup_b]
competitors =len(teams)
playersperteam =11
players_stats = np.random.uniform(0,1,(competitors,playersperteam,19))
players_names = np.zeros((competitors,playersperteam,16)).tolist()
for i in range(0,competitors):
    for j in range(0,playersperteam):
        players_names[i][j][0] = j
        players_names[i][j][1] = str(i) + "," + str(j)
        players_names[i][j][2] = "Player"
        players_names[i][j][3] = 1
        players_names[i][j][4] = setup_a[j][0]
        players_names[i][j][5] = setup_a[j][1]        
    players_names[i][0][12] =1
    players_names[i][8][13] =1
    players_names[i][8][14] =1
    players_names[i][10][15] =1
    
players_total = [players_names,players_stats]

league_table=np.tile(0,(competitors,9)).tolist()
# generation code - for cut and paste
for i in range(len(teams)):
    league_table[i][0]=i
    league_table[i][1] = teams[i]


self_stats = np.random.uniform(0,1,(18,19))
self_stats = np.around(self_stats,decimals=3)

## change players in squad
def show(self_stats):
    for i in range(18):
        self_stats[i][1]=i
    print(tabulate(self_stats[:,1:12],headers=["Number","Shooting","Heading", "Long Pass","Short Pass","Interception","Goal Keeping", "Stamina","Oppotunism", "Aggression", "Positioning"],tablefmt="grid"))
    return

def other(player_stats,nr):
    show_table = player_stats[nr][:][:]
    for i in range(11):
        show_table[i][1]=i
    print(tabulate(show_table[:,1:12],headers=["Number","Shooting","Heading", "Long Pass","Short Pass","Interception","Goal Keeping", "Stamina","Oppotunism", "Aggression", "Positioning"],tablefmt="grid"))
    return

def swap(self_stats):
    first_player = input("Select number player 1: ")
    second_player = input("Select number player 2: ")
    try:
        first_nr,second_nr = int(first_player),int(second_player)
    except ValueError:
        print("Please fill in numbers.")
        return(self_stats)
    if first_nr in range(18) and second_nr in range(18):
        self_stats[first_nr], self_stats[second_nr]= self_stats[second_nr], self_stats[first_nr].copy()
        print("Swapped!")
    else:
        print("Failed to swap.")
    return self_stats
    
def implement(self_stats,players_stats):
    players_stats[0][2:19]=self_stats[:playersperteam][2:19]
    for i in range(11):
        players_stats[0][i][3] = 1
#    for i in range(18):
#        if i < 11:
#            players_stats[0][i][3] = 1
#        else:
#            players_stats[0][i][3] = 0
    players_names[0][0][12] =1
    players_names[0][8][13] =1
    players_names[0][8][14] =1
    players_names[0][10][15] =1    
    return players_stats


def fixtures(teams):
    if len(teams) % 2:
        teams.append('Day off')  # if team number is odd - use 'day off' as fake team     

    rotation = list(teams)       # copy the list

    fixtures = []
    for i in range(0, len(teams)-1):
        fixtures.append(rotation)
        rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1]

    return fixtures

def returns(schedule,competitors): #make schedule fo return matches
    for i in range(competitors-1):
        new_fixture = [0]*competitors
        for j in range(competitors-1):
            new_fixture[j]= schedule[i][competitors-1-j]
        schedule.append(new_fixture)
    return(schedule)


def print_table(league_table):
    ranked_table= sorted(league_table, key =lambda tup: (-tup[5],-tup[6],-tup[7],-tup[2],tup[1]))
    for i in range(len(teams)):
        ranked_table[i][0]=i+1
    #print(ranked_table)
    print(tabulate(ranked_table,headers=["Position", "Team", "Wins", "Draws", "Losses", "Points", "Goals Difference", "Goals For", "Goals Against"],tablefmt="grid"))
    return

def play_competition(schedule,competitors,league_table,self_stats,i):
    for j in range(competitors//2):
        team_a=schedule[i][j]
        team_b=schedule[i][competitors-j-1]
        #print(teams[team_a] + "-" + teams[team_b]+ ": ")
        players= [[players_total[0][team_a],players_total[0][team_b]],[players_total[1][team_a],players_total[1][team_b]]]
        team_names = [teams[team_a],teams[team_b]]
        playing = [1,0]
        if team_a==0:
            playing = [0,0]
        if team_b ==0:
            playing = [0,1]
        [score,players_change]=match.match(players,piecetakers,team_names,setups,playing)
        [players_total[0][team_a],players_total[0][team_b], players_total[1][team_a],players_total[1][team_b]] = players_change
        print(teams[team_a] + "-" + teams[team_b]+ ": " + str(score[0]) + "-" + str(score[1]))
        league_table[team_a][7]+=score[0]
        league_table[team_b][7]+=score[1]
        league_table[team_a][8]+=score[1]
        league_table[team_b][8]+=score[0] 
        for teamgd in [team_a,team_b]:
            league_table[teamgd][6] = league_table[teamgd][7] - league_table[teamgd][8]
               
        if score[0] > score[1]:#win team a
            league_table[team_a][2] +=1
            league_table[team_a][5] +=3
            league_table[team_b][4] +=1
        elif score[0] < score[1]:#win team b
            league_table[team_b][2] +=1
            league_table[team_b][5] +=3
            league_table[team_a][4] +=1
        elif score[0] ==score[1]:#draw
            league_table[team_b][5] +=1
            league_table[team_a][5] +=1
            league_table[team_b][3] +=1
            league_table[team_a][3] +=1
               
    print_table(league_table)
    return

#return(league_table)                    

     
def menu(schedule,competitors,league_table,self_stats):
    number_match=0   
    while number_match < 2*(competitors-1):
        check_go=input("What do you want to do? (play/stop/show/swap)")
        if check_go == "stop":
            break
        elif check_go == "play":
            implement(self_stats,players_stats)
            play_competition(schedule,competitors,league_table,self_stats,number_match)
            number_match +=1
        elif check_go == "show":
            show(self_stats)
        elif check_go == "swap":
            self_stats= swap(self_stats)
        elif check_go == "other":
            nr = int(input("Number of team:"))
            other(players_stats,nr)
    return

schedule = fixtures(list(range(competitors)))
schedule = returns(schedule,competitors)
menu(schedule,competitors,league_table,self_stats)
            