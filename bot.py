from basketball_reference_scraper.box_scores import get_box_scores
from basketball_reference_scraper.teams import get_team_stats
from basketball_reference_scraper.players import get_stats
from flask import Flask, request, jsonify
from groupy import Client

def match_result(date, team1, team2):
    output_str = 'Match Results:'

    d = get_box_scores(date, team1, team2)
    team1dict = list(d[team1].to_dict('records'))
    team2dict = list(d[team2].to_dict('records'))
    team1score = team1dict[-1]['PTS']
    team2score = team2dict[-1]['PTS']
    notable_players = []

    for i in [*team1dict, *team2dict]:
        try:
            int(i['PTS'])
        except:
            continue

        if int(i['PTS']) >= 20:
            notable_players.append(i)

    output_str += f'Match score: {team1} {team1score} : {team2score} {team2}\n\n'
    for i in notable_players:
        if i['PLAYER'] == 'Team Totals':
            continue

        for j in i.items():
            output_str += f'{j[0]}: {j[1]}\n'
        output_str += '\n'

    return output_str

def player_match_stats(date, team1, team2, player):
    output_str = f'{player} Match Stats:'

    d = get_box_scores(date, team1, team2)
    team1dict = list(d[team1].to_dict('records'))
    team2dict = list(d[team2].to_dict('records'))
    
    for i in [*team1dict, *team2dict]:
        if i['PLAYER'] == player:
            for j in i.items():
                output_str += f'{j[0]}: {j[1]}\n'
    
    return output_str

def player_form(player):
    output_str = '{player} Form Over Current Season:\n'

    d = get_stats(player)
    playerdict = list(d.to_dict('records'))[-1]

    for j in playerdict.items():
        output_str += f'{j[0]}: {j[1]}\n'
    
    return output_str

def team_stats(team, season = 2021):
    output_str = f'{team} Form Over {season - 1}-{season} Season:\n'

    d = get_team_stats(team, season).to_dict()
    for j in d.items():
        output_str += f'{j[0]}: {j[1]}\n'
    
    return output_str

def help():
    return \
    """My commands are:
        match_result [date in format YYYY-MM-DD] [Team 1 Abbreviation] [Team 2 Abbreviation]
        player_match_stats [date in format YYYY-MM-DD] [Team 1 Abbreviation] [Team 2 Abbreviation] [Player Full Name]
        player_form [Player Full Name]
        team_stats [Team Abbreviation] [Optional: Season End Year (e.g. 2020-2021 season is 2021)]
    """

client = Client.from_token('XzJ1vmbfp1mkmDRQyGejQMvXrIEI56ndIYY7G6zM')
group = None
bot = None
for g in client.groups.list().autopage():
    if g.name == '#SurvivePreAP':
        group = g
        break

for b in client.bots():
    if b.bot_id == '	7304ee8ea1ca2a73edf126a614':
        bot = b
        break

app = Flask(__name__)

@app.route('/', methods=['POST'])
def home():
    global group

    data = request.json
    msgtext = data['text']
    args = msgtext.split()
    retstr = ''

    if args[0] != '>>>':
        return jsonify(success=True)

    try:
        if args[1] == 'match_result':
            retstr = match_result(args[2], args[3], args[4])
        elif args[1] == 'player_match_stats':
            retstr = player_match_stats(args[2], args[3], args[4], args[5])
        elif args[1] == 'player_form':
            retstr = player_form(args[2])
        elif args[1] == 'team_stats':
            if len(args) == 2:
                retstr = team_stats(args[2])
            elif len(args) == 3:
                retstr = team_stats(args[2], int(args[3]))
            else:
                retstr = 'Invalid Arguments'
        elif args[1] == 'help':
            retstr = help()
        else:
            retstr = 'Invalid Request'
    except:
        retstr = 'Internal Server Error'

    bot.post(text=retstr)

    return jsonify(success=True)

app.run(host='0.0.0.0', port=80)

