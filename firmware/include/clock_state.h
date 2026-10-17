#ifndef CLOCK_STATE_H
#define CLOCK_STATE_H
#include "calendar.h"
#include <stdint.h>
typedef struct {
    int64_t anchor_calendar_us;
    uint64_t anchor_monotonic_us;
    bool time_set,date_set;
    unsigned brightness;
    uint32_t frame_interval_us,render_us,transfer_us;
} ClockState;
void clock_state_init(ClockState *s,uint64_t now_us);
bool clock_state_now(const ClockState *s,uint64_t now_us,ClockDateTime *dt,double *seconds_of_day);
bool clock_state_set_time(ClockState *s,uint64_t now_us,int hour,int minute,int second);
bool clock_state_set_date(ClockState *s,uint64_t now_us,int year,int month,int day);
/* Counts out of 10000; logarithmic duty scale. */
uint16_t clock_brightness_pwm(unsigned level);
#endif

