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
    if player := app_tables.player.get(player=score_card['player']):
        # store player score
        if app_tables.score.add_row(
            player=player,
            level=score_card['level'],
            score=score_card['score'],
            target_count=score_card['target_count']
        ):
            return True # add score card successful

    return False # add score card failed