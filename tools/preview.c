#include <stdio.h>
#include <stdlib.h>
#include "clock_render.h"
#include "clock_state.h"
static uint16_t frame[240*240];
int main(int argc,char **argv) {
    if(argc!=5) { fprintf(stderr,"Usage: preview output.ppm hh mm ss\n");return 2; }
    ClockState s;clock_state_init(&s,0);
    if(!clock_state_set_date(&s,0,2026,10,17)||
       !clock_state_set_time(&s,0,atoi(argv[2]),atoi(argv[3]),atoi(argv[4]))) return 2;
    clock_render(frame,&s,0);
    FILE *f=fopen(argv[1],"wb");if(!f)return 1;
    fprintf(f,"P6\n240 240\n255\n");
    for(int i=0;i<240*240;++i) {
        unsigned char rgb[3]={(unsigned char)(((frame[i]>>11)&31)*255/31),
            (unsigned char)(((frame[i]>>5)&63)*255/63),(unsigned char)((frame[i]&31)*255/31)};
        fwrite(rgb,1,3,f);
    }
    fclose(f);return 0;
}

