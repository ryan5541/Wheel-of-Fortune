from config import wheeltextloc

f = open(wheeltextloc, "w")
for value in range(100, 950, 50):
    f.write(f"{value}\n")
f.write("Lose a Turn\nBankrupt")
f.close()

f= open("englishwords.txt", "r")
g = open("dictionary.txt", "w")
word_list = [x.strip() for x in f.readlines()]
for word in word_list:
    if len(word) > 5:
        g.write(word + "\n")
f.close()
g.close()