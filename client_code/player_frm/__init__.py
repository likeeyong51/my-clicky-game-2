from ._anvil_designer import player_frmTemplate
from anvil import *
from ..game_frm import game_frm

class player_frm(player_frmTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    def load_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.player_txb.text:
            # show game panel
            self.game_pnl.visible= True
            # load game form
            self.game_pnl.add_component(game_frm())
