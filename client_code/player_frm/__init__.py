from ._anvil_designer import player_frmTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# from anvil import Notification
from ..game_frm import game_frm
import anvil.media

class player_frm(player_frmTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    def load_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.player_txb.text: # if player name is not empty
            self.player_txb.text = self.player_txb.text.strip().title()
            # add player to player's table
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
            self.item['player']   = self.player_txb.text
            self.game_frm         = game_frm(self, player=self.item['player'].title())
            self.game_pnl.add_component(self.game_frm)
            # show game panel
            self.game_pnl.visible = True
            # show history option if available
            if anvil.server.call('get_score', self.player_txb.text) is not None:
                self.history_chk.visible  = True
                self.download_btn.visible = True
            else:
                self.history_chk.visible  = False
                self.download_btn.visible = False
                
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
        '''called from game_frm - to refresh score list after each game'''
        self.history_chk.raise_event('change')
        self.refresh_data_bindings()

    def reset_hist_chk_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        # confirm with user if reset history is a go
        if not alert(
            'Are you sure you want to reset your score history?',
            buttons=[('Yes', True), ('No', False)]):
            # reset ui and exit if user cancel
            self.reset_hist_chk.checked = False
            return
        
        # ask if the user wants a backup
        user_wants_backup = alert(
            'Do you want a copy of your score history?',
            buttons=[('Yes', True), ('No', False)])
        
        # assume these at the start:
        backup_media_obj           = None
        history_successfully_reset = False
        player_id                  = self.item['player']
        
        if user_wants_backup:
            # try tp build the backup file
            backup_media_obj = anvil.server.call('build_score_history', player_id)

            if backup_media_obj:
                # backup was successfully prepared.  Now, delete the history
                if anvil.server.call('delete_score_history', player_id):
                    Notification('Your history has been reset.  Your back is downloading...').show()
                    # download the prepared backup
                    anvil.media.download(backup_media_obj)
                    history_successfully_reset = True
                else:
                    # Backup was made, but deletion failed. This is an error state.
                    # The user still has their data in backup_media_obj if we chose to download it,
                    # but it's safer not to download if the primary operation (delete) failed.
                    Notification('Score history backup was prepared, but an error occurred while resetting your history. Please try again.').show()
            else:
                # No history found to back up (and thus nothing to reset in this path)
                Notification('No score history found to back up or reset.').show()
        else:
            # User does not want a backup. Just try to delete.
            if anvil.server.call('delete_score_history', player_id):
                Notification('Your history has been reset.').show()
                history_successfully_reset = True
        
        # update ui if reset was successful
        if history_successfully_reset:
            # Confirm score history deletion by fetching the (hopefully empty) new state
            score_history_after_reset = anvil.server.call('get_score', player_id)
        
            # If score history is available (should be None or empty after reset)
            # Ensure self.score_pnl.items handles None gracefully, e.g., by treating it as an empty list
            self.score_pnl.items = score_history_after_reset if score_history_after_reset is not None else []
            self.refresh_data_bindings()

        # Always reset the ui checkbox at the end for the remaining choices
        self.reset_hist_chk.checked = False
        

    def download_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        # get a copy of the score history
        backup_media = anvil.server.call('build_score_history', self.item['player'])

        # activate download is available
        if backup_media is None:
            Notification('No score history found...').show()
        else:
            anvil.media.download(backup_media)
