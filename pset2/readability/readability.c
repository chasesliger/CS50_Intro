#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    //get input from user using CS50 provided function
    string text = get_string("Text: ");
    //create variables to keep track of the number of letters, words, and sentences
    int letters = 0;
    //initiating at 1, because it won't count the first word with this algorithm
    int words = 1;
    int sentences = 0;
    //for loop to iterate through text and increment the counts depending on the character
    for (int i = 0; i < strlen(text); i++)
    {
        //check for letters
        if (isalpha(text[i]) > 0)
        {
            letters++;
        }
        //check for spaces i.e. words
        if (isspace(text[ i + 1]) > 0)
        {
            words++;
        }
        //check for new sentences by looking for punction...each number is a ?, !, or .
        if (text[i] == 33 || text[i] == 63 || text[i] == 46)
        {
            sentences++;
        }
    }

    float L = ((float) letters) / ((float) words) * 100;
    float S = ((float) sentences) / ((float) words) * 100;;

    float index =  0.0588 * L - 0.296 * S - 15.8;

//prints out the grade level, if it is below first grade or above sixteenth, it prints that out instead (as per CS50 specifications)
    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", (int) round(index));
    }
}