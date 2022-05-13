# countdown
import random
import time

with open('my_words.txt') as file:
    word_list = file.read().split('\n')

conundrum_list = [i for i in word_list if len(i) == 9]

class MainGame:
    
    def __init__(self):
        self.options = {
            '1': CountDown.single_player,
            '2': TwoPlayer.main,
            '3': Conundrum.main,        
        }
    
    def display_menu():
        '''Prints the instructions of the game along with the options menu. '''
        print('''
                                    Welcome to Countdown!
                                    ---------------------
                                    
    - You choose a total of 9 letters. you can choose either vowels or consonants which will be randomly generated.
    - You have 30 seconds to make the longest word from the 9 letters supplied.
    - In single Player mode you play one round against the computer for practice. 
    - In two player mode, you play four rounds. 
    - The player with the longest valid word receives points equal to the word length. The opponent gets nothing.
    - In the event of a tie, both players recieve the points. If a player uses all 9 letters, 18 points are awarded. 
    - In conundrum, the players are given a scrambled 9-letter word and they must try to solve the word.

                                    Menu Options
                                    -----------------
                                    1. Single Player
                                    2. Two Player
                                    3. Conundrum
                                    4. Quit
    ''')
        
    def counter(self, manual=False, count=30):
            '''counts down from 30. If manual set to false, countdown begins automatically. '''
            if manual:
                start = input('Press any key to start the countdown. ')
            for i in range(count):
                print(count,', ', end='')
                count -= 1
                time.sleep(1)
                
    def main(self):
        game_running = True
        while game_running:
            selection = input('Choose an option. ')
            if selection == '4':
                game_running = False
            if selection in self.options.keys():
                selection()       

class Conundrum:
    
    def __init__(self):
        self.conundrum_list = conundrum_list
        self.word = random.choice(conundrum_list)
        self.scrambled = ''
        
    def scrambler(self):
        '''Takes a str word, scrambles it, and returns a scrambled str. '''
        scrambled = list(self.word)
        random.shuffle(scrambled)
        scrambled = ''.join(scrambled)
        return scrambled

    def main(self):
        Conundrum.scrambler()
        print(f'The Conundrum word is:  ', Conundrum.scrambled)
        MainGame.counter()
        guess = input('\nSolve the conundrum: ')
        if guess == self.word:
            print(f'congratulations! the word is ', self.word)
        else:
            print(f'The word is ', self.word)
            to_main = input('\nPress any key to return to the main menu.')

class CountDown:
    
    def __init__(self):
        self.word_list = word_list
        self.consonants = 'bcdfghjklmnpqrstvwxyz'
        self.vowels = 'aeiou'
        self.letters = []   
        self.valid_words = []
        
    def is_valid(self, contestant_word):
        '''Takes the contestant word and checks if it is a valid word. if not, returns 0, if yes,
        returns the length of the word along with printing info about word to the console. '''
        if contestant_word not in self.valid_words:
            print(f'Sorry. {contestant_word} is not a valid word.')
            return 0 
        else:
            print(f'{contestant_word} is {len(contestant_word)} letters long and it is a valid choice.')
            return len(contestant_word)
        
    def show_results(self, detailed=True):
        '''Takes a list of all valid words, displays the longest one/s along with letter count
        and shows a separate list of all other possible words in no particular order. '''
        longest = max([len(i) for i in self.valid_words])
        longest_words = [i for i in self.valid_words if len(i) == longest]
        print(f'The longest word is {longest} letters long.')
        print(', '.join(longest_words))
        if detailed:
            print('\nThis is the list of all possible words.\n')
            print(', '.join(self.valid_words))
        
    def format_letters(self):
        print(f'''
            
            .----------------------------.
            | {', '.join(self.letters)}  |
            |____________________________|
            
            ''')
        
    def get_letters(self):
        '''Allows the user to choose a ramdomly generated consonant or vowel to populate
        a 9-letter list of letters.'''
        for i in range(9):
            selection = input('Choose "v" for a vowel or any other key for a consonant. ')
            if selection == 'v':
                self.letters.append(random.choice(self.vowels))
                print(', '.join(self.letters))
            else:
                self.letters.append(random.choice(self.consonants))
                print(', '.join(self.letters))
        
    
    def possible_words(self):
        '''Checks all words in the word_list against letters in the letter_list
        and returns all words that can be constructed from the letters in letter_list.'''
        for word in self.word_list:
            word_copy = list(word)
            letter_list_copy = self.letters.copy()
            for letter in word:
                if letter in letter_list_copy:
                    word_copy.remove(letter)
                    letter_list_copy.remove(letter)
            if not word_copy:
                self.valid_words.append(word)
    

    def single_player(self):
        self.get_letters()
        self.format_letters()            
        self.possible_words()
        self.counter()
        contestant_word = input('\nEnter your word: ')
        self.is_valid(contestant_word)            
        self.show_results()
        to_main = input('\nPress any key to return to the main menu.')
    
class TwoPlayer:
  
    def __init__(self):
        self.countdown = CountDown()
        self.rounds = 1
        self.player_1 = input('Enter name for player 1: ')
        self.player_2 = input('Enter name for player 2: ')
        self.players = {self.player_1: 0, self.player_2: 0}
        self.player = ''
        self.p1_score = 0
        self.p2_score = 0 
               
    def compare_score(self):
        '''Compares the players scores. If scores are equal, both are returned. if one is greater than
        the other, the former is returned unmodified and the latter is zeroed. '''
        if self.p1_score == self.p2_score:
            pass
        elif self.p1_score > self.p2_score:
            self.p2_score = 0
        else:
            self.p1_score = 0
    

    def main(self):
        while self.rounds < 5:
            if self.rounds % 2 != 0:
                self.player = self.player_1
            else:
                self.player = self.player_2
            print(f'Round {self.rounds}: {self.player} chooses the letters.')
            self.countdown.get_letters()
            self.countdown.format_letters()
            self.countdown.possible_words()
            MainGame.counter()
            player_1_word = input(f'\n{self.player_1}, enter your word:\n')
            player_2_word = input(f'\n{self.player_2}, enter your word:\n')
            self.p1_score = self.countdown.is_valid(player_1_word)
            self.p2_score = self.countdown.is_valid(player_2_word)
            self.compare_score()
            self.countdown.show_results(detailed=False)
                
            print(f'Score for {self.player_1}: {self.players[self.player_1]}')
            print(f'Score for {self.player_2}: {self.players[self.player_2]}')
            self.rounds += 1
            to_main = input('\nPress any key to return to the main menu.')
            
            
            

if __name__ == '__main__':
    MainGame.main()
