//Kingsley Kim
#include <iostream>
#include <random>
#include <fstream>
#include <tuple>
#include <cmath>

#include <vector>
using namespace std;
ofstream out("triangle.ppm");
const int dimx = 800, dimy = 800;
// static int(*image)[dimx] = new int[dimx][dimy];
static int image[dimx][dimy];
class Point{ //Point class for easier access
    private:
        int x_coord;
        int y_coord;
    public:
        Point(int x, int y) { x_coord = x; y_coord = y;}
        int getX() { return x_coord; }
        int getY() { return y_coord; }
};
int set_pixel(int x, int y)
{
    image[x][y] = 1;
    return 0;
}
int draw_circle(double radius, Point center)
{
    int x, y, xmax, y2, y2_new, ty;
    xmax = (int)(radius * 0.70710678);
    y = (int)(radius);
    y2 = y * y;
    ty = (2*y) - 1;
    y2_new = y2;
    for(x = 0; x <= xmax; x++)
    {
        if((y2 - y2_new) >= ty){
            y2 -= ty;
            y -= 1;
            ty -= 2;
        }
        if(center.getX() + x < dimx && center.getY() + y < dimy) {set_pixel(center.getX() + x, center.getY() + y);}
        if(center.getX() + x < dimx && center.getY() - y > 0) {set_pixel(center.getX() + x, center.getY() - y);}
        if(center.getX() - x > 0 && center.getY() + y < dimy) {set_pixel(center.getX() - x, center.getY() + y);}
        if(center.getX() - x > 0 && center.getY() - y > 0) {set_pixel(center.getX() - x, center.getY() - y);}
        if(center.getX() + y < dimy && center.getY() + x < dimx) {set_pixel(center.getX() + y, center.getY() + x);}
        if(center.getX() + y < dimx && center.getY() - x > 0) {set_pixel(center.getX() + y, center.getY() - x); }
        if(center.getX() - y > 0 && center.getY() + x < dimy) {set_pixel(center.getX() - y, center.getY() + x);}
        if(center.getX() - y > 0 && center.getY() - x > 0) {set_pixel(center.getX() - y, center.getY() - x);}
        
        y2_new -= (2*x) - 3;
        
    }

    return 0;
}
Point find_ninecenter(Point x, Point y, Point z)
{
    return Point((x.getX() + y.getX() + z.getX())/3, (x.getY() + y.getY() + z.getY())/3);
}
Point find_orthocenter(Point cc, Point cen)
{
    return Point(3 * cen.getX() - 2 * cc.getX(), 3* cen.getY() - 2 * cc.getY());
}
void lineFromPoints(Point A, Point B, double &a, double &b, double &c){
   a = B.getY() - A.getY();
   b = A.getX() - B.getX();
   c = a*(A.getX())+ b*(A.getY());
}
void perpendicularBisectorFromLine(Point A, Point B, double &a, double &b, double &c){
   Point mid_point = Point((A.getX() + B.getX())/2, (A.getY() + B.getY())/2);
   c = -b*(mid_point.getX()) + a*(mid_point.getY());
   double temp = a;
   a = -b;
   b = temp;
}
Point lineLineIntersection(double a1, double b1, double c1, double a2, double b2, double c2){ //find intersection between lines
   double det= a1*b2 - a2*b1;
   {
      double x = (b2*c1 - b1*c2)/det;
      double y = (a1*c2 - a2*c1)/det;
      if(x < 0) {x += 800;}
      if(y < 0) {y += 800;}
      return Point(x, y);
   }
}
Point findCircumCenter(Point A, Point B, Point C){
   double a, b, c;
   lineFromPoints(A, B, a, b, c);
   double e, f, g;
   lineFromPoints(B, C, e, f, g);
   perpendicularBisectorFromLine(A, B, a, b, c);
   perpendicularBisectorFromLine(B, C, e, f, g);
   return lineLineIntersection(a, b, c, e, f, g);
}

Point find_incenter(Point A, Point B, Point C, double a, double b, double c)
{
    int finx = (int) (b * A.getX() + c * B.getX() + a * C.getX()) / (a + b + c);
    int finy = (int) (b * A.getY() + c * B.getY() + a * C.getY()) / (a + b + c);
    if(finx < 0) {finx = 800 + finx;}
    if(finy < 0) {finy += 800;}
    return Point(finx, finy);
}
double find_distance(int x1, int y1, int x2, int y2)
{
    return sqrt(pow((x2-x1), 2) + pow((y2-y1), 2));
}

void bresenham(int x_1, int y_1, int x_2, int y_2) //bresenham's algorithim
{ 
    int delta_x = x_2 - x_1;
    int delta_y = y_2 - y_1;
    double m = delta_y / (double) delta_x;
    if(m > 0)
    {
        if(y_2 > y_1)
        {
            if(delta_x >= delta_y)
            {
                int j = y_1;
                int ep = delta_y - delta_x;
                for(int i = x_1; i < x_2; i++)
                {
                    set_pixel(i, j);
                    if(ep >= 0)
                    {
                    j += 1;
                    ep -= delta_x;
                    }  
                    ep += delta_y;
                }
            }
            else 
            {
                
                int j = x_1;
                int ep = delta_y - delta_x;
                for(int i = y_1; i < y_2; i++)
                {
                    set_pixel(j , i);
                    if(ep >= 0)
                    {
                    j += 1;
                    ep -= delta_y;

                    }
                        
                    ep += delta_x;
                }
                
            }
            
        }
        else
        {
            if(delta_x >= delta_y)
            {
                int j = y_2;
                int ep = delta_y - delta_x;
                for(int i = x_2; i < x_1; i++)
                {
                    set_pixel(i, j);
                    if(ep >= 0)
                    {
                    j += 1;
                    ep -= delta_x;

                    }
                        
                    ep += delta_y;
                }
            }
            else
            {
                int j = x_2;
                int ep = delta_y - delta_x;
                for(int i = y_2; i < y_1; i++)
                {
                    set_pixel(j , i);
                    if(ep >= 0)
                    {
                    j += 1;
                    ep -= delta_y;

                    }
                        
                    ep += delta_x;
                }
            }
        }        
    }

    else
    {
        delta_x = abs(x_2 - x_1);
        delta_y = abs(y_2 - y_1);
        if(y_1 > y_2)
        {
            if(delta_x >= delta_y)
            {
                int j = y_1;
                int ep = delta_y - delta_x;
                for(int i = x_1; i < x_2; i++)
                {
                    set_pixel(i, j);
                    if(ep >= 0)
                    {
                        j -= 1;
                        ep -= delta_x;
                    }
                    ep += delta_y;
                }
            }
            else
            {
                int j = x_1;
                int ep = delta_x - delta_y;
                for(int i = y_1; i > y_2; i--)
                {
                    set_pixel(j, i);
                    if(ep >= 0)
                    {
                        j += 1;
                        ep -= delta_y;
                    }
                    ep += delta_x;
                }
            }
        }
        else
        {
            if(delta_x >= delta_y)
            {
                int j = y_2;
                int ep = delta_y - delta_x;
                for(int i = x_2; i < x_1; i++)
                {
                    set_pixel(i, j);
                    if(ep >= 0)
                    {
                        j -= 1;
                        ep -= delta_x;
                    }
                    ep += delta_y;
                }
            }
            else
            {
                int j = x_2;
                int ep = delta_x - delta_y;
                for(int i = y_2; i > y_1; i--)
                {
                    set_pixel(j, i);
                    if(ep >= 0)
                    {
                        j += 1;
                        ep -= delta_y;
                    }
                    ep += delta_x;
                }
            }
        }
    }
    
    
    
    

}
void bresenham_neg(int x_1, int y_1, int x_2, int y_2) //modified bresenham for negative slope 
{
    int delta_x = abs(x_2 - x_1);
    int delta_y = abs(y_2 - y_1);
    if(delta_x >= delta_y)
    {
        int j = y_1;
        int ep = delta_y - delta_x;
        for(int i = x_1; i < x_2; i++)
        {
            set_pixel(i, j);
            if(ep >= 0)
            {
                j -= 1;
                ep -= delta_x;
            }
            ep += delta_y;
        }
    }
    else
    {
        int j = x_1;
        int ep = delta_x - delta_y;
        for(int i = y_1; i > y_2; i--)
        {
            set_pixel(j, i);
            if(ep >= 0)
            {
                j += 1;
                ep -= delta_y;
            }
            ep += delta_x;
        }
    }
}

void draw_euler(Point oc, Point cc)
{
    double slope = (double)(oc.getY() - cc.getY()) / (oc.getX() - cc.getX());
    double intercept = oc.getY() - slope * oc.getX();
    int top_intercept = (int)((800 - intercept) / slope);
    int bottom_intercept = (int)(-intercept / slope);
    if(slope > 0) 
    {bresenham(bottom_intercept, 0, top_intercept, 800);}
    else { bresenham_neg(top_intercept, 800, bottom_intercept, 0);}
}
    
    // else if(delta_y > delta_x)
    // {
    //     float m = delta_x / delta_y;
    //     int i = x_1;
    //     float ep = m-1;
    //     for(int j = y_1; j < y_2; j++)
    //     {
    //         set_pixel(i, j);
    //         if(ep >= 0)
    //         {
    //             i += 1; ep -= 1.0;
    //         }
            
    //         ep += m;
    //     }
    // }


int main()
{
    
    out << "P3" << endl << dimx << " " << dimy << endl << "1" << endl;

    int a, b, c, d, e, f;
    random_device rd;
    
    default_random_engine generator(rd());
    uniform_real_distribution<double> distribution(0, 1.0);
    for(int i = 0; i < dimx; i++)
    {
        for(int j = 0; j < dimy; j++)
        {
            
            image[i][j] = 0;
        }
    }
    //two random points
    a = (int)(distribution(generator) * 200);
    b = (int)(distribution(generator) * 200);
    c = (int)(distribution(generator) * 100) + 400;
    d = (int)(distribution(generator) * 100) + 200;
    e = (int)(distribution(generator)*50) + 300;
    f = (int)(distribution(generator)*50) + 300;
    image[a][b] = 1; image[c][d] = 1; image[e][f] = 1;
    bresenham(a, b, c, d); bresenham_neg(e, f, c, d); bresenham(a, b, e, f);
    // cout << a << " " << b << " " << c << " " << d << " " << e << " " << f << endl;
    double x = find_distance(a, b, c, d); double y = find_distance(c, d, e, f); double z = find_distance(e, f, a, b); // x = AB, y = BC, z = CA
    double semi = 0.5 * (x + y + z);
    double in_r = sqrt(((semi-x) * (semi - y) * (semi - z)) / (semi));
    double circum_r =(x * y * z) / ( 4 * in_r * semi);
    double nine_r = circum_r / 2; 
    Point one = Point(a, b);
    Point two = Point(c, d);
    Point three = Point(e, f);
    Point circumcenter = findCircumCenter(one, two, three);
    Point incenter = find_incenter(one, two, three, x, y, z);
    Point ninecenter = find_ninecenter(one, two, three); 
    Point orthocenter = find_orthocenter(circumcenter, ninecenter);
    // cout << orthocenter.getX() << " " << orthocenter.getY() << " " << circumcenter.getX() << " " << circumcenter.getY() << endl;
    set_pixel(orthocenter.getX(), orthocenter.getY()); set_pixel(circumcenter.getX(), circumcenter.getY());
    draw_euler(orthocenter, circumcenter);
    draw_circle(in_r, incenter); draw_circle(circum_r, circumcenter); draw_circle(nine_r, ninecenter);
    draw_circle(4, Point(700, 700));
        for(int j = dimy-1; j > -1; j--)
        {
            for(int i = 0; i < dimx; i++)

            {out << image[i][j] << " " << image[i][j] << " " << image[i][j] << endl;}
        }
    
    out.close();
    return 0;
}

