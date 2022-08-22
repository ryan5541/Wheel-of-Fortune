from config import dictionaryloc
from config import turntextloc
from config import wheeltextloc
from config import maxrounds
from config import vowelcost
from config import roundstatusloc
from config import finalprize
from config import finalRoundTextLoc
from config import bankruptLoc
from config import finalroundLoc
from config import letterLoc
from config import solveLoc
from config import spinwheelLoc
from config import wrongguessLoc
from config import beginroundLoc
from config import finalroundguessingLoc
from config import finalroundwrongguessLoc
from config import finalroundcorrectguessLoc

import random
import time
import pkg_resources

players={0:{"roundtotal":0,"gametotal":0,"name":""},
         1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""},
        }

roundNum = 0
dictionary = []
turntext = ""
wheellist = []
roundWord = ""
blankWord = []
vowels = {"a", "e", "i", "o", "u"}
roundstatus = ""
finalroundtext = ""
roundcompleted = False
final_round = False
debug_mode = False
audio_enabled = False
letters_guessed = []
playsound_imported = False
final_round_guesses = []

try:
    from playsound import playsound
    if pkg_resources.get_distribution("playsound").version == '1.2.2': #There's a bug with the latest version of playsound. Which is why we need this version. -Ryan
        playsound_imported = True
    else:
        playsound_imported = False
except:
    audio_enabled = False
    playsound_imported = False
    
def readDictionaryFile():
    global dictionary
    # Read dictionary file in from dictionary file location
    f = open(dictionaryloc, "r", newline = "\n")
    # Store each word in a list.
    dictionary = [x.strip() for x in f.readlines()]
    f.close()
    
def readTurnTxtFile():
    global turntext   
    #read in turn intial turn status "message" from file
    f = open(turntextloc, "r")
    turntext = f.read()
    f.close()
    
def readFinalRoundTxtFile():
    global finalroundtext   
    #read in turn intial turn status "message" from file
    f = open(finalRoundTextLoc, "r")
    finalroundtext = f.read()
    f.close()
    
def readRoundStatusTxtFile():
    global roundstatus
    # read the round status  the Config roundstatusloc file location 
    f = open(roundstatusloc, "r")
    roundstatus = f.read()
    f.close()

def readWheelTxtFile():
    global wheellist
    # read the Wheel name from input using the Config wheelloc file location 
    f = open(wheeltextloc, "r", newline = "\n")
    wheellist = [x.strip() for x in f.readlines()]
    f.close()
    
def getPlayerInfo():
    global players
    
    # read in player names from command prompt input
    for index, value in enumerate(players):
        players[index]["name"] = input(f"What is Player {index+1}'s name?\n")
        if players[index]["name"] == "":
            players[index]["name"] = f"Player {index + 1}"

def gameSetup():
    # Read in File dictionary
    # Read in Turn Text Files
    global turntext
    global dictionary
        
    print("Welcome to WHEEL! OF! FORTUNE!")
    enable_debug_mode()
    if playsound_imported:
        enable_audio()        
    readDictionaryFile()
    readTurnTxtFile()
    readWheelTxtFile()
    getPlayerInfo()
    readRoundStatusTxtFile()
    readFinalRoundTxtFile() 
    
def getWord():
    global dictionary
    #choose random word from dictionary
    roundWord = random.choice(dictionary).lower()
    #make a list of the word with underscores instead of letters.
    roundUnderscoreWord = ["_"] * len(roundWord)
    return roundWord,roundUnderscoreWord

def wofRoundSetup():
    global players
    global roundWord
    global blankWord
    global letters_guessed
    # Set round total for each player = 0
    for key, value in enumerate(players):
        players[key]["roundtotal"] = 0
    letters_guessed.clear()
    # Return the starting player number (random)
    initPlayer = random.choice(list(players.keys()))
    # Use getWord function to retrieve the word and the underscore word (blankWord)
    roundWord, blankWord = getWord()
    return initPlayer


def spinWheel(playerNum):
    global wheellist
    global players
    global vowels
    stillinTurn = False
    if audio_enabled:
        print("Spinning wheel...")
        playsound(spinwheelLoc)
    # Get random value for wheellist
    wheel_value = random.choice(wheellist)
    #wheel_value = "Lose a Turn" #This is here for debugging purposes. -Ryan
    print(f"You landed on: {wheel_value}")
    if not wheel_value.isnumeric():
    # Check for bankrupcy, and take action.
        if wheel_value.lower() == "bankrupt":
            players[playerNum]["roundtotal"] = 0
            stillinTurn = False #This is technically redundant, but simplifies readability -Ryan
            if audio_enabled:
                playsound(bankruptLoc)
    # Check for loose turn
        elif wheel_value.lower() == "lose a turn":
            if audio_enabled:
                playsound(wrongguessLoc)
            stillinTurn = False #Again, readability. -Ryan
            
    # Get amount from wheel if not loose turn or bankruptcy
    else: 
        wheel_value = int(wheel_value)
    # Ask user for letter guess
        guess = enter_consonant()
    # Use guessletter function to see if guess is in word, and return count
        goodGuess, count = guessletter(guess, playerNum)
    # Change player round total if they guess right.
        if goodGuess:
            players[playerNum]["roundtotal"] += wheel_value * count
            stillinTurn = True
    return stillinTurn


def guessletter(letter, playerNum): 
    global players
    global blankWord
    global final_round
    global letters_guessed
    
    goodGuess = False
    count = 0
    # parameters:  take in a letter guess and player number
    # Change position of found letter in blankWord to the letter instead of underscore
    letters_guessed.append(letter) #In order to get to this function, the user is forced to put a letter that isn't on this list already.
    if letter in roundWord:
        if not final_round:
            print(f"Good Guess! There are {letter.upper()}s!")
        for index, char in enumerate(list(roundWord)):
            if letter == char:
                blankWord[index] = char
                count += 1
                if audio_enabled:
                    print(blankWord)
                    playsound(letterLoc)
                    time.sleep(1)
                    
        goodGuess = True
    else:
        if not final_round:
            print(f"Sorry! There are no {letter.upper()}s!")
            playsound(wrongguessLoc)
    # return goodGuess= true if it was a correct guess
    # return count of letters in word. 
    # ensure letter is a consonate.
    
    return goodGuess, count

def buyVowel(playerNum):
    global players
    global vowels
    
    # Take in a player number
    # Ensure player has 250 for buying a vowelcost
    if players[playerNum]["roundtotal"] >= vowelcost:
    # Use guessLetter function to see if the letter is in the file
        guess = enter_vowel()
        goodGuess, count = guessletter(guess, playerNum)
    # Ensure letter is a vowel
        # Handled in enter_vowel() - Ryan
    #    pass
        if goodGuess:
            players[playerNum]["roundtotal"] -= vowelcost
    else:
        print("You do not have enough money to buy a vowel!")
        goodGuess = True #This just ensures that the turn is preserved. -Ryan
    # If letter is in the file let goodGuess = True
    
    return goodGuess      
        
def guessWord(playerNum):
    global players
    global blankWord
    global roundWord
    global roundcompleted
    global final_round_guesses
    
    # Take in player number
    # Ask for input of the word and check if it is the same as wordguess
    guess = enter_word()
    # Fill in blankList with all letters, instead of underscores if correct
    if not final_round:
        if guess == roundWord:
            blankWord = list(roundWord)
            print(f"Correct! The word was {roundWord}!")
            roundcompleted = True
            if audio_enabled:
                playsound(solveLoc)
        else:
            print("Sorry! That's not the word!")
            roundcompleted = False
            if audio_enabled:
                playsound(wrongguessLoc)
    else:
        final_round_guesses.append(guess)
    # return False ( to indicate the turn will finish)  
    
    return False
    
    
def wofTurn(playerNum):  
    global roundWord
    global blankWord
    global turntext
    global players
    global roundcompleted
    global roundstatus
    
    # take in a player number. 
    # use the string.format method to output your status for the round
    # and Ask to (s)pin the wheel, (b)uy vowel, or G(uess) the word using
    # Keep doing all turn activity for a player until they guess wrong
    # Do all turn related activity including update roundtotal 
    roundcompleted = False
    stillinTurn = True
    number_spins = 0
    while stillinTurn:
        
        # use the string.format method to output your status for the round
            #...or an f-string
        
        # Get user input S for spin, B for buy a vowel, G for guess the word
        print(f"\n{players[playerNum]['name']}'s turn!")
        print(blankWord)
        print(f"Guessed Letters: {letters_guessed}")
        if debug_mode:
            print(f"#ANSWER: {roundWord}")
        print("\nRound Totals:")
        roundstatus = ""
        for index, value in enumerate(players):    
            roundstatus = f"{roundstatus}{players[index]['name']}: {players[index]['roundtotal']}\n"
        
        print(f"{roundstatus}")
        choice = input(f"{turntext}\n")
        if(choice.strip().upper() == "S"):
            stillinTurn = spinWheel(playerNum)
            number_spins += 1
        elif(choice.strip().upper() == "B"):
            if number_spins > 0: #Guarantees that the person spins first BEFORE buying vowels.
                stillinTurn = buyVowel(playerNum)
            else:
                print("You need to spin at least once before buying a vowel!")
        elif(choice.upper() == "G"):
            stillinTurn = guessWord(playerNum)
        else:
            print("Not a correct option")        
    
    # Check to see if the word is solved, and return false if it is,
    if roundcompleted:
        for index, value in enumerate(players):
            if index == playerNum:
                players[index]["gametotal"] += players[index]["roundtotal"]
            else:
                players[index]["gametotal"] += 0
        
    return roundcompleted
    # Or otherwise break the while loop of the turn.     
        # Nah.

def wofRound():
    global players
    global roundWord
    global blankWord
    global roundstatus
    global turntext
    
    initPlayer = wofRoundSetup()
    if audio_enabled:
        print("Setting up round...")
        playsound(beginroundLoc)
        
    current_player = initPlayer #Redundant, but this is mainly for readability purposes...
    roundcompleted = False
    # Keep doing things in a round until the round is done ( word is solved)
        # While still in the round keep rotating through players
    while roundcompleted == False:
        # Use the wofTurn fuction to dive into each players turn until their turn is done.
        roundcompleted = wofTurn(current_player)
        if current_player != 2:
            current_player += 1
        else:
            current_player = 0
    # Print roundstatus with string.format, tell people the state of the round as you are leaving a round.
        # ...or use an f-string instead.
    print("\nGame Totals:")
    roundstatus = ""
    for key, value in enumerate(players):
        roundstatus = f"{roundstatus}{players[key]['name']}: {players[key]['gametotal']}\n"
    print(f"{roundstatus}")

def wofFinalRound():
    global roundWord
    global blankWord
    global finalroundtext
    global final_round
    global letters_guessed
    global final_round_guesses
    
    current_time = 0
    winplayer = 0
    amount = 0
    final_round = True
    letters_guessed.clear()
    # Find highest gametotal player.  They are playing.
    for index, value in enumerate(players):
        if players[index]["gametotal"] > amount:
            winplayer = index
            amount = players[index]["gametotal"]
    # Print out instructions for that player and who the player is.
    print(f"The player for the final round is: {players[winplayer]['name']}!")
    if audio_enabled:
        playsound(finalroundLoc)
    # Use the getWord function to reset the roundWord and the blankWord ( word with the underscores)
    roundWord, blankWord = getWord()
    # Use the guessletter function to check for {'R','S','T','L','N','E'}
    print("Filling in 'R, S, T, L, N, E'")
    for letter in {"R", "S", "T", "L", "N", "E"}:
        guessletter(letter.lower(), winplayer)
    # Print out the current blankWord with whats in it after applying {'R','S','T','L','N','E'}
    print(blankWord)
    if debug_mode:
        print(f"#ANSWER: {roundWord}")
    print(finalroundtext)
    # Gather 3 consonats and 1 vowel and use the guessletter function to see if they are in the word
    letter_guesses = [None]*4
    for i in range(len(letter_guesses)):
        if i < len(letter_guesses) - 1:
            letter_guesses[i] = enter_consonant()
        else:
            letter_guesses[i] = enter_vowel()
    
    for guess in letter_guesses: #I could have incorporated this into the for loop above, but this accomodates for the audio case. -Ryan
        guessletter(guess,winplayer)    
    # Print out the current blankWord again
    # Remember guessletter should fill in the letters with the positions in blankWord
    print(blankWord)
    if audio_enabled:
        print("When the music starts, you have 10 seconds! Guess as many words as you can!") #I'm well aware that the rubric only allows 1 guess. But this line requires audio to be run, and that's additional material, so... -Ryan
        time.sleep(2)
        print("Good Luck!")
        playsound(finalroundguessingLoc, False) #False allows lines of code to be run while the sound plays. -Ryan
        current_time = time.time()
        while time.time() < current_time + 10:
            final_round_guesses.append(input("")) #Apparently, there is no way to kill input() safely, so technically, you could just hang around on the input screen forever. -Ryan
    else:
        print("You have one guess, good luck!")
    # Get user to guess word
        guessWord(winplayer)
            
    # If they do, add finalprize and gametotal and print out that the player won 
    if roundWord in final_round_guesses:
        print("You won!")
        print(f"You received an additional {finalprize}!")
        if audio_enabled:
            playsound(finalroundcorrectguessLoc)
        amount += finalprize
    else:
        print("Sorry!")
        if audio_enabled:
            playsound(finalroundwrongguessLoc)
        print(f"The correct answer was {roundWord}!")
        amount = amount #Readability. -Ryan
    print(f"Grand total: {amount}")

def enter_consonant():
    global guessed_letters
    
    valid = False
    while not valid:
        letter = input("Enter a consonant:\n")
        if letter.isalpha() and letter not in vowels and len(letter) == 1 and letter not in blankWord and letter not in letters_guessed:
            valid = True
        else:
            print("Please enter a valid consonant that isn't guessed already!")
    
    return letter

def enter_vowel():
    valid = False
    while not valid:
        letter = input("Enter a vowel:\n")
        if letter.isalpha() and letter in vowels and len(letter) == 1 and letter not in blankWord and letter not in letters_guessed:
            valid = True
        else:
            print("Please enter a valid vowel that isn't in the word already!")
    
    return letter

def enter_word():
    valid = False
    while not valid:
        word = input("Enter a word:\n")
        if word.isalpha():
            valid = True
        else:
            print("Please enter a word! (Made up ones count!)")
        
    return word

def letter_prompt(letter, count):
    if count > 0:
        print(f"There are {count} {letter}s!")
    else:
        print("There are no {letter}s!")
        
def check_yes_no(prompt):
    valid = False
    value = False
    while not valid:
        response = input(prompt)
        if response not in ["y","n"]:
            print("Please enter either 'y' or 'n'!")
        else:
            valid = True
    if response == "y":
        value = True
    else:
        value = False
    return value

def enable_debug_mode():
    global debug_mode
    enabled = check_yes_no("Would you like to enable Debug Mode?\n(All answers are revealed.)(y/n)\n")
    debug_mode = enabled

def enable_audio():
    global audio_enabled
    enabled = check_yes_no("Would you like to enable audio? (y/n)\n")
    audio_enabled = enabled
    
def main():
    gameSetup()    

    for i in range(0,maxrounds):
        if i in [0,1]:
            print(f"\nRound {i + 1}!")
            wofRound()
        else:
            print("\nFinal Round!")
            wofFinalRound()

if __name__ == "__main__":
    main()
    
    
