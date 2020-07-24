#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    //for loop to go through rows
    for (int i = 0; i < height; i++)
    {
        //for loop to go through columns
        for (int j = 0; j < width; j++)
        {
            //find average of all colors of a cell, the reassing that to red, green, blue
            float avg = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtRed = avg;

        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    //for loop to go through rows
    for (int i = 0; i < height; i++)
    {
        //for loop to go through columns
        for (int j = 0; j < width; j++)
        {
            //use formulas to go calculate sepia for each value of a pixel
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);

            //if sepiaValue is greater than 255, set to 255, otherwise set it to calculated value
            if (sepiaRed > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = sepiaRed;
            }

            //if sepiaValue is greater than 255, set to 255, otherwise set it to calculated value
            if (sepiaGreen > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = sepiaGreen;
            }

            //if sepiaValue is greater than 255, set to 255, otherwise set it to calculated value
            if (sepiaBlue > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = sepiaBlue;
            }
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //for loop to go through rows
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width/2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //create copy of image to use the original values to calculate changes, by first initializing an array, then copying the orignal with 2 for loops
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }


    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //initialize sums of each color, plus a count, so we can calculate the average
            int sumGreen = 0;
            int sumBlue = 0;
            int sumRed = 0;
            int count = 0;
            //use two loops to calculate the average of the 9 squares around a square, by starting at -1 and going to 1
            for (int r = -1; r <= 1; r++)
            {
                for (int c = -1; c <= 1; c++)
                {
                    //if statement to take care of corner cases...checks to make sure r and c don't go beyond height and width arrays
                    if (i + r >= 0 && i + r < height && j + c >= 0 && j + c < width)
                    {
                        sumGreen = sumGreen + copy[i + r][j + c].rgbtGreen;
                        sumBlue = sumBlue + copy[i + r][j + c].rgbtBlue;
                        sumRed = sumRed + copy[i + r][j + c].rgbtRed;
                        count++;
                    }
                }
            }
            //set original image values to new calculated values
            image[i][j].rgbtGreen = round((float) sumGreen/count);
            image[i][j].rgbtBlue = round((float)sumBlue/count);
            image[i][j].rgbtRed = round((float) sumRed/count);

        }
    }
    return;
}
