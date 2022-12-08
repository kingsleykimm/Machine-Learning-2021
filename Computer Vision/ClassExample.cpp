#include <iostream>
#define STACKSIZE 100
using namespace std;

class Stack { // a simple stack implementation that does no error checking
  private:    // member data
    int items[STACKSIZE];
    int top;
  public:     // available member methods
      Stack()          { top = 0; }   // constructor; called when the new is called
      void push(int i) { items[top++] = i; }
      int pop()        { return items[--top]; }
      bool isEmpty()   { return top==0; }
      int size()       { return top; }
      ~Stack()         { cout << "Stack deleted.\n"; }  // destructor; called when the delete is called
														// the destructor is supposed to delete any memory occupied, close any file handlers...
};


int main() {
  Stack *s = new Stack();  //s is a pointer in C++; the constructor is called
  cout << "Stack has " << s -> size() << " items.\n"; //to call a method on a pointer i C++ you must use the -> operator
  s -> push(5); 
  s -> push(8);
  cout << "Stack has " << s -> size() << " items.\n";
  cout << s -> pop() << '\n';
  cout << s -> pop() << '\n';
  cout << "Stack has " << s -> size() << " items.\n";
  delete s;		//in C++ there is no garbage collector so before you exit a program you must release the memory; the destructor is called
}

