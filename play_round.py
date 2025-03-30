# -*- coding: utf-8 -*-
"""
Created on Thu May 13 00:55:43 2021

@author: Roel
"""
# import random
import ai_match
import match_markov_v2 as match
import match_ui_v4 as human_match
import ai_formation as ai_for
import loading_screen

def play_competition(schedule,competitors,week_nr):    
    for j in range(len(schedule.weeks[week_nr])):
        home_team = schedule.weeks[week_nr][j].home_team
        away_team = schedule.weeks[week_nr][j].away_team
        matchdata_form = match.class_matchdata(home_team,away_team)
        if home_team.human == 1 or away_team.human ==1:
            for team in [home_team,away_team]:
                if team.human == 0:
                    team = ai_for.initial_setup(team,(4,3,3))
            matchdata_form = human_match.main(matchdata_form)
        else:
            matchdata_form = ai_match.main(matchdata_form)
            
        home_team = matchdata_form.home_team
        away_team = matchdata_form.away_team
        # score =[random.randint(0,10),random.randint(0,10)]
        score = matchdata_form.score
        schedule.weeks[week_nr][j].home_team_score = score[0]
        schedule.weeks[week_nr][j].away_team_score = score[1]
        # for i in [1,2]:
        #     home_team.goals_for[i] += score[0]
        #     home_team.goals_against[i] += score[1]
        #     away_team.goals_for[i] +=score[1]
        #     away_team.goals_against[i] +=score[0]
        print(home_team.name + "-" + away_team.name + ": " + str(score[0]) + "-" + str(score[1]))
        if score[0] > score[1]:#win home team
            for i in range(3):
                home_team.wins[i] += 1
                away_team.losses[i] += 1
        elif score[0] < score[1]:#win away team 
            for i in range(3):
                away_team.wins[i] += 1
                home_team.losses[i] += 1   
        elif score[0] == score[1]:#draw
            for i in range(3):
                away_team.draws[i] += 1
                home_team.draws[i] += 1                   
    
    return