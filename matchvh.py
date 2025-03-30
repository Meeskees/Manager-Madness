import random
import math
import time
import set_upv5 as set_up
import init_players_and_teams as initp
from keyboardmaster import keyboard

class class_matchdata:
    
    def __init__(self,home_team,away_team,human_playing):
        self.teams = [home_team,away_team]
        self.human_playing = human_playing
        self.possession = find_piecetaker(home_team,0)
        self.score=[0,0]
        self.minute = 0
        self.second = 0
        self.situation = 0
        self.position = [0,0]
        self.substitutions = [[1,0],[1,0]]

def find_player(team,player):
    for i in range(len(team.players)):
        if team.players[i].id_number == player.id_number:
            return i
    return 0

def find_player_id(team,player_id):
    for i in range(len(team.players)):
        if team.players[i].id_number == player_id:
            return i
    return 0

def nr_players_in_team(team):
    return sum(team.players[i].playing for i in range(len(team.players)))

def players_on_field(teams):
    [home_team,away_team]=teams
    home_players_on_field = []
    away_players_on_field = []
    for i in range(len(home_team.players)):
        if home_team.players[i].playing == 1:
            home_players_on_field.append(home_team.players[i])
    for i in range(len(away_team.players)):
        if away_team.players[i].playing == 1:
            away_players_on_field.append(away_team.players[i])
    return [home_players_on_field,away_players_on_field]
    

def find_piecetaker(team,set_piece): #0 keeper,1 free kick, 2 corner, 3 penalty
    if set_piece ==0:
        for j in range(len(team.players)):
            if team.players[j].is_keeper == 1:
                return team.players[j]
    elif set_piece ==1:
        for j in range(len(team.players)):
            if team.players[j].takes_freekick == 1:
                return team.players[j]
    elif set_piece ==2:
        for j in range(len(team.players)):
            if team.players[j].takes_corner == 1:
                return team.players[j]
    elif set_piece ==3:
        for j in range(len(team.players)):
            if team.players[j].takes_penalty == 1:
                return team.players[j]
    return 0
    
def goal(teams,matchdata):
#    print("Goal: " + matchdata.possession.first_name+" "+ matchdata.possession.second_name)
    posshoa = matchdata.possession.home_or_away #is possessor at home or away?
    defending_team=teams[1-posshoa]
    attacking_team= teams[posshoa]
    keeper = find_piecetaker(defending_team,0)
    scorer= attacking_team.players[find_player(attacking_team, matchdata.possession)]
    for i in range(2):
       if posshoa==i:
           matchdata.score[i] +=1
           for j in range(3):
               teams[i].goals_for[j] +=1 #adding goal scored team
               teams[i].players[find_player(attacking_team, matchdata.possession)].goals[j] +=1 # adding goal scored player
               teams[1-i].goals_against[j] +=1 #adding goal conceived team
    if matchdata.human_playing > 0:
        print(str(matchdata.minute)+":"+str(matchdata.second)+ " Goal Team "+ str(attacking_team.name) 
        +" by " +str(scorer.first_name)+ " "+ str(scorer.second_name)+"! " + str(matchdata.score[0]) + "-" +  str(matchdata.score[1]))
    matchdata.possession = keeper
    return teams,matchdata

def freekick_shot(teams,matchdata):
    posshoa = matchdata.possession.home_or_away
    matchdata.situation =0
    keeper = find_piecetaker(teams[1-posshoa],0)
    freekicker = find_piecetaker(teams[posshoa],1)
    [x1,y1] = matchdata.position
    fkshoot = freekicker.freekick_accuracy[0]
    keepskill = keeper.goal_keeping[0]
    root =math.sqrt(1.49)
    distg = distance(x1,y1,0.5,1-posshoa)
    fkshotprob=distg/root*(1/100)*fkshoot+(root-distg)/root*fkshoot 
    if random.uniform(0,1) > fkshotprob : #target missed
        if matchdata.human_playing > 0: print("Miss!")
        matchdata.situation = 2        
    else:
        saveprob= ((root-distg)/root)*keepskill+distg/root
        if  saveprob*random.uniform(0,1)< fkshotprob*random.uniform(0,2/3): #goal
            teams,matchdata = goal(teams,matchdata)
        else:
            result = random.uniform(0,1)
            if result < keepskill: #keeper saves
                matchdata.possession = keeper
                if matchdata.human_playing > 0: print("Keeper saves!")
            elif result < keepskill + 2/7*(1-keepskill): # offender gets ball
                matchdata.position = [0.5,1-posshoa]
                matchdata.possession = close(teams,matchdata,posshoa)
            elif result < keepskill + 5/7*(1-keepskill): # defender gets ball
                matchdata.position = [0.5,1-posshoa]
                matchdata.possession = close(teams,matchdata,1-posshoa)
            else: #penalty
                matchdata.situation = 4
    return teams,matchdata

def free_kick(teams,matchdata):
    posshoa = matchdata.possession.home_or_away
    keeper = find_piecetaker(teams[1-posshoa],0)
    freekicker = find_piecetaker(teams[posshoa],1)
    matchdata.possession = freekicker
    [x1,y1] = matchdata.position
    freekickacc = freekicker.freekick_accuracy[0]
    players_ofl=players_on_field(teams) 
    keepskill = keeper.goal_keeping[0]
    root =math.sqrt(1.49)
    heads = [[0]*len(players_ofl[i]) for i in range(2)]
    opp = freekicker.opportunism[0]
    root=math.sqrt(1.49)
    crosspass=[ random.uniform(0,1)]*3
    for i in range(2):
        for j in range(len(players_ofl[i])):
            [x1,y1] =players_ofl[i][j].position
            dist = distance(x1,y1,1-posshoa,0.5)
            headskill = players_ofl[i][j].heading[0]
            heads[i][j] = (root-dist)/root*headskill
            if players_ofl[i][j].takes_freekick == 1: #free kicker cannot head
                heads[i][j] =0
    cumheads = [sum(heads[0]),sum(heads[1])]
    choice_of_action = random.uniform(0,1)
    if choice_of_action < (1-opp)/4: #quick pass
        matchdata.situation =1
        matchdata.position = [0,0]
        return teams,matchdata
    if choice_of_action > (4-3*opp)/4: #shot
        teams,matchdata = freekick_shot(teams,matchdata)
        return teams,matchdata    
    if (1-freekickacc)*0.1 > crosspass[0]: #ball goes behind
        matchdata.situation =3
        matchdata.position = [0,0]
        return teams,matchdata
    elif (1-freekickacc)*0.17 > crosspass[0]: #ball goes out
        matchdata.situation =2
        matchdata.position = [0,0]
        return teams,matchdata
    if (cumheads[posshoa]*2*freekickacc-cumheads[1-posshoa])/(cumheads[0]+cumheads[1]+0.01) < crosspass[1]:
        matchdata.position=[1-posshoa,0.5]
        matchdata.possession = close(teams,matchdata,posshoa)
    else:
        playerheader = weighted_pick(heads[posshoa])
        if (1-players_ofl[posshoa][playerheader].heading[0])*0.1> random.uniform(0,1): #player heads out
            matchdata.possession = keeper
            matchdata.situation =0
            matchdata.position = [0,0]
            return teams,matchdata          
        if players_ofl[posshoa][playerheader].heading[0]*random.uniform(0.85,1.15) > keepskill:
            matchdata.possession = players_ofl[posshoa][playerheader]
            teams,matchdata= goal(teams,matchdata)
        else:
            if 0.5*crosspass[2] < keepskill:
                matchdata.possession = keeper #keeper got the ball
            else:
                matchdata.position=[1-posshoa,0.5]
                matchdata.possession = close(teams,matchdata,posshoa) #offender gets the abll
    matchdata.situation =0
    matchdata.position = [0,0]
    return teams,matchdata

def corner(teams,matchdata):
    posshoa = matchdata.possession.home_or_away    
#    poss=matchdata.possession
    keeper = find_piecetaker(teams[1-posshoa],0)
    cornerkicker = find_piecetaker(teams[posshoa],2)
    matchdata.possession = cornerkicker
    [x1,y1] = matchdata.position
    corneracc = cornerkicker.corner_accuracy[0]
    players_ofl=players_on_field(teams) 
    keepskill = keeper.goal_keeping[0]
    root =math.sqrt(1.49)
    heads = [[0]*len(players_ofl[i]) for i in range(2)]
    opp = cornerkicker.opportunism[0]
    root=math.sqrt(1.49)
    crosspass=[ random.uniform(0,1)]*3
    for i in range(2):
        for j in range(len(players_ofl[i])):
            [x1,y1] =players_ofl[i][j].position
            dist = distance(x1,y1,1-posshoa,0.5)
            headskill = players_ofl[i][j].heading[0]
            heads[i][j] = (root-dist)/root*headskill
            if players_ofl[i][j].takes_freekick == 1: #free kicker cannot head
                heads[i][j] =0
    cumheads = [sum(heads[0]),sum(heads[1])]
    choice_of_action = random.uniform(0,1)
    if choice_of_action < (1-opp)/2: #quick pass
        matchdata.situation =1
        matchdata.position = [0,0]
        return teams,matchdata
    if (1-corneracc)*0.1 > crosspass[0]: #ball goes behind
        matchdata.situation =3
        matchdata.position = [0,0]
        return teams,matchdata
    elif (1-corneracc)*0.17 > crosspass[0]: #ball goes out
        matchdata.situation =2
        matchdata.position = [0.5,1-posshoa]
        return teams,matchdata
    if (cumheads[posshoa]*2*corneracc-cumheads[1-posshoa])/(cumheads[0]+cumheads[1]+0.01) < crosspass[1]:
        matchdata.position=[1-posshoa,0.5]
        matchdata.possession = close(teams,matchdata,posshoa)
    else:
        playerheader = weighted_pick(heads[posshoa])
        if (1-players_ofl[posshoa][playerheader].heading[0])*0.1> random.uniform(0,1): #player heads out
            matchdata.possession = keeper
            matchdata.situation =0
            matchdata.position = [0,0]
            return teams,matchdata          
        if players_ofl[posshoa][playerheader].heading[0]*random.uniform(0.85,1.15) > keepskill:
            matchdata.possession = players_ofl[posshoa][playerheader]
            teams,matchdata= goal(teams,matchdata)
        else:
            if 0.5*crosspass[2] < keepskill:
                matchdata.possession = keeper #keeper got the ball
            else:
                matchdata.position=[1-posshoa,0.5]
                matchdata.possession = close(teams,matchdata,posshoa) #offender gets the abll
    matchdata.situation =0
    matchdata.position = [0,0]
    return teams,matchdata

def penalty(teams,matchdata):
    posshoa = matchdata.possession.home_or_away
    penalty_taker = find_piecetaker(teams[posshoa],3)
    matchdata.possession = penalty_taker
    keeper = find_piecetaker(teams[1-posshoa],0)
    penaltyacc = penalty_taker.penalty_accuracy[0]
    keepskill = keeper.goal_keeping[0]    
    matchdata.situation =0   
    distg=0.11
    root=math.sqrt(1.49)
    shoot = penalty_taker.shooting[0]
    shotprob=(root-distg)/root*(1/4)*(shoot+penaltyacc+2)+distg/root*(shoot+penaltyacc+6)/8
    if matchdata.human_playing > 0: 
        print("Penalty!")
    if random.uniform(0,1) > shotprob : #target missed
        if matchdata.human_playing > 0:
            print("Miss!")
        matchdata.situation =2 
        matchdata.position = [0.5,1-posshoa]
        return teams,matchdata
    else:
        saveprob= (root-distg)/root*keepskill+distg/root
        if  random.uniform(0,1)> saveprob-(1/2)* shotprob: #goal
            [teams,matchdata] = goal(teams,matchdata)
        else:
            result = random.uniform(0,1)
            if result < keepskill: #keeper saves
                matchdata.possession = keeper
                #print("Keeper saves!")
            elif result < keepskill + 2/7*(1-keepskill): # offender gets ball
                matchdata.position=[0.5,1-posshoa]
                matchdata.possession = close(teams,matchdata,posshoa)
            elif result < keepskill + 5/7*(1-keepskill): # defender gets ball
                matchdata.position=[0.5,1-posshoa]
                matchdata.possession = close(teams,matchdata,1-posshoa)
            else:
                matchdata.situation = 4
    return teams,matchdata

def sent_off(teams, player_sent_off,team_nr):
    team=teams[team_nr]
    player_sent_off=team.players[find_player(team, player_sent_off)]
    player_sent_off.playing=0
    if player_sent_off.is_keeper == 1:
        for player in team.players:
            if all( player.playing*player.is_keeper ==0 for player in team.players):
                if player.playing ==1:
                    player.is_keeper = 1
                    player.position =[0,0]
    if player_sent_off.takes_freekick == 1:
        for player in team.players:
            if all( player.playing*player.takes_freekick ==0 for player in team.players):
                if player.playing ==1:
                    player.takes_freekick = 1
    if player_sent_off.takes_corner == 1:
        for player in team.players:
            if all( player.playing*player.takes_corner ==0 for player in team.players):
                if player.playing ==1:
                    player.takes_corner = 1
    if player_sent_off.takes_penalty == 1:
        for player in team.players:
            if all( player.playing*player.takes_penalty ==0 for player in team.players):
                if player.playing ==1:
                    player.takes_penalty = 1
    return teams

def foul(teams,matchdata,offender):
    posshoa = matchdata.possession.home_or_away
    possession=matchdata.possession
    possessor=teams[posshoa].players[find_player(teams[posshoa], matchdata.possession)]
    offender= teams[1-posshoa].players[find_player(teams[1-posshoa], possession)]
    intensity = random.uniform(0,1)
    aggressiveness = offender.aggression[0]
    matchdata.position = possession.position
    if matchdata.human_playing > 0:
        print("Foul!")
    if 0.4 < (aggressiveness+random.normalvariate(0,0.3))*intensity : #yellow card
        if matchdata.human_playing > 0: 
            print(str(offender.first_name)+ " "+ str(offender.second_name) +" booked! (Yellow card)")        
            for j in range(3):
                offender.yellow_cards[j] += 1
        if offender.yellow_cards[0]==2:
            for j in range(3):
                offender.red_cards[j] += 1
            teams= sent_off(teams,offender,1-posshoa)
    elif 0.8 < (aggressiveness+random.normalvariate(0,0.3))*intensity : #red card
        if matchdata.human_playing > 0: 
            print(str(offender.first_name)+ " "+ str(offender.second_name) +" booked! (Red card)")  
            for j in range(3):
                offender.red_cards[j] += 1
        teams= sent_off(teams,offender,1-posshoa)
    if intensity > 0.995:
        possessor.injured=1
        possessor = stats_updated_player(possessor,0)
        if matchdata.human_playing > 0:  #injury
            print( possessor.first_name +  possessor.second_name + " injured!")
            for k in range(2):
                if matchdata.human_playing ==k:
                    nr =matchdata.human_playing-1
                    teams[nr],matchdata.substitutions[nr] = set_up.menu(teams[nr],matchdata.substitutions[nr]) 
    matchdata.situation = 5
    return teams,matchdata 

def distance(x1,y1,x2,y2):
    return math.sqrt((0.49*(x1-x2))**2+(y1-y2)**2)

def close(teams,matchdata,team_nr):# pick a person close to x1,y1 from team team_nr
    players_ofl=players_on_field(teams)    
    root = math.sqrt(1.49)
    playersinteam = len(players_ofl[team_nr])
    if playersinteam == 0: print('Kaduuk!')
    dist = [0]*playersinteam
    for i in range(playersinteam):
        dist[i]= root - distance(matchdata.position[0],matchdata.position[1],players_ofl[team_nr][i].position[0],players_ofl[team_nr][i].position[1])
    return teams[team_nr].players[find_player(teams[team_nr],players_ofl[team_nr][weighted_pick(dist)])]


def weighted_pick(list_pos_floats):
    try:
        random.choices(list(range(len(list_pos_floats))),list_pos_floats)[0] = float(random.choices(list(range(len(list_pos_floats))),list_pos_floats)[0])
    except IndexError:
        print('List of floats:')
        print(list_pos_floats)
    return random.choices(list(range(len(list_pos_floats))),list_pos_floats)[0]

def ballout(teams,matchdata,last_toucher):
    matchdata.position= last_toucher.position
    return close(teams,matchdata,last_toucher.home_or_away)

def ballbehind(teams,matchdata,last_toucher):
    keeper= find_piecetaker(teams[1-last_toucher.home_or_away],0)
    return keeper
        
def balloutself(teams, matchdata,aimed_at,distp):
    matchdata.situation =0
    posshoa=matchdata.possession.home_or_away
    keeper = find_piecetaker(teams[1-posshoa],0)  
    shortp = matchdata.possession.short_pass[0]
    longp = matchdata.possession.long_pass[0] 
    root =math.sqrt(1.49)
    if matchdata.possession.id_number == aimed_at.id_number:
        outprob = (matchdata.possession.ball_control[0]+7)/8 #chemistry somewhere here as well?
    else:
        outprob = (matchdata.possession.ball_control[0]+3*aimed_at.ball_control[0]+8)*(((root-distp)/root)*shortp+distp*longp/root+9)/(90*(1+distp**2))
    if  random.uniform(0,1) > outprob:#ball goes out without interception
        [x2,y2]=aimed_at.position
        typeout = random.uniform(0,1)
        widthprob = 1-1/6*(x2-x2**2)
        posneg= 2*(posshoa -1/2)
        lengthprob = ((1- posshoa)+posneg*y2)*widthprob + (posshoa-posneg*y2)*(1-widthprob)
        if typeout < widthprob: #throw in opponent
            matchdata.position = [x2,y2]
            matchdata.position[0]=1-posshoa
            matchdata.possession = close(teams,matchdata,1-posshoa)
            matchdata.situation =0
            matchdata.position = [0,0]
        elif typeout <lengthprob: #behind, for the opponent keeper
            matchdata.possession = keeper
        else: # opponent corner
            matchdata.situation= 3
            
    return matchdata

def passing(teams,matchdata): #determine to whom the pass goes
    posshoa=matchdata.possession.home_or_away
    players_ofl=players_on_field(teams)
    players_choice = players_ofl[posshoa]
    chemistry =0.5
    aimed_at = [0,0]
    opp = matchdata.possession.opportunism[0]
    [x1,y1] =  matchdata.possession.position
    playersinteam = len(players_ofl[posshoa])
    newprob = [0]*playersinteam
    distp = [0]*playersinteam
    for i in range(playersinteam):
        [x2,y2] = players_choice[i].position
        distp[i]=distance(x1,y1,x2,y2)
        posit = players_choice[i].positioning[0] 
        newprob[i]= 20/(1+10000*distp[i]**2)+((posit+1)/2)*chemistry*math.exp(-((x2-x1-2*opp+1)**2))
    j= weighted_pick(newprob)
    aimed_at = teams[posshoa].players[find_player(teams[posshoa],players_ofl[posshoa][j])]
    return [matchdata,aimed_at,distp[j]]

def interception(teams,matchdata,aimed_at,distp):# decide if there is an interception
    posshoa=matchdata.possession.home_or_away
    poss=matchdata.possession
    players_ofl=players_on_field(teams)     
    [x1,y1] = poss.position
    [x2,y2] = aimed_at.position
    [shortp,longp] = [poss.short_pass[0],poss.long_pass[0]]
    root =math.sqrt(1.49)
    playersinteam = len(players_ofl[1-posshoa])
    order = list(range(0,playersinteam))
    random.shuffle(order)
    for interceptor in players_ofl[1-posshoa]:
        [x3,y3] = interceptor.position
        interc = interceptor.interception[0]
        agress = interceptor.aggression[0]
        distb= distance((x2-x1)/2,(y2-y1)/2,x3,y3)
        if poss == aimed_at: #player tries to keep ball
            ballc = poss.ball_control[0]
            intprob = random.uniform(0,1)
            newprob = 1 - (root- distb)* interc/(root*(1+ballc))
            #print("Ball control:", newprob)
            if intprob > 1 - (root- distb)* (interc+0.1*agress)/(root*40*(1.1+2*ballc)):
                matchdata.possession = interceptor
                if random.uniform(0,1) < 0.01*interceptor.aggression[0]:
                    matchdata.possession = aimed_at
                    teams,matchdata=foul(teams,matchdata,interceptor)
                    matchdata.situation=5
                    matchdata.position = [x2,y2]
                return matchdata
        else: #player tries to pass ball
            norm = (((root-distp)/root)*shortp+distp*longp/root)/((1+distp**2))
            newprob= 1-(1/40)*((root-distb)/root)*(interc+0.1*agress)/(1.1+norm)
            intprob = random.uniform(0,1)
            if intprob > newprob:
                matchdata.possession = interceptor
                if random.uniform(0,1) < 0.01*interceptor.aggression[0]:
                    teams,matchdata=foul(teams,matchdata,interceptor)
                    matchdata.situation=5
                    matchdata.position = [x2,y2]
                return matchdata
    matchdata = balloutself(teams, matchdata,aimed_at,distp) 
    return matchdata

def shot(teams,matchdata):
    matchdata.situation =0
    poss=matchdata.possession
    posshoa = matchdata.possession.home_or_away
    keeper = find_piecetaker(teams[1-posshoa],0)
    [x1,y1] = poss.position
    shoot = poss.shooting[0]
    keepskill = keeper.goal_keeping[0]
    root =math.sqrt(1.49)
    distg = distance(x1,y1,0.5,1-posshoa)
    shotprob=distg/root*(1/100)*shoot+(root-distg)/root*shoot 
    if random.uniform(0,1) > shotprob : #target missed
        if matchdata.human_playing > 0: print("Miss!")
        matchdata.situation = 2        
    else:
        saveprob= ((root-distg)/root)*keepskill+distg/root
        if  saveprob*random.uniform(0,1)< shotprob*random.uniform(0,1/2): #goal
            [teams,matchdata] = goal(teams,matchdata)
        else:
            result = random.uniform(0,1)
            if result < keepskill: #keeper saves
                matchdata.possession = keeper
                if matchdata.human_playing > 0: print("Keeper saves!")
            elif result < keepskill + 2/7*(1-keepskill): # offender gets ball
                matchdata.position = [0.5,posshoa]
                matchdata.possession = close(teams,matchdata,posshoa)
            elif result < keepskill + 5/7*(1-keepskill): # defender gets ball
                matchdata.position = [0.5,1-posshoa]
                matchdata.possession = close(teams,matchdata,1-posshoa)
            else: #penalty
                matchdata.situation = 4
    return teams,matchdata

def passing_total(teams,matchdata):
    [matchdata,aimed_at,distp]=passing(teams,matchdata)
    matchdata = balloutself(teams, matchdata,aimed_at,distp)
    if matchdata.situation == 0:
        if matchdata.possession.id_number == aimed_at.id_number:
            matchdata = interception(teams,matchdata,aimed_at,distp)

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
    for player in team.players:
        player = stats_updated_player(player,1)
    return team

def stats_updated_player(player,out_of_match): # 0 if match is going on, 1 if before or after match
    oom =out_of_match
    inj = player.injured
    inj_fac = 3/(inj+3)
    if player.playing == 1:
        player.shooting[0] = inj_fac*player.shooting[oom]
        player.heading[0] = inj_fac*player.heading[oom]
        player.long_pass[0] = inj_fac*player.long_pass[oom]
        player.short_pass[0]  = inj_fac*player.short_pass[oom]
        player.interception[0]  = inj_fac*player.interception[oom]
        player.goal_keeping[0]  = inj_fac*player.goal_keeping[oom]
        player.positioning[0]  = inj_fac*player.positioning[oom]
        player.ball_control[0]  = inj_fac*player.ball_control[oom]           
        player.opportunism[0] = inj_fac*player.opportunism[oom]
        player.aggression[0] =  inj_fac*player.aggression[oom]
        player.stamina[0] =  inj_fac*player.stamina[oom]
        player.freekick_accuracy[0]  = inj_fac*player.freekick_accuracy[oom]
        player.corner_accuracy[0]   = inj_fac*player.corner_accuracy[oom]
        player.penalty_accuracy[0] = inj_fac*player.penalty_accuracy[oom]
    return player    

def decrease_stats(stat,stamina,inj_fac,mpm):
    return inj_fac*(1-stamina[0])*stat/(4*mpm)

def decrease_stats_two(stat,stamina,inj_fac,mpm):
    return inj_fac*(1-stamina[0])*stat/(8*mpm)
    
def stats_after_stamina(team,mpm): #mpm = minutes per match
    for player in team.players:
        inj = player.injured
        inj_fac = 3/(inj+3)
        stamina= player.stamina
        if player.playing == 1:
            player.shooting[0] -= decrease_stats(player.shooting[1],stamina,inj_fac,mpm)
            player.heading[0] -= decrease_stats(player.heading[1],stamina,inj_fac,mpm)
            player.long_pass[0] -= decrease_stats(player.long_pass[1],stamina,inj_fac,mpm)
            player.short_pass[0] -= decrease_stats(player.short_pass[1],stamina,inj_fac,mpm)
            player.interception[0] -= decrease_stats(player.interception[1],stamina,inj_fac,mpm)
            player.goal_keeping[0] -= decrease_stats(player.goal_keeping[1],stamina,inj_fac,mpm)
            player.positioning[0] -= decrease_stats(player.positioning[1],stamina,inj_fac,mpm)
            player.ball_control[0] -= decrease_stats(player.ball_control[1],stamina,inj_fac,mpm)            
            
            player.freekick_accuracy[0] -= decrease_stats_two(player.freekick_accuracy[1],stamina,inj_fac,mpm)
            player.corner_accuracy[0] -= decrease_stats_two(player.corner_accuracy[1],stamina,inj_fac,mpm)
            player.penalty_accuracy[0] -= decrease_stats_two(player.penalty_accuracy[1],stamina,inj_fac,mpm)
    return team

def injuries_passing(teams):
    for team in teams:
        for player in team.players:
            if player.injured > 0:
                player.injured= max(0,player.injured-1)
    return teams

def match(home_team,away_team,human_playing):
    
    
    for player in home_team.players:
        player.home_or_away =0
    for player in away_team.players:
        player.home_or_away =1 
        
    teams = [home_team,away_team]
    #class property players home or away
    for i in range(2): #put all current cards/goals to zero
        for player in teams[i].players:
            player.yellow_cards[0]=0
            player.red_cards[0]=0
            player.goals[0]=0
    matchdata= class_matchdata(home_team,away_team,human_playing)
    possession_histo =[[0]*len(home_team.players),[0]*len(away_team.players)]
    situation_histo =[0]*6 
    shots = 0
    penalties =0
    cornerc =0
    total_poss = [0,0]
#    home_team = implement_setup_home(home_team)
#    away_team = implement_setup_away(away_team)
    home_team = implement_setup(home_team,0)
    away_team = implement_setup(away_team,1)
    for team in teams:
        team=stats_begin(team)
    secpermin =60
    minpermatch = 90
    for matchdata.minute in range(0,minpermatch):
        if human_playing > 0: print(str(matchdata.minute)+"'")
        for matchdata.second in range(0,secpermin):
            action = random.random()
            if matchdata.situation ==0:             
                if action< 1-0.01*matchdata.possession.opportunism[0]: #pass
                    matchdata = passing_total(teams,matchdata)       
                else:
                    shots +=1
                    if human_playing > 0: print("Shot by", matchdata.possession.first_name, matchdata.possession.second_name + "!")
                    (teams,matchdata)=shot(teams,matchdata)
            elif matchdata.situation == 1: #ball out
                matchdata.possession = ballout(teams,matchdata,matchdata.possession)
                matchdata.situation = 0
            elif matchdata.situation == 2: # ball behind
                matchdata.possession = ballbehind(teams,matchdata,matchdata.possession) 
                matchdata.situation =0
            elif matchdata.situation == 3:#corner
                if human_playing > 0: print("Corner for", teams[matchdata.possession.home_or_away].name +"!")
                (teams,matchdata) = corner(teams,matchdata)
                cornerc +=1
            elif matchdata.situation == 4:#penalty
                (teams,matchdata) =  penalty(teams,matchdata)             
                penalties +=1
            elif matchdata.situation == 5:#free kick
                if human_playing > 0: print("Free kick for", teams[matchdata.possession.home_or_away].name +"!")
                teams,matchdata =  free_kick(teams,matchdata)             
            situation_histo[matchdata.situation] +=1
            for i in range(0,2):
                for j in range(len(teams[i].players)):
                   if teams[i].players[j].id_number == matchdata.possession.id_number:
                       total_poss[i]+=1
                       possession_histo[i][j] +=1

        if human_playing > 0: time.sleep(0.2)
        if human_playing > 0:
            if keyboard.is_pressed('s'):  # if key 's' is pressed 
                teams[human_playing-1], matchdata.substitutions[human_playing-1] = set_up.menu(teams[human_playing-1], matchdata.substitutions[human_playing-1])
        for team in teams:
            team= stats_after_stamina(team,minpermatch)
    if human_playing > 0: print(possession_histo)
    if human_playing > 0: print("Total possession:", total_poss)
    if human_playing > 0: print("Total situations:", situation_histo)
    
    injuries_passing(teams)
    for team in teams:
        team=stats_begin(team)
        
    return [matchdata.score, teams[0],teams[1]]

# team1,team2 = initp.create_basic_team("Julianadorp"), initp.create_basic_team("Roodeschool")

# match(team1,team2,1)
