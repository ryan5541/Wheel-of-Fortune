# Wheel-of-Fortune

For the full experience, please install playsound 1.2.2. This can be done by typing in 

pip install playsound==1.2.2

in the command prompt. The reason we need this particular version is because there's an issue with the current version in regards to file reading.
How

The sound effects were taken from this video: https://www.youtube.com/watch?v=5YECHrV_W3I

The words_alpha.txt file is a text file of English words. This can be found here: https://github.com/dwyl/english-words

The englishwords.txt file is a text file of COMMON English words. (Mainly to make it easier to play.) 
The source of this can be found here: https://www.ef.edu/english-resources/english-vocabulary/top-1000-words/
This was then saved as .txt.

The txtediting.py file was created to isolate the words from the rest of the website, and return words greater than 5 characters.
It was also used to populate the wheeldata.txt file.
