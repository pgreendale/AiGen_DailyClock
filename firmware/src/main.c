#include <stdio.h>
#include "pico/stdlib.h"
#include "pico/stdio_usb.h"
#include "clock_state.h"
#include "clock_render.h"
#include "protocol.h"
#include "lcd.h"
static uint16_t frame[240*240];
int main(void) {
    stdio_init_all();
    ClockState state; clock_state_init(&state,time_us_64());
    ClockLineReader reader={0};
    char reply[CLOCK_REPLY_CAPACITY];
    lcd_init();
    clock_render(frame,&state,time_us_64()); lcd_present(frame);
    lcd_set_brightness(state.brightness);
    bool connected_before=false;
    unsigned last_brightness=state.brightness;
    uint64_t next_frame=time_us_64();
    uint64_t last_frame_start=0;
    while(true) {
        bool connected=stdio_usb_connected();
        if(connected&&!connected_before) {
            reader=(ClockLineReader){0};
            printf("Nonlinear Clock 1.0 - USB CDC ready\n");
            clock_protocol_help(reply,sizeof(reply)); printf("%s",reply);
        }
        connected_before=connected;
        for(unsigned count=0;count<256&&connected;++count) {
            int ch=getchar_timeout_us(0);
            if(ch==PICO_ERROR_TIMEOUT) break;
            if(clock_protocol_feed(&reader,&state,time_us_64(),(char)ch,reply,sizeof(reply))) printf("%s",reply);
        }
        if(last_brightness!=state.brightness) {
            lcd_set_brightness(state.brightness); last_brightness=state.brightness;
        }
        uint64_t now=time_us_64();
        if(now>=next_frame) {
            if(last_frame_start) state.frame_interval_us=(uint32_t)(now-last_frame_start);
            last_frame_start=now;
            clock_render(frame,&state,now);
            uint64_t rendered=time_us_64();
            state.render_us=(uint32_t)(rendered-now);
            lcd_present(frame);
            state.transfer_us=(uint32_t)(time_us_64()-rendered);
            next_frame+=1000000; /* 1 position/second; absolute, no accumulated sleep drift. */
            if(next_frame<=now) next_frame=now+1000000;
        }
        sleep_ms(1);
    }
}

