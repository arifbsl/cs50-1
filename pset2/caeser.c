#include <stdio.h>
#include <cs50.h>
#include <math.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{

string message = NULL;
int key = 0, n = 0, i = 0;

    //checks to see if you they typed in the correct amount of arguments
    if (argc != 2)
    {
        printf("Please enter program followed by a number that will be your cipher key \n");

        //tells command line that program failed
        return 1;
    }
    else

    // gets key and converts it to an integer
    key = atoi(argv[1]);

    //checks to see if the key is a positive integer
    if (key <= 0)
    {
        printf("Please use a positive integer for your cipher key \n");

        //tells command line that program failed
        return 1;
    }
    else
    {
        // prompts user for the message they want to cipher
        message = get_string ("Please type in the message you would like to encipher: ");

        //prefaces what input and output are
        {
          printf("plaintext: %s\n", message);
          printf("ciphertext: ");
        }
        
        for (i = 0, n = strlen(message); i < n ; i++)
        {
            //checks if character is lower case and applies cipher then prints
            if islower(message[i])
                printf("%c", ('a' + ((message[i] - 'a' + key) % 26)));

            //checks if character is upper case and applies cipher then prints
            else if isupper(message[i])
                printf("%c", ('A' + ((message[i] - 'A' + key) % 26)));

            //prints character if not a letter
            else
                printf("%c",message[i]);
        }

        //adds a line break
        printf("\n");

        //tells command line that cipher has succeeded
        return 0;
    }

}

