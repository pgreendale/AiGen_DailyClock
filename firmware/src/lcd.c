/* Waveshare GC9A01A initialisation data: see licenses/Waveshare.txt. */
#include "lcd.h"
#include "clock_state.h"
#include "gc9a01_init.h"
#include "pico/stdlib.h"
#include "hardware/spi.h"
#include "hardware/pwm.h"
#define LCD_SPI spi1
#define PIN_DC 8
#define PIN_CS 9
#define PIN_SCK 10
#define PIN_MOSI 11
#define PIN_RESET 12
#define PIN_BACKLIGHT 25
static void command(uint8_t reg,const uint8_t *data,unsigned size) {
    gpio_put(PIN_CS,0); gpio_put(PIN_DC,0);
    spi_write_blocking(LCD_SPI,&reg,1);
    if(size) { gpio_put(PIN_DC,1); spi_write_blocking(LCD_SPI,data,size); }
    while(spi_is_busy(LCD_SPI)) tight_loop_contents();
    gpio_put(PIN_CS,1);
}
void lcd_set_brightness(unsigned level) {
    if(level>=1&&level<=10) pwm_set_gpio_level(PIN_BACKLIGHT,clock_brightness_pwm(level));
}
void lcd_init(void) {
    gpio_init(PIN_CS); gpio_set_dir(PIN_CS,GPIO_OUT); gpio_put(PIN_CS,1);
    gpio_init(PIN_DC); gpio_set_dir(PIN_DC,GPIO_OUT); gpio_put(PIN_DC,0);
    gpio_init(PIN_RESET); gpio_set_dir(PIN_RESET,GPIO_OUT);
    gpio_init(PIN_BACKLIGHT); gpio_set_dir(PIN_BACKLIGHT,GPIO_OUT); gpio_put(PIN_BACKLIGHT,0);
    spi_init(LCD_SPI,40000000);
    gpio_set_function(PIN_SCK,GPIO_FUNC_SPI);
    gpio_set_function(PIN_MOSI,GPIO_FUNC_SPI);
    /* GP12 is RESET, not SPI RX. */
    spi_set_format(LCD_SPI,8,SPI_CPOL_0,SPI_CPHA_0,SPI_MSB_FIRST);
    gpio_put(PIN_RESET,1); sleep_ms(100);
    gpio_put(PIN_RESET,0); sleep_ms(100);
    gpio_put(PIN_RESET,1); sleep_ms(100);
    for(unsigned i=0;i<sizeof(gc9a01_init)/sizeof(gc9a01_init[0]);++i) {
        command(gc9a01_init[i].reg,gc9a01_init[i].data,gc9a01_init[i].count);
        if(gc9a01_init[i].delay_ms) sleep_ms(gc9a01_init[i].delay_ms);
    }
    /* MX+MY rotates the image by 180 degrees, preserving BGR order. */
#if CLOCK_LCD_ROTATION == 180
    static const uint8_t direction=0xc8;
#else
    static const uint8_t direction=0x08;
#endif
    command(0x36,&direction,1);
    gpio_set_function(PIN_BACKLIGHT,GPIO_FUNC_PWM);
    uint slice=pwm_gpio_to_slice_num(PIN_BACKLIGHT);
    pwm_config cfg=pwm_get_default_config();
    pwm_config_set_wrap(&cfg,9999);
    pwm_config_set_clkdiv(&cfg,1.0f); /* 12.5 kHz at 125 MHz (RP2040), 15 kHz at 150 MHz (RP2350). */
    pwm_init(slice,&cfg,true);
    pwm_set_gpio_level(PIN_BACKLIGHT,0); /* Enable after the first complete frame. */
}
void lcd_present(const uint16_t *frame) {
    static const uint8_t window[]={0,0,0,239};
    command(0x2a,window,4); command(0x2b,window,4);
    command(0x2c,0,0);
    gpio_put(PIN_CS,0); gpio_put(PIN_DC,1);
    /* RGB565 values in CPU order; 16-bit SPI shifts the MSB first. */
    spi_set_format(LCD_SPI,16,SPI_CPOL_0,SPI_CPHA_0,SPI_MSB_FIRST);
    spi_write16_blocking(LCD_SPI,frame,240*240);
    while(spi_is_busy(LCD_SPI)) tight_loop_contents();
    gpio_put(PIN_CS,1);
    spi_set_format(LCD_SPI,8,SPI_CPOL_0,SPI_CPHA_0,SPI_MSB_FIRST);
}

