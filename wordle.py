# wordle
import random

with open('my_words.txt', 'r') as file:
    word_list = file.read().split('\n')
    
word_list = [i for i in word_list if len(i) == 5]

class Wordle:
    
    def __init__(self):
        self.word_list = word_list
        self.attempts = 1
        self.word = random.choice(self.word_list)
        self.guesses = []
        self.not_in_word = set()
        self.guess = ''
        self.in_word = []
        self.hidden = ['_','_','_','_','_']
        self.not_in = set()
                              
    def print_menu(self):
        print('''
                            Welcome to Wordle! The world's popular word guessing game. 
                            ----------------------------------------------------------
            
    Guess the secret 5-letter word in five attempts. Begin by typing in any 5-letter word and pressing enter.

    - Letters in the correct position of the word will show in the word.
    - Letters in the word but in the wrong postion will be shown in the word list.
    - If your guess is not in the wordle word list, you will be prompted to enter a different word with no penalty.

        Options

        1. Play
        2. Quit
    ''')

    def definite_match(self):
        '''takes word and guess as input and returns correct letter
        position matches and a list of letters in word but not correct postion.'''
        editable_word = list(self.word).copy()
        editable_guess = list(self.guess).copy()
        
        # find exact letter matches
        for i in range(5):
            if self.guess[i] == self.word[i]:
                self.hidden[i] = self.word[i]
                editable_guess.remove(self.guess[i])
                editable_word.remove(self.guess[i])
                
        # search for letters not in the word and add to not_in set
        for letter in editable_guess:
            if letter not in editable_word:
                self.not_in.update(letter)
                
        # search for letters in the word but in the wrong position and add to the set
        for letter in editable_guess:
            if letter in editable_word:
                self.in_word.append(letter)
                editable_word.remove(letter)

    def check_answer(self):
        '''Check if the guessed word is the correct answer'''
        if ''.join(self.hidden) == self.word:
            return True
        return False
        
    def check_guess_input(self):
        '''Continually checks for valid word input and returns a valid word once entered'''
        while True:
            self.guess = input('Guess: ').lower()
            if self.guess not in self.word_list:
                print(f'{self.guess} is not in the wordle word list.')
                continue
            break
        return self.guess

    def main(self):
        running = True
        while running:
            self.print_menu()       
            choice = input('Choose an option. ')
            if choice == '2':
                running = False
            if choice == '1':
                w = Wordle()
                while w.attempts < 6:
                    print(f'Attempt {w.attempts} of 5. ', end='')
                    w.check_guess_input()
                    w.definite_match()
                    if w.check_answer():
                        print(f'You win! the word is {w.word}.')
                        break
                    elif not w.check_answer() and w.attempts == 5:
                        print(f'You loose. The word was {w.word}.')
                        break
                    else:
                        w.guesses.append(w.guess)
                        w.not_in_word.update(w.not_in) 
                        print('Guessed words: ', ', '.join(w.guesses))
                        print('Guessed letters that are not in the word: ', ', '.join(w.not_in_word))
                        print('In word but in wrong position: ', ', '.join(w.in_word))
                        w.in_word.clear()
                        print('Secret Word: ', ' '.join(w.hidden))
                        print('=======================================================')
                        print()
                        w.attempts += 1
                        
if __name__ == '__main__':
    Wordle().main()