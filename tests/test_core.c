#ifdef NDEBUG
#undef NDEBUG
#endif
#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "calendar.h"
#include "clock_state.h"
#include "protocol.h"
#include "clock_model.h"
#include "clock_assets.h"
#include "clock_render.h"
#define PI 3.14159265358979323846
static void calendars(void) {
    assert(calendar_is_leap(2000));
    assert(!calendar_is_leap(1900));
    assert(!calendar_is_leap(2100));
    assert(calendar_is_leap(2400));
    ClockDateTime d={2000,1,1,23,59,59};
    int64_t first;
    assert(calendar_to_seconds(&d,&first));
    /* Entire 400-year Gregorian cycle: every day, including all leap boundaries. */
    for(int i=0;i<146097;++i) {
        ClockDateTime actual;
        int64_t value=first+(int64_t)i*86400,again;
        assert(calendar_from_seconds(value,&actual));
        assert(calendar_to_seconds(&actual,&again) && again==value);
        assert(actual.hour==23&&actual.minute==59&&actual.second==59);
    }
    const int years[]={1,4,100,400,1600,1900,2000,2100,2400,9999};
    for(unsigned i=0;i<sizeof(years)/sizeof(years[0]);++i) {
        for(int m=1;m<=12;++m) {
            d=(ClockDateTime){years[i],m,calendar_days_in_month(years[i],m),0,0,0};
            int64_t seconds; ClockDateTime result;
            assert(calendar_to_seconds(&d,&seconds));
            assert(calendar_from_seconds(seconds,&result));
            assert(result.year==d.year&&result.month==m&&result.day==d.day);
        }
    }
    d=(ClockDateTime){2100,2,29,0,0,0}; assert(!calendar_valid(&d));
    d=(ClockDateTime){2000,2,29,0,0,0}; assert(calendar_valid(&d));
    d=(ClockDateTime){2026,4,31,0,0,0}; assert(!calendar_valid(&d));
    assert(!calendar_from_seconds(-1,&d));
    d=(ClockDateTime){9999,12,31,23,59,59};
    assert(calendar_to_seconds(&d,&first));
    assert(!calendar_from_seconds(first+1,&d));
}
static void commands(void) {
    ClockState s; char out[CLOCK_REPLY_CAPACITY];
    clock_state_init(&s,0);
    assert(clock_protocol_command(&s,0,"T:2024:02:28",out,sizeof(out)));
    assert(clock_protocol_command(&s,0,"T:23:59:59",out,sizeof(out)));
    ClockDateTime d; double sec;
    assert(clock_state_now(&s,2000000,&d,&sec));
    assert(d.year==2024&&d.month==2&&d.day==29&&d.hour==0&&d.minute==0&&d.second==1);
    assert(fabs(sec-1)<1e-12);
    assert(clock_protocol_command(&s,2000000,"T:2100:02:28",out,sizeof(out)));
    assert(clock_protocol_command(&s,2000000,"T:23:59:59",out,sizeof(out)));
    assert(clock_state_now(&s,4000000,&d,&sec));
    assert(d.month==3&&d.day==1&&d.second==1);
    const char *bad[]={"T:24:00:00","T:00:60:00","T:00:00:60","T:2023:02:29","T:0000:01:01",
        "T:2026:04:31","T:2x26:01:01","T:12:34:56X","T:1:02:03","B:0","B:11","B:-1","B:1x","B:001","x"};
    for(unsigned i=0;i<sizeof(bad)/sizeof(bad[0]);++i) {
        ClockState before=s;
        assert(!clock_protocol_command(&s,4000000,bad[i],out,sizeof(out)));
        assert(s.anchor_calendar_us==before.anchor_calendar_us&&s.brightness==before.brightness);
        assert(strstr(out,"Commands")&&strstr(out,"ERR"));
    }
    for(unsigned i=1;i<=10;++i) {
        char text[8]; snprintf(text,sizeof(text),"B:%02u",i);
        assert(clock_protocol_command(&s,4000000,text,out,sizeof(out))&&s.brightness==i);
    }
    assert(clock_brightness_pwm(1)==100&&clock_brightness_pwm(10)==10000);
    for(unsigned i=1;i<10;++i) assert(clock_brightness_pwm(i+1)>clock_brightness_pwm(i));
    ClockLineReader r={0}; bool ready=false;
    for(int i=0;i<80;++i) assert(!clock_protocol_feed(&r,&s,4000000,'X',out,sizeof(out)));
    const char *tail="B:1\r\n";
    for(size_t i=0;i<strlen(tail);++i) ready|=clock_protocol_feed(&r,&s,4000000,tail[i],out,sizeof(out));
    assert(ready&&s.brightness==10&&strstr(out,"ERR"));
    unsigned replies=0;
    const char *good="B:2\r\n";
    for(size_t i=0;i<strlen(good);++i) replies+=clock_protocol_feed(&r,&s,4000000,good[i],out,sizeof(out));
    assert(replies==1&&s.brightness==2);
    clock_protocol_feed(&r,&s,4000000,'B',out,sizeof(out));
    clock_protocol_feed(&r,&s,4000000,'\0',out,sizeof(out));
    assert(clock_protocol_feed(&r,&s,4000000,'\n',out,sizeof(out)));
    assert(strstr(out,"ERR"));
    /* Date changes retain subsecond phase; time changes start on a whole second. */
    clock_state_init(&s,0);
    assert(clock_state_set_time(&s,0,12,0,0));
    assert(clock_state_set_date(&s,250000,2026,12,31));
    assert(clock_state_now(&s,250000,&d,&sec)&&fabs(sec-43200.25)<1e-9);
    assert(clock_state_set_time(&s,250000,23,59,59));
    assert(clock_state_now(&s,1250000,&d,&sec)&&d.year==2027&&d.month==1&&d.day==1&&sec==0);
}
static void model(void) {
    assert(fabs(clock_angle(0))<1e-12);
    assert(fabs(clock_angle(43200)-PI)<1e-12);
    assert(fabs(clock_angle(86400))<1e-12);
    double last=-1;
    for(int second=0;second<86400;second+=5) {
        double angle=clock_angle(second);
        assert(angle>last&&angle>=0&&angle<2*PI);
        assert(clock_density(second)>0);
        assert(clock_density_normalized(second)>0 && clock_density_normalized(second)<=1);
        if(second>0&&second<86399&&abs(second-43200)>1) {
            double derivative=(clock_angle(second+.01)-clock_angle(second-.01))/.02;
            assert(fabs(derivative-2*PI*clock_density(second)/3600)<1e-8);
        }
        last=angle;
    }
    for(int step=0;step<60;++step) {
        double expected=2*PI*step/60;
        assert(fabs(clock_second_angle(step)-expected)<1e-12);
        assert(fabs(clock_second_angle(step+.999)-expected)<1e-12);
    }
    assert(clock_second_angle(60)==0);
    assert(clock_second_angle(86400)==0);
    assert(fabs(clock_second_angle(-.125)-2*PI*59/60)<1e-12);
    assert(clock_angle(-1)>6);
    assert(clock_hand_colour(NAN)==clock_palette[0]);
}
static void renderer(void) {
    uint16_t *memory=malloc((240*240+2)*sizeof(uint16_t));
    assert(memory);
    memory[0]=0xabcd; memory[240*240+1]=0x1234;
    ClockState state; clock_state_init(&state,0);
    clock_render(memory+1,&state,0);
    unsigned red_curve_pixels=0;
    for(int y=55;y<=107;++y) for(int x=62;x<=177;++x) {
        uint16_t pixel=memory[1+y*240+x];
        if((pixel>>11)>0 && (pixel&0x07ff)==0) ++red_curve_pixels;
    }
    assert(red_curve_pixels>80);
    assert(memory[0]==0xabcd&&memory[240*240+1]==0x1234);
    assert(clock_state_set_date(&state,0,2026,10,17));
    const int hours[]={0,3,6,8,12,18,23};
    for(unsigned i=0;i<sizeof(hours)/sizeof(hours[0]);++i) {
        assert(clock_state_set_time(&state,0,hours[i],15,30));
        clock_render(memory+1,&state,123456);
        assert(memory[0]==0xabcd&&memory[240*240+1]==0x1234);
        assert(memory[1+119*240+119]==0xffff);
    }
    free(memory);
}
int main(void) {
    calendars();commands();model();renderer();
    puts("PASS: 400-year calendar cycle, century/year rollovers, strict USB protocol, logarithmic PWM, model and framebuffer guards");
    return 0;
}



