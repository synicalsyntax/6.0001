# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)

import random
import string
import re

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()

letters_guessed = []


def is_word_guessed(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in
      letters_guessed; False otherwise
    """
    return all(letter in letters_guessed for letter in set(secret_word))


def get_guessed_word(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that
      represents which letters in secret_word have been guessed so far.
    """
    word = [l if l in letters_guessed else '_ ' for l in secret_word]
    return ''.join(word)


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which
      letters have not yet been guessed.
    """
    letters = [l for l in string.ascii_lowercase if l not in letters_guessed]
    return ''.join(letters)


def hangman(secret_word):
    """
    secret_word: string, the secret word to guess.
    Starts up an interactive game of Hangman.
    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.
    * The user should start with 6 guesses
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.
    * After each guess, you should display to the user the
      partially guessed word so far.
    Follows the other limitations detailed in the problem write-up.
    """
    start_round(secret_word, 6, 3, False, True)


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def start_round(secret_word, guesses_remaining, warnings_remaining,
                hints_enabled, is_first_round=False):
    """
    Starts a round of Hangman.

    :param secret_word: The secret word that the user needs to guess.
    :type secret_word: str
    :param guesses_remaining: The amount of guesses remaining.
    :type guesses_remaining: int
    :param warnings_remaining: The amount of warnings remaining.
    :type warnings_remaining: int
    :param hints_enabled: Whether or not hint requests are enabled.
    :type warnings_remaining: bool
    :param is_first_round: Whether or not the player just started the game.
    :type warnings_remaining: bool
    :rtype: None
    """
    # Greet user for new game
    if is_first_round:
        print('Welcome to the game Hangman!')
        print('I am thinking of a word that is {} letters long.'
              .format(len(secret_word)))
        print('You have 3 warnings left.')

    # Prompt the user for a guess
    guesses = pluralize('guess', guesses_remaining)
    print('-------------\nYou have {} left.'.format(guesses))
    letters = get_available_letters(letters_guessed)
    print('Available letters:', letters)
    guess = input('Please guess a letter: ')

    # Handle hint requests
    if hints_enabled and guess == '*':
        guessed_word = get_guessed_word(secret_word, letters_guessed)
        print('Possible matches are:')
        show_possible_matches(guessed_word)
        start_round(secret_word, guesses_remaining, warnings_remaining,
                    hints_enabled)
        return

    # Handle invalid guesses
    if guess in letters_guessed or not re.match('[a-z]', guess, re.I):
        warning = 'Oops! That is not a valid letter.'
        if guess in letters_guessed:
            warning = 'Oops! You already guessed that letter.'
        if warnings_remaining < 1:  # Subtract a guess
            warnings_remaining = 3
            guesses_remaining -= 1
            if guesses_remaining < 1:
                lose_game(secret_word)
            warning += ' You have no warnings left so you lose one guess: '
        else:  # Subtract a warning
            warnings_remaining -= 1
            warnings = pluralize('warning', warnings_remaining)
            warning += ' You have {} left: '.format(warnings)
        warning += get_guessed_word(secret_word, letters_guessed)
        print(warning)
        start_round(secret_word, guesses_remaining, warnings_remaining,
                    hints_enabled)
        return

    # Update guesses
    letters_guessed.append(guess)
    lost_guesses = get_lost_guesses(guess, secret_word)
    guesses_remaining -= lost_guesses

    # Output guess success or failure
    guessed_word = get_guessed_word(secret_word, letters_guessed)
    if lost_guesses == 0:
        print('Good guess:', guessed_word)
    else:
        print('Oops! That letter is not in my word:', guessed_word)

    # Player wins game when all letters are guessed
    if is_word_guessed(secret_word, letters_guessed):
        win_game(secret_word, guesses_remaining)

    if guesses_remaining < 1:  # Player loses game if no guesses remain
        lose_game(secret_word)
    else:  # Start a new round if player has guesses remaining
        start_round(secret_word, guesses_remaining, warnings_remaining,
                    hints_enabled)


def pluralize(noun, quantity):
    """
    Returns a pluralization of a noun preceded by its quantity by
    suffixing a morpheme (limited to the regular plural morphemes
    's' and 'es').

    :param noun: The noun to be pluralized.
    :type noun: str
    :param quantity: The quantity of the noun.
    :type quantity: int
    :returns: The pluralization of the noun.
    :rtype: str
    """
    unpluralized_noun = ' '.join([str(quantity), noun])
    if (quantity == 1):
        return unpluralized_noun
    morpheme = 's'
    if (noun.endswith('s')):
        morpheme = 'es'
    return ''.join([unpluralized_noun, morpheme])


def get_lost_guesses(guessed_letter, secret_word):
    """
    Calculates the number of guesses lost from a guess according to
    the secret_word.

    :param guessed_letter: The letter the player guessed.
    :type guessed_letter: str
    :param secret_word: The secret word that the player needs to guess.
    :type secret_word: str
    :returns: The number of guesses the player lost.
    :rtype: int
    """
    if guessed_letter in secret_word:
        return 0
    else:
        if guessed_letter in 'aeiou':
            return 2
        return 1


def win_game(secret_word, guesses_remaining):
    """
    Alerts the player that they won the game before terminating the game.

    :param secret_word: The secret word that the player guessed.
    :type secret_word: str
    :param guesses_remaining: The amount of guesses remaining.
    :type guesses_remaining: int
    :rtype: None
    """
    score = len(set(secret_word)) * guesses_remaining
    print('------------\nCongratulations, you won!')
    print('Your total score for this game is:', score)
    exit()


def lose_game(secret_word):
    """
    Alerts the player that they lost the game before terminating the game.

    :param secret_word: The secret word that the player failed to guess.
    :type secret_word: str
    :rtype: None
    """
    print('Sorry, you ran out of guesses. The word was', secret_word)
    exit()


def match_with_gaps(my_word, other_word):
    """
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special
        symbol _ , and my_word and other_word are of the same length;
        False otherwise:
    """
    my_word = my_word.replace('_ ', '_')
    other_word_letters = []
    non_other_word_letters = []
    if len(my_word) != len(other_word):
        return False
    for index, letter in enumerate(my_word):
        other_letter = other_word[index]
        if letter == '_':
            non_other_word_letters.append(other_letter)
            if other_letter in other_word_letters:
                return False
        else:
            other_word_letters.append(other_letter)
            if letter != other_letter or letter in non_other_word_letters:
                return False
    return True


def show_possible_matches(my_word):
    """
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches
             my_word. Keep in mind that in hangman when a letter is guessed,
             all the positions at which that letter occurs in the secret word
             are revealed. Therefore, the hidden letter(_ ) cannot be one of
             the letters in the word that has already been revealed.
    """
    matches = [word for word in wordlist if match_with_gaps(my_word, word)]
    if len(matches) == 0:
        print('No matches found')
    print(' '.join(matches))


def hangman_with_hints(secret_word):
    """
    Starts an interactive game of Hangman with hints.

    :param secret_word: The secret word that the player guessed.
    :type secret_word: str
    :rtype: None
    """
    start_round(secret_word, 6, 3, True, True)


# When you've completed your hangman_with_hint function, comment the two
# similar lines above that were used to run the hangman function, and then
# uncomment these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

    ###############

    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.

    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
