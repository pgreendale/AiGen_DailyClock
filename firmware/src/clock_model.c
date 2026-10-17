#include "clock_model.h"
#include "clock_assets.h"
#include <math.h>
#define TAU 6.283185307179586476925286766559
static double wrap_hours(double seconds) {
    double h=fmod(seconds/3600.0,24.0); return h<0?h+24:h;
}
static double primitive(const double *p,double u) {
    return p[0]*u+p[1]*u*u/2+p[2]*u*u*u/3+p[3]*u*u*u*u/4;
}
static double integral_from_first_knot(double z) {
    double turns=floor(z/24),x=z-turns*24;
    unsigned i=(unsigned)(x*4); if(i>95) i=95;
    double u=(x-i*.25)*4;
    return turns+clock_model_prefix[i]+.25*primitive(clock_model_coefficients[i],u);
}
static double original_cdf(double h) {
    return integral_from_first_knot(h-.125)-clock_model_origin;
}
static double original_density(double h) {
    double x=h-.125; if(x<0) x+=24;
    unsigned i=(unsigned)(x*4); if(i>95) i=95;
    double u=(x-i*.25)*4; const double *p=clock_model_coefficients[i];
    return ((p[3]*u+p[2])*u+p[1])*u+p[0];
}
double clock_angle(double seconds) {
    if(!isfinite(seconds)) return 0;
    double h=wrap_hours(seconds),f=original_cdf(h);
    double g=h<=12?.5*f/clock_model_half_mass:.5+.5*(f-clock_model_half_mass)/(1-clock_model_half_mass);
    return TAU*fmin(1.0,fmax(0.0,g));
}
double clock_density(double seconds) {
    if(!isfinite(seconds)) return 0;
    double h=wrap_hours(seconds);
    return .5*original_density(h)/(h<12?clock_model_half_mass:1-clock_model_half_mass);
}
double clock_density_normalized(double seconds) {
    double v=clock_density(seconds)/clock_model_max_density;
    if(!isfinite(v)||v<0) return 0;
    return v>1?1:v;
}
uint16_t clock_hand_colour(double seconds) {
    double v=clock_density_normalized(seconds);
    unsigned i=(unsigned)(v*256); if(i>255) i=255;
    return clock_palette[i];
}



double clock_second_angle(double seconds) {
    if(!isfinite(seconds)) return 0;
    double phase=fmod(seconds,60.0);
    if(phase<0) phase+=60;
    return TAU*floor(phase)/60.0;
}
