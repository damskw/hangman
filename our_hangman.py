import random
import pyfiglet
import re
import string
from slowprint.slowprint import *


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


HANGMAN = (
    """
 ------
 |    |
 |
 |
 |
 |
 |
 |
 |
----------
""",
    """
 ------
 |    |
 |    O
 |
 |
 |
 |
 |
 |
----------
""",
    """
 ------
 |    |
 |    O
 |   -+-
 | 
 |   
 |   
 |   
 |   
----------
""",
    """
 ------
 |    |
 |    O
 |  /-+-
 |   
 |   
 |   
 |   
 |   
----------
""",
    """
 ------
 |    |
 |    O
 |  /-+-/
 |   
 |   
 |   
 |   
 |   
----------
""",
    """
 ------
 |    |
 |    O
 |  /-+-/
 |    |
 |   
 |   
 |   
 |   
----------
""",
    """
 ------
 |    |
 |    O
 |  /-+-/
 |    |
 |    |
 |   | 
 |   | 
 |   
----------
""",
    """
 ------
 |    |
 |    O
 |  /-+-/
 |    |
 |    |
 |   | |
 |   | |
 |  
----------
""")


def greet_player():
    ascii_banner = pyfiglet.figlet_format("Welcome to Hangman!")
    slowprint(BColors.OKGREEN + ascii_banner + BColors.ENDC, 0.01)
    player_name = input("How can we call you? : ")
    if player_name.upper().lower() == "quit":
        goodbye()
    print("Welcome to Hangman,", player_name + '!')
    return player_name


def goodbye():
    goodbye_anim = pyfiglet.figlet_format("Goodbye!")
    slowprint(BColors.WARNING + goodbye_anim + BColors.ENDC, 0.01)
    exit()


def leaderboards(player_name, wrong_guesses, difficulty_level):
    # Save to file
    score = str((42 - wrong_guesses) * difficulty_level)
    line = "\n" + player_name + " " + score + " "
    with open("leaderboards.txt", "a") as f:
        f.write(line)

    # Reading from file
    leader_list_to_sort = []
    with open("leaderboards.txt", "r") as f:
        for line in f:
            current_line = []
            current_word = ""
            for letter in line:
                if letter != " ":
                    current_word = current_word + letter
                else:
                    current_line.append(current_word)
                    current_word = ""
            leader_list_to_sort.append(current_line)
    # print(list)

    # Title screen
    title_screen = pyfiglet.figlet_format("HALL OF FAME")
    slowprint(BColors.OKGREEN + title_screen + BColors.ENDC, 0.01)

    # Sorting algorithm
    indexing_length = len(leader_list_to_sort) - 1
    is_sorted = False

    while not is_sorted:
        is_sorted = True
        for i in range(0, indexing_length):
            if int(leader_list_to_sort[i][1]) < int(leader_list_to_sort[i + 1][1]):
                is_sorted = False
                leader_list_to_sort[i], leader_list_to_sort[i + 1] = leader_list_to_sort[i + 1], leader_list_to_sort[i]

    # Current player score
    words_of_encouragement = ["You're great!",
                              "You did very well.",
                              "Unbelievable how many points you've gotten!",
                              "Looks like you're a professional.",
                              "Well done, not many players score that high."]
    random_word_of_encouragement = words_of_encouragement[random.randint(0, 3)]
    print(f"Congratulations, {player_name}! You've managed to get: {score} points! {random_word_of_encouragement}")

    # List of winners
    counter = 0
    # TODO: make use of iterator `line` in this for loop, delete comments if this piece works well
    # iteration = 0
    for line in leader_list_to_sort:
        counter += 1
        # highscore_show_player_name = leader_list_to_sort[iteration][0]
        highscore_show_player_name = line[0]
        # highscore_show_points = leader_list_to_sort[iteration][1]
        highscore_show_points = line[1]
        print(f"{counter}. {highscore_show_player_name} {highscore_show_points} points")
        # iteration += 1


def welcome_back(player_name, is_win):
    print()
    random.seed()
    random_message_index = random.randint(0, 2)
    if is_win == 0:
        if random_message_index == 0:
            print(BColors.OKCYAN + "Welcome back",
                  player_name + "! Let's try again! Try to save the man from cruelty!" + BColors.ENDC)
        elif random_message_index == 1:
            print(BColors.OKCYAN + "If you don't try, you never fail", player_name + "!" + BColors.ENDC)
        elif random_message_index == 2:
            print(BColors.OKCYAN + "There is no failure except in no longer trying! Let's keep going",
                  player_name + "!" + BColors.ENDC)
    elif is_win == 1:
        if random_message_index == 0:
            print(BColors.OKBLUE + "We can see you are good at it",
                  player_name + "! Do you know names of all the countries on earth though?" + BColors.ENDC)
        elif random_message_index == 1:
            print(BColors.OKBLUE + "Winners are not afraid of losing. But losers are. Failure is part of the process "
                                   "of success", player_name + "!" + BColors.ENDC)
        elif random_message_index == 2:
            print(BColors.OKBLUE + "Many innocent people are to be saved",
                  player_name + "! Please be quick!" + BColors.ENDC)


def get_level(level=""):
    print("\nWe are going to draw a country or a capital from a long list for you. ")
    print("We have divided the words by a number of distinctive letters into 3 groups.")
    print(" 1 - Easy")
    print(" 2 - Medium")
    print(" 3 - Hard")
    while True:
        try:
            print("Please select level of difficulty: ")
            level = input("")
            if level.upper().lower() == "quit":
                goodbye()
            level = int(level)
        except ValueError:
            print("Please enter a valid character. ")
            continue
        while level > 3 or level <= 0:
            level = input("You have chosen wrong level, try again. ")
            continue
        break

    if level == 1:
        print("You've chosen easy level. ")
    elif level == 2:
        print("You've chosen medium level. ")
    else:
        print("You've chosen hard level. ")
    return int(level)


def damage(level_local):
    if level_local == 1:
        damage_local = 1
    elif level_local == 2:
        damage_local = 3
    else:
        damage_local = 6
    return damage_local


def create_word_list(filepath="./countries-and-capitals.txt"):
    word_list_local = []
    with open(filepath, newline='') as file:
        for line in file.read().splitlines():
            words_local = line.split("|")
            for word in words_local:
                word_list_local.append(word.strip())
    return word_list_local


def draw_word_from_list(word_list, level_local, played_words_local: set):
    random.seed()
    word_number = random.randint(0, len(word_list) - 1)
    word = word_list[word_number]
    if level_local == 1:
        while not(len(word) <= 5) or word in played_words_local:
            word_number = random.randint(0, len(word_list) - 1)
            word = word_list[word_number]
        return word

    elif level_local == 2:
        while not(5 < len(word) <= 8) or word in played_words_local:
            word_number = random.randint(0, len(word_list) - 1)
            word = word_list[word_number]
        return word

    elif level_local == 3:
        while not(len(word) > 8) or word in played_words_local:
            word_number = random.randint(0, len(word_list) - 1)
            word = word_list[word_number]
        return word
    else:
        # TODO: handle case
        raise ValueError
        pass


def validate_input():
    az_check = string.ascii_letters
    guess = input("Please enter your guess: ")
    if guess.upper().lower() == "quit":
        goodbye()
    else:
        while len(guess) > 1:
            print("Please enter only one character. ")
            guess = validate_input()
        while guess not in az_check:
            print("Please use A-Z characters. ")
            guess = validate_input()
    return guess


def guess_letter(word, encoded_word, level_local, wrong_guesses, guess_counter, already_tried_letters_local: set,
                 lives_left_local):
    guess = validate_input()
    while guess.upper() in already_tried_letters_local or guess.upper() in encoded_word.upper():
        print(BColors.OKCYAN + "You've already provided that character. " + BColors.ENDC)
        guess = validate_input()
    for letter_index in range(0, len(word)):
        if word[letter_index] == guess.upper() or word[letter_index] == guess.lower():
            if word[letter_index].isupper():
                guess = guess.upper()
            elif word[letter_index].islower():
                guess = guess.lower()
            encoded_word = encoded_word[0:letter_index] + guess + encoded_word[letter_index + 1:len(word)]
            guess_counter += 1
    if guess_counter == 0 and guess.upper() not in already_tried_letters_local:
        already_tried_letters_local.add(guess.upper())
        wrong_guesses = wrong_guesses + damage(level_local)
        lives_left_local = lives_left_local - 1
    return wrong_guesses, encoded_word, already_tried_letters_local, lives_left_local


def get_hangman(max_wrong_guesses, graphics_list):
    return int(max_wrong_guesses / (len(graphics_list) - 1))


def input_check_play_again(decision_local=""):
    """input_check_play_again() takes a string (player input) and checks if it is of the expected format.
    If the string meets the requirements, it is returned.
    Otherwise the user is asked repetitively to provide a proper input and runs it against
    the checks until the input meets the requirements and only then is returned.

    In: str, default = ''
    Out: str decision that  is either 'Y', 'y', 'N', 'n'"""
    while decision_local.lower() != "y" and decision_local.lower() != "n":
        decision_local = input("I didn't get it! Would you like to play? Yes or no? (y/n) ")
        if decision_local.upper().lower() == "quit":
            goodbye()
    return decision_local.lower()


def main(game_round, player_name="", played_words=None):
    if played_words is None:
        played_words = set()
    if game_round == 'first':
        player_name = greet_player()
    elif game_round == 'next':
        welcome_back(player_name, 1)
    elif game_round == 'fail':
        welcome_back(player_name, 0)

    level = get_level()
    word_base = create_word_list()
    word_to_guess = draw_word_from_list(word_base, level, played_words)
    played_words.add(word_to_guess)
    original_word = word_to_guess
    encoded_word = re.sub('[0-9a-zA-Z]', '_', word_to_guess)
    # print(word_to_guess)  # Print selected word
    print(HANGMAN[0])  # Starting Hangman
    print(encoded_word)  # Print word with _
    already_tried_letters = set()
    max_wrong_guesses = 42  # Must be every 3
    wrong_guesses = 0  # Starting value
    guess_counter = 0  # Starting value for loop
    lives_left = int(max_wrong_guesses / damage(level)) # Starting value for lives left

    # =================================== MAIN GAME LOGIC ============================================
    while wrong_guesses < max_wrong_guesses and "_" in encoded_word:
        # TODO: introduce exception handling, e.g. if game_state_tuple doesn't get the return values assigned correctly
        game_state_tuple = guess_letter(word_to_guess, encoded_word, level, wrong_guesses, guess_counter,
                                        already_tried_letters, lives_left)
        wrong_guesses = game_state_tuple[0]
        encoded_word = game_state_tuple[1]
        already_tried_letters = game_state_tuple[2]
        hangman_graphics_index = int(wrong_guesses / get_hangman(max_wrong_guesses, HANGMAN))
        print(HANGMAN[hangman_graphics_index])
        print("Letters you've guessed wrong:")
        for i in already_tried_letters:
            print(BColors.WARNING + i, " " + BColors.ENDC, end="")
        print(" ")
        # Print encoded word
        lives_left = game_state_tuple[3]
        print(BColors.BOLD + encoded_word + BColors.ENDC, BColors.FAIL + "\tlives left: ", str(lives_left) +
              BColors.ENDC)
    else:
        if wrong_guesses >= max_wrong_guesses:
            decision = input("So sorry, you've failed! The word was %s. Do you want to play again? (y/n) "
                             % original_word)
            if decision.upper().lower() == "quit":
                goodbye()
            decision = input_check_play_again(decision)
            try:
                if decision.lower() == "y":
                    main("fail", player_name, played_words)
                elif decision.lower() == 'n':
                    print("I hope you enjoyed the game! See you next time!")
                    goodbye()
                else:
                    raise ValueError
            except ValueError:
                input_check_play_again()
        else:
            leaderboards(player_name, wrong_guesses, level)
            decision = input("Congratulations, you've won the game! Do you want to try again? (y/n) ")
            decision = input_check_play_again(decision)
            try:
                if decision.lower() == "y":
                    main("next", player_name, played_words)
                elif decision.lower() == 'n':
                    print("Thank you for your time. See you in the next one!")
                    goodbye()
                else:
                    raise ValueError
            except ValueError:
                input_check_play_again()


if __name__ == '__main__':
    main("first")
