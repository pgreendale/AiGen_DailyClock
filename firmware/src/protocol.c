#include "protocol.h"
#include <stdio.h>
#include <string.h>
static const char help[]=
    "Commands (finish with CR or LF):\n"
    "  T:hh:mm:ss    Set local time, 00:00:00..23:59:59\n"
    "  T:yyyy:mm:dd  Set Gregorian date, years 0001..9999\n"
    "  B:1..10       Backlight, logarithmic PWM (01..10 also accepted)\n"
    "  S             Read clock status\n"
    "  ?             Show this help\n";
void clock_protocol_help(char *out,size_t cap) { if(cap) snprintf(out,cap,"%s",help); }
static int number(const char *s,size_t n) {
    int v=0;
    for(size_t i=0;i<n;++i) { if(s[i]<'0'||s[i]>'9') return -1; v=v*10+s[i]-'0'; }
    return v;
}
static bool fail(char *out,size_t cap) {
    if(cap) snprintf(out,cap,"ERR Invalid command or value\n%s",help);
    return false;
}
bool clock_protocol_command(ClockState *s,uint64_t now,const char *line,char *out,size_t cap) {
    if(!s||!line||!out||!cap) return false;
    size_t n=strlen(line);
    if(!strcmp(line,"?")) { clock_protocol_help(out,cap); return true; }
    if(!strcmp(line,"S")) {
        ClockDateTime d;
        if(!clock_state_now(s,now,&d,NULL)) return fail(out,cap);
        snprintf(out,cap,"STATUS T:%02d:%02d:%02d T:%04d:%02d:%02d B:%u TIME_SET:%u DATE_SET:%u FRAME_US:%lu RENDER_US:%lu TRANSFER_US:%lu\n",
            d.hour,d.minute,d.second,d.year,d.month,d.day,s->brightness,
            (unsigned)s->time_set,(unsigned)s->date_set,
            (unsigned long)s->frame_interval_us,(unsigned long)s->render_us,(unsigned long)s->transfer_us);
        return true;
    }
    if(n==10 && line[0]=='T' && line[1]==':' && line[4]==':' && line[7]==':') {
        int h=number(line+2,2),m=number(line+5,2),sec=number(line+8,2);
        if(!clock_state_set_time(s,now,h,m,sec)) return fail(out,cap);
        snprintf(out,cap,"OK TIME %02d:%02d:%02d\n",h,m,sec); return true;
    }
    if(n==12 && line[0]=='T' && line[1]==':' && line[6]==':' && line[9]==':') {
        int y=number(line+2,4),m=number(line+7,2),day=number(line+10,2);
        if(!clock_state_set_date(s,now,y,m,day)) return fail(out,cap);
        snprintf(out,cap,"OK DATE %04d:%02d:%02d\n",y,m,day); return true;
    }
    if((n==3||n==4) && line[0]=='B' && line[1]==':') {
        int level=number(line+2,n-2);
        if(level<1||level>10) return fail(out,cap);
        s->brightness=(unsigned)level;
        snprintf(out,cap,"OK B %u PWM %u/10000\n",s->brightness,clock_brightness_pwm(s->brightness)); return true;
    }
    return fail(out,cap);
}
bool clock_protocol_feed(ClockLineReader *r,ClockState *s,uint64_t now,char ch,char *out,size_t cap) {
    if(ch=='\r'||ch=='\n') {
        if(r->overflow) {
            r->used=0; r->overflow=false;
            if(cap) snprintf(out,cap,"ERR Line too long or non-ASCII input\n%s",help);
            return true;
        }
        if(!r->used) return false;
        r->line[r->used]='\0'; r->used=0;
        clock_protocol_command(s,now,r->line,out,cap); return true;
    }
    if(r->overflow) return false;
    if((unsigned char)ch<32||(unsigned char)ch>126||r->used>=sizeof(r->line)-1) {
        r->overflow=true; return false;
    }
    r->line[r->used++]=ch; return false;
}

