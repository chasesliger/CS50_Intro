#include <cs50.h>
#include <stdio.h>

//define functions ahead of time so that C will compile
void print_space(int);
void print_block(int);

int main(void)
{
    int height;
    do {
    height = get_int("Height: ");
    } while ((height > 8) || (height < 1)); //keep asking user for a number between 1 and 8 (inclusive 8)

//a for loop, that prints the height minus i spaces
    for (int i = 0; i < height; i++)
    {
        print_space(height-i-1);
        print_block(i+1);
        printf("\n");
    }
}

//make two functions, one for printing spaces and the other for printing '#' i.e. blocks
void print_space(int n)
    {
    for (int i = 0; i < n; i++)
        {
            printf(" ");
        }
    }

void print_block(int n)
    {
    for (int i = 0; i < n; i++)
        {
            printf("#");
        }
    }
