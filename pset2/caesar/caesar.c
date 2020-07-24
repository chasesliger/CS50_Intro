#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    //check to make sure that the the user inputed a key
    if (argc == 2)
    {
        //make sure that the key they inputed are integers
        for (int i = 0; i < strlen(argv[1]); i++)
        {
            if (isdigit(argv[1][i]) == 0)
            {
                printf("Usage: ./caesar key \n");
                return (1);
            }
        }
        //convert the key from a string to an integer, using stdlib functiuon atoi
        int key =  atoi(argv[1]);
        //ask the user for the message to be encyphered with CS50 provided function
        string plain = get_string("plaintext:  ");
        printf("ciphertext:  ");

        for (int i = 0; i < strlen(plain); i++)
        {
            char c = plain[i];
            //check to see if c is a letter, then check if it is upper or lower
            if (isalpha(c) > 0)
            {

                if (isupper(c) > 0)
                {
                    //convert to alphabetical index
                    int con_c = c - 65;
                    //shift alphabetical index using formula
                    int shifted_index = (con_c + key) % 26;
                    //convert back to ascii
                    int decon_c = shifted_index + 65;
                    printf("%c", decon_c);
                }

                if (islower(c) > 0)
                {
                    //convert to alphabetical index
                    int con_c = c - 97;
                    //shift alphabetical index using formula
                    int shifted_index = (con_c + key) % 26;
                    //convert back to ascii
                    int decon_c = shifted_index + 97;
                    printf("%c", decon_c);
                }

            }

            else
            {
                printf("%c", c);
            }
        }
        //start a new line just for styling output
        printf("\n");
    }
    else
    {
        printf("Usage: ./caesar key \n");
        return (1);
    }
}