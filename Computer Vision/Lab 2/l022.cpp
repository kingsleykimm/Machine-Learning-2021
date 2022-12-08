//Kingsley Kim
#include <iostream>
#include <random>
#include <fstream>
#include <tuple>
#include <iomanip>
#include <cmath>
#include <string>
#include <vector>
using namespace std; 
ofstream out("output.ppm");
ofstream pout("output.txt");
ifstream in("points.txt");
const int dimx = 800, dimy = 800;
static int image[dimx][dimy];
void set_pixel(int x, int y)
{
    image[x][y] = 0;
    
}

double find_distance(double x1, double y1, double x2, double y2)
{   

    double dist = sqrt(pow((x2-x1), 2) + pow((y2-y1), 2));

    return dist;
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

        void copy(Point a) {setX(a.getX()); setY(a.getY()); } //copying the contents of a 


};
void draw_circle(double radius, Point center) //
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
        if(x_coord + x < dimx && y_coord + y < dimy) {set_pixel(x_coord + x, y_coord + y);}
        if(x_coord + x < dimx && y_coord - y > 0) {set_pixel(x_coord + x, y_coord - y);}
        if(x_coord - x > 0 && y_coord + y < dimy) {set_pixel(x_coord - x, y_coord + y);}
        if(x_coord - x > 0 && y_coord - y > 0) {set_pixel(x_coord- x, y_coord - y);}
        if(x_coord + y < dimy && y_coord + x < dimx) {set_pixel(x_coord + y, y_coord + x);}
        if(x_coord + y < dimx && y_coord- x > 0) {set_pixel(x_coord + y, y_coord - x); }
        if(x_coord - y > 0 && y_coord + x < dimy) {set_pixel(x_coord - y, y_coord + x);}
        if(x_coord - y > 0 && y_coord - x > 0) {set_pixel(x_coord - y, y_coord - x);}
        
        y2_new -= (2*x) - 3;
        
    }


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
                a = end.getY() - start.getY();
                b = start.getX() - end.getX();
                c = a*(start.getX())+ b*(start.getY()); }
        double getLength() { return find_distance(start.getX(), start.getY(), end.getX(), end.getY()); }
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
        
        void lineExtended()
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
                        temp.drawLine();
                    }
                    else if(evaluateX(1) > 1)
                    {
                        double left_int = evaluateY(0);
                        double right_int = evaluateY(1);
                        Line temp = Line(Point(0, left_int), Point(1, right_int));
                        temp.drawLine();
                    }
                }
                else if(evaluateY(0) < 0)
                {
                    if(evaluateY(1) > 1)
                    {
                        double bot_int = evaluateX(0);
                        double top_int = evaluateX(1);
                        Line temp = Line(Point(bot_int, 0), Point(top_int, 1));
                        temp.drawLine();
                    }
                    else if(evaluateX(1) > 1)
                    {
                        double bot_int = evaluateX(0);
                        double right_int = evaluateY(1);
                        Line temp = Line(Point(bot_int, 0), Point(1, right_int));
                        temp.drawLine();
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
                        temp.drawLine();
                    }
                    else if(evaluateX(1) < 0)
                    {
                        double left_int = evaluateY(0);
                        double right_int = evaluateY(1);
                        Line temp = Line(Point(0, left_int), Point(1, right_int));
                        temp.drawLine();
                    }
                }
                else if(evaluateY(1) < 0)
                {
                    if(evaluateY(0) > 1)
                    {
                        double top_int = evaluateX(1);
                        double bottom_int = evaluateX(0);
                        Line temp = Line(Point(top_int, 1), Point(bottom_int, 0));
                        temp.drawLine();
                    }
                    else if(evaluateX(1) < 0)
                    {
                        double bottom_int = evaluateX(0);
                        double left_int = evaluateY(0);
                        Line temp = Line(Point(0, left_int), Point(bottom_int, 0));
                        temp.drawLine();
                    }
                }
            }


        }
        void drawLine() //rasterized algorithim
        {
            
            int x_1 = (int)(start.getX() * dimx); int y_1 = (int)(start.getY()* dimy);
            int x_2 = (int)(end.getX() * dimx); int y_2 = (int)(end.getY() * dimy);
            int stepx, stepy;
            int dx = x_2 - x_1;
            int dy = y_2 - y_1;
            if(dy < 0) { dy = -dy; stepy = -1;} else{ stepy = 1;}
            if (dx < 0) { dx = -dx; stepx = -1; } else {stepx = 1; }
            dx *= 2; dy *= 2;
            
            if((0 <= x_1) && (x_1 < dimx) && (0 <= y_1) && (y_1 < dimy)) {set_pixel(x_1, y_1);}   
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
                    if((0 <= x_1) && (x_1 < dimx) && (0 <= y_1) && (y_1 < dimy)) {set_pixel(x_1, y_1);}
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
                    if((0 <= x_1) && (x_1 < dimx) && (0 <= y_1) && (y_1 < dimy)) {set_pixel(x_1, y_1);}
                }
            }
            
        }
        
};
class Square{
    private:
        Point a, b, c, d;
        Line side;
    public:
        Square(Point a_con, Point b_con, Point c_con, Point d_con) {a = a_con; b = b_con; c = c_con; d = d_con; side = Line(a_con, b_con); }
        double getArea() { return side.getLength() * side.getLength();  }
        void draw() //lines extended
        {
            Line ab = Line(a, b); Line bc = Line(b, c); Line cd = Line(c, d); Line da = Line(d, a);
            ab.lineExtended(); bc.lineExtended(); cd.lineExtended(); da.lineExtended();
            // ab.drawLine(); bc.drawLine(); cd.drawLine(); da.drawLine();



        }
        vector<Point> getPoints() { vector<Point> ret; ret.push_back(a); ret.push_back(b); ret.push_back(c); ret.push_back(d); return ret;}
        void print() { a.print(); b.print(); c.print(); d.print();  }
};

Point random_point()
{
    random_device rd;
    default_random_engine generator(rd());
    uniform_real_distribution<float> distribution(0, 1.0);
    return Point(distribution(generator), distribution(generator));
}
void lineFromPoints(Point A, Point B, double &a, double &b, double &c){
   a = B.getY() - A.getY();
   b = A.getX() - B.getX();
   c = a*(A.getX())+ b*(A.getY());
}

bool in_triangle(Point a, Point b, Point c, Point d) //first three points are the triangle, Point D is the one we're testing
{
    double A, B, C;
    lineFromPoints(a, b, A, B, C); //AB
    double D, E, F;
    lineFromPoints(b, c, D, E, F); //BC
    double G, H, I;
    lineFromPoints(c, a, G, H, I); //CA
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
void part1()
{
    ofstream prout("points.txt");
    Point a = random_point();
    Point b = random_point();
    Point c = random_point();
    Point d = random_point();
    
    while(in_triangle(a, b, c, d) == true
            && in_triangle(d, b, c, a) == true
                && in_triangle(a, d, c, b) == true
                    && in_triangle(a, b, d, c) == true)
    {
        d = random_point();
    }
    prout << setprecision(17);
    
    prout << "(" << a.getX() << "," << a.getY() << ") ," << endl;
    prout << "(" << b.getX()<< "," << b.getY() << ") ," << endl;
    prout << "(" << c.getX() << "," << c.getY() << ") ," << endl;
    prout << "(" << d.getX() << "," << d.getY() << ")" << endl;
    prout.close();
}

Point read_input(string s)
{
    int len = s.length();
    vector<double> point;
    int i = 1; int j = 1;
    while(i < len - 1)
    {
        if(s[i] == '.')
        {
            string temp;
            while(s[j] != ',')
            {
                j++;
            }

            point.push_back(stod(s.substr(i-1, j)));
            j = i; 
        }
        i++;
    }

    return Point(point[0], point[1]);

}
Square first_case(Line ac, Point a, Point b, Point c, Point d)
{

    Point s1, s2, s3, s4, e;
    double length = ac.getLength();
    double perpSlope = ac.getperpSlope();
    double angle = atan(perpSlope);
    double delta_x = abs(length * cos(angle));
    double delta_y = abs(length * sin(angle));

    if (perpSlope > 0)
    {
        if(c.getY() < a.getY())
        {
            e.setX(b.getX() - delta_x);
            e.setY(b.getY() - delta_y); 
        }
        else
        {
            e.setX(b.getX() + delta_x);
            e.setY(b.getY() + delta_y);
        }
    }
    else
    {
        if(c.getY() < a.getY())
        {
            e.setX(b.getX() - delta_x);
            e.setY(b.getY() + delta_y);
        }
        else
        {
            e.setX(b.getX() + delta_x);
            e.setY(b.getY() - delta_y);
        }
    }
    Line de = Line(d, e);
    perpSlope = de.getperpSlope();
    Line c_line = Line(c, perpSlope);
    Line a_line = Line(a, perpSlope);
    Line b_line = Line(b, de.getSlope());
    s4 = de.lineLineIntersection(c_line.geta(), c_line.getb(), c_line.getc());
    s3 = de.lineLineIntersection(a_line.geta(), a_line.getb(), a_line.getc());
    s2 = a_line.lineLineIntersection(b_line.geta(), b_line.getb(), b_line.getc());
    s1 = c_line.lineLineIntersection(b_line.geta(), b_line.getb(), b_line.getc());

    return Square(s1, s2, s3, s4);
}
Square second_case(Line ac, Point a, Point b, Point c, Point d)
{
    Point e = Point(); 
    Point s1, s2, s3, s4;
    double length = ac.getLength();
    double perpSlope = ac.getperpSlope();
    double angle = atan(perpSlope);
    double delta_x = abs(length * cos(angle));
    double delta_y = abs(length * sin(angle));
    if (perpSlope > 0)
    {
        if(c.getY() < a.getY())
        {
            e.setX(b.getX() + delta_x);
            e.setY(b.getY() + delta_y); 
        }
        else
        {
            e.setX(b.getX() - delta_x);
            e.setY(b.getY() - delta_y);
        }
    }
    else
    {
        if(c.getY() < a.getY())
        {
            e.setX(b.getX() + delta_x);
            e.setY(b.getY() - delta_y);
        }
        else
        {
            e.setX(b.getX() - delta_x);
            e.setY(b.getY() + delta_y);
        }
    }
    Line de = Line(d, e);
    perpSlope = de.getperpSlope();
    Line c_line = Line(c, perpSlope);
    Line a_line = Line(a, perpSlope);
    Line b_line = Line(b, de.getSlope());
    s4 = de.lineLineIntersection(c_line.geta(), c_line.getb(), c_line.getc());
    s3 = de.lineLineIntersection(a_line.geta(), a_line.getb(), a_line.getc());
    s2 = a_line.lineLineIntersection(b_line.geta(), b_line.getb(), b_line.getc());
    s1 = c_line.lineLineIntersection(b_line.geta(), b_line.getb(), b_line.getc());
    return Square(s1, s2, s3, s4);

}
pair<Square, Square> find_squares(Point a, Point b, Point c, Point d)
{
    Line ac = Line(a, c); 

    Square sq1 = first_case(ac, a, b, c, d);
    Square sq2 = second_case(ac, a, b, c, d);
    return make_pair(sq1, sq2);
}
void setupPPM()
{
    out << "P3" << endl << dimx << " " << dimy << endl << "1" << endl;
    
    for(int j = 0; j < dimy; j++)
    {
        for(int i = 0; i < dimx; i++)

        { 
            
            out << image[i][j] << " " << image[i][j] << " " << image[i][j] << endl;}
    }
    out.close();
}
void setupOutput(vector<Point> points, vector<Square> squares)
{
    pout << setprecision(17);
    int len = points.size();
    for(int i = 0; i < len; i++)
    {
        if(i == len - 1)
        {
            pout << "(" << points[i].getX() << "," << points[i].getY() << ")" << endl;
        }
        else
        {pout << "(" << points[i].getX() << "," << points[i].getY() << ") , ";}
    }
    int len2 = squares.size();
    for(int i = 0; i < len2; i++)
    {
        vector<Point> points = squares[i].getPoints();
        for(int j = 0; j < len; j++)
        {
            if(j == len - 1)
            {
                pout << "(" << points[j].getX() << "," << points[j].getY() << ") Area = " << squares[i].getArea() << endl;
            }
            else
            {pout << "(" << points[j].getX() << "," << points[j].getY() << ") , ";}
        }
 
    }
}
int findMinArea(vector<Square> squares)
{
    double min = 10000; int index = 0; int len = squares.size();
    for(int i = 0; i < len; i++)
    {
        if(squares[i].getArea() < min)
        {
            min = squares[i].getArea();
            index = i;
        }
    }
    return index;
}

void draw_circles(vector<Point> points)
{
    int len = points.size();
    for(int i = 0; i < len; i++)
    {
        draw_circle(2, points[i]);
    }
}
void part2()
{
    string p1, p2, p3, p4, filler; 
    vector<Point> points; vector<Square> squares;
    in >> p1 >> filler >> p2 >> filler >> p3 >> filler >> p4;
   
    Point a = read_input(p1); points.push_back(a); 
    Point b = read_input(p2); points.push_back(b); 
    Point c = read_input(p3); points.push_back(c); 
    Point d = read_input(p4); points.push_back(d); 
    pair<Square, Square> sq1 = find_squares(a, b, c, d); squares.push_back(sq1.first); squares.push_back(sq1.second);
    pair<Square, Square> sq2 = find_squares(a, b, d, c); squares.push_back(sq2.first); squares.push_back(sq2.second);
    pair<Square, Square> sq3 = find_squares(a, c, b, d); squares.push_back(sq3.first); squares.push_back(sq3.second);
    for(int j = dimy-1; j > -1; j--)
    {
        for(int i = 0; i < dimx; i++)
        {
            image[i][j] = 1;
        }
    }  
    squares[findMinArea(squares)].draw();
    draw_circles(points);
    setupPPM();
    setupOutput(points, squares);
    


}
//after doing the GeoGebra, make sure to do this:
//drop perpendiculars from A and C to DE to get two more lines
//drop perpendicular from B to line from A or C 

//to write this program:
//pick 2 points that will be opposite side of the square, connect the two points, A and C
//2. Pick out of the other points and a perpendcular line to step 1, picked B
//3. Pick E on the line from step 2 such that BE = AC
//4. Connect the last point with E is you'
//5. From points from step 1, draw a line perpendicular to the line from S4 DE
//6. Draw a perpedicular line from B (Step 2) on one of the lines from S5. 
int main()
{
    // part1();
    part2();
    return 0;
}