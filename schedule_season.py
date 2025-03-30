# -*- coding: utf-8 -*-
"""
Created on Thu May 13 00:47:42 2021

@author: Roel
"""
class match_in_week:
    def __init__(self, schedule, teams,week_nr,match_nr):
        self.home_team = teams[schedule[week_nr][match_nr][0]]
        self.away_team = teams[schedule[week_nr][match_nr][1]]
        self.home_team_score = " "
        self.away_team_score = " "

class schedule_total:
    def __init__(self, schedule,teams):
        nr_weeks = (len(teams)-1)*2
        nr_matches_per_week = len(teams)//2
        self.weeks = []
        for i in range(nr_weeks):
            self.weeks.append([match_in_week( schedule, teams,i,j) for j in range(nr_matches_per_week)])

        
def fixtures(nr_teams):
    rotation = list(range(nr_teams)) 
    fixtures = []
    for i in range(0, nr_teams-1):
        fixtures.append(rotation)
        rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1]

    return fixtures
    
def make_schedule(teams): #only import an even number of teams
    nr_teams = len(teams)
    schedule=[]
    schedule_old = fixtures(nr_teams)
    for k in range(2):
        for i in range(len(schedule_old)) :
            if (i+k) % 2 ==0:
                schedule.append([[schedule_old[i][j],schedule_old[i][len(teams)-j-1]] for j in range(len(teams)//2 )])
            elif (i+k) % 2 == 1:
                schedule.append([[schedule_old[i][len(teams)-j-1],schedule_old[i][j]] for j in range(len(teams)//2 )])
      
    return schedule_total(schedule, teams) 

# make_schedule(range(8))