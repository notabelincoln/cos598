// Abe Jordan		montecarlo.h
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include "pthread.h"
#ifndef MONTECARLO_H
#define MONTECARLO_H
// Structure of data to pass to computational function
typedef struct {
	uint32_t size, counter;
	double x, y, z;
	uint32_t *points_out;
} data_vars;

// Generates points in the circle
void *generate_points(void *gp_arg);
#endif

