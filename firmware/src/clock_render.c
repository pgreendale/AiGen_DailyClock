#include "clock_render.h"
#include "clock_assets.h"
#include "clock_model.h"
#include <math.h>
#include <stdio.h>
#include <string.h>
#define WHITE 0xffffu
#define TAU_F 6.2831853071795864769f
typedef struct { float x,y; } Point;
static void pixel(uint16_t *fb,int x,int y,uint16_t colour,unsigned coverage) {
    if(x<0||x>=240||y<0||y>=240||!coverage) return;
    uint16_t old=fb[y*240+x];
    unsigned r=(((colour>>11)&31)*coverage+((old>>11)&31)*(4-coverage)+2)/4;
    unsigned g=(((colour>>5)&63)*coverage+((old>>5)&63)*(4-coverage)+2)/4;
    unsigned b=((colour&31)*coverage+(old&31)*(4-coverage)+2)/4;
    fb[y*240+x]=(uint16_t)((r<<11)|(g<<5)|b);
}
static void polygon(uint16_t *fb,const Point *p,int n,uint16_t colour) {
    float x0=p[0].x,x1=x0,y0=p[0].y,y1=y0;
    for(int i=1;i<n;++i) {
        x0=fminf(x0,p[i].x); x1=fmaxf(x1,p[i].x);
        y0=fminf(y0,p[i].y); y1=fmaxf(y1,p[i].y);
    }
    int left=(int)floorf(x0)-1,right=(int)ceilf(x1)+1;
    int top=(int)floorf(y0)-1,bottom=(int)ceilf(y1)+1;
    if(left<0) left=0;
    if(right>239) right=239;
    if(top<0) top=0;
    if(bottom>239) bottom=239;
    for(int y=top;y<=bottom;++y) for(int x=left;x<=right;++x) {
        unsigned coverage=0;
        for(int sy=0;sy<2;++sy) for(int sx=0;sx<2;++sx) {
            float xx=x+(sx?.25f:-.25f),yy=y+(sy?.25f:-.25f);
            bool positive=false,negative=false;
            for(int i=0;i<n;++i) {
                int j=(i+1)%n;
                float cross=(p[j].x-p[i].x)*(yy-p[i].y)-(p[j].y-p[i].y)*(xx-p[i].x);
                positive|=cross>0; negative|=cross<0;
            }
            coverage+=!(positive&&negative);
        }
        pixel(fb,x,y,colour,coverage);
    }
}
static Point local_point(float a,float along,float across) {
    float s=sinf(a),c=cosf(a);
    return (Point){CLOCK_CENTER+s*along+c*across,CLOCK_CENTER-c*along+s*across};
}
static void bar(uint16_t *fb,float a,float tail,float tip,float width,uint16_t colour,bool pointed) {
    float shoulder=pointed?tip-5.0f:tip;
    Point p[5]={local_point(a,tail,-width/2),local_point(a,shoulder,-width/2),
        local_point(a,tip,0),local_point(a,shoulder,width/2),local_point(a,tail,width/2)};
    if(pointed) polygon(fb,p,5,colour);
    else { Point rect[4]={p[0],p[1],p[3],p[4]}; polygon(fb,rect,4,colour); }
}
/* Uniform 24-hour horizontal axis, maximum-normalized density vertically.
   The complete chart rectangle remains inside the upper black semicircle. */
#define PLOT_LEFT 64.0f
#define PLOT_RIGHT 175.0f
#define PLOT_BASE 105.0f
#define PLOT_HEIGHT 48.0f
#define RED 0xf800u
static void stroke(uint16_t *fb,Point a,Point b,float width,uint16_t colour) {
    float dx=b.x-a.x,dy=b.y-a.y,length=sqrtf(dx*dx+dy*dy);
    if(length<.0001f) return;
    float nx=-dy*width/(2*length),ny=dx*width/(2*length);
    Point corners[4]={{a.x+nx,a.y+ny},{b.x+nx,b.y+ny},
        {b.x-nx,b.y-ny},{a.x-nx,a.y-ny}};
    polygon(fb,corners,4,colour);
}
static void density_chart(uint16_t *fb,bool show_marker,double seconds) {
    /* Render the fixed curve once. Retain only its small black-background
       rectangle, not another full framebuffer, to fit comfortably in RP2040 RAM. */
    enum { SEGMENTS=222,CACHE_X=62,CACHE_Y=55,CACHE_W=116,CACHE_H=53 };
    static uint16_t chart_cache[CACHE_H][CACHE_W];
    static bool prepared=false;
    if(!prepared) {
        Point previous={PLOT_LEFT,PLOT_BASE-PLOT_HEIGHT*(float)clock_density_normalized(0)};
        for(int i=1;i<=SEGMENTS;++i) {
            Point next={PLOT_LEFT+(PLOT_RIGHT-PLOT_LEFT)*i/SEGMENTS,
                PLOT_BASE-PLOT_HEIGHT*(float)clock_density_normalized(i*86400.0/SEGMENTS)};
            stroke(fb,previous,next,1.0f,RED);
            previous=next;
        }
        for(int row=0;row<CACHE_H;++row)
            memcpy(chart_cache[row],fb+(CACHE_Y+row)*240+CACHE_X,sizeof(chart_cache[row]));
        prepared=true;
    } else {
        for(int row=0;row<CACHE_H;++row)
            memcpy(fb+(CACHE_Y+row)*240+CACHE_X,chart_cache[row],sizeof(chart_cache[row]));
    }
    if(show_marker) {
        double phase=fmod(seconds,86400.0);
        if(phase<0) phase+=86400;
        float x=PLOT_LEFT+(PLOT_RIGHT-PLOT_LEFT)*(float)(phase/86400.0);
        float y=PLOT_BASE-PLOT_HEIGHT*(float)clock_density_normalized(seconds);
        stroke(fb,(Point){x,PLOT_BASE+1},(Point){x,y-1},2.2f,RED);
        /* A short cap keeps the exact current value visible at low densities. */
        stroke(fb,(Point){x-1.5f,y},(Point){x+1.5f,y},1.5f,RED);
    }
}
static const uint16_t digit[10]={
    0x7b6f, /* 111 101 101 101 111 */
    0x2492, /* 010 010 010 010 010 */
    0x73e7, /* 111 001 111 100 111 */
    0x73cf, /* 111 001 111 001 111 */
    0x5bc9, /* 101 101 111 001 001 */
    0x79cf, /* 111 100 111 001 111 */
    0x79ef, /* 111 100 111 101 111 */
    0x7249, /* 111 001 001 001 001 */
    0x7bef, /* 111 101 111 101 111 */
    0x7bcf  /* 111 101 111 001 111 */
};
static void date_text(uint16_t *fb,const char *text) {
    int n=(int)strlen(text),x=(240-(n*8-2))/2;
    int top=(int)lroundf(CLOCK_CENTER+CLOCK_INNER_RADIUS*.67f)-5;
    for(int i=0;i<n;++i) {
        uint16_t bits=text[i]>='0'&&text[i]<='9'?digit[text[i]-'0']:0;
        if(text[i]=='.') bits=2;
        if(text[i]=='-') bits=7<<6;
        for(int row=0;row<5;++row) for(int col=0;col<3;++col) {
            if(!(bits&(1u<<(14-row*3-col)))) continue;
            for(int dy=0;dy<2;++dy) for(int dx=0;dx<2;++dx)
                pixel(fb,x+i*8+col*2+dx,top+row*2+dy,WHITE,4);
        }
    }
}
void clock_render(uint16_t *frame,const ClockState *state,uint64_t now) {
    memcpy(frame,clock_face,sizeof(uint16_t)*240*240);
    for(int quarter=0;quarter<4;++quarter)
        bar(frame,quarter*TAU_F/4,CLOCK_INNER_RADIUS-8,CLOCK_INNER_RADIUS-2,1.3f,WHITE,false);
    ClockDateTime d;
    double seconds=0;
    bool valid=clock_state_now(state,now,&d,&seconds);
    char date[16];
    if(valid&&state->date_set) snprintf(date,sizeof(date),"%02d.%02d.%04d",d.day,d.month,d.year);
    else snprintf(date,sizeof(date),"--.--.----");
    date_text(frame,date);
    density_chart(frame,valid&&state->time_set,seconds);
    if(valid&&state->time_set) {
        bar(frame,(float)clock_angle(seconds),-3,114.0f,2.2f,clock_hand_colour(seconds),false);
        float minute=(float)fmod(seconds,3600.0)*TAU_F/3600.0f;
        bar(frame,minute,-4,CLOCK_INNER_RADIUS-2,2.0f,WHITE,true);
        bar(frame,(float)clock_second_angle(seconds),-5,CLOCK_INNER_RADIUS-3,1.2f,0xf800u,false);
        for(int y=118;y<=121;++y) for(int x=118;x<=121;++x) {
            float dx=x-CLOCK_CENTER,dy=y-CLOCK_CENTER;
            if(dx*dx+dy*dy<3.5f) pixel(frame,x,y,WHITE,4);
        }
    }
}

