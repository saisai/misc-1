
#include "postgres.h"
#include "fmgr.h"
#include <math.h>

#ifdef PG_MODULE_MAGIC
PG_MODULE_MAGIC;
#endif

const double M_D2R = M_PI/180.0;  // degree to radian
const double M_R2D = 180.0/M_PI;  // radian to degree

static inline double fclamp(double x, double min, double max)
{
    if(x < min) return min;
    if(x > max) return max;
    return x;
}

static void loc2pos(text *txtloc, double *lat, double *lng)
{
  char loc[6];
  memcpy(loc, VARDATA(txtloc), 6);

  *lat = (double) (loc[5] - 'A') * (1.0 / 24.0);
  *lng = (double) (loc[4] - 'A') * (2.0 / 24.0);

  *lat += (double) (loc[3] - '0') * 1.0;
  *lng += (double) (loc[2] - '0') * 2.0;

  *lat += (double) (loc[1] - 'J') * 10.0;
  *lng += (double) (loc[0] - 'J') * 20.0;
}

int dist(text *arg1, text *arg2)
{
  double latref, lngref;
  loc2pos(arg1, &latref, &lngref);

  double lat, lng;
  loc2pos(arg2, &lat, &lng);

  double
    a = (90.0 - lat) * M_D2R,
    b = (90.0 - latref) * M_D2R,
    gamma = (lng - lngref) * M_D2R,
    t = cos(a) * cos(b) + sin(a) * sin(b) * cos(gamma);

  t = fclamp(t, -1.0, +1.0);

  return (int4) (acos(t) * 111.2 * M_R2D + 0.99);
}
