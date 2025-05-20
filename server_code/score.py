import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def add_score(score_card):
    # get player
    # print(f"storing score card for {score_card['player']}")
    if player:= app_tables.player.get(player=score_card['player']):
        # print('adding row')
        # store player score
        if app_tables.score.add_row(
            player=player,
            level=score_card['level'],
            score=score_card['score'],
            target_count=score_card['target_count']
        ):
            # print('added a score card')
            return True # add score card successful

    return False # add score card failed

@anvil.server.callable
def get_score(player_name):
    # get player
    if player:= app_tables.player.get(player=player_name):
        score_list = []
        # store player score
        scores = app_tables.score.search(player=player)
        # check if player has a score history
        # print(len(scores))
        if len(scores) >= 1:
            score_list = [
                {
                    'player': player_name,
                    'level': hist['level'],
                    'score': str(hist['score']) + '/' + str(hist['target_count'])
                } for hist in scores
            ]
            
        # print(score_list)
        return score_list # return player's history

    return None # player does not have a history yet