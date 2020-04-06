// Abe Jordan		montecarlo.c
#include "montecarlo.h"

// Mathematically generate the points in the circle
void *generate_points(void *gp_arg)
{
	struct pthread_vars vars* = (struct pthread_vars *)gp_arg;
	printf("Generating Points\n");

	for (vars->counter = 0; vars->counter < vars->size; (vars->counter)++) {
		vars->x = (double) rand() / RAND_MAX * 2 - 1;
		vars->y = (double) rand() / RAND_MAX * 2 - 1;
		vars->z = (vars->x) * (vars->x) + (vars->y) * (vars->y);
		if (vars->z <= 1.0)
			(vars->points_out)++;
		}
	}

	pthread_exit((void *)(&(vars->points_out)));
}
