#ifndef CLOCK_LCD_H
#define CLOCK_LCD_H
#include <stdint.h>
void lcd_init(void);
void lcd_set_brightness(unsigned level);
void lcd_present(const uint16_t *frame);
#endif


