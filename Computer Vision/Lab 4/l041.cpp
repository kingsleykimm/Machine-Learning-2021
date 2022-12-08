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
#include <set>
#include <unordered_map>
using namespace std; 




ofstream ppmout("convex.ppm");
const int dimx = 400, dimy = 400;
static string image[dimx][dimy];
void set_pixel(int x, int y, string color)
{
    image[x][y] = color;
    
}



class Point{ //Point class for easier access
    private: 
    public:
        double x_coord;
        double y_coord;
        Point() { x_coord = 0.0; y_coord = 0.0;}
        Point(double x, double y) { x_coord = x; y_coord = y;}
        double  getX() { return x_coord; }
        double getY() { return y_coord; }
        
        void setX(double x) { x_coord = x;}
        void setY(double y) {y_coord = y; }
        void print() { cout << "(" << x_coord << "," << y_coord << ")" << endl; }
        // void printout() {res << setprecision(23); res << "(" << x_coord << "," << y_coord << ")" << endl;}
        void copy(Point a) {setX(a.getX()); setY(a.getY()); } //copying the contents of a 
        bool operator<(const Point& pt) const 
        {
        return (x_coord < pt.x_coord || (y_coord <= pt.y_coord));  //assume that you compare the record based on a
        }

};
void printSet(set<Point> s)
{
    set<Point>::iterator it = s.begin();
    while(it != s.end())
    {
        Point p = *it;
        p.print();
    }
}
double find_distance(Point a, Point b)
{
    return sqrt(pow((b.getX()-a.getX()), 2) + pow((b.getY()-a.getY()), 2));
}
class Line{
    private:
        Point start;
        Point end;
        double a, b, c;
    public:
        Line() {start = Point(); end = Point(); }
        Line(Point s, Point e) { start = s; end = e; cvrtStandard(); }
        Line(Point s, double slope) {  a = (-1.0) * slope; b = 1; c = (-1.0) * slope * s.getX() + s.getY(); } //point slope form constructor 
        void cvrtStandard() { a = -getSlope(); b = 1; c = -getSlope() * start.getX() + start.getY(); }
        Point getStart() { return start; }
        Point getEnd() { return end;}
        double geta() { return a; }
        double getb() { return b; }
        double getc() { return c; }
        double getSlope() { return (end.getY() - start.getY()) / (end.getX() - start.getX());}
        void lineFromPoints(double &a, double &b, double &c){
                a = start.getY() - end.getY();
                b = end.getX() - start.getX();
                c = start.getX() * end.getY() - end.getX() * start.getY(); }
        double getLength() { return find_distance(start, end); }
        double getperpSlope() {return -1.0 / (getSlope()); }
        void print() {start.print(); end.print(); }
        Point lineLineIntersection(double a2, double b2, double c2){ //find intersection between lines
            double det= a*b2 - a2*b;
            
            double x = (b2*c - b*c2)/det;
            double y = (a*c2 - a2*c)/det;
            if(x < 0) {x += 1.0;}
            if(y < 0) {y += 1.0;}
            return Point(x, y);
        
        }
        

        double evaluateX(double y)
        {
            
            return (c - b * y) / a;
        }
        double evaluateY(double x)
        {
            
            return (c - a * x) / b;
        }
        
        void lineExtended(string color)
        {
            //cases: where the line extends past the left and right sides, or past the top and bottom sides 

            if(getSlope() > 0)
            {
                if(evaluateX(0) < 0)
                {
                    if(evaluateY(1) > 1)
                    {
                        double left_int = evaluateY(0);
                        double top_int = evaluateX(1);
                        Line temp = Line(Point(0, left_int), Point(top_int, 1));
                        temp.drawLine(color);
                    }
                    else if(evaluateX(1) > 1)
                    {
                        double left_int = evaluateY(0);
                        double right_int = evaluateY(1);
                        Line temp = Line(Point(0, left_int), Point(1, right_int));
                        temp.drawLine(color);
                    }
                }
                else if(evaluateY(0) < 0)
                {
                    if(evaluateY(1) > 1)
                    {
                        double bot_int = evaluateX(0);
                        double top_int = evaluateX(1);
                        Line temp = Line(Point(bot_int, 0), Point(top_int, 1));
                        temp.drawLine(color);
                    }
                    else if(evaluateX(1) > 1)
                    {
                        double bot_int = evaluateX(0);
                        double right_int = evaluateY(1);
                        Line temp = Line(Point(bot_int, 0), Point(1, right_int));
                        temp.drawLine(color);
                    }
                }

            }
            else 
            {
                if(evaluateX(0) > 1)
                {
                    if(evaluateY(0) > 1)
                    {
                        double top_int = evaluateX(1);
                        double right_int = evaluateY(1);
                        Line temp = Line(Point(top_int, 1), Point(1, right_int));
                        temp.drawLine(color);
                    }
                    else if(evaluateX(1) < 0)
                    {
                        double left_int = evaluateY(0);
                        double right_int = evaluateY(1);
                        Line temp = Line(Point(0, left_int), Point(1, right_int));
                        temp.drawLine(color);
                    }
                }
                else if(evaluateY(1) < 0)
                {
                    if(evaluateY(0) > 1)
                    {
                        double top_int = evaluateX(1);
                        double bottom_int = evaluateX(0);
                        Line temp = Line(Point(top_int, 1), Point(bottom_int, 0));
                        temp.drawLine(color);
                    }
                    else if(evaluateX(1) < 0)
                    {
                        double bottom_int = evaluateX(0);
                        double left_int = evaluateY(0);
                        Line temp = Line(Point(0, left_int), Point(bottom_int, 0));
                        temp.drawLine(color);
                    }
                }
            }


        }
        void drawLine(string color) //rasterized algorithim
        {
            
            int x_1 = (int)(start.getX() * dimx); int y_1 = (int)(start.getY()* dimy);
            int x_2 = (int)(end.getX() * dimx); int y_2 = (int)(end.getY() * dimy);
            int stepx, stepy;
            int dx = x_2 - x_1;
            int dy = y_2 - y_1;
            if(dy < 0) { dy = -dy; stepy = -1;} else{ stepy = 1;}
            if (dx < 0) { dx = -dx; stepx = -1; } else {stepx = 1; }
            dx *= 2; dy *= 2;
            
            if((0 <= x_1) && (x_1 < dimx) && (0 <= y_1) && (y_1 < dimy)) {set_pixel(x_1, y_1, color);}   
            if(dx > dy)
            {
                int frac = dy - (dx * 2);
                while(x_1 != x_2)
                {
                    x_1 += stepx;
                    if(frac >= 0){
                        y_1 += stepy;
                        frac -= dx;
                    }
                    frac += dy;
                    if((0 <= x_1) && (x_1 < dimx) && (0 <= y_1) && (y_1 < dimy)) {set_pixel(x_1, y_1, color);}
                }
            } 
            else
            {
                int frac = dx - 2 * dy;
                while(y_1 != y_2)
                {
                    if(frac >= 0)
                    {
                        x_1 += stepx;
                        frac -= dy;
                    }
                    y_1 += stepy;
                    frac += dx;
                    if((0 <= x_1) && (x_1 < dimx) && (0 <= y_1) && (y_1 < dimy)) {set_pixel(x_1, y_1, color);}
                }
            }
            
        }
        
};


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
        // void printout() {one.printout(); two.printout();}
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

vector<Point> input_list()
{
    ofstream out("points.txt");
    for(int j = 0; j < dimy; j++)
    {
        for(int i = 0; i < dimx; i++)
        {
            image[i][j] = "256256256";
        }
    }
    vector<Point> points;
    for(int i = 0; i < 60; i++)
    {
        Point p = random_point();
        points.push_back(p);

    }
    out << fixed;
    out << setprecision(23);

    for(vector<Point>::iterator it = points.begin(); it != points.end(); it++)
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

bool cmp(Point x, Point y)
{
    return (x.getX() < y.getX());
}
bool cmp2(Point x, Point y)
{
    return (x.getY() < y.getY());
}

bool in_triangle(Point a, Point b, Point c, Point d) //first three points are the triangle, Point D is the one we're testing
{
    double A, B, C;
    Line ab = Line(a, b);
    ab.lineFromPoints(A, B, C);
    double D, E, F;
    Line bc = Line(b, c);
    bc.lineFromPoints(D, E, F);
    double G, H, I;
    Line ca = Line(c, a);
    ca.lineFromPoints(G, H, I);

    //we want the points to have the same sign 
    //test for AB, means that points c and d will be tested
    double diff = (C - A * c.getX()) / B - c.getY(); //the y on the line - y of the point 
    double diff1 = (C - A * d.getX()) / B - d.getY();
    if ((diff >= 0) ^ (diff1 >= 0)) { return false;} //if they're different from each other, it will return false. If the statements are identical, will continue. 
    //Thus, if one is positive, and the other isn't positive, will return false.
    //test for BC, means that the points a, d will be tested
    double diff2 = (F - D * a.getX()) / E - a.getY();
    double diff3 = (F - D * d.getX()) / E - d.getY();
    if((diff2 >= 0) ^ (diff3 >= 0)) { return false; }
    //test for CA, means that the points b, d
    double diff4 = (I - G * b.getX()) / H - b.getY();
    double diff5 = (I - G * d.getX()) / H - d.getY();
    if((diff4 >= 0) ^ (diff5 >= 0)) { return false; }

    return true;
}
vector<Point> allonRight(vector<Point> pts, Point a, Point b) // directed lien: a to b
{
    int len = pts.size();
    vector<Point> ret;
    for(int i = 0; i < len; i++)
    {
        double position = (b.x_coord - a.x_coord) * (pts[i].y_coord - a.y_coord) - (b.y_coord - a.y_coord) * (pts[i].x_coord - a.x_coord);
        // cout << directionOfPoint(a, b, pts[i]) << endl;
        if(position < 0)
        {
            ret.push_back(pts[i]);
        }
    }
    return ret;
}


double dist(Point a, Point b, Point c) //first two are the points that make up the line, c is the comparing point
{
    double A, B, C;
    Line ab = Line(a, b);
    ab.lineFromPoints(A, B, C);
    return abs(A*c.getX() + B*c.getY() + C) / sqrt(A*A+B*B);
}
void convex_hull(vector<Point> qh, vector<Point>& ch, Point a, Point b)
{
    if(qh.size() == 0)
    {
        return;
    }

    int len = qh.size();
    double max_dist = -1;
    Point max_point;

    for(int i = 0; i < len; i++)
    {
        if(dist(a, b, qh[i]) > max_dist)
        {
            max_dist = dist(a, b, qh[i]);
            max_point = qh[i];
        }
    }


    int index = 0;

    for(int i = 0; i < (int)ch.size(); i++)
    {
        if(ch[i].getX() == b.getX() && ch[i].getY() == b.getY())
            index = i;
    }
    ch.insert(ch.begin() + index, max_point);
    



    
    
    vector<Point> s1, s2;
    
    s1 = allonRight(qh, a, max_point);
    s2 = allonRight(qh, max_point, b); //problem here is that max point is still being registerd
    
    convex_hull(s1, ch, a, max_point);
    convex_hull(s2, ch, max_point, b);
    return;
}

void part1()
{
    vector<Point> pts = input_list();


    sort(pts.begin(), pts.end(), cmp2);
    Point min = pts[0];
    Point max = pts.back();
    vector<Point> s1 = allonRight(pts, max, min); //EG right
    vector<Point> s2 = allonRight(pts, min, max); //GE right
    vector<Point> ch;
    ch.push_back(max);
    ch.push_back(min);
    ch.push_back(max);
    //{E, G, E}
    convex_hull(s1, ch, max, min);
    convex_hull(s2, ch, min, max);

    for(int i = 0; i < (int)ch.size()-1; i++)
    {
        draw_circle(3, ch[i], "256000000");
        Line temp = Line(ch[i], ch[i+1]);
        temp.drawLine("256000000");
    }

    setupPPM();
    

}
int main()
{
    part1();
}