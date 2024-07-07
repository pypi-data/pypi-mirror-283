#!/usr/bin/env python3

import casioplot
import fxcg

set_pixel(100, 50, (255, 0, 0))
set_pixel(101, 50, (255, 0, 0))
set_pixel(102, 50, (255, 0, 0))
set_pixel(100, 51, (255, 0, 0))
set_pixel(100, 52, (255, 0, 0))
set_pixel(101, 52, (255, 0, 0))
set_pixel(102, 52, (255, 0, 0))

GetKey()

clear_screen()

GetKey()

draw_string(100, 50, "Hello", (0, 255, 0), "large")
