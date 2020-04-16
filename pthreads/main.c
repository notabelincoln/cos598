// Abe Jordan		main.c
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "pthread.h"

#define NUM_THREADS 4
#define NUM_POINTS 10000000

volatile uint32_t pi_points = 0; // number of points in circle
pthread_mutex_t mutex_j = PTHREAD_MUTEX_INITIALIZER; // prevents race condition


// Generates points in the circle
void *generate_points(void *gp_arg);


// Structure of data to pass to computational function
typedef struct {
	uint32_t size, counter;
	double x, y, z;
	uint32_t result;
} data_vars;


// MAIN FUNCTION
int main(int argc, char *argv[])
{
	//void *add_points; // stores reutrn value of computation function
	uint8_t ret; // return value during pthread initialization
	pthread_t threads[NUM_THREADS]; // array of pthreads
	data_vars *pass_vars; // array of pointers to data

	srand(time(0));

	ret = 0;

	// Set the correct data
	for (int i = 0; i < NUM_THREADS; i++) {
		pass_vars = (data_vars *)malloc(sizeof(data_vars));
		pass_vars->size = NUM_POINTS / NUM_THREADS;
		pass_vars->result = 0;
		//printf("Address of pass_vars: %p\n", pass_vars);
		ret = pthread_create(&threads[i], NULL, generate_points, (void *)pass_vars);

		if (ret) {
			printf("Bad news bears\n");
			exit(0);
		}
	}

	for (int i = 0; i < NUM_THREADS; i++)
		pthread_join(threads[i], NULL);

	pthread_mutex_destroy(&mutex_j);
	printf("Pi ~= %lf\n", (double) pi_points / NUM_POINTS * 4);
	return 0;
}


// PERFORM MONTECARLO SIMULATION
void *generate_points(void *arg)
{
	data_vars *ptr = (data_vars *)arg;

	for (ptr->counter = 0; ptr->counter < NUM_POINTS / NUM_THREADS; ptr->counter++) {
		ptr->x = (double) rand() / RAND_MAX * 2 - 1;
		ptr->y = (double) rand() / RAND_MAX * 2 - 1;
		ptr->z = pow(ptr->x, 2) + pow(ptr->y, 2);

		//printf("Address of arg: %p\n", arg);

		if (ptr->z <= 1)
			ptr->result++;
	}

	pthread_mutex_lock(&mutex_j);
	pi_points += ptr->result;
	pthread_mutex_unlock(&mutex_j);

	free(ptr);

	pthread_exit(NULL);
}
