import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media
import json

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

# @anvil.server.callable
def get_backup_history(player_name):
    # get player
    if player:= app_tables.player.get(player=player_name):
        # search player's score history
        history = app_tables.score.search(player=player)
        # backup to a list of dictionary
        backup_score = [{
            "player":player_name,
            "level":score['level'],
            "score":score['score'],
            "target_count":score['target_count']
        } for score in history]

        return history, backup_score

@anvil.server.callable
def empty_history(player_name):
    # get player's history and backup score list
    history, backup_score = get_backup_history(player_name)
    # check for zero history
    if history is None:
        return False # history does not exist
    
    # create a backup file name
    backup_filename = f'{player_name}_backup.json'
    # backup player history
    with open(backup_filename, 'w') as f:
        json.dump(backup_score, f)

    # Create a Media object from the backup file
    with open(backup_filename, 'rb') as f:
        backup_media = anvil.media.from_file(f)

    # empty player history from main table
    for row in history:
        row.delete()
    
    anvil.media.download(backup_media)
    
    return True # reset player history successful
        
        