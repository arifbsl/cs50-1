import cs50
import sys
import re


def main():

    # Checks command line arguement, get's input from user, and stores both dictionary and input
    while True:
        if len(sys.argv) != 2:
            print("Please enter program followed by your banned word list")
            exit(1)
        else:
            Dictionary = sys.argv[1]
            message = cs50.get_string("What message would you like to censor? ")
            break

    # takes user input and puts it into a list, does the same with Dictionary of banned words
    BannedWords = set()
    with open(Dictionary, "r") as file:
        for line in file.readlines():
            BannedWords.add(line.strip())
    
    # stored length so it would have to calculate it each time through the loop
    WordsGiven = message.strip().split()
    LengthOfWordsGiven = len(WordsGiven)
    
    # checks given word again banned words and then either prints censored version or the given word
    for givenword in WordsGiven:
        if givenword.lower() in BannedWords:
            print ("*" * len(givenword), end="")
        if givenword.lower() not in BannedWords:
            print (givenword, end="")
        if givenword == WordsGiven[LengthOfWordsGiven-1]:
            break
        print(" ", end="")
    print()


if __name__ == "__main__":
    main()
