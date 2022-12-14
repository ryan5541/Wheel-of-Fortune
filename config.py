import random

# Dictionary file location, change if needed.
dictionaryloc = 'data/dictionary.txt'

# Turn text file location, change if needed.
turntextloc = 'data/turntext.txt'

# Wheel contents for file location, change if needed.
wheeltextloc = 'data/wheeldata.txt'

# End of Round Status status file, change if needed.
roundstatusloc = 'data/roundstatus.txt'

# number of rounds in a game
maxrounds = 3

# Vowel cost
vowelcost = 250

# final prize, you fill this in
finalprize = random.choice([25000, 50000, 100000, 1000000])

# final round, change if needed.
finalRoundTextLoc = 'data/finalround.txt'

#location of audio files
bankruptLoc = 'sounds/bankrupt.wav'
finalroundLoc = 'sounds/finalround.wav'
letterLoc = 'sounds/letter.wav'
solveLoc = 'sounds/solve.wav'
spinwheelLoc = 'sounds/spinwheel.wav'
wrongguessLoc = 'sounds/wrongguess.wav'
beginroundLoc = 'sounds/beginround.wav'
finalroundguessingLoc = 'sounds/finalroundguessing.wav'
finalroundwrongguessLoc = 'sounds/finalroundwrongguess.wav'
finalroundcorrectguessLoc = 'sounds/finalroundcorrectguess.wav'