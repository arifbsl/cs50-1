// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>
#include <cs50.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define HASH_TABLE_SIZE 36067

//creates and initializes variables
int size_of_dictionary = 0;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

//a modified version of djb2 originally by Dan Bernstein adapted by Neel Mehta. found at: https://github.com/hathix/cs50-section/blob/master/code/7/sample-hash-functions/good-hash-function.c

unsigned int hash(const char *word)
{
    unsigned long b = 5381;
    for (const char *ptr = word; *ptr != '\0'; ptr++)
    {
        b = (((b << 5) + b) + (tolower(*ptr)));
    }

    return b % HASH_TABLE_SIZE;
}

// creates hashtable of pointers to nodes and initializes it
node *hashtable[HASH_TABLE_SIZE] = {NULL};


// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Open dictionary and creates a pointer to it called file
    FILE *file = fopen(dictionary, "r");

    //checks to see if file was actually opened properly
    if (file == NULL)
    {
        fprintf(stderr, "File %s could not be opened.\n", dictionary);
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        node *new_word = malloc(sizeof(node));

        //makes sure memory for new_node was actually allocated
        if (new_word == NULL)
        {
            fprintf(stderr, "Creation of new_word failed.\n");
            return false;
        }

        //copies word to new_word
        strcpy(new_word->word, word);

        //hashes the word and stores it as the hash_index
        int hash_index = hash(word);

        //if first word in that hash_index, update that hash_index pointer to that of new_word and set the pointer portion of new_word to NULL
        if (hashtable[hash_index] == NULL)
        {
            hashtable[hash_index] = new_word;
            new_word->next = NULL;
        }

        //if not the first word in the hash_index, change the pointer portion of new_word to the address of first word in the index and change the pointer in the hash index to a pointer of the new_word
        else
        {
            new_word->next = hashtable[hash_index];
            hashtable[hash_index] = new_word;
        }

        //counts how many words are in the dictionary
        size_of_dictionary++;

    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    //hash the words and set a cursor pointer in the appropriate spot
    node *cursor = hashtable[hash(word)];

    //search the linked list of words from the dictionary against the word in the text chosen starting with the hash_index spot
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        else
        {
            cursor = cursor->next;
        }
    }
    //increase number of misspel
    return false;
}

//returns number of words in dictionary
unsigned int size(void)
{
    if (size_of_dictionary > 0)
    {
        return size_of_dictionary;
    }

    else
    {
        return 0;
    }
}


// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < HASH_TABLE_SIZE; i++)
    {
        node *cursor = hashtable[i];

        //if that spot in the hashtable has something delete all linked lists in that spot of the hashtable
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}


