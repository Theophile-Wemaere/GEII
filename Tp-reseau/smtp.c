#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "lib.h"

char* ip = "192.168.0.27";
int port=25;
char data[255];

char* helo="HELO\r\n";
char* from="MAIL FROM:theogus@geii.fr\r\n";
char* to="RCPT TO:theogus@geii.fr\r\n";
char* DATA="DATA\r\n";
char* text="From:theogusgmail.com\n\rTo:theogusgmail.com\n\rsubject:Test\r\n\r\nHello world, send with C langage (god langage)\r\n";
char* end=".\r\n";
char* quit="QUIT\r\n";

void printResponse(char *data, int s);

int main(void)
{
	int s=createSocketTCP();
	printf("socket: %d\n",s);
	if(s==-1)
	{
		perror("error creating socket");
		return -1;
	}
  /////////////////////////////////////////
	int c=connectServer(s,ip,port);
	if(c==-1)
	{
		perror("error conecting server");
		return -1;
	}
	/////////////////////////////////////////
	int rD=receveData(s,data,100); 
	if(rD==-1)
	{
		perror("error receiving Data");
		return -1;
	}
	printResponse(data, 100);
  /////////////////////////////////////////
	int sD=sendData(s,helo);
	if(sD==-1)
	{
		perror("error sending Data : HELO");
		return -1;
	}
	rD=receveData(s,data,255); 
	if(rD==-1)
	{
		perror("error receiving Data : HELO");
		return -1;
	}
	printResponse(data,rD);
  /////////////////////////////////////////
	sD=sendData(s,from);
	if(sD==-1)
	{
		perror("error sending Data : FROM");
		return -1;
	}
	rD=receveData(s,data,255); 
	if(rD==-1)
	{
		perror("error receiving Data : FROM");
		return -1;
	}
	printResponse(data,rD);
	/////////////////////////////////////////
	sD=sendData(s,to);
	if(sD==-1)
	{
		perror("error sending Data : TO");
		return -1;
	}
	rD=receveData(s,data,255); 
	if(rD==-1)
	{
		perror("error receiving Data : TO");
		return -1;
	}
	printResponse(data,rD);
	/////////////////////////////////////////
	sD=sendData(s,DATA);
	if(sD==-1)
	{
		perror("error sending Data : DATA");
		return -1;
	}
	rD=receveData(s,data,255); 
	if(rD==-1)
	{
		perror("error receiving Data : DATA");
		return -1;
	}
	printResponse(data,rD);
	/////////////////////////////////////////
	sD=sendData(s,text);
	if(sD==-1)
	{
		perror("error sending Data : text");
		return -1;
	}
  /////////////////////////////////////////
	sD=sendData(s,end);
	if(sD==-1)
	{
		perror("error sending Data : .");
		return -1;
	}
	rD=receveData(s,data,255);
	if(rD==-1)
	{
		perror("error receiving Data : .");
		return -1;
	}
	printResponse(data,rD);
	/////////////////////////////////////////
  sD=sendData(s,quit);
	if(sD==-1)
	{
		perror("error sending Data : quit");
		return -1;
	}
	rD=receveData(s,data,255); 
	if(rD==-1)
	{
		perror("error receiving Data : quit");
		return -1;
	}
	printResponse(data,rD);
	/////////////////////////////////////////
	int s2= closeSocket(s);
	if(s2==-1)
	{
		perror("error closing socket");
		return -1;
	}
}

void printResponse(char *data, int s)
{
	for(int i=0;i<s;i++)
	{
		
		printf("%c", data[i]);
	}
	printf("\n");
}
