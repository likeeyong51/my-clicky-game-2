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

    def load_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.player_txb.text:
            self.player_txb.text = self.player_txb.text.title()
            if anvil.server.call('add_player', player_name=self.player_txb.text):
                Notification(f'{self.player_txb.text} added').show()
            else:
                Notification(f'{self.player_txb.text} has been taken.\nRegister a new player name if you are a new user').show()

            # reset history options
            self.score_grd.visible   = False
            self.score_pnl.items     = None
            self.history_chk.checked = False
            self.history_chk.raise_event('change')
            # clear old
            self.game_pnl.clear()
            # load game form
            self.game_frm = game_frm(self, player=self.item['player'].title())
            self.game_pnl.add_component(self.game_frm)
            # show game panel
            self.game_pnl.visible = True
            # show history option if available
            if anvil.server.call('get_score', self.player_txb.text) is not None:
                self.history_chk.visible = True
            else:
                self.history_chk.visible = False
                
        else: # name is empty
            Notification('Please enter your name').show()

    def hide_player_card(self, show):
        self.player_crd.visible = show

    def history_chk_change(self, **event_args):
        """This event toggles between show and hide player's history"""
        # check if game component has been loaded
        if self.history_chk.checked and self.game_frm in self.game_pnl.get_components():
            score_history = anvil.server.call('get_score', self.item['player'])
            # if score history is available
            if score_history is not None: 
                # toggle history_chk
                self.history_chk.text  = "Hide history"
                # add score list to the score panel
                self.score_pnl.items   = score_history
                # show score panel
                self.score_grd.visible = True
                # for score in score_history:
                #     print(f"Level: {score['level']} Score:{score['score']}")
        else:
            # toggle check option back to show player's history
            self.history_chk.text  = "Show history"
            self.score_grd.visible = False
                

    def refresh_bindings(self):
        '''called from game_frm'''
        self.history_chk.raise_event('change')
        self.refresh_data_bindings()
