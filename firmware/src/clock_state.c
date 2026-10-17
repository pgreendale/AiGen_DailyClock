#include "clock_state.h"
#include <math.h>
#include <stddef.h>
#define US_PER_SECOND INT64_C(1000000)
static int64_t current_us(const ClockState *s,uint64_t now) {
    uint64_t elapsed=now>=s->anchor_monotonic_us?now-s->anchor_monotonic_us:0;
    return s->anchor_calendar_us+(int64_t)elapsed;
}
void clock_state_init(ClockState *s,uint64_t now) {
    ClockDateTime start={2000,1,1,0,0,0}; int64_t epoch;
    calendar_to_seconds(&start,&epoch);
    *s=(ClockState){.anchor_calendar_us=epoch*US_PER_SECOND,
        .anchor_monotonic_us=now,.time_set=false,.date_set=false,.brightness=6};
}
bool clock_state_now(const ClockState *s,uint64_t now,ClockDateTime *d,double *day_sec) {
    if(!s || !d) return false;
    int64_t us=current_us(s,now);
    if(!calendar_from_seconds(us/US_PER_SECOND,d)) return false;
    if(day_sec) *day_sec=d->hour*3600.0+d->minute*60.0+d->second+(us%US_PER_SECOND)/1000000.0;
    return true;
}
bool clock_state_set_time(ClockState *s,uint64_t now,int h,int m,int sec) {
    ClockDateTime d;
    if(!clock_state_now(s,now,&d,NULL)) return false;
    d.hour=h; d.minute=m; d.second=sec; int64_t epoch;
    if(!calendar_to_seconds(&d,&epoch)) return false;
    s->anchor_calendar_us=epoch*US_PER_SECOND; s->anchor_monotonic_us=now; s->time_set=true;
    return true;
}
bool clock_state_set_date(ClockState *s,uint64_t now,int y,int m,int day) {
    ClockDateTime d;
    if(!clock_state_now(s,now,&d,NULL)) return false;
    int64_t fractional=current_us(s,now)%US_PER_SECOND;
    d.year=y; d.month=m; d.day=day; int64_t epoch;
    if(!calendar_to_seconds(&d,&epoch)) return false;
    s->anchor_calendar_us=epoch*US_PER_SECOND+fractional; s->anchor_monotonic_us=now; s->date_set=true;
    return true;
}
uint16_t clock_brightness_pwm(unsigned level) {
    if(level<1 || level>10) return 0;
    return (uint16_t)lround(100.0*pow(100.0,(level-1)/9.0));
}

