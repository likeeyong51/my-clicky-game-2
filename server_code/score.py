import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media
import json
from datetime import datetime

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
    '''add player's score card to the score table'''
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
    '''get player's score history list'''
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

def get_backup_history_data(player_name):
    """
    Retrieves player's score history rows and prepares a list of dictionaries for backup.
    Returns a tuple: (list_of_score_rows, list_of_backup_dictionaries).
    If player not found, returns (None, None).
    If player found but no history, returns ([], []).
    """
    # get player
    if player_row:= app_tables.player.get(player=player_name):
        # search player's score history
        history_rows = app_tables.score.search(player=player_row)

        if len(history_rows) > 0:
            # backup to a list of dictionary
            backup_score_data = [{
                "player":player_name,
                "level":score['level'],
                "score":score['score'],
                "target_count":score['target_count']
            } for score in history_rows]
    
            return history_rows, backup_score_data

    return None, None # player not found

@anvil.server.callable
def build_score_history(player_name):
    '''backup player's score history into a json file for download'''
    if not player_name:
        return None

    # get player's history and backup score list
    history_rows_to_delete, backup_score_list = get_backup_history_data(player_name)
    # history, backup_score = get_backup_history(player_name)
    # check for zero history
    if history_rows_to_delete is None:
        return None # history does not exist

    # Create a unique backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Sanitise player_name for filename if it can contain special characters
    safe_player_name = "".join(c if c.isalnum() or c in (' ','.','_') else '_' for c in player_name).rstrip()
    # create a backup file name
    backup_filename = f'{safe_player_name}_score_backup_{timestamp}.json'

    # Convert the backup data to a JSON string
    try:
        json_string = json.dumps(backup_score_list, indent=2) # indent for readability
    except TypeError as e:
        # This might happen if your score data contains non-serializable types
        print(f"Error serializing backup data to JSON for player {player_name}: {e}")
        # raise anvil.server.ExecutionError(f"Could not serialize backup data: {e}") # Or return an error object
        return {"error": f"Could not serialize backup data: {e}"}

    # Create a Media object from the JSON string
    backup_media = anvil.BlobMedia(
        content_type='application/json',
        content=json_string.encode('utf-8'),  # Must be bytes
        name=backup_filename
    )

    # Return the Media object. Anvil will handle making it downloadable for the client.
    return backup_media

@anvil.server.callable
def delete_score_history(player_name):
    '''find and delete all the player's score history'''
    # get player's history and backup score list
    history_rows_to_delete, backup_score_list = get_backup_history_data(player_name)
    # history, backup_score = get_backup_history(player_name)
    # check for zero history
    if history_rows_to_delete is None:
        return False # history does not exist
        
    # empty player history from main table
    for row in history_rows_to_delete:
        row.delete()
    
    return True # history found and deleted
    
@anvil.server.callable
def empty_and_backup_history(player_name):
    """
    Backs up a player's score history to a JSON Media object,
    deletes the history from the database, and returns the Media object for download.
    Returns:
        - anvil.Media object: On success, for client-side download.
        - None: If the player is not found.
        - anvil.Media object (with empty JSON array): If player exists but has no history.
    """
    if not player_name:
        return None
        
    # get player's history and backup score list
    history_rows_to_delete, backup_score_list = get_backup_history_data(player_name)
    # history, backup_score = get_backup_history(player_name)
    # check for zero history
    if history_rows_to_delete is None:
        return None # history does not exist
        
    # Create a unique backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Sanitise player_name for filename if it can contain special characters
    safe_player_name = "".join(c 
                               if c.isalnum() or c in (' ','.','_') 
                               else '_' 
                               for c in player_name).rstrip()
    # create a backup file name
    backup_filename = f'{safe_player_name}_score_backup_{timestamp}.json'

    # Convert the backup data to a JSON string
    try:
        json_string = json.dumps(backup_score_list, indent=2) # indent for readability
    except TypeError as e:
        # This might happen if your score data contains non-serializable types (e.g., datetime objects without a custom handler)
        print(f"Error serializing backup data to JSON for player {player_name}: {e}")
        # raise anvil.server.ExecutionError(f"Could not serialize backup data: {e}") # Or return an error object
        return {"error": f"Could not serialize backup data: {e}"}

    # Create a Media object from the JSON string
    backup_media = anvil.BlobMedia(
        content_type='application/json',
        content=json_string.encode('utf-8'),  # Must be bytes
        name=backup_filename
    )


    # Delete player history from the main table
    # This will happen in a single transaction if history_rows_to_delete is not excessively large.
    # If it can be very large (thousands of rows), then consider batching or background tasks.
    if history_rows_to_delete: # Only attempt deletion if there's something to delete
        # backup player history
        # with open(backup_filename, 'w') as f:
        #     json.dump(backup_score_list, f)

        # empty player history from main table
        for row in history_rows_to_delete:
            row.delete()

    print(f"Successfully backed up and emptied history for player '{player_name}'. Backup file: {backup_filename}")
    # Return the Media object. Anvil will handle making it downloadable for the client.
    return backup_media
    