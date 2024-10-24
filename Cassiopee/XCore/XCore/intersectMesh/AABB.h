#pragma once

#include "xcore.h"

struct AABB {
    E_Float xmin;
    E_Float ymin;
    E_Float zmin;
    E_Float xmax;
    E_Float ymax;
    E_Float zmax;
};

const AABB AABB_HUGE = {EFLOATMIN, EFLOATMIN, EFLOATMIN,
                        EFLOATMAX, EFLOATMAX, EFLOATMAX};

void AABB_clamp(AABB &box, const AABB &parent);