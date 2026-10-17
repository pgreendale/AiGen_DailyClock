#ifndef CLOCK_RENDER_H
#define CLOCK_RENDER_H
#include "clock_state.h"
#include <stdint.h>
#define CLOCK_WIDTH 240
#define CLOCK_HEIGHT 240
void clock_render(uint16_t *frame,const ClockState *state,uint64_t now_us);
#endif


