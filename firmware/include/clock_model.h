#ifndef CLOCK_MODEL_H
#define CLOCK_MODEL_H
#include <stdint.h>
/* Seconds since local midnight; 24 h periodic, 0 at top, clockwise. */
double clock_angle(double seconds_of_day);
double clock_density(double seconds_of_day);
/* Same maximum normalization used by the ring and the density chart: 0..1. */
double clock_density_normalized(double seconds_of_day);
/* Conventional seconds hand: one revolution/minute, positions at 1 second. */
double clock_second_angle(double seconds_of_day);
uint16_t clock_hand_colour(double seconds_of_day);
#endif

