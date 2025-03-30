import random
import math
# import time
import set_upv5 as set_up
import init_players_and_teams as initp
import copy
# from keyboardmaster import keyboard


class class_matchdata:
    
    def __init__(self,home_team,away_team):
        self.home_team = home_team
        self.away_team = away_team
        self.human_playing = self.human_in_match(home_team, away_team)
        self.possession = find_piecetaker(home_team,"is_keeper")
        self.score=[0,0]
        self.minute = 0
        self.second = 0
        self.situation = 0
        self.position = [0,0]
        self.substitutions = [5,5]
        self.penalties, self.corners , self.shots, self.free_kicks = 0,0,0,0
        self.total_possession = [0,0]
        self.message = []
        self.secpermin = 60
        self.minpermatch = 90
        
    def human_in_match(self,home_team, away_team):
        if home_team.human == 1 or away_team.human ==1:
            return 1
        else:
            return 0
        
"Colors"
black = (23,23,23)
white = (254,254,254)
green = (31,122,20)
red = (223,119,96)
yellow = (208,214,27)
blue_purple = (115,100,176)
blue_cyan = (103,122,220)
blue_dark = (56,71,148)
        
# def find_player(team,player):
#     for i in range(len(team.players)):
#         if team.players[i].id_number == player.id_number:
#             return i
#     return 0

# def find_player_id(team,player_id):
#     for i in range(len(team.players)):
#         if team.players[i].id_number == player_id:
#             return i
#     return 0

def find_players_team(matchdata,team_nr): #returns home team if team nr is 1, 
                                                    #away team if team nr is 0, and [0,0] else
    if team_nr == 0:
        return [matchdata.home_team,matchdata.away_team]
    elif team_nr == 1:
        return [matchdata.away_team,matchdata.home_team]
    else:
        return [0,0]

def send_message(matchdata, str_message):
    matchdata.message.append([str(matchdata.minute),str(matchdata.second),str_message])
    return matchdata

# def nr_players_in_team(team):
#     return sum(team.players[i].playing for i in range(len(team.players)))

# def players_on_field(teams):
#     [home_team,away_team]=teams
#     home_players_on_field = []
#     away_players_on_field = []
#     for i in range(len(home_team.players)):
#         if home_team.players[i].playing == 1:
#             home_players_on_field.append(home_team.players[i])
#     for i in range(len(away_team.players)):
#         if away_team.players[i].playing == 1:
#             away_players_on_field.append(away_team.players[i])
#     return [home_players_on_field,away_players_on_field]
    

# def find_piecetaker(team,set_piece): #0 keeper,1 free kick, 2 corner, 3 penalty
#     if set_piece =="keeper":
#         for j in range(len(team.players)):
#             if team.players[j].is_keeper == 1:
#                 return team.players[j]
#     elif set_piece =="free_kick":
#         for j in range(len(team.players)):
#             if team.players[j].takes_freekick == 1:
#                 return team.players[j]
#     elif set_piece =="corner":
#         for j in range(len(team.players)):
#             if team.players[j].takes_corner == 1:
#                 return team.players[j]
#     elif set_piece =="penalty":
#         for j in range(len(team.players)):
#             if team.players[j].takes_penalty == 1:
#                 return team.players[j]
#     return 0

def find_piecetaker(team,set_piece):
    for player in team.players:
        if getattr(player, set_piece) ==1:
            return player
    return 0
    
def goal(matchdata,scorer):
#    print("Goal: " + matchdata.possession.first_name+" "+ matchdata.possession.second_name)
    poss = matchdata.possession
    posshoa = poss.home_or_away #is possessor at home or away?
    poss_team,opp_team=find_players_team(matchdata, posshoa)
    keeper = find_piecetaker(opp_team,"is_keeper")
    for i in range(2):
       if posshoa==i:
           matchdata.score[i] +=1
           for j in range(3):
               poss_team.goals_for[j] +=1 #adding goal scored team
               poss.goals[j] +=1 # adding goal scored player
               opp_team.goals_against[j] +=1 #adding goal conceived team
    if matchdata.human_playing > 0:
        matchdata = send_message(matchdata," Goal by " +str(scorer.first_name)+ " "+ str(scorer.second_name)
                       + " (" + str(poss_team.name)+ ")! " + str(matchdata.score[0]) + "-" +  str(matchdata.score[1]))
    matchdata.possession = keeper
    return matchdata

def freekick_shot(matchdata):
    poss = matchdata.possession #the player who has the ball
    [poss_team,opp_team]=find_players_team(matchdata, poss.home_or_away) #the team which has the ball is poss_team, opp_team the other
    posshoa= poss.home_or_away
    keeper = find_piecetaker(opp_team,"is_keeper")  
    # posshoa = matchdata.possession.home_or_away
    freekicker = find_piecetaker(poss_team,"takes_freekick")
    # posshoa = matchdata.possession.home_or_away
    matchdata.situation =0
    # keeper = find_piecetaker(teams[1-posshoa],0)
    # freekicker = find_piecetaker(teams[posshoa],1)
    [x1,y1] = matchdata.position
    fkshoot = freekicker.freekick_accuracy[0]
    keepskill = keeper.goal_keeping[0]
    distg = distance((x1,y1),(0.5,1-posshoa))
    fkshotprob=distg*(1/100)*fkshoot+(1-distg)*fkshoot 
    if random.uniform(0,1) > fkshotprob : #target missed
        # if matchdata.human_playing > 0: 
        matchdata = send_message(matchdata,"Missed free kick by " +str(freekicker.first_name)
                                     + " "+ str(freekicker.second_name)+ " (" + str(poss_team.name)  + ")! ")
        matchdata.situation = 2        
    else:
        saveprob= (1-distg)*keepskill+distg
        if  saveprob*random.uniform(0,1)< fkshotprob*random.uniform(0,2/3): #goal
            matchdata = goal(matchdata,freekicker)
        else:
            result = random.uniform(0,1)
            if result < keepskill: #keeper saves
                matchdata.possession = keeper
                # if matchdata.human_playing > 0: 
                matchdata = send_message(matchdata,"Keeper "+str(keeper.first_name)+ " "
                                             + str(keeper.second_name)+ " (" + str(opp_team.name) + ") saves!")
            elif result < keepskill + 2/7*(1-keepskill): # offender gets ball
                matchdata.position = [0.5,1-posshoa]
                matchdata.possession = close(matchdata,posshoa)
            elif result < keepskill + 5/7*(1-keepskill): # defender gets ball
                matchdata.position = [0.5,1-posshoa]
                matchdata.possession = close(matchdata,1-posshoa)
            else: #penalty
                matchdata.situation = 4
    return matchdata

def free_kick(matchdata):
    poss = matchdata.possession #the player who has the ball
    [poss_team,opp_team]=find_players_team(matchdata, poss.home_or_away) #the team which has the ball is poss_team, opp_team the other
    posshoa= poss.home_or_away
    keeper = find_piecetaker(opp_team,"is_keeper")  
    # posshoa = matchdata.possession.home_or_away
    freekicker = find_piecetaker(poss_team,"takes_freekick")
    # penalty_taker = find_piecetaker(teams[posshoa],3)
    # matchdata.possession = penalty_taker
    posshoa = matchdata.possession.home_or_away
    # keeper = find_piecetaker(teams[1-posshoa],0)
    # freekicker = find_piecetaker(teams[posshoa],1)
    matchdata.possession = freekicker
    [x1,y1] = matchdata.position
    freekickacc = freekicker.freekick_accuracy[0]
    # players_ofl=players_on_field(teams) 
    # keepskill = keeper.goal_keeping[0]
    # heads = [[0]*len(players_ofl[i]) for i in range(2)]
    # opp = freekicker.opportunism[0]
    # crosspass=[ random.uniform(0,1)]*3
    # for i in range(2):
    #     for j in range(len(players_ofl[i])):
    #         [x1,y1] =players_ofl[i][j].position
    #         dist = distance(x1,y1,1-posshoa,0.5)
    #         headskill = players_ofl[i][j].heading[0]
    #         heads[i][j] = (1-dist)*headskill
    #         if players_ofl[i][j].takes_freekick == 1: #free kicker cannot head
    #             heads[i][j] =0
    keepskill = keeper.goal_keeping[0]
    heads = [[],[]]
    opp = freekicker.opportunism[0]
    crosspass=random.uniform(0,1)
    matchdata = send_message(matchdata,"Free kick taken by " +str(freekicker.first_name)
                                     + " "+ str(freekicker.second_name)+ " (" + str(poss_team.name)  + ")! ")
    for team in [poss_team,opp_team]:
        for heading_dist_player in team.players:
            [x1,y1] =heading_dist_player.position
            dist = distance((x1,y1),(1-posshoa,0.5))
            headskill = heading_dist_player.heading[0]*heading_dist_player.playing*(1-heading_dist_player.takes_freekick)
            heads[int(heading_dist_player.home_or_away != posshoa)].append((1-dist)*headskill)
            # if players_ofl[i][j].takes_freekick == 1: #free kicker cannot head
            #     heads[i][j] =0
    cumheads = [sum(heads[0]),sum(heads[1])]#0 is for poss_team, 1 is for opp_team
    cumheads = [sum(heads[0]),sum(heads[1])]
    choice_of_action = random.uniform(0,1)
    if choice_of_action < (1-opp)/4: #quick pass
        matchdata.situation =1
        matchdata.position = [0,0]
        return matchdata
    if choice_of_action > (4-3*opp)/4: #shot
        matchdata = freekick_shot(matchdata)
        return matchdata    
    if (1-freekickacc)*0.1 > crosspass: #ball goes behind
        matchdata.situation =3
        matchdata.position = [0,0]
        return matchdata
    elif (1-freekickacc)*0.17 > crosspass: #ball goes out
        matchdata.situation =2
        matchdata.position = [0,0]
        return matchdata
    if (cumheads[posshoa]*2*freekickacc-cumheads[1-posshoa]) < random.uniform(0,1)*(cumheads[0]+cumheads[1]+0.01):
        matchdata.position=[1-posshoa,0.5]
        matchdata.possession = close(matchdata,posshoa)
    else:
        playerheader = poss_team.players[weighted_pick(heads[0])]
        if (1-playerheader.heading[0])*0.1> random.uniform(0,1): #player heads out
            matchdata.possession = keeper
            matchdata.situation =0
            matchdata.position = [0,0]
            return matchdata          
        if playerheader.heading[0]*random.uniform(0.85,1.15) > keepskill:
            matchdata.possession = playerheader
            matchdata= goal(matchdata,matchdata.possession)
        else:
            if 0.5*random.uniform(0,1) < keepskill:
                matchdata.possession = keeper #keeper got the ball
            else:
                matchdata.position=[1-posshoa,0.5]
                matchdata.possession = close(matchdata,posshoa) #offender gets the abll
    matchdata.situation =0
    matchdata.position = [0,0]
    return matchdata

def corner(matchdata):
    poss = matchdata.possession #the player who has the ball
    [poss_team,opp_team]=find_players_team(matchdata, poss.home_or_away) #the team which has the ball is poss_team, opp_team the other
    posshoa= poss.home_or_away
    keeper = find_piecetaker(opp_team,"is_keeper")  
    # posshoa = matchdata.possession.home_or_away    
#    poss=matchdata.possession
    # keeper = find_piecetaker(teams[1-posshoa],0)
    cornerkicker = find_piecetaker(poss_team,"takes_corner")
    matchdata.possession = cornerkicker
    [x1,y1] = matchdata.position
    corneracc = cornerkicker.corner_accuracy[0]
    # players_ofl=players_on_field(teams) 
    keepskill = keeper.goal_keeping[0]
    heads = [[],[]]
    opp = cornerkicker.opportunism[0]
    crosspass=random.uniform(0,1)
    matchdata = send_message(matchdata,"Corner taken by " +str(cornerkicker.first_name)
                                     + " "+ str(cornerkicker.second_name)+ " (" + str(poss_team.name)  + ")! ")
    for team in [poss_team,opp_team]:
        for heading_dist_player in team.players:
            [x1,y1] =heading_dist_player.position
            dist = distance((x1,y1),(1-posshoa,0.5))
            headskill = heading_dist_player.heading[0]*heading_dist_player.playing*(1-heading_dist_player.takes_freekick)
            heads[int(heading_dist_player.home_or_away != posshoa)].append((1-dist)*headskill)
            # if players_ofl[i][j].takes_freekick == 1: #free kicker cannot head
            #     heads[i][j] =0
    cumheads = [sum(heads[0]),sum(heads[1])]#0 is for poss_team, 1 is for opp_team
    choice_of_action = random.uniform(0,1)
    if choice_of_action < (1-opp)/2: #quick pass
        matchdata.situation =0
        # matchdata.position = [0,0]
        return matchdata
    if (1-corneracc)*0.1 > crosspass: #ball goes behind
        matchdata.situation =2
        matchdata.position = [0,0]
        return matchdata
    elif (1-corneracc)*0.17 > crosspass: #ball goes out
        matchdata.situation =1
        matchdata.position = [0.5,1-posshoa]
        return matchdata
    if (cumheads[0]*2*corneracc-cumheads[1]) < random.uniform(0,1)*(cumheads[0]+cumheads[1]+0.01): #no offender heads
        matchdata.position=[1-posshoa,0.5]
        matchdata.possession = close(matchdata,posshoa)
    else:
        playerheader = poss_team.players[weighted_pick(heads[0])]
        if (1-playerheader.heading[0])*0.1> random.uniform(0,1): #player heads out
            matchdata.possession = keeper
            matchdata.situation =0
            # matchdata.position = [0,0]
            return matchdata          
        if playerheader.heading[0]*random.uniform(0.85,1.15) > keepskill:
            matchdata.possession = playerheader
            matchdata= goal(matchdata,playerheader)
        else:
            if 0.5*random.uniform(0,1) < keepskill:
                matchdata.possession = keeper #keeper got the ball
            else:
                matchdata.position=[1-posshoa,0.5]
                matchdata.possession = close(matchdata,posshoa) #offender gets the abll
    matchdata.situation =0
    matchdata.position = [0,0]
    return matchdata

def penalty(matchdata):
    poss = matchdata.possession #the player who has the ball
    [poss_team,opp_team]=find_players_team(matchdata, poss.home_or_away) #the team which has the ball is poss_team, opp_team the other
    posshoa= poss.home_or_away
    keeper = find_piecetaker(opp_team,"is_keeper")  
    # posshoa = matchdata.possession.home_or_away
    penalty_taker = find_piecetaker(poss_team,"takes_penalty")
    # penalty_taker = find_piecetaker(teams[posshoa],3)
    matchdata.possession = penalty_taker
    # keeper = find_piecetaker(teams[1-posshoa],0)
    penaltyacc = penalty_taker.penalty_accuracy[0]
    keepskill = keeper.goal_keeping[0]    
    matchdata.situation =0   
    distg=distance([1/2,0],[1/2,0.11])
    shoot = penalty_taker.shooting[0]
    shotprob=(1-distg)*(1/4)*(shoot+penaltyacc+2)+distg*(shoot+penaltyacc+6)/8
    # if matchdata.human_playing > 0: 
    matchdata = send_message(matchdata,"Penalty taken by " +str(penalty_taker.first_name)
                                     + " "+ str(penalty_taker.second_name)+ " ("  + str(poss_team.name)  + ")! ")
        # matchdata = send_message(matchdata,"Penalty!")
    if random.uniform(0,1) > shotprob : #target missed
        # if matchdata.human_playing > 0:
        matchdata = send_message(matchdata,"Penalty missed by " +str(penalty_taker.first_name)
                                     + " "+ str(penalty_taker.second_name)+ " (" + str(poss_team.name)  + ")! ")
            # matchdata = send_message(matchdata,"Miss!")
        matchdata.situation =2 
        matchdata.position = [0.5,1-posshoa]
        return matchdata
    else:
        saveprob= (1-distg)*keepskill+distg
        if  random.uniform(0,1)> saveprob-(1/2)* shotprob: #goal
            matchdata = goal(matchdata,penalty_taker)
        else:
            result = random.uniform(0,1)
            if result < keepskill: #keeper saves
                matchdata.possession = keeper
                #print("Keeper saves!")
            elif result < keepskill + 2/7*(1-keepskill): # offender gets ball
                matchdata.position=[0.5,1-posshoa]
                matchdata.possession = close(matchdata,posshoa)
            elif result < keepskill + 5/7*(1-keepskill): # defender gets ball
                matchdata.position=[0.5,1-posshoa]
                matchdata.possession = close(matchdata,1-posshoa)
            else:
                matchdata.situation = 4 #another penalty
    return matchdata

# def sent_off(team, player_sent_off):
#     # team=teams[team_nr]
#     # player_sent_off=team.players[find_player(team, player_sent_off)]
#     player_sent_off.playing=0
#     if player_sent_off.is_keeper == 1:
#         for player in team.players:
#             if all( player.playing*player.is_keeper ==0 for player in team.players):
#                 if player.playing ==1:
#                     player.is_keeper = 1
#                     player.position =[0,0]
#     if player_sent_off.takes_freekick == 1:
#         for player in team.players:
#             if all( player.playing*player.takes_freekick ==0 for player in team.players):
#                 if player.playing ==1:
#                     player.takes_freekick = 1
#     if player_sent_off.takes_corner == 1:
#         for player in team.players:
#             if all( player.playing*player.takes_corner ==0 for player in team.players):
#                 if player.playing ==1:
#                     player.takes_corner = 1
#     if player_sent_off.takes_penalty == 1:
#         for player in team.players:
#             if all( player.playing*player.takes_penalty ==0 for player in team.players):
#                 if player.playing ==1:
#                     player.takes_penalty = 1
#     return team

def sent_off(team,player_sent_off):
    player_sent_off.playing =0
    # if getattr(player_sent_off, "is_keeper") ==1:
    #    setattr(player_sent_off, "is_keeper",0)
    #    for other_player in team.players:
    #        if other_player.playing ==1:
    #            other_player.is_keeper =1
    #            other_player.position = [1/2,other_player.home_or_away]
    #            break
    
    for set_piece in ["is_keeper", "takes_freekick", "takes_corner", "takes_penalty"]:
        if getattr(player_sent_off, set_piece) ==1:
            setattr(player_sent_off, set_piece,0) 
            for other_player in team.players:
                if other_player.playing ==1:
                    setattr(other_player, set_piece,1)
                    if set_piece == "is_keeper":
                        other_player.position = [1/2,other_player.home_or_away]
                    break
    return team

def foul(matchdata,offender): #start here correcting the code
    # posshoa = matchdata.possession.home_or_away
    poss_team,opp_team=find_players_team(matchdata, 1-offender.home_or_away)
    # offender is in opp_team
    poss=matchdata.possession
    # possessor=teams[posshoa].players[find_player(teams[posshoa], matchdata.possession)]
    # offender= teams[1-posshoa].players[find_player(teams[1-posshoa], possession)]
    intensity = random.uniform(0,1)
    aggressiveness = offender.aggression[0]
    matchdata.position = poss.position
    # if matchdata.human_playing > 0:
    matchdata = send_message(matchdata,"Foul by " +str(offender.first_name)
                                     + " "+ str(offender.second_name)+ " (" + str(opp_team.name)  + ")! ")
    if 0.4 < (aggressiveness+random.normalvariate(0,0.3))*intensity : #yellow card
        # if matchdata.human_playing > 0: 
        matchdata = send_message(matchdata,str(offender.first_name)+ " "+ str(offender.second_name) 
                                     + " (" +  str(opp_team.name)  + ") booked! (Yellow card)")        
        for j in range(3):
            offender.yellow_cards[j] += 1
        if offender.yellow_cards[0]==2:
            for j in range(3):
                offender.red_cards[j] += 1
            opp_team= sent_off(opp_team,offender)
    elif 0.8 < (aggressiveness+random.normalvariate(0,0.3))*intensity : #red card
        # if matchdata.human_playing > 0: 
        matchdata = send_message(matchdata,str(offender.first_name)+ " "+ str(offender.second_name)  
                                     + " (" + str(opp_team.name)  + ") booked! (Red card)")  
        for j in range(3):
            offender.red_cards[j] += 1
        opp_team= sent_off(opp_team,offender)
    if intensity > 0.995:
        poss.injured=1
        poss = stats_updated_player(poss,0)
        if matchdata.human_playing > 0:  #injury
            matchdata = send_message(matchdata, str(poss.first_name)+ " "+ str(poss.second_name)  
                                     + " (" + str(poss_team.name)  + ") injured!")
            # for k in range(2):
            #     if matchdata.human_playing ==k:
            #         nr =matchdata.human_playing-1
            #         teams[nr],matchdata.substitutions[nr] = set_up.menu(teams[nr],matchdata.substitutions[nr]) 
    matchdata.situation = 5
    return matchdata 

def distance(pos1,pos2): #gives a distance between two positions, with 0 minimal and 1 maximal
    return math.sqrt((0.49*(pos1[0]-pos2[0]))**2+(pos1[1]-pos2[1])**2/1.49)

def dist_players(player_1,player_2):
    return distance(player_1.position,player_2.position)

def close(matchdata,team_nr):# pick a person close to matchdata.position from team team_nr
    # players_ofl=players_on_field(teams)   
    # poss = matchdata.possession
    poss_team,opp_team=find_players_team(matchdata, team_nr)
    dist_play = []
    for player_choice in poss_team.players:
       if player_choice.playing == 1:
           dist_play.append(1 - distance(matchdata.position,player_choice.position))
       else:
           dist_play.append(0)
    
    return poss_team.players[weighted_pick(dist_play)] #returns the player who is relatively close to the ball
    # if playersinteam == 0: print('Kaduuk!')
    # dist = [0]*playersinteam
    # for i in range(playersinteam):
    #     dist[i]= root - distance(matchdata.position[0],matchdata.position[1],players_ofl[team_nr][i].position[0],players_ofl[team_nr][i].position[1])
    # return teams[team_nr].players[find_player(teams[team_nr],players_ofl[team_nr][weighted_pick(dist)])]


def weighted_pick(list_pos_floats):
    try:
        random.choices(list(range(len(list_pos_floats))),list_pos_floats)[0] = float(random.choices(list(range(len(list_pos_floats))),list_pos_floats)[0])
    except IndexError:
        print('List of floats:')
        print(list_pos_floats)
    return random.choices(list(range(len(list_pos_floats))),list_pos_floats)[0]

def ballout(matchdata):
    poss = matchdata.possession
    matchdata.position = [int(poss.position[0]+random.random()),poss.position[1]] #perhaps some pertubation to the y-variable?
    return close(matchdata,1-poss.home_or_away)

def ballbehind(matchdata):
    poss = matchdata.possession
    [poss_team,opp_team]=find_players_team(matchdata, poss.home_or_away)
    keeper= find_piecetaker(opp_team,"is_keeper")
    return keeper
        
def balloutself(matchdata,aimed_at): #need to rework the probabilities probably
    matchdata.situation =0
    poss = matchdata.possession #the player who has the ball
    # if matchdata.possession.playing ==0:
    #     print("Get go")
    [poss_team,opp_team]=find_players_team(matchdata, poss.home_or_away) #the team which has the ball is poss_team, opp_team the other
    posshoa= poss.home_or_away
    keeper = find_piecetaker(opp_team,"is_keeper")  
    shortp = poss.short_pass[0]
    longp = poss.long_pass[0] 
    distp = dist_players(poss, aimed_at)
    if id(poss) == id(aimed_at): #keeping the ball
        outprob = (poss.ball_control[0]+7)/8
    else: #trying to play to someone else
        outprob = (poss.ball_control[0]+3*aimed_at.ball_control[0]+8)*((1-distp)*shortp+distp*longp+9)/(90*(1+distp**2))  #chemistry somewhere here as well?
    if  random.uniform(0,1) > outprob:#ball goes out without interception
        [x2,y2]=aimed_at.position
        typeout = random.uniform(0,1)
        widthprob = 1-1/6*(x2-x2**2)
        posneg= 2*(posshoa -1/2)
        lengthprob = ((1- posshoa)+posneg*y2)*widthprob + (posshoa-posneg*y2)*(1-widthprob)
        if typeout < widthprob: #throw in opponent
            matchdata.position = [x2,y2]
            matchdata.position[0]=int(x2+random.uniform(0,1)) #determine the side the ball goes out
            matchdata.possession = close(matchdata,1-posshoa)
            # if matchdata.possession.playing ==0:
            #     print("close 1")
            # matchdata.situation =0
            # matchdata.position = [0,0]
        elif typeout <lengthprob: #behind, for the opponent keeper
            matchdata.possession = keeper
            # if matchdata.possession.playing ==0:
            #     print("close 1")
        else: # opponent corner
            matchdata.situation= 3
            matchdata.possession = close(matchdata,1-posshoa)
    #         if matchdata.possession.playing ==0:
    #             print("close 2")
    # if matchdata.possession.playing ==0:
    #     print("Ball out self!")
    return matchdata

# def passing(matchdata): #determine to whom the pass goes
#     poss = matchdata.possession
#     posshoa=find_players_team(matchdata.home_team, matchdata.away_team, poss)
#     players_ofl=players_on_field(matchdata,posshoa)
#     players_choice = players_ofl[posshoa]
#     chemistry =0.5
#     aimed_at = [0,0]
#     opp = matchdata.possession.opportunism[0]
#     [x1,y1] =  matchdata.possession.position
#     playersinteam = len(players_ofl[posshoa])
#     newprob = [0]*playersinteam
#     distp = [0]*playersinteam
#     for i in range(playersinteam):
#         [x2,y2] = players_choice[i].position
#         distp[i]=distance(x1,y1,x2,y2)
#         posit = players_choice[i].positioning[0] 
#         newprob[i]= 20/(1+10000*distp[i]**2)+((posit+1)/2)*chemistry*math.exp(-((x2-x1-2*opp+1)**2))
#     j= weighted_pick(newprob)
#     aimed_at = teams[posshoa].players[find_player(teams[posshoa],players_ofl[posshoa][j])]
#     return [matchdata,aimed_at,distp[j]]

def passing(matchdata): #determine to whom the pass goes
    poss = matchdata.possession
    poss_team,opp_team=find_players_team(matchdata, poss.home_or_away)
    chemistry =0.5
    newprob = []
    [x1,y1] =  poss.position
    opp = poss.opportunism[0]
    for player_choice in poss_team.players:
        if player_choice.playing == 1:
            [x2,y2] = player_choice.position
            dist = dist_players(poss,player_choice)
            posit = player_choice.positioning[0]
            newprob.append((20/(1+10000*dist**2)+((posit+1)/2)*chemistry*math.exp(-((x2-x1-2*opp+1)**2)))*player_choice.playing)
        else:
            newprob.append(0)
    
    return poss_team.players[weighted_pick(newprob)] #returns the player who is aimed at

def interception(matchdata,aimed_at):# decide if there is an interception
    poss=matchdata.possession
    # posshoa=poss.home_or_away
    poss_team,opp_team=find_players_team(matchdata, poss.home_or_away)
    [x1,y1] = poss.position
    [x2,y2] = aimed_at.position
    [shortp,longp] = [poss.short_pass[0],poss.long_pass[0]]
    distp = dist_players(poss, aimed_at)
    # playersinteam = len(players_ofl[1-posshoa])
    # order = list(range(0,playersinteam))
    opp_team_sh = opp_team.players.copy()
    random.shuffle(opp_team_sh)
    for interceptor in opp_team_sh:
        if interceptor.playing == 1:
            [x3,y3] = interceptor.position
            interc = interceptor.interception[0]
            agress = interceptor.aggression[0]
            distb= distance([(x2-x1)/2,(y2-y1)/2],[x3,y3])
            if poss == aimed_at: #player tries to keep ball
                ballc = poss.ball_control[0]
                # intprob = random.uniform(0,1)#interception probability
                # newprob = 1 - rel_dist* interc/(1+ballc)
                #print("Ball control:", newprob)
                # if random.uniform(0,1) > 1 - rel_dist* (interc+0.1*agress)/(40*(1.1+2*ballc)): #interception takes place
                # if random.uniform(0,1) < distb* (interc+0.1*agress)/(40*(1.1+2*ballc)): #interception takes place
                if random.uniform(0,1) < (interc+0.1*agress)/(40*(1.1+2*ballc)): #interception takes place                    
                    if random.uniform(0,1) < 0.01*interceptor.aggression[0]: #interceptor committed a foul, free kick
                        # matchdata.possession = aimed_at
                        matchdata=foul(matchdata,interceptor)
                        matchdata.situation=5
                        matchdata.position = [x2,y2]
                    matchdata.possession = interceptor
                    return matchdata
            else: #player tries to pass ball
                norm = distb*shortp+distp*longp/(1+distp**2)
                newprob= 1-(1/40)*distb*(interc+0.1*agress)/(1.1+norm)
                # intprob = random.uniform(0,1)
                # if intprob > newprob:
                if random.uniform(0,1) > newprob: #interception takes place
                    matchdata.possession = interceptor
                    if random.uniform(0,1) < 0.01*interceptor.aggression[0]:
                        matchdata=foul(matchdata,interceptor)
                        matchdata.situation=5
                        matchdata.position = [x2,y2]
                        return matchdata
                else: 
                    matchdata.possession = aimed_at #pass succeeds
    # matchdata = balloutself(teams, matchdata,aimed_at,distp) #apply this only once per second?
    return matchdata

def shot(matchdata):
    matchdata.situation =0
    poss = matchdata.possession #the player who has the ball
    [poss_team,opp_team]=find_players_team(matchdata, poss.home_or_away) #the team which has the ball is poss_team, opp_team the other
    posshoa= poss.home_or_away
    keeper = find_piecetaker(opp_team,"is_keeper")
    # matchdata.situation =0
    # poss=matchdata.possession
    # posshoa = poss.home_or_away
    # keeper = find_piecetaker(teams[1-posshoa],0)
    [x1,y1] = poss.position
    shoot = poss.shooting[0]
    keepskill = keeper.goal_keeping[0]
    distg = distance((x1,y1),(0.5,1-posshoa))
    shotprob=distg*(1/100)*shoot+(1-distg)*shoot 
    if random.uniform(0,1) > shotprob : #target missed
        # if matchdata.human_playing > 0: 
            # matchdata = send_message(matchdata,"Miss!")
        matchdata = send_message(matchdata,"Missed shot by " +str(poss.first_name)
                                     + " "+ str(poss.second_name)+ " (" + str(poss_team.name)  + ")! ")
        matchdata.situation = 2        
    else:
        saveprob= (1-distg)*keepskill+distg
        # if  saveprob*random.uniform(0,1)< shotprob*random.uniform(0,1/2): #goal
        if  saveprob*random.uniform(0,0.1)< shotprob*random.uniform(0,1/2): #goal
            matchdata = goal(matchdata,poss)
        else:
            result = random.uniform(0,1)
            if result < keepskill: #keeper saves
                matchdata.possession = keeper
                # if matchdata.human_playing > 0: 
                    # matchdata = send_message(matchdata,"Keeper saves!")
                matchdata = send_message(matchdata,"Keeper "+str(keeper.first_name)+ " "
                                             + str(keeper.second_name)+ " (" + str(opp_team.name) + ") saves!")
            elif result < keepskill + 2/7*(1-keepskill): # offender gets ball
                matchdata.position = [0.5,posshoa]
                matchdata.possession = close(matchdata,posshoa)
            elif result < keepskill + 5/7*(1-keepskill): # defender gets ball
                matchdata.position = [0.5,posshoa]
                matchdata.possession = close(matchdata,1-posshoa)
            else: #penalty
                matchdata.situation = 4
    return matchdata

def passing_total(matchdata):
    aimed_at=passing(matchdata)
    # if aimed_at.home_or_away != matchdata.possession.home_or_away:
    #     print("incongruence")
    # if aimed_at.playing ==0:
    #             print("aimed_at")
    matchdata = balloutself(matchdata,aimed_at)
    # if matchdata.possession.playing ==0:
    #             print("no_interception")
    if matchdata.situation == 0:
        # if matchdata.possession.id_number == aimed_at.id_number:
        matchdata = interception(matchdata,aimed_at)
        # if matchdata.possession.playing ==0:
        #             print("interception")
    return matchdata


#def implement_setup_home(team):
#    for player in team.players:
#        player.playing =0
#    for set_up_player in team.set_up:
#        player_nr = find_player_id(team,set_up_player[0])
#        team.players[player_nr].position = set_up_player[1:3]
#        if team.players[player_nr].is_keeper ==1:
#            team.players[player_nr].position = [1/2,0]
#        if team.players[player_nr].injured == 0 and team.players[player_nr].suspended ==0:
#            team.players[player_nr].playing =1
#    return team
#
#def implement_setup_away(team):
#    for player in team.players:
#        player.playing =0
#    for set_up_player in team.set_up:
#        player_nr = find_player_id(team,set_up_player[0])
#        team.players[player_nr].position = [1-set_up_player[1],1-set_up_player[2]]
#        if team.players[player_nr].is_keeper ==1:
#            team.players[player_nr].position = [1/2,1]
#        if team.players[player_nr].injured == 0 and team.players[player_nr].suspended ==0:
#            team.players[player_nr].playing =1
#    return team
    
def implement_setup(team,hoa):
    for player in team.players:
        player.playing = 0
    for i in range(11):
        if team.players[i].suspended == 0:
            team.players[i].playing =1
            for j in range(2):
                team.players[i].position[j] = hoa*team.set_up[i][j+1]+(1-hoa)*(1-team.set_up[i][j+1])
            if team.players[i].is_keeper ==1:
                team.players[i].position = [1/2,hoa]
    return team

def stats_begin(team):
    team.substitutions =1
    for player in team.players:
        player = stats_updated_player(player,1)
    return team

def stats_updated_player(player,out_of_match): # 0 if match is going on, 1 if before or after match
    oom =out_of_match
    inj = player.injured
    inj_fac = 3/(inj+3)
    if player.playing == 1:
        for str_stat in ["shooting", "heading", "long_pass", "short_pass", "interception", "goal_keeping", 
                             "positioning","ball_control","freekick_accuracy", "corner_accuracy", "penalty_accuracy"]:
                stat = getattr(player,str_stat)
                stat[0] = inj_fac*stat[oom]
        # player.shooting[0] = inj_fac*player.shooting[oom]
        # player.heading[0] = inj_fac*player.heading[oom]
        # player.long_pass[0] = inj_fac*player.long_pass[oom]
        # player.short_pass[0]  = inj_fac*player.short_pass[oom]
        # player.interception[0]  = inj_fac*player.interception[oom]
        # player.goal_keeping[0]  = inj_fac*player.goal_keeping[oom]
        # player.positioning[0]  = inj_fac*player.positioning[oom]
        # player.ball_control[0]  = inj_fac*player.ball_control[oom]           
        # player.opportunism[0] = inj_fac*player.opportunism[oom]
        # player.aggression[0] =  inj_fac*player.aggression[oom]
        # player.stamina[0] =  inj_fac*player.stamina[oom]
        # player.freekick_accuracy[0]  = inj_fac*player.freekick_accuracy[oom]
        # player.corner_accuracy[0]   = inj_fac*player.corner_accuracy[oom]
        # player.penalty_accuracy[0] = inj_fac*player.penalty_accuracy[oom]
    return player    

def decrease_stats(stat,stamina,inj_fac,mpm,nr):
    return inj_fac*(1-stamina[0])*stat/(nr*mpm)

# def decrease_stats_two(stat,stamina,inj_fac,mpm):
#     return inj_fac*(1-stamina[0])*stat/(8*mpm)
    
def stats_after_stamina(team,mpm): #mpm = minutes per match
    for player in team.players:
        inj = player.injured
        inj_fac = 3/(inj+3)
        stamina= player.stamina
        if player.playing == 1:
            for str_stat in ["shooting", "heading", "long_pass", "short_pass", "interception", "goal_keeping", 
                             "positioning","ball_control"]:
                stat= getattr(player, str_stat)
                setattr(player,str_stat,[stat[0]-decrease_stats(stat[1],stamina,inj_fac,mpm,4),stat[1]])
                # stat[0] -= decrease_stats(stat[1],stamina,inj_fac,mpm,4)
            # player.shooting[0] -= decrease_stats(player.shooting[1],stamina,inj_fac,mpm)
            # player.heading[0] -= decrease_stats(player.heading[1],stamina,inj_fac,mpm)
            # player.long_pass[0] -= decrease_stats(player.long_pass[1],stamina,inj_fac,mpm)
            # player.short_pass[0] -= decrease_stats(player.short_pass[1],stamina,inj_fac,mpm)
            # player.interception[0] -= decrease_stats(player.interception[1],stamina,inj_fac,mpm)
            # player.goal_keeping[0] -= decrease_stats(player.goal_keeping[1],stamina,inj_fac,mpm)
            # player.positioning[0] -= decrease_stats(player.positioning[1],stamina,inj_fac,mpm)
            # player.ball_control[0] -= decrease_stats(player.ball_control[1],stamina,inj_fac,mpm)            
            for str_stat_2 in ["freekick_accuracy", "corner_accuracy", "penalty_accuracy"]:
                stat = getattr(player, str_stat)
                setattr(player,str_stat,[stat[0]-decrease_stats(stat[1],stamina,inj_fac,mpm,8),stat[1]])
                # stat = getattr(player,str_stat_2)
                # stat[0] -= decrease_stats_two(stat[1],stamina,inj_fac,mpm,8)
            # player.freekick_accuracy[0] -= decrease_stats_two(player.freekick_accuracy[1],stamina,inj_fac,mpm)
            # player.corner_accuracy[0] -= decrease_stats_two(player.corner_accuracy[1],stamina,inj_fac,mpm)
            # player.penalty_accuracy[0] -= decrease_stats_two(player.penalty_accuracy[1],stamina,inj_fac,mpm)
    return team

def injuries_passing(team):
    for player in team.players:
        if player.injured > 0:
            player.injured= max(0,player.injured-1)
    return team


def setup_start(home_team,away_team):
    for player in home_team.players:
        player.home_or_away =0
        player.color = blue_cyan
    for player in away_team.players:
        player.home_or_away =1
        player.color=red
        player.position = [1-player.position[0],1-player.position[1]]
    for player in home_team.players +away_team.players:
        player.yellow_cards[0]=0
        player.red_cards[0]=0
        player.goals[0]=0    
        
    return(home_team,away_team)
        
    #Verder bij close, passing en balloutself zijn geupdatet

def match_second(matchdata):
     
#     home_team,away_team = setup_start(home_team,away_team)
#     teams= [home_team,away_team]
    
        
   
#     #class property players home or away
   
#     # matchdata= class_matchdata(home_team,away_team,human_playing)
#     matchdata = class_matchdata(home_team,away_team)
#     possession_histo =[[0]*len(home_team.players),[0]*len(away_team.players)]
#     situation_histo =[0]*6 
#     # shots = 0
#     # penalties =0
#     # cornerc =0
#     # total_poss = [0,0]
# #    home_team = implement_setup_home(home_team)
# #    away_team = implement_setup_away(away_team)
#     # home_team = implement_setup(home_team,0)
#     # away_team = implement_setup(away_team,1)
#     for team in teams:
#         team=stats_begin(team)
#     secpermin =60
#     minpermatch = 90
#     for matchdata.minute in range(0,minpermatch):
#         # if human_playing > 0: print(str(matchdata.minute)+"'")
#         for matchdata.second in range(0,secpermin):
    
    
    
    #matchdata should probably incorporate both teams, give it back to the teams in the end
        action = random.random()
        if matchdata.situation ==0:             
            # if action< 1-0.01*matchdata.possession.opportunism[0]: #pass
            if action< 1-0.01*matchdata.possession.opportunism[0]: #pass
                matchdata = passing_total(matchdata)       
            else:
                matchdata.shots +=1
                # if human_playing > 0: print("Shot by", matchdata.possession.first_name, matchdata.possession.second_name + "!")
                matchdata=shot(matchdata)
            # if matchdata.possession.playing ==0:
            #     print("pass")
        elif matchdata.situation == 1: #ball out
            matchdata.possession = ballout(matchdata)
            matchdata.situation = 0
            # if matchdata.possession.playing ==0:
            #     print("ball_out")
        elif matchdata.situation == 2: # ball behind
            matchdata.possession = ballbehind(matchdata) 
            matchdata.situation =0
            # if matchdata.possession.playing ==0:
            #     print("ball_behind")
        elif matchdata.situation == 3:#corner
            # if human_playing > 0: print("Corner for", teams[matchdata.possession.home_or_away].name +"!")
            matchdata = corner(matchdata)
            matchdata.corners +=1
            # if matchdata.possession.playing ==0:
            #     print("corner")
        elif matchdata.situation == 4:#penalty
            matchdata =  penalty(matchdata)             
            matchdata.penalties +=1
        elif matchdata.situation == 5:#free kick
            # if human_playing > 0: print("Free kick for", teams[matchdata.possession.home_or_away].name +"!")
            matchdata =  free_kick(matchdata)             
        # matchdata.situation_histo[matchdata.situation] +=1
        # for i in range(0,2):
        #     for j in range(len(teams[i].players)):
        #        if teams[i].players[j].id_number == matchdata.possession.id_number:
        #            matchdata.total_poss[i]+=1
                   # possession_histo[i][j] +=1

        # if human_playing > 0: time.sleep(0.2)
        # if human_playing > 0:
            # if keyboard.is_pressed('s'):  # if key 's' is pressed 
                # teams[human_playing-1], matchdata.substitutions[human_playing-1] = set_up.menu(teams[human_playing-1], matchdata.substitutions[human_playing-1])
        # for team in [matchdata.home_team,matchdata.away_team]: #stamina calculations once per game minute
        #     team= stats_after_stamina(team,minpermatch)
    # if human_playing > 0: print(possession_histo)
    # if human_playing > 0: print("Total possession:", total_poss)
    # if human_playing > 0: print("Total situations:", situation_histo)
    
    # injuries_passing(teams)
    # for team in teams:
    #     team=stats_begin(team)
        # if matchdata.possession.playing ==0:
        for play_player in matchdata.away_team.players[11:]:
            if play_player ==  matchdata.possession:
                print(play_player.playing)
        
        return matchdata

team1,team2 = initp.create_basic_team("Julianadorp"), initp.create_basic_team("Roodeschool")

