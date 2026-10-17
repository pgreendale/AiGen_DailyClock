#include "calendar.h"
#include <stddef.h>
bool calendar_is_leap(int y) { return y%4==0 && (y%100!=0 || y%400==0); }
int calendar_days_in_month(int y,int m) {
    static const int days[12]={31,28,31,30,31,30,31,31,30,31,30,31};
    if(y<1||y>9999||m<1||m>12) return 0;
    return days[m-1]+(m==2 && calendar_is_leap(y));
}
bool calendar_valid(const ClockDateTime *d) {
    return d && d->year>=1 && d->year<=9999 && d->month>=1 && d->month<=12 &&
        d->day>=1 && d->day<=calendar_days_in_month(d->year,d->month) &&
        d->hour>=0 && d->hour<24 && d->minute>=0 && d->minute<60 && d->second>=0 && d->second<60;
}
static int64_t days_before_year(int y) {
    int64_t n=y-1; return 365*n+n/4-n/100+n/400;
}
bool calendar_to_seconds(const ClockDateTime *d,int64_t *out) {
    if(!out || !calendar_valid(d)) return false;
    int64_t days=days_before_year(d->year)+d->day-1;
    for(int m=1;m<d->month;++m) days+=calendar_days_in_month(d->year,m);
    *out=days*86400+d->hour*3600+d->minute*60+d->second; return true;
}
bool calendar_from_seconds(int64_t seconds,ClockDateTime *d) {
    if(!d || seconds<0 || seconds>=days_before_year(10000)*86400) return false;
    int64_t days=seconds/86400;
    int lo=1,hi=9999;
    while(lo<hi) { int mid=(lo+hi+1)/2;
        if(days_before_year(mid)<=days) lo=mid; else hi=mid-1; }
    d->year=lo; days-=days_before_year(lo); d->month=1;
    while(days>=calendar_days_in_month(lo,d->month))
        days-=calendar_days_in_month(lo,d->month++);
    d->day=(int)days+1;
    int rem=(int)(seconds%86400);
    d->hour=rem/3600; d->minute=rem/60%60; d->second=rem%60;
    return true;
}

