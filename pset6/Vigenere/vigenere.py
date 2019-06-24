import sys
import cs50
import string

# checks to see if command line input is correct
while True:
    if len(sys.argv) != 2:
        print("Please enter program followed by a word that will be your cipher key")
        exit(1)
    else:
        break

# checks to see if key is appropriate aka a word
while True:
    if sys.argv[1].isalpha():
        key = sys.argv[1]
        break
    else:
        print("Please use a word for your cypher key")
        exit(1)

# gets message from user
message = cs50.get_string("Please type in the message you would like to encipher: ")
print()

# initializes a bunch of variables
key, LengthOfKey, j, stringkey, stringmessage = key.lower(), len(key), 0, [], []

# makes a list of key ascii values
for p in key:
    stringkey.append(ord(p) - ord('a'))

# makes a list of characters from the message
for n in message:
    stringmessage.append(n)

print("plaintext: {}".format(message))

print("ciphertext: ", end="")

# ciphers message character by character and prints ciphered message
for i in range(len(stringmessage)):

    if stringmessage[i].isalpha():

        if stringmessage[i].isupper():
            b = chr(ord('A') + ((ord(stringmessage[i])+stringkey[j % LengthOfKey] - ord('A')) % 26))
            print(b, end="")
            j += 1

        elif stringmessage[i].islower():
            c = chr(ord('a') + ((ord(stringmessage[i])+stringkey[j % LengthOfKey] - ord('a')) % 26))
            print(c, end="")
            j += 1

    else:
        print(stringmessage[i], end="")

print()
