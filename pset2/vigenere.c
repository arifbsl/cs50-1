#include <stdio.h>
#include <cs50.h>
#include <math.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{

    string message = NULL, key = NULL;
    int n = 0, i = 0, j = 0, p = 0, key_length = 0, cipher_key = 0;

    //checks to see if you they typed in the correct amount of arguments
    if (argc != 2)
    {
        printf("Please enter 'program' followed by a word that will be your cipher key \n");

        //tells command line that program failed
        return 1;
    }
    
    //checks to see if the key is a word, if each character is not a letter return phrase to command line
    else
    {
        for (j = 0, p = strlen(argv[1]); j < p ; j++)
            //checks if each character is alphabetical, returns false if not
            if (!isalpha(argv[1][j]))
            {
                printf("Please use a word for your cipher key \n");

                return 1;
            }

    }
    
    //after verifying user has put in an valid cipher key, store key and find length 
    key = argv[1];
    key_length = strlen(key);
    
    {
        // prompts user for the message they want to cipher
        message = get_string("Please type in the message you would like to encipher: ");
        
        //adds context to input and output
        {
            printf("plaintext: %s\n", message);
            printf("ciphertext: ");
        }
        
        //applies cipher to message and then prints enciphered message
        for (i = 0, n = strlen(message), j = 0; i < n ; i++)
        {
            //creates cipher from key
            cipher_key = tolower(key[j % key_length]) - 'a';

            //checks if character is lower case and applies cipher then prints
            if islower(message[i])

            {
                printf("%c", ('a' + ((message[i] - 'a' + cipher_key) % 26)));

                j++;
            }

            //checks if character is upper case and applies cipher then prints
            else if isupper(message[i])

            {
                printf("%c", ('A' + ((message[i] - 'A' + cipher_key) % 26)));

                j++;
            }

            //prints character if not a letter
            else
            {    
                printf("%c", message[i]);
            }
        }

        //adds a line break
        printf("\n");

        //tells command line that cipher has succeeded
        return 0;
    }

}


