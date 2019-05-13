// Copies a BMP file

#include <stdio.h>
#include <cs50.h>
#include <math.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: resize size infile outfile\n");
        return 1;
    }
    // what size factor you want to increase the size by
    int size = atoi(argv[1]);

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf, bf_resize;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    bf_resize = bf;

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi, bi_resize;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    bi_resize = bi;

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    bi_resize.biWidth = bi.biWidth * size;
    bi_resize.biHeight = bi.biHeight * size;

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int new_padding = (4 - (bi_resize.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // Calculating size info with image resized
    bi_resize.biSizeImage = (bi_resize.biWidth * sizeof(RGBTRIPLE) + new_padding) * (abs(bi_resize.biHeight));
    bf_resize.bfSize = bi_resize.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf_resize, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi_resize, sizeof(BITMAPINFOHEADER), 1, outptr);

     // allocate a memory to store one scanline
    RGBTRIPLE scanline[bi_resize.biWidth * sizeof(RGBTRIPLE)];

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        //iterates over individual lines horizontally,  does this a "size" amount of times
        for (int t = 0; t < size; t++)
        {
            // iterate over pixels in scanline
            for (int j = 0; j < bi.biWidth; j++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                //iterates pixel a "size" number of times
                for (int n = 0; n < size; n++)
                {
                    scanline[(j * size) + n] = triple;
                }
            }

            // skip over padding, if any
            fseek(inptr, padding, SEEK_CUR);

            //writes scanlines a "size" number of times
            for (int p = 0; p < size; p++)
            {
                // writes a scanline once
                fwrite(scanline, sizeof(RGBTRIPLE), bi_resize.biWidth, outptr);

                //adds new padding
                for (int k = 0; k < new_padding; k++)
                {
                    fputc(0x00, outptr);
                }
            }
        }
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
