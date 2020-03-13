//Abe Jordan	test.c
#include "pthread.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N_THREADS 8
#define M_POINTS 10000000

pthread_mutex_t fastmutex = PTHREAD_MUTEX_INITIALIZER;
pthread_t ThreadID[N_THREADS];	// array of pthread IDs
const uint32_t n_runs = M_POINTS / N_THREADS;
uint32_t circle_pts;	// points in circle per thread

void *Compute(void *place_i);

/* MAIN FUNCTION, PRODUCES END COMPUTATION OF PI */
int main(int argc, char *argv[])
{
	int ret = 0;
	int Total_Hits = 0;

	for (int i = 0; i < N_THREADS; i++) {
		ret = pthread_create(&ThreadID[i], NULL, Compute, NULL);

		if (ret) {
			printf("Bad news Bears!\n");
			exit(0);
		}
	}

	for (int k = 0; k < N_THREADS; k++) {
		pthread_join(ThreadID[k], NULL);
	}

	printf("Pi is about %f\n", (float)circle_pts / M_POINTS * 4.0);
	pthread_mutex_destroy(&fastmutex);
	pthread_exit(NULL);
}


/* COMPUTATION THREAD, RETURNS NUMBER OF POINTS IN CIRCLE */
void *Compute(void *arg)
{	
	float *x;
	float *y;
	float *z;

	x = (float *)malloc(sizeof(float));
	y = (float *)malloc(sizeof(float));
	z = (float *)malloc(sizeof(float));
	// compute number of points for n_runs
	for (int j = 0; j < n_runs; j++) {
		pthread_mutex_lock(&fastmutex);
		*x = (float)random() / RAND_MAX * 2 - 1;
		*y = (float)random() / RAND_MAX * 2 - 1;
		
		*z = (*x) * (*x) + (*y) * (*y);
		if (*z <= 1)
			circle_pts++;
		pthread_mutex_unlock(&fastmutex);
	}
	// exit function and return number of points in circle

	free (x);
	free (y);
	free (z);
	pthread_exit(NULL);
}
