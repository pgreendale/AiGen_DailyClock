#ifndef CLOCK_CALENDAR_H
#define CLOCK_CALENDAR_H
#include <stdbool.h>
#include <stdint.h>
typedef struct { int year, month, day, hour, minute, second; } ClockDateTime;
bool calendar_is_leap(int year);
int calendar_days_in_month(int year, int month);
bool calendar_valid(const ClockDateTime *dt);
/* Gregorian years 1..9999; seconds since 0001-01-01. No time zone/DST. */
bool calendar_to_seconds(const ClockDateTime *dt, int64_t *seconds);
bool calendar_from_seconds(int64_t seconds, ClockDateTime *dt);
#endif

