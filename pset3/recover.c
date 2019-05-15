#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{   
    //checks to make sure the number of arguements is correct, sends error to command line if not
    if (argc != 2)
    {
        fprintf(stderr, "please type in the program followed by the jpeg you'd like recover\n");
        return 1;
    }
    
    //stores input file as a variable
    char *raw_data = argv[1];
    FILE *inptr = fopen(raw_data, "r");
    
    //makes sure input file contains data. if not sends error to command line
    if (inptr == NULL)
    {
        fprintf(stderr, "%s could not be opened\n", raw_data);
        return 2;
    }

    //creating an initializing variables
    FILE *images = NULL;
    unsigned char buffer[512];
    int jpeg_found = 0;

    //reads the file in 512 byte Blocks
    while (fread(buffer, 512, 1, inptr))
    {
        // if end of file is reached, it'll close the program and folders
        if (feof(inptr) != 0)
        {
            fclose(inptr);

            if (images != NULL)
            {
                fclose(images);
            }

            return 0;
        }

        // checks the first four bytes of each 512 block for the header of a jpeg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //closes the file if previously opened and still open
            if (images != NULL)
            {
                fclose(images);
            }

            //creates an array with the maximium possible number of jpegs with a 3 digit address
            char filename[1000];

            //names and stores that name as "###.jpg" in the array filename
            sprintf(filename, "%03d.jpg", jpeg_found);

            //writes filename to the folder images
            images = fopen(filename, "w");

            //if images fails to update it'll close folders and send an error message to the command line
            if (images == NULL)
            {
                fclose(images);
                fclose(inptr);
                fprintf(stderr, "Could not output %3s.jpg\n", filename);
                return 3;
            }

            //updates the number of jpegs found
            jpeg_found++;

        }
        //goes back to the start of the while loop if the first jpeg hasn't been found
        if (jpeg_found == 0)
        {
            continue;
        }

        //writes the jpeg to the file named images. explicitly it copies what's in the buffer to images
        fwrite(buffer, 512, 1, images);

    }
}
