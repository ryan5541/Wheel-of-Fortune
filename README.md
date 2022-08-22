# Wheel-of-Fortune

For the full experience, please install the playsound library, version 1.2.2. This can be done by typing in 

pip install playsound==1.2.2

in the command prompt. The reason we need this particular version is because there's an issue with the current version in regards to file reading.
However, I've programmed it so that the program will run even without this library. (As in, you will not be prompted to enable audio).

If you're one of the instructors, however, if you want to get through everything as quickly as possible, I recommend keeping audio disabled.
On a similar vein, "debug mode" is just a convenient way of viewing the answers. I recommend this to be selected as well.

The sound effects were taken from this video: https://www.youtube.com/watch?v=5YECHrV_W3I

The words_alpha.txt file is a text file of English words. This can be found here: https://github.com/dwyl/english-words

The englishwords.txt file is a text file of COMMON English words. (Mainly to make it easier to play.) 
The source of this can be found here: https://www.ef.edu/english-resources/english-vocabulary/top-1000-words/
This was then saved as .txt.

The txtediting.py file was created to isolate the words from the rest of the website, and return words greater than 5 characters.
It was also used to populate the wheeldata.txt file.

Issues as of submission: In the final round, on the case where audio is enabled, the code will not proceed unless there is an input after the time runs out. This COULD be solved by manipulating threads, but that will be revisted after submission.
