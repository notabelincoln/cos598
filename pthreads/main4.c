// Abe Jordan		main.c
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "pthread.h"

#define NUM_THREADS 1
#define NUM_POINTS 10000000

volatile uint32_t pi_points = 0; // number of points in circle
pthread_mutex_t mutex_j = PTHREAD_MUTEX_INITIALIZER; // prevents race condition


// Generates points in the circle
void *generate_points(void *gp_arg);


// MAIN FUNCTION
int main(int argc, char *argv[])
{
	uint8_t ret; // return value during pthread initialization
	pthread_t threads[NUM_THREADS];

	srand(time(0));

	ret = 0;

	// Set the correct data
	for (int i = 0; i < NUM_THREADS; i++) {
		//printf("Address of pass_vars: %p\n", pass_vars);
		ret = pthread_create(&threads[i], NULL, generate_points, NULL);

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
	static double x, y, z, sum;
	static uint32_t j;

	sum = 0;

	for (j = 0; j < NUM_POINTS / NUM_THREADS; j++) {
		x = (double) rand() / RAND_MAX * 2 - 1;
		y = (double) rand() / RAND_MAX * 2 - 1;
		z = pow(x, 2) + pow(y, 2);

		if (z <= 1)
			sum++;

		}

	pthread_mutex_lock(&mutex_j);
	pi_points += sum;
	pthread_mutex_unlock(&mutex_j);

	pthread_exit(NULL);
}
