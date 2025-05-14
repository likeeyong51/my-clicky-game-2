from ._anvil_designer import player_frmTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# from anvil import Notification
from ..game_frm import game_frm

class player_frm(player_frmTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        print('player form')

    def load_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.player_txb.text:
            # if not anvil.server.call('add_player', player_name=self.item['player']):
            #     Notification('Add player failed').show()
            # clear old
            self.game_pnl.clear()
            # load game form
            self.game_pnl.add_component(game_frm(player=self.item['player'].title()))
            # show game panel
            self.game_pnl.visible= True
        # else:
        #     Notification('Please enter your name').show()

    def hide_player_card(self, show):
        self.player_crd.visible = show
        