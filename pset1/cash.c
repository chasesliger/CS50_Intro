#include <cs50.h>
#include <stdio.h>
#include <math.h>

//initialize variables for worth of each coin along with other variables
int q = 25;
int d = 10;
int n = 5;
int p = 1;
float dollars;
int cents;
int coins;

int main(void)
{
//do loop to check to make sure that the user enters in a non-negative number using provided get_float function
    do
    {
        dollars = get_float("Change owed: ");
    }
    while (dollars < 0);

//round function to change float to an integer
    cents = round(dollars * 100);
    coins = 0;

//series of while loops that try to divide cents by coin value, iterate coin count, subtract that value from cents
    while ((cents / q) >= 1)
    {
        coins++;
        cents = cents - q;
    }

    while ((cents / d) >= 1)
    {
        coins++;
        cents = cents - d;
    }

    while ((cents / n) >= 1)
    {
        coins++;
        cents = cents - n;
    }

    while ((cents / p) >= 1)
    {
        coins++;
        cents = cents - p;
    }

//print out final answer
    printf("%i\n", coins);


}
