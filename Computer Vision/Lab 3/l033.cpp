//Kingsley Kim
#include <iostream>
#include <random>
#include <fstream>
#include <tuple>
#include <iomanip>
#include <cmath>
#include <string>
#include <algorithm>
#include <list>
#include <chrono>
#include <vector>
using namespace std; 

ofstream res("results.txt");
ofstream ppmout("points.ppm");
const int dimx = 800, dimy = 800;
static string image[dimx][dimy];
void set_pixel(int x, int y, string color)
{
    image[x][y] = color;
    
}


class Point{ //Point class for easier access
    private:
        double x_coord;
        double y_coord;
       
    public:
        Point() { x_coord = 0.0; y_coord = 0.0;}
        Point(double x, double y) { x_coord = x; y_coord = y;}
        double  getX() { return x_coord; }
        double getY() { return y_coord; }
        
        void setX(double x) { x_coord = x;}
        void setY(double y) {y_coord = y; }
        void print() { cout << "(" << x_coord << "," << y_coord << ")" << endl; }
        void printout() {res << setprecision(23); res << "(" << x_coord << "," << y_coord << ")" << endl;}
        void copy(Point a) {setX(a.getX()); setY(a.getY()); } //copying the contents of a 


};

double find_distance(Point a, Point b)
{
    return sqrt(pow((b.getX()-a.getX()), 2) + pow((b.getY()-a.getY()), 2));
}
class DoublePoint{
    private:
        Point one;
        Point two;
        double dist;
    public:
        DoublePoint() { one = Point(); two = Point(); dist = 0;}
        DoublePoint(Point x, Point y) { one = x; two = y; dist = find_distance(one, two);}
        double getDist() { return dist; }
        Point getFirst() { return one;}
        Point getSecond() { return two; }
        void print() { one.print(); cout << " "; two.print(); cout << endl; }
        void printout() {one.printout(); two.printout();}
};

void draw_circle(double radius, Point center, string color) //
{
    int x, y, xmax, y2, y2_new, ty;
    xmax = (int)(radius * 0.70710678);
    y = (int)(radius);
    y2 = y * y;
    ty = (2*y) - 1;
    y2_new = y2;

    int x_coord = (int)(center.getX() * dimx);
    int y_coord = (int)(center.getY() * dimx);
    
    for(x = 0; x <= xmax; x++)
    {
        if((y2 - y2_new) >= ty){
            y2 -= ty;
            y -= 1;
            ty -= 2;
        }
        if(x_coord + x < dimx && y_coord + y < dimy) {set_pixel(x_coord + x, y_coord + y, color);}
        if(x_coord + x < dimx && y_coord - y > 0) {set_pixel(x_coord + x, y_coord - y, color);}
        if(x_coord - x > 0 && y_coord + y < dimy) {set_pixel(x_coord - x, y_coord + y, color);}
        if(x_coord - x > 0 && y_coord - y > 0) {set_pixel(x_coord- x, y_coord - y, color);}
        if(x_coord + y < dimy && y_coord + x < dimx) {set_pixel(x_coord + y, y_coord + x, color);}
        if(x_coord + y < dimx && y_coord- x > 0) {set_pixel(x_coord + y, y_coord - x, color); }
        if(x_coord - y > 0 && y_coord + x < dimy) {set_pixel(x_coord - y, y_coord + x, color);}
        if(x_coord - y > 0 && y_coord - x > 0) {set_pixel(x_coord - y, y_coord - x, color);}
        
        y2_new -= (2*x) - 3;
        
    }


}

Point random_point()
{
    random_device rd;
    default_random_engine generator(rd());
    uniform_real_distribution<double> distribution(0, 1.0);
    return Point(distribution(generator), distribution(generator));
}
void lineFromPoints(Point A, Point B, double &a, double &b, double &c){
   a = B.getY() - A.getY();
   b = A.getX() - B.getX();
   c = a*(A.getX())+ b*(A.getY());
}
void setupPPM()
{
    ppmout << "P3" << endl << dimx << " " << dimy << endl << "256" << endl;
    
    for(int j = dimy-1; j > -1; j--)
    {
        for(int i = 0; i < dimx; i++)
        { 
            
            ppmout << image[i][j].substr(0, 3) << " " << image[i][j].substr(3, 6) << " " << image[i][j].substr(6, 9) << " " << endl;}
        }
    ppmout.close();
}

list<Point> input_list()
{
    ofstream out("points.txt");
    for(int j = 0; j < dimy; j++)
    {
        for(int i = 0; i < dimx; i++)
        {
            image[i][j] = "256256256";
        }
    }
    list<Point> points;
    for(int i = 0; i < 100000; i++)
    {
        Point p = random_point();
        points.push_back(p);
    }
    out << fixed;
    out << setprecision(23);

    for(list<Point>::iterator it = points.begin(); it != points.end(); it++)
    {
        
        out << (*it).getX() << "  " << (*it).getY() << endl;
        draw_circle(3, (*it), "000000000"); //draw initial black circles
    }
    return points;
}
vector<Point> input_vector()
{
    ifstream in("points.txt");
    for(int j = 0; j < dimy; j++)
    {
        for(int i = 0; i < dimx; i++)
        {
            image[i][j] = "256256256";
        }
    }
    vector<Point> points;
    double x, y;
    while(in >> x >> y)
    {
        points.push_back(Point(x, y));
    }
    int len = points.size();
    for(int i = 0; i < len; i++)
    {
        draw_circle(3, points[i], "000000000"); //draw initial black circles
    }
    return points;
}
double part1()

{
    list<Point> points = input_list();
    pair<Point, Point> min = make_pair(Point(), Point());
    double temp = 0; double m = 10;
    chrono::high_resolution_clock::time_point begin = chrono::high_resolution_clock::now();
    for(list<Point>::iterator i = points.begin(); i != points.end(); i++)
    {
        for(list<Point>::iterator j = i; j != points.end(); j++)
        {
            if(j == i) {continue;}
            else { 
                temp = find_distance(*i, *j);
                if(m > temp)
                {
                    m = temp;
                    min = make_pair(*i, *j);
                }
            }
        }
    }
    chrono::high_resolution_clock::time_point end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = chrono::duration_cast<chrono::milliseconds>(end - begin);
    Point one = min.first; Point two = min.second;
    res << "First Run" << endl;
    one.printout(); two.printout(); res << "Distance: " << find_distance(one, two) << endl;
    draw_circle(2, one, "256000000"); draw_circle(3, one, "256000000"); draw_circle(2, two, "256000000"); draw_circle(3, two, "256000000");
    setupPPM();
    return elapsed.count();
    

    //now, need to draw the red circle for smallest

}
bool cmp(Point x, Point y)
{
    return (x.getX() < y.getX());
}
bool cmp2(Point x, Point y)
{
    return (x.getY() < y.getY());
}
DoublePoint findMin(vector<Point> wide, double d, DoublePoint minpoint, vector<Point> vec, string tag)
{
    double min = d;
    sort(wide.begin(), wide.end(), cmp2);
    DoublePoint minpointcopy = minpoint;
    int len = wide.size();
    if(tag == "2")
    {for(int i = 0; i < len; i++)
    {
        for(int j = i+1; j < len && (wide[j].getY() - wide[i].getY()) < min; j++)
        {
            if(find_distance(wide[i], wide[j]) < minpointcopy.getDist())
            {
                minpointcopy = DoublePoint(wide[i], wide[j]);
            }
        }
    }}
    else if(tag == "3")
    {
        for(int i = 0; i < len; i++)
        {
            for(int j = i+1; j < i + 8 && j < len; j++)
            {
                if(find_distance(wide[i], wide[j]) < minpointcopy.getDist())
                {
                    minpointcopy = DoublePoint(wide[i], wide[j]);
                }
            }
        }

    }

    return minpointcopy;
}

DoublePoint ms(vector<Point> vec, int s, int e, string tag)
{
    
    if(e - s == 2) {   return DoublePoint(vec[0], vec[1]); }
    else if(e - s == 3) { 
        double temp = 0; double m = 10;
        DoublePoint dp = DoublePoint();
        for(int i = s; i < e; i++)
        {
            for(int j = s; j < e; j++)
            {
                if(j == i) {continue; }
                temp = find_distance(vec[i], vec[j]);
                if(m > temp) 
                {
                    m = temp;
                    dp = DoublePoint(vec[i], vec[j]);
                }
            }
        }
        return dp;
    }
    else 
    {
        int mid = (s + e) / 2;
        DoublePoint left = ms(vec, s, mid, tag);
        DoublePoint right = ms(vec, mid, e, tag);
        // left.print(); cout << left.getDist() << endl;
        DoublePoint min = DoublePoint();
        //zipper merge
        double d = 0;
        if(left.getDist() <= right.getDist()){ d = left.getDist(); min = left; }
        else { d = right.getDist(); min = right;}

        // int left_track, right_track = mid;
        vector<Point> wide;
        for(int i = s; i < e; i++)
        {
            if(abs(vec[i].getX() - vec[mid].getX()) < d)
                wide.push_back(vec[i]);
        }
        
        return findMin(wide, d, min, vec, tag);

    }
}

double part2()
{
    vector<Point> points = input_vector();
    chrono::high_resolution_clock::time_point begin = chrono::high_resolution_clock::now();
    sort(points.begin(), points.end(), cmp);
    DoublePoint min = ms(points, 0, points.size(), "2");
    chrono::high_resolution_clock::time_point end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = chrono::duration_cast<chrono::milliseconds>(end - begin);
    res << "Part 2" << endl;
    min.printout();
    res << "Distance: " << min.getDist() << endl;
    draw_circle(3, min.getFirst(), "256000000"); draw_circle(2, min.getFirst(), "256000000");
    draw_circle(3, min.getSecond(), "256000000"); draw_circle(2, min.getSecond(), "256000000");  
    setupPPM();
    return elapsed.count();
    
}
double part3()
{
    vector<Point> points = input_vector();
    chrono::high_resolution_clock::time_point begin = chrono::high_resolution_clock::now();
    sort(points.begin(), points.end(), cmp);
    DoublePoint min = ms(points, 0, points.size(), "3");
    chrono::high_resolution_clock::time_point end = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = chrono::duration_cast<chrono::milliseconds>(end - begin);
    res << "Part 3" << endl;
    min.printout();
    res << "Distance :" << min.getDist() << endl;
    draw_circle(3, min.getFirst(), "256000000"); draw_circle(2, min.getFirst(), "256000000");
    draw_circle(3, min.getSecond(), "256000000"); draw_circle(2, min.getSecond(), "256000000");

    return elapsed.count();  
}
//use mergesort for part 2 for faster algo
//ms(arr, se)
//if length(<=1) return;
//mid = s+e/2;
//ms(arr, s, mid)
//ms(arr, mid+1, e)
//zipper merge
//make a class that takes in two points and records a distance
//Notes: use vectors instead of arrays, use only 1 vector, read from points.txt
//1. Sort vector based on the x-coordinate, call sort method 
//2. recursivity, find point in the middle, divide vector half from mid, code for case where length is even and odd
//3. Base cases, 2 points: min distance = distance between two points, 3 points: calculate three distances and find the min
//4. One side will return a (dist, p1, p2), and the other side will return another set of distance and closest points, 
//for each time the method is called
//5. Find which of the pairs is the minimum, get the d and then draw strips d wide from the middle point, length 2d, so all points outside this strip hsould not be calculated for distance
//6. In the strip, there could be points in the strip between the sides that weren't calculated before, so need to find the distances between those to see if they're smaller. 
//7. To avoid recalculating distances on one side of the strip, only calculate distance pairs between ponits on left and right, and update min distance if less than
//8. 

//Part 3 (Modified Version of Part 2)
//In a strip of d, we know that a box of width d/2 must have at most one point
//Since we need to find minimum distance, we need to check boxes in a 4x4 area of d/2 boxes around the point, so checking 15 boxes
//But realistically, you're only checking the other side of the strip each time
//Algorithm:
//Create a new vector for the strip and sort by 'Y'
//For each p1 in the strip:
// For each p2 in next 15 points
//     find_distance(p1, p2) compare to d, and update d & points if needed
// scp -P 22 points1m.txt username@remote.tjhsst.edu:/cluster/username 
int main()
{
    double elapsed2 = part2();
    res << "Runtime: " << elapsed2 << " milliseconds" << endl;
    double elapsed3 = part3();
    res << "Runtime: " << elapsed3 << " milliseconds" << endl;
    res.close();
    return 0;

}