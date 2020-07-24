#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    //ensure user runs programs with two prompts
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    //open the memory card file
    FILE *f = fopen(argv[1], "r");

    //create a buffer to read the 512 byte chunks into
    unsigned char *buffer = malloc(512);
    //create variable to keep track of the image count
    int img_count = 0;
    //initialize file to write to variable
    FILE *img = NULL;
    //create string to for filename
    char filename[8];
    //flag to see if a jpeg has been detected
    bool flag = false;

    while (fread(buffer, sizeof(unsigned char), 512, f) == 512)
    {

        //initial test to see if a jpeg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0 && flag == false)
        {
            sprintf(filename, "%03i.jpg", img_count);
            img = fopen(filename, "w");
            fwrite(buffer, sizeof(unsigned char), 512, img);
            flag = true;
        }

        //if a new jpeg is detected
        if (flag == true && buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //fwrite(buffer, sizeof(unsigned char), 512, img);
            img_count++;
            fclose(img);
            sprintf(filename, "%03i.jpg", img_count);
            img = fopen(filename, "w");
            fwrite(buffer, sizeof(unsigned char), 512, img);
        }

        //else keep writing to the current file
        else if (flag == true)
        {
            fwrite(buffer, sizeof(unsigned char), 512, img);
        }
     }

    fclose(img);
    fclose(f);

    //free up the memory assigned by malloc for the buffer
    free(buffer);
    //close the memory card file
    fclose(f);
    return 0;

}
