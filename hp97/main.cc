/*
 *  Emulator for HP 97
 *  
 *  Author: Ilan Schnell, 2001
 *  Free for non-commercial and non-military use
 */

#include <stdlib.h>
#include <iostream.h>
#include <iomanip.h>
#include <fstream.h>
#include <strstream.h>
#include <math.h>
#include <builtin.h>
#include <String.h>

#define TINY 1E-15

double x, y, z, t;		// stack
double xx;			// last x
int flag[26];			// flags
int stl;			// stack lift

// registers
double reg[26];			// register 0 .. 19  A  B  C  D  E  I

// program
int lin[1000];			// line in code
double Num[1000];
String Cmd[1000], Val[1000];

int sub[50], subN, N=0;		// Subroutine stuff

int nearest( double x )
{
  if(x>0) return (int)(x+0.5);
  else return (int)(x-0.5);
}

int isnum( String A )
{
  String NUM="0123456789.-+Ee ";
  int len=A.length();
  for( int i=0; i<len; i++ )
    if( !NUM.contains(A.at(i,1)) ) return 0;
  
  String NUM123="0123456789";
  if(len==1) if( NUM123.contains(A) ) return 1; else return 0;
  if(len==0) return 0;
  return 1;
}

int u( String A )
{
  if(isnum(A)) {
    istrstream s(A);
    int a;  s >> a;  return a;
  }
  if(A=="A") return 20;
  if(A=="B") return 21;
  if(A=="C") return 22;
  if(A=="D") return 23;
  if(A=="E") return 24;
  if(A=="I") return 25;
  cout << "Error in u: No such register!\n";
}

String v( double x )
{
  int i=nearest(x);
  if(i<20) {
    static char buffer[10];
    int n=snprintf( buffer, 10, "%i", i ); n++;
    return buffer;
  }
  if(i==20) return "A";
  if(i==21) return "B";
  if(i==22) return "C";
  if(i==23) return "D";
  if(i==24) return "E";
  if(i==25) return "I";
  cout << "Error in v: No such register!\n"; return "X";
}

void print()
{
  cout.precision(4);
  for( int i=0; i<20; i++ ) cout << reg[i] << " "; cout << "\n";
  for( int i=20; i<25; i++ ) cout << reg[i] << " "; cout << "\n";
  cout << "reg I : " << reg[25] << "\n";
  cout << "last x=" << xx << "\n";
  cout << "Flags: "; for( int i=0; i<26; i++ ) cout << flag[i]; cout << "\n";
  cout << "Sub:"; for( int i=0; i<subN; i++ ) cout <<" "<< sub[i]; cout << "\n";
  cout.precision(9);
  cout << "t=" << t << "\n";
  cout << "z=" << z << "\n";
  cout << "y=" << y << "\n";
  cout << "x=" << x << "\n";
}

void put( double a )
{
  if(stl) { t=z; z=y; y=x; }
  x=a;
}

void loadreg( String File )
{
  ifstream fin(File);
  char tmp[20];
  while( fin.getline( tmp, 20 ) ) {
    String Line=tmp, Name;
    double value;
    if(Line.at(0,1)!="#" && Line.length()!=0) {
      istrstream str(Line);
      str >> Name >> value;
      Name=upcase(Name);
      for( int i=0; i<26; i++ )	if(v(i)==Name) reg[i]=value;
      if(Name=="T") t=value;
      if(Name=="Z") z=value;
      if(Name=="Y") y=value;
      if(Name=="X") x=value;
    }
  }
  fin.close();
  
  cout << "Registers:\n";
  for( int i=0; i<26; i++ )
    cout << setw(3) << v(i) << " " << reg[i] << "\n";
}

void loadprg( String File )
{
  ifstream fin(File);
  char tmp[20];
  while( fin.getline( tmp, 20 ) ) {
    String Line=tmp;
    if(Line.at(0,1)!="#" && Line.length()!=0) {
      istrstream str(Line);
      str >> lin[N];
      if(!isnum(Line.after(3))) {
	str >> Cmd[N] >> Val[N];
	Cmd[N]=upcase(Cmd[N]);
      } else {
	str >> Num[N];
	Cmd[N]="n";
      }
      N++;
    }
  }
  fin.close();
  
  cout << "Program:\n";
  for( int n=0; n<N; n++ ) {
    cout << setw(3) << lin[n] << " " << setw(7) << Cmd[n];
    if(Cmd[n]=="n") cout << "umber " << Num[n];
    else cout << " " << Val[n];
    cout << "\n";
  }
  
  for( int n=1; n<N; n++ ) {
    if(Cmd[n-1]=="n" && Cmd[n]=="n") {
      cerr << "Error: Two numbers follow each other in line "
	   << lin[n-1] << " and " << lin[n] << ".\n";
      exit(0);
    }
  }
}

int main( int argc, char* argv[] )
{
  // reset HP 97
  for( int i=0; i<26; i++ ) reg[i]=0.0;
  for( int i=0; i<26; i++ ) flag[i]=0;
  x=y=z=t=xx=0.0;
  sub[0]=-2;
  subN=1;
  stl=1;

  // load registers
  loadreg("errfunc.reg");
  
  // load program
  loadprg("errfunc.prg");
  
  // if given set stack x to value in argument
  if(argc==2) {
    istrstream st2(argv[1]);
    double inputx;
    st2 >> inputx;
    put(inputx);
  }

  print();

  cout << "Execute:\n";
  int n=0; // program pointer
  for(;;) {
  BEGIN:
    if(n>=N) { cerr << "Warning: Reached end of code!\n"; break; }
    if(n==-1) break;
    
    String cmd=Cmd[n], val=Val[n];
    
    // write a number in stack
    if(cmd=="n") { put(Num[n]); goto NEXT; }
    if(cmd=="PI") { put(M_PI); goto NEXT; }
    if(cmd=="LSTX") { put(xx); goto NEXT; }
    if(cmd=="RCL") { put( reg[u(val)] ); goto NEXT; }
    stl=1;
    
    // math operations
    if(cmd=="+") { xx=x; x=y+x; y=z; z=t; goto NEXT; }
    if(cmd=="-") { xx=x; x=y-x; y=z; z=t; goto NEXT; }
    if(cmd=="*") { xx=x; x=y*x; y=z; z=t; goto NEXT; }
    if(cmd=="/") { xx=x; x=y/x; y=z; z=t; goto NEXT; }
    if(cmd=="SIN") { xx=x; x=sin(x); goto NEXT; }
    if(cmd=="COS") { xx=x; x=cos(x); goto NEXT; }
    if(cmd=="TAN") { xx=x; x=tan(x); goto NEXT; }
    if(cmd=="SQRT") { xx=x; x=sqrt(x); goto NEXT; }
    if(cmd=="X^2") { xx=x; x=x*x; goto NEXT; }
    if(cmd=="Y^X") { xx=x; x=pow(y,x); y=z; z=t; goto NEXT; }
    if(cmd=="1/X") { xx=x; x=1.0/x; goto NEXT; }
    if(cmd=="E^X") { xx=x; x=exp(x); goto NEXT; }
    if(cmd=="LN") { xx=x; x=log(x); goto NEXT; }
    if(cmd=="10^X") { xx=x; x=pow(10.0,x); goto NEXT; }
    if(cmd=="LOG") { xx=x; x=log(x)/log(10.0); goto NEXT; }
    if(cmd=="CHS") { xx=x; x=-x; goto NEXT; }
    if(cmd=="ABS") { xx=x; x=abs(x); goto NEXT; }
    if(cmd=="INT") { xx=x; x=floor(x+TINY); goto NEXT; }
    
    // stack manipulations
    if(cmd=="EXCH") { double tmp=x; x=y; y=tmp; goto NEXT; }
    if(cmd=="RDOWN") { double tmp=x; x=y; y=z; z=t; t=tmp; goto NEXT; }
    if(cmd=="RUP") { double tmp=t; t=z; z=y; y=x; x=tmp; goto NEXT; }
    if(cmd=="CLX") { x=0.0; stl=0; goto NEXT; }
    if(cmd=="ENTER") { t=z; z=y; y=x; stl=0; goto NEXT; }
    
    // print commands
    if(cmd=="PRINT") { print(); goto NEXT; }
    if(cmd=="PRINTX") { cout << x << "\n"; goto NEXT; }
    
    // register opterations
    if(cmd=="STO") { reg[u(val)]=x; goto NEXT; }
    if(cmd=="ST+") { reg[u(val)]+=x; goto NEXT; }
    if(cmd=="ST-") { reg[u(val)]-=x; goto NEXT; }
    if(cmd=="ST*") { reg[u(val)]*=x; goto NEXT; }
    if(cmd=="ST/") { reg[u(val)]/=x; goto NEXT; }
    
    if(cmd=="ISZ") { if(++reg[nearest(-reg[25])]) goto NEXT; else goto JUMP; }
    if(cmd=="DSZ") { if(--reg[nearest(-reg[25])]) goto NEXT; else goto JUMP; }
    
    // flags
    if(cmd=="SF") { flag[u(val)]=1; goto NEXT; }
    if(cmd=="CF") { flag[u(val)]=0; goto NEXT; }
    if(cmd=="F?") if(flag[u(val)]) goto NEXT; else goto JUMP;
    
    // tests
    if(cmd=="X>0?") if(x>TINY) goto NEXT; else goto JUMP;
    if(cmd=="X<0?") if(x<-TINY) goto NEXT; else goto JUMP;
    if(cmd=="X<=0?") if(x<TINY) goto NEXT; else goto JUMP;
    if(cmd=="X=0?") if(abs(x)<TINY) goto NEXT; else goto JUMP;
    if(cmd=="X<Y?") if(x<y-TINY) goto NEXT; else goto JUMP;
    if(cmd=="X<=Y?") if(x<y+TINY) goto NEXT; else goto JUMP;
    if(cmd=="X!=Y?") if(abs(x-y)>TINY) goto NEXT; else goto JUMP;
    
    // goto, gosub, ...
    if(cmd=="STOP") break;
    if(cmd=="LBL") goto NEXT;
    if(cmd=="RTN") { n=sub[subN-1]+1; subN--; goto BEGIN; }
    if(cmd=="GSB" || cmd=="GTO") {
      if(val=="i") {
	int l = lin[n]+nearest(reg[25]); // line to go to
	for( int i=0; i<N; i++ ) if(lin[i]==l) { n=i; break; }
	goto BEGIN;
      }
      if(cmd=="GSB") { sub[subN]=n; subN++; }
      n=-1;
      for( int i=0; i<N; i++ )
	if(Cmd[i]=="LBL") if(Val[i]==val) { n=i; break;	}
      if(n==-1) { cerr << "Can't find label: " << val << "\n"; exit(0); }
      goto BEGIN;
    }
    
    //  ERROR:
    cerr << "Error in Line " << lin[n] << "\n";
  JUMP:
    n++;
  NEXT:
    n++;
  }
  print();
  cout << "-------------\n";
  
  cout.precision(9);
  cout << "x=" << x << "\n";
  
  exit(0);
}
