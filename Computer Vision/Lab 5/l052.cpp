//Kingsley Kim, Period 4

// 'finding contours of an image:
// make sure image is not square
// take in a jpg image and first convert it to ppm, then grayscale all the pixel, using (R+B+G)/3
//after you grayscale, save a grayscale.ppm, put the average three times for making the ppm

//apply Sobel operator: x-direc: [-1, 0, 1]  y-direction: [-1, -2, -1]
                            //   [-2, 0, 2]               [0, 0, 0]
                            //   [-1, 0, 1]               [1, 2, 1]

//multiply these operators onto the greyscale pixels, all of them
//Apply the sobel operator for x and y
//then change the gradient x and y into gradient magnitude, 
//then transform the thing into ppm of only 0 and 1, edges.ppm
#include <iostream>
#include <random>
#include <fstream>
#include <tuple>
#include <cmath>
#include <string>
#include <algorithm>
#include <list>
#include <vector>
#include <set>
#include <stack>
#include <queue>
using namespace std; 

ifstream in("image.ppm");
ofstream gray("imageg.ppm");
ofstream edge("imagem.ppm");
ofstream second("image1.ppm");
int dimx, dimy;

string** run_input()
{
    string P3; 
    in >> P3;
    gray << P3 << endl;
    
    in >> dimy >> dimx;
    gray << dimy << " " << dimx << endl;
    int max_col;
    in >> max_col;
    gray << max_col << endl;
    string** im;
    im = new string*[dimx];

    for(int i = 0; i < dimx; i++)
    {
        im[i] = new string[dimy];
        for(int j = 0; j < dimy; j++)
        {   
            string temp1, temp2, temp3;
            in >> temp1 >> temp2 >> temp3;

            string avg = to_string((int)(stof(temp1) / max_col * 255 + stof(temp2) / max_col * 255 + stof(temp3) / max_col * 255)/3);
            // cout << "c" << endl;


            im[i][j] = avg;
            gray << avg << " " << avg << " "  << avg << " " << endl;
        }
    }

    return im;

}

double dot_product(vector<double> m1, vector<double> m2)
{
    double cum_sum = 0.0;

    for(int i = 0; i < (int)m1.size(); i++)
    {

        cum_sum += (m1[i] * m2[m1.size()-i-1]);
    }

    return cum_sum;
}

void hysteris_recur(vector<vector<double> > &output, int i, int j)
{
    if(output[i][j] == 0)
    {
        return;
    }
    else if(output[i][j] == 1)
    {
        output[i][j] = 2;
        hysteris_recur(output, i-1, j-1);
        hysteris_recur(output, i-1, j);
        hysteris_recur(output, i-1, j+1);
        hysteris_recur(output, i, j-1);
        hysteris_recur(output, i, j+1);
        hysteris_recur(output, i+1, j-1);
        hysteris_recur(output, i+1, j);
        hysteris_recur(output, i+1, j+1);
    }
    return;

}

void part2()
{
    string** image = run_input();
    double grayscale[dimx][dimy];
    for(int i = 0; i < dimx; i++)
    {
        for(int j = 0; j < dimy; j++)
        {
            grayscale[i][j] = stoi(image[i][j]);
        }
    }
    vector<double> x_direc;
    x_direc.push_back(-1.0); x_direc.push_back(0.0); x_direc.push_back(1.0); x_direc.push_back(-2.0); x_direc.push_back(0.0);
    x_direc.push_back(2.0); x_direc.push_back(-1.0); x_direc.push_back(0.0); x_direc.push_back(1.0); 
    vector<double> y_direc;
    y_direc.push_back(-1.0); y_direc.push_back(-2.0); y_direc.push_back(-1.0); y_direc.push_back(0.0); y_direc.push_back(0.0);
    y_direc.push_back(0.0); y_direc.push_back(1.0); y_direc.push_back(2.0); y_direc.push_back(1.0);
    double mag[dimx][dimy];
    for(int i = 0; i < dimx; i++)
    {
        mag[i][0] = 0;
        mag[i][dimy-1] = 0;
    }
    for(int i = 0; i < dimy; i++)
    {
        mag[0][i] = 0;
        mag[dimx-1][i] = 0;
    }

    for(int i = 1; i < dimx-1; i++)
    {
        for(int j = 1; j < dimy-1; j++)
        {
            vector<double> temp;

            for(int b = j-1; b <= j+1; b++)
            {
                for(int a = i-1; a <= i+1; a++)
                {
                    temp.push_back(grayscale[a][b]);
                }
            }

            // cout << temp.size() << x_direc.size() << y_direc.size() << endl;
            mag[i][j] = sqrt(pow(dot_product(temp, x_direc), 2) + pow(dot_product(temp, y_direc), 2));
           
        }
    }

    double threshold_low = 80;
    double threshold_high = 200;




    for(int i = 0; i < dimx; i++)
    {
        for(int j = 0; j < dimy; j++)
        {
            // edge << 1 << " " << 1 << " "  << 1 << " " << endl;
            // edge << 255 << " " << 255 << " " << 255 << " " << endl;
            if(mag[i][j] > threshold_low && mag[i][j] < threshold_high)
            {
                mag[i][j] = 1;

            }
            else if(mag[i][j] < threshold_low)
            {
                mag[i][j] = 0;

            }
            else if(mag[i][j] > threshold_high)
            {
                mag[i][j] = 2;
            }

        }
    }
    vector<vector<double> > output;
    
    for(int i = 0; i < dimx; i++)
    {
        vector<double> temp;
        for(int j = 0; j < dimy; j++)
        {
            temp.push_back(mag[i][j]);
        }
        output.push_back(temp);
    }
    
    for(int i = 1; i < dimx-1; i++)
    {
        for(int j = 1; j < dimy-1; j++)
        {
            if(output[i][j] == 2)
            {
                hysteris_recur(output, i, j);
            }
        }
    }
    
    
    second << "P3" << endl << dimy << " " << dimx << endl << "1" << endl;
    for(int i = 0; i < dimx; i++)
    {
        for(int j = 0; j < dimy; j++)
        {
            if(output[i][j] == 0)
            {
                second << 0 << " " << 0 << " " << 0 << endl;

            }
            else if(output[i][j] == 2)
            {
                second << 1 << " " << 1 << " " << 1 << endl;

            }
            else
            {
                second << 0 << " " << 0 << " " << 0 << endl;
            }
        }
    }
    // cout << count1 << " " << count2 << endl;


    //for eachi
    //for each j
    // if the pixel in threshold[i][j] == 2, recursive call for that pixel
}

void part1()
{
    
    string** image = run_input();

    double grayscale[dimx][dimy];
    for(int i = 0; i < dimx; i++)
    {
        for(int j = 0; j < dimy; j++)
        {
            grayscale[i][j] = stoi(image[i][j]);
        }
    }



    vector<double> x_direc;
    x_direc.push_back(-1.0); x_direc.push_back(0.0); x_direc.push_back(1.0); x_direc.push_back(-2.0); x_direc.push_back(0.0);
    x_direc.push_back(2.0); x_direc.push_back(-1.0); x_direc.push_back(0.0); x_direc.push_back(1.0); 
    vector<double> y_direc;
    y_direc.push_back(-1.0); y_direc.push_back(-2.0); y_direc.push_back(-1.0); y_direc.push_back(0.0); y_direc.push_back(0.0);
    y_direc.push_back(0.0); y_direc.push_back(1.0); y_direc.push_back(2.0); y_direc.push_back(1.0);
    double mag[dimx][dimy];
    for(int i = 0; i < dimx; i++)
    {
        mag[i][0] = 0;
        mag[i][dimy-1] = 0;
    }
    for(int i = 0; i < dimy; i++)
    {
        mag[0][i] = 0;
        mag[dimx-1][i] = 0;
    }

    for(int i = 1; i < dimx-1; i++)
    {
        for(int j = 1; j < dimy-1; j++)
        {
            vector<double> temp;

            for(int b = j-1; b <= j+1; b++)
            {
                for(int a = i-1; a <= i+1; a++)
                {
                    temp.push_back(grayscale[a][b]);
                }
            }

            // cout << temp.size() << x_direc.size() << y_direc.size() << endl;
            mag[i][j] = sqrt(pow(dot_product(temp, x_direc), 2) + pow(dot_product(temp, y_direc), 2));
           
        }
    }

    double threshold = 150;


    edge << "P3" << endl << dimy << " " << dimx << endl << "1" << endl;

    for(int i = 0; i < dimx; i++)
    {
        for(int j = 0; j < dimy; j++)
        {
            // edge << 1 << " " << 1 << " "  << 1 << " " << endl;
            // edge << 255 << " " << 255 << " " << 255 << " " << endl;
            if(mag[i][j] < threshold)
            {
                edge << 0 << " " << 0 << " "  << 0 << " " << endl;
                // count1++;
            }
            else 
            {
                edge << 1 << " " << 1 << " "  << 1 << " " << endl;
                // count2++;
            }

        }
    }
    // cout << count1 << " " << count2 << endl;
    // cout << dimy * dimx << endl;

    // for(int j = dimy-1; j > -1; j--)
    // {
    //     for(int i = 0; i < dimx; i++)
    //     {
    //         edge << output[i][j] << " " << output[i][j] << " " << output[i][j] << " " << endl;
    //     }
    // }
    

}

int main()
{
    // part1();
    part2();
    return 0;
}