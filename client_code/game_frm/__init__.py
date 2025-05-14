from ._anvil_designer import game_frmTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from random import choice

class game_frm(game_frmTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        # get player's name
        self.item['player'] = properties['player']
        # set game parameters
        self.item['target_letter'] = 'A'
        self.item['start_timer']   = False
        self.item['level']         = 0 # up to 20 levels
        self.item['speed']         = 0.05
        # the player's score
        self.score_card = {}
        # self.score_card = {
        #     'player':self.item['player'], 
        #     'level':self.item['level'], 
        #     'score':self.item['score'], 
        #     'target_count':self.item['target_count']
        # }

        self.refresh_data_bindings()


    def start_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.start_btn.text in 'Play again':
            # change the text button to 'Click me'
            self.start_btn.text = 'Click Me'
            self.start_btn.icon = 'fa:arrow-circle-down'
            self.level_lbl.text = 'Level ' + str(self.item['level'])
            # start the game's timer countdown
            self.item['start_timer']   = True
            # set start-game parameters
            self.item['time']          = 25
            self.item['previous']      = 'X'
            self.item['score']         = 0
            self.item['target_count']  = 0
            self.item['instruction']   = f"Click on the letter '{self.item['target_letter']}' as many times as you can in 25 seconds."
            self.refresh_data_bindings()
            
        # when game is played:
        # add a point every time the player clicks on the letter A
        else: # play the game
            if self.letter_lbl.text == self.item['target_letter']:
                # add a point to the player's score
                self.item['score'] += 1
                # update scoreboard
                self.score_lbl.text = str(self.item['score']) + '/' + str(self.item['target_count'])
        

    def game_tmr_tick(self, **event_args):
        """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
        if self.item['start_timer']: # game started
            # start timer countdown
            self.item['time'] -= 1
            # update timer in ui
            self.timer_lbl.text = str(self.item['time'])
            # hide game instructions when the game starts
            self.game_crd.visible = False
            # hide player card from parent form: <My_Clicky_Game_2.player_frm.player_frm object>
            # print(get_open_form())
            get_open_form().hide_player_card(show=False)
            # show results
            self.score_lbl.text = str(self.item['score']) + '/' + str(self.item['target_count'])
                
            # if countdown is zero, game over
            if self.item['time'] == 0:
                # stop game timer
                self.item['start_timer'] = False

                # reset play button to start button for the next level
                self.start_btn.text = 'Play again'
                self.start_btn.icon = 'fa:arrow-circle-right'
                # # reset target
                self.letter_lbl.text = self.item['previous'] = 'X'
                # # reset timer interval
                self.timer_lbl.text = str(25)
                
                # show game instructions again
                self.game_crd.visible = True
                # hide player card from parent form: <My_Clicky_Game_2.player_frm.player_frm object>
                get_open_form().hide_player_card(show=True)

                # store score card
                self.score_card = {
                    'player':self.item['player'], 
                    'level':self.item['level'], 
                    'score':self.item['score'], 
                    'target_count':self.item['target_count']
                }
                if not anvil.server.call('add_score', self.score_card):
                    Notification('Score card did not save properly...').show()
                    
                # write results of the score list ui
                self.score_list_txa.text   += f"Level {self.item['level']}: {self.item['score']}/{self.item['target_count']}\n"
                self.score_list_txa.visible = True

                # go to the next level: adjust some game parameters
                self.item['level']            += 1
                self.game_tmr.interval        -= self.item['speed']
                self.item['target_letter']     = self.get_random_letter(target=True) # randomly change target letter for subsequent level
                self.game_instruction_lbl.text = f"Click on the letter '{self.item['target_letter']}' as many times as you can in 25 seconds."

                # if at the level 20
                if self.game_tmr.interval == 0:
                    if alert("Congratulations! You've completed all game levels.\nDo you want to start over",
                         buttons=[('Yes', True),('No', False)]):
                        self.game_tmr.interval = 1

            # generate random letters and display it on the screen
            # Note: no two subsequent letters should be the same
            self.letter_lbl.text = self.get_random_letter()

            # keep count of target letter
            if self.letter_lbl.text == self.item['target_letter']:
                self.item['target_count'] += 1
            
        # else: # game finished
            
            
    def get_random_letter(self, letters='ABCDEFG', target=False):
        '''randomly return a letter between A and G'''
        random_letter = choice(letters)

        # no two subsequent letters should be the same
        while random_letter == self.item['previous']: # if the same
            # choose another random letter
            random_letter = choice(letters)
        if not target: # if not generating a random target letter
            # update previous to latest random letter
            self.item['previous'] = random_letter

        return random_letter # returned current random letter
            