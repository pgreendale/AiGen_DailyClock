#ifndef CLOCK_PROTOCOL_H
#define CLOCK_PROTOCOL_H
#include "clock_state.h"
#include <stddef.h>
#define CLOCK_REPLY_CAPACITY 640
void clock_protocol_help(char *out,size_t capacity);
bool clock_protocol_command(ClockState *s,uint64_t now_us,const char *line,char *out,size_t capacity);
typedef struct { char line[64]; size_t used; bool overflow; } ClockLineReader;
/* CR/LF/CRLF. Discard entire overlong/non-ASCII lines, never execute fragments. */
bool clock_protocol_feed(ClockLineReader *r,ClockState *s,uint64_t now_us,char byte,char *out,size_t capacity);
#endif

