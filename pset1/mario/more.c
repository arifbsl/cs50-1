#include <stdio.h>
#include <cs50.h>
#include <ctype.h>

int main(void)
{
int height;
int spaces;
int hashes;

do
{
    height = get_int ("Height: ");
}
while (height < 0 || height > 23);


for (int i = 0; i < height; i++)
{
    for (spaces = (height - i); spaces > 0; spaces--)
    {
        printf(" ");
    }

    for (hashes = 0; hashes < (i+1); hashes++)
    {
        printf("#");
    }
    
    printf("  ");

     for (hashes = 0; hashes < (i+1); hashes++)
    {
        printf("#");
    }

     for (spaces = (height - i); spaces > 0; spaces--)
    {
        printf(" ");
    }


    printf("\n");


}
}

