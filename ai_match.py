# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 00:55:34 2021

@author: Roel
"""
import match_markov_v2 as match
import ai_formation as ai_for
# import init_players_and_teams as initpat

def main(matchdata):
    for team in [matchdata.home_team,matchdata.away_team]:   # things to do when the match begins
        team = match.stats_begin(team)
        team = ai_for.initial_setup(team,(4,3,3))
    matchdata.home_team,matchdata.away_team = match.setup_start(matchdata.home_team,matchdata.away_team)
    
    for matchdata.minute in range(matchdata.minpermatch):
        # print(str(matchdata.minute)+ "'")
        for team in [matchdata.home_team,matchdata.away_team]: #stamina calculations once per game minute
            team= match.stats_after_stamina(team,matchdata.minpermatch)
        team.substitutions,matchdata=ai_for.substition_check(team,(matchdata.minute,matchdata.minpermatch),team.substitutions,matchdata)
        
        for matchdata.second in range(matchdata.secpermin):
            matchdata=match.match_second(matchdata)
            
    for team in [matchdata.home_team,matchdata.away_team]:   # things to do when the match is over
        team =match.stats_begin(team)
        team =match.injuries_passing(team)
    
    for player in matchdata.away_team.players:
        player.position = [1-player.position[0],1-player.position[1]]
    
    print(matchdata.score)
    return(matchdata)

# test_team = initpat.create_basic_team("Huizenhoog")
# test_team2= initpat.create_basic_team("Bomenbeukers")

# test_team= ai_for.initial_setup(test_team,(4,3,3))
# test_team2= ai_for.initial_setup(test_team2,(4,3,3))

# form = match.class_matchdata(test_team, test_team2)

# main(form)