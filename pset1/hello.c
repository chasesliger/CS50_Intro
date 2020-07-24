#include <stdio.h>
#include <cs50.h>

//simple hello world program that asks for user's name

int main(void)
{
    string name = get_string("What is your name?\n");
    printf("hello, %s!\n", name);
}
