from ._anvil_designer import game_frmTemplate
from anvil import *
from random import choice

class game_frm(game_frmTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.time = 25
        self.start_timer = False

        self.previous = 'X'
        self.score = 0
        self.target_letter = 'A'
        self.target_count = 0

    def start_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.start_btn.text == 'Start':
            # change the text button to 'Click me'
            self.start_btn.text = 'Click Me'
            self.start_btn.icon = 'fa:arrow-circle-down'
            # start the game's timer countdown
            self.start_timer = True
            
        # when game is played:
        # add a point every time the player clicks on the letter A
        else: # this is the game 'Click Me'
            if self.letter_lbl.text == self.target_letter:
                # add a point to the player's score
                self.score = self.score + 1
                # update scoreboard
                self.score_lbl.text = str(self.score)
        


    def game_tmr_tick(self, **event_args):
        """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
        if self.start_timer: # game started
            # start timer countdown
            self.time = self.time - 1
            # update screen
            self.timer_lbl.text = str(self.time)
            # if countdown is zero, game over
            if self.time == 0:
                # stop timer
                self.start_timer = False
                # reset target
                self.letter_lbl.text = self.previous = 'X'
                # reset timer interval
                self.time = 25
                # show results
                score = str(self.score) + '/' + str(self.target_count)
                alert('Your score is ' + score)

            # generate random letters and display it on the screen
            # Note: no two subsequent letters should be the same
            self.letter_lbl.text = self.get_random_letter()
            # increment count if letter matches target
            if self.letter_lbl.text == self.target_letter:
                self.target_count = self.target_count + 1
        # else: # game finished
            
            
    def get_random_letter(self):
        '''randomly return a letter between A and G'''
        letters = 'ABCDEFG'
        random_letter = choice(letters)

        # no two subsequent letters should be the same
        while random_letter == self.previous:
            random_letter = choice(letters)
        # update previous to latest random letter
        self.previous = random_letter

        return random_letter
            