/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

// # This Source Code Form is subject to the terms of the Mozilla Public
// # License, v. 2.0. If a copy of the MPL was not distributed with this
// # file, You can obtain one at https://mozilla.org/MPL/2.0/.

// <!-- This Source Code Form is subject to the terms of the Mozilla Public
//    - License, v. 2.0. If a copy of the MPL was not distributed with this
//    - file, You can obtain one at https://mozilla.org/MPL/2.0/. -->

// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

`timescale 1ns/1ps


package gg_fpga;

typedef enum bit[1:0] {
    STATIC = 0,
    BOUNCE_BACK = 1,
    HIT_WIDTH_SHIFT = 2
} trigger_mode_t;

endpackage
