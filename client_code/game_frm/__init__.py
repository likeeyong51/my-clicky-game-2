from ._anvil_designer import game_frmTemplate
from anvil import *
from random import choice

class game_frm(game_frmTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        # get player's name
        self.item['player'] = properties['player']
        self.refresh_data_bindings()
        # set game parameters
        self.item['start_timer'] = False


    def start_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.start_btn.text == 'Start':
            # change the text button to 'Click me'
            self.start_btn.text = 'Click Me'
            self.start_btn.icon = 'fa:arrow-circle-down'
            # start the game's timer countdown
            self.item['start_timer'] = True
            # set start-game parameters
            self.item['time'] = 25
            self.item['previous'] = 'X'
            self.item['score'] = 0
            self.item['target_letter'] = 'A'
            self.item['target_count'] = 0
        # when game is played:
        # add a point every time the player clicks on the letter A
        else: # play the game
            if self.letter_lbl.text == self.item['target_letter']:
                # add a point to the player's score
                self.item['score'] += 1
                # update scoreboard
                self.score_lbl.text = str(self.item['score'])
        

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
                
            # if countdown is zero, game over
            if self.item['time'] == 0:
                # stop game timer
                self.item['start_timer'] = False
                # reset play button to start button
                self.start_btn.text = 'Start'
                # # reset target
                self.letter_lbl.text = self.item['previous'] = 'X'
                # # reset timer interval
                self.timer_lbl.text = str(25)
                # show results
                # self.score_lbl.text = str(self.item['score']) + '/' + str(self.item['target_count'])
                # show game instructions again
                self.game_crd.visible = True
                # hide player card from parent form: <My_Clicky_Game_2.player_frm.player_frm object>
                get_open_form().hide_player_card(show=True)
            
            self.refresh_data_bindings()

            # generate random letters and display it on the screen
            # Note: no two subsequent letters should be the same
            self.letter_lbl.text = self.get_random_letter()
            
        # else: # game finished
            
            
    def get_random_letter(self):
        '''randomly return a letter between A and G'''
        letters = 'ABCDEFG'
        random_letter = choice(letters)

        # no two subsequent letters should be the same
        while random_letter == self.item['previous']:
            random_letter = choice(letters)
        # update previous to latest random letter
        self.item['previous'] = random_letter
        # keep count of target letter
        if random_letter == self.item['target_letter']:
            self.item['target_count'] += 1

        return random_letter
            