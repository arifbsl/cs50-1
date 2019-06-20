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
    WordsGiven = message.strip().split()

    # reads banned word list and stores it in a list
    BannedWords = []
    with open(Dictionary, "r") as file:
        for line in file.readlines():
            BannedWords.append(line.rstrip())

    # finds length of each list
    LengthOfBannedWords = len(BannedWords)
    LengthOfWordsGiven = len(WordsGiven)

    # prints out censored version of message
    # interates over each of the words given
    for i in range(LengthOfWordsGiven):

        # interates over each of type words
        j = 0
        for j in range(LengthOfBannedWords):

            # Compares words in message against banned words in dictionary, prints censored version if matched
            if (WordsGiven[i].lower() == BannedWords[j].lower()):
                print("*" * len(WordsGiven[i]), end="")
                break

            # prints word if not in banned word list
            if LengthOfBannedWords - j == 1:
                print("{}".format(WordsGiven[i]), end="")
                break
        # ensures last word of the sentence doesn't have space after it
        if LengthOfWordsGiven - i == 1:
            break
        print(" ", end="")

    # line breaks at the end of the sentence
    print()


if __name__ == "__main__":
    main()
