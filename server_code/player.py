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
def add_player(player_name):
    '''adds a new player to the player table'''
    # check if the player exists in the player table
    if app_tables.player.get(player=player_name):
        return False # the player exists
        
    if app_tables.player.add_row(player=player_name):
        return True # added successfully
