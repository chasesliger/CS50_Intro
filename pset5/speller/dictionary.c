// Implements a dictionary's functionality

#include <stdbool.h>

#include "dictionary.h"
#include <stdio.h>
#include <stdlib.h>

//string.h for the strcasemp method to compare strings case-insensitively, and to copy strings
#include <string.h>
#include <ctype.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 50;

// Hash table
node *table[N];

//Dictionary Size
int dict_size = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int size = strlen(word) + 1;

    char lower_case[size];

    //for loop to make sure every letter is lower case in the word
    for (int i = 0; i < size; i++)
    {
        lower_case[i] = tolower(word[i]);
    }

    int index = hash(lower_case);

    node *cursor = table[index];

    while (cursor != NULL)
    {
        if (strcmp(cursor->word, lower_case) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{

    //Hash function found online and adabapted from the following website -> https://github.com/hathix/cs50-section/blob/master/code/7/sample-hash-functions/good-hash-function.c
    unsigned long hash = 5381;

    for (const char *ptr = word; *ptr != '\0'; ptr++)
    {
        hash = ((hash << 5) + hash) + tolower(*ptr);
    }

    return hash % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
// First open the dictionary file, and make sure it isn't NULL
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    char *new_word = malloc(46 * (sizeof(char)));

//while loop to that goes until the end of the file,
    while (fscanf(file, "%s", new_word) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return 1;
        }
        strcpy(n->word, new_word);
        unsigned int index = hash(new_word);
        //first case if there is not yet a linked list
        if (&table[index] == NULL)
        {
            table[index] = n;
        }
        else
        {
            n->next = table[index];
            table[index] = n;
        }
        //keeping track of the size of the dictionary
        dict_size++;
    }

    free(new_word);
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return dict_size;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // for and while loops to go through and free's every node in the dictionary
    int i = 0;
    for (i = 0; i < N; i++)
    {
        node *cursor = table[i];

        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }

    return true;
}
