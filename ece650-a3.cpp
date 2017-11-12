#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include<iostream>
#ifndef RGEN
#define RGEN "./rgen"
#define A1 "python ./ece650-a1.py"
#define A2 "./ece650-a2"
#endif
using namespace std;

int 
main(int argc, char *argv[])
{
  
  /*parent start fork rgen*/
  int pid_rgen, pipe_r_rgen[2];
  pipe(pipe_r_rgen);
  switch(pid_rgen = fork())
  {
  	case -1:
  		exit(EXIT_FAILURE);
  	case 0://child process - rgen
  		close(pipe_r_rgen[0]);
  		dup2(pipe_r_rgen[1], STDOUT_FILENO);
  		close(pipe_r_rgen[1]);
		execvp(RGEN, argv);

  }

  
  close(pipe_r_rgen[1]);
  /*parent finish rgen fork*/

  /*parent start fork a1*/
  int pid_a1, pipe_r_a1[2];
  pipe(pipe_r_a1);
  switch(pid_a1 = fork())
  {
  	case -1: // Couldnt able to do the fork the child
  		exit(EXIT_FAILURE);
  	case 0: //pid_a1
  		dup2(pipe_r_rgen[0], STDIN_FILENO);
  		close(pipe_r_rgen[0]);
  		close(pipe_r_a1[0]);
  		dup2(pipe_r_a1[1], STDOUT_FILENO);
  		close(pipe_r_a1[1]);
  		execl("/bin/sh", "sh", "-c", A1, NULL);
  }
  close(pipe_r_rgen[0]);
  close(pipe_r_a1[1]);
  /*parent finish a1 fork*/

  /*parent fork a2 using popen*/
  FILE* write_to_a2 = popen(A2, "w");//a2-process 

   /*parent start fork a1 reader*/
  int pid_a1_reader;
  switch(pid_a1_reader = fork())
  {
  	case -1: // Couldnt able to do the fork the child
  		exit(EXIT_FAILURE);
  	case 0://pid_a1_reader
  		{
  		FILE* read_from_a1 = fdopen(pipe_r_a1[0],"r");
  		char* line = NULL;
  		size_t bytes = 0;
  		while(getline(&line, &bytes, read_from_a1) != -1)
  		{
  			printf("%s", line);
  			fputs(line, write_to_a2);
  			fflush(write_to_a2);
  		}
  		fclose(read_from_a1);
      fclose(write_to_a2);
  		exit(EXIT_SUCCESS);
  	}
  }
  
  close(pipe_r_a1[0]);//does not read a1 at stdin reader
  char* line = NULL;
  size_t bytes = 0;
// send the standard input Assignment to so that Assigment 2 can print shortest Path.
  while(getline(&line, &bytes, stdin) != -1)
  {
  	fputs(line, write_to_a2);
  	fflush(write_to_a2);
  }
  kill(pid_rgen, SIGTERM); // Killing Rgen when there is EOF line Input by user

  pclose(write_to_a2); // Sending the the End of line to the Assignment
  return EXIT_SUCCESS;
}

