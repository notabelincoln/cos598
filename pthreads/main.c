// Abe Jordan		main.c
#include <stdio.h>
#include <time.h>
#include "montecarlo.h"
#define NUM_THREADS 2
#define NUM_POINTS 10000000
int main(int argc, char *argv[])
{
	void *add_points = (uint32_t *)malloc(sizeof(uint32_t));;
	struct data_vars *pass_vars;
	struct data_vars space_vars;
	uint32_t pi_points = 0;
	uint8_t ret = 0;
	pthread_mutex_t mutex_j = PTHREAD_MUTEX_INITIALIZER;
	pthread_t threads[NUM_THREADS];

	srand(time(0));


	// Set the correct data
	for (int i = 0; i < NUM_THREADS; i++) {
		pass_vars = (struct data_vars *)calloc(1, sizeof(space_vars));
		pass_vars->size = NUM_POINTS / NUM_THREADS;
		ret = pthread_create(&threads[i], NULL, generate_points, (void *)pass_vars);
		if (ret) {
			printf("Bad news bears\n");
			exit(0);
		}
	}

	for (int i = 0; i < NUM_THREADS; i++) {
		pthread_join(threads[i], (void *)&add_points);
		pi_points += *(uint32_t *)(add_points);
	}

	pthread_mutex_destroy(&mutex_j);
	printf("Pi ~= %lf\n", (double) pi_points / NUM_POINTS * 4);
	return 0;
}
