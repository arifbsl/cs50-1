#include <stdio.h>
#include <cs50.h>
#include <ctype.h>

int main(void)
{
    //listing variable used by program
    int height, spaces, hashes;
    
    //asks user for input and make sure input is valid for use
    do
    {
        height = get_int("Height: ");
    }
    while (height <= 0 || height > 8);
    
    //makes pyramid line by line
    for (int i = 0; i < height; i++)
    {
        //makes first of half of pyramid
        for (spaces = (height - i); spaces > 1; spaces--)
        {
            printf(" ");
        }

        for (hashes = 0; hashes < (i + 1); hashes++)
        {
            printf("#");
        }
        
        //puts two spaces between the halves
        printf("  ");
        
        //makes second half of pyramid
        for (hashes = 0; hashes < (i + 1); hashes++)
        {
            printf("#");
        }
        
        //goes to the next line
        printf("\n");


    }
}


