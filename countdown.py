# countdown.py fix the score in two player option. 
#================================imports==========================================
import random
import time
#================================Constants========================================

with open('my_words.txt') as file:
    word_list = file.read().split('\n')

conundrum_list = [i for i in word_list if len(i) == 9]


def counter(manual=False, count=30):
    '''counts down from 30. If manual set to false, countdown begins automatically. '''
    if manual:
        start = input('Press any key to start the countdown. ')
    for i in range(count):
        print(count,', ', end='')
        count -= 1
        time.sleep(1)

# =======================Declare Conundrum Class==================================
class Conundrum:
    conundrum_list = conundrum_list
    def __init__(self):
        self.word = random.choice(conundrum_list) 
        self.scrambled = ''
    
    def scrambler(self):
        '''Takes a str word, scrambles it, and returns a scrambled str. '''
        mixed = list(self.word)
        random.shuffle(mixed)
        self.scrambled = ''.join(mixed)
        
# ======================Declare CountdownSinglePlayer Class=======================
class CountdownSinglePlayer:
    word_list = word_list
    consonants = 'bcdfghjklmnpqrstvwxyz'
    vowels = 'aeiou'

    def __init__(self):
        self.letters = []
        self.valid_words = []
 
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

    def format_letters(self):
        print(f'''
            
            .----------------------------.
            | {', '.join(self.letters)}  |
            |____________________________|
            
            ''')
        
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

    def is_valid(self, contestant_word):
        '''Takes the contestant word and checks if it is a valid word. if not, returns 0, if yes,
        returns the length of the word along with printing info about word to the console. '''
        if contestant_word not in self.valid_words:
            print(f'Sorry. {contestant_word} is not a valid word.')
            return 0 
        else:
            print(f'{contestant_word} is {len(contestant_word)} letters long and it is a valid choice.')
            return len(contestant_word)

# =======================Declare CountdownTwoPlayer Class=========================
class CountdownTwoPlayer(CountdownSinglePlayer):
    
    def __init__(self):
        super().__init__()
        self.player_1 = ''
        self.player_2 = ''
        self.player_1_score = 0
        self.player_2_score = 0
        self.rounds = 1
        
    def compare_score(self, p1, p2):
        '''Compares the players scores. If scores are equal, both are returned. if one is greater than
        the other, the former is returned unmodified and the latter is zeroed. '''
        if p1 == p2:
            self.player_1_score += p1
            self.player_2_score += p2
        
        elif p1 > p2:
            self.player_1_score += p1
            self.player_2_score += 0
            
        else:
            self.player_1_score += 0
            self.player_2_score += p2
    
    
# =======================counudrum game function==================================
def conundrum():
    c = Conundrum() 
    c.scrambler()
    print('The Conundrum word is: ',c.scrambled)
    counter()
    guess = input('\nSolve the conundrum: ')
    if guess == c.word:
        print(f'congratulations! the word is {c.word}.')
    else:
        print(f'The word is {c.word}.')
    to_main = input('\nPress any key to return to the main menu.')

# ==========================single_player game function===========================
def single_player():
    s = CountdownSinglePlayer()
    s.get_letters()
    s.format_letters()            
    s.possible_words()
    counter()
    contestant_word = input('\nEnter your word: ')
    s.is_valid(contestant_word)            
    s.show_results()
    to_main = input('\nPress any key to return to the main menu.')
    
# =========================two_player game function===============================
def two_player():
    t = CountdownTwoPlayer()
    t.player_1 = input('Enter name for player 1: ')
    t.player_2 = input('Enter name for player 2: ')
    while t.rounds < 5:
        if t.rounds % 2 != 0:
            player = t.player_1
        else:
            player = t.player_2
        print(f'Round {t.rounds}: {player} chooses the letters.')
        t.get_letters()
        t.format_letters()
        t.possible_words()
        counter()
        player_1_word = input(f'\n{t.player_1}, enter your word:\n')
        player_2_word = input(f'\n{t.player_2}, enter your word:\n')
        p1_score = t.is_valid(player_1_word)
        p2_score = t.is_valid(player_2_word)
        t.compare_score(p1_score, p2_score)
        t.show_results(detailed=False)                
        print(f'Score for {t.player_1}: {t.player_1_score}')
        print(f'Score for {t.player_2}: {t.player_2_score}')
        t.letters.clear()
        t.rounds += 1
    to_main = input('\nPress any key to return to the main menu.')


# ==========================Declare Menu Class====================================

class Menu:
    options = {
        '1': conundrum,
        '2': single_player,
        '3': two_player,
    }

    def display_menu(self):
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
                                    1. Conundrum
                                    2. Single Player Countdown
                                    3. Two Player Countdown
                                    4. Quit
    ''')

    def game_running(self):
        running = True
        while running:
            self.display_menu()
            selection = input('Choose an option. ')
            if selection == '4':
                running = False
            if selection in self.options:
                option = self.options.get(selection)
                option()
            
if __name__ == '__main__':
    Menu().game_running()

