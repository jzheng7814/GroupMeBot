from basketball_reference_scraper.box_scores import get_box_scores
from basketball_reference_scraper.teams import get_team_stats
from basketball_reference_scraper.players import get_stats
from flask import Flask, request, jsonify

def match_result_str(date, team1, team2):
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

def player_match_stats_str(date, team1, team2, player):
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

app = Flask(__name__)

@app.route('/postjson', methods=['POST'])
def home():
    data = request.json
    print(jsonify(data))
    return jsonify(data)

app.run(debug=True, port=4096)