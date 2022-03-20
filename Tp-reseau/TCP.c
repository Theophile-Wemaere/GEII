#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "lib.h"

char* ip = "192.168.0.25";
int port=3651;
char data[25];
float moy[20];
int a=0;

void clearScreen(void);
void Moy(float* val);

int main(void)
{
	while(1)
	{
		int s=createSocketTCP();
		printf("socket: %d",s);
		if(s==-1)
		{
			perror("error creating socket");
			return -1;
		}
		int c=connectServer(s,ip,port);
		if(c==-1)
		{
			perror("error conecting server");
			return -1;
		}
	
		int rD=receveData(s,data,50); 
		if(rD==-1)
		{
			perror("error receiving Data");
			return -1;
		}
		
		int s2= closeSocket(s);
		if(s2==-1)
		{
			perror("error closing socket");
			return -1;
		}
		
		printf("\ndata : ");
		for(int i=0;i<50;i++)
		{
			printf("%c", data[i]);
		}
		float angle,speed;
		int check;
		sscanf(data,"$WIMWV,%f,R,%f,N,A*%d",&angle,&speed,&check); 
		moy[a%200] = speed;
		printf("angle : %f\n",angle);
		printf("speed : %f\n",speed);
		printf("checksum : %d\n",check);
		Moy(moy);
		sleep(1);
		clearScreen();
		a++;
	}
}

void clearScreen(void)
{
  const char *CLEAR_SCREEN_ANSI = "\e[1;1H\e[2J";
  write(STDOUT_FILENO, CLEAR_SCREEN_ANSI, 12);
}

void Moy(float* val)
{
	int i=0;
	float sum=0;
	for(i=0;i<20;i++)
	{
		sum += val[i];
	}
	printf("valeur moyenne : %f\n",sum/20); 
}
