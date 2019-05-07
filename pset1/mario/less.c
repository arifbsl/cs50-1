#include <stdio.h>
#include <cs50.h>

int main(void)
{
//lists variables used in this program
    int height, spaces, hashes;

//gets height from user for program
    do
    {
        height = get_int("Height: ");
    }
    while (height <= 0 || height > 8);

//creates the pyramid
    for (int i = 0; i < height; i++)
    {
        //puts in spaces
        for (spaces = (height - i); spaces > 1; spaces--)
        {
            printf(" ");
        }
    
        //puts in hashes
        for (hashes = 0; hashes < (i + 1); hashes++)
        {
            printf("#");
        }
        printf("\n");
    }
}
