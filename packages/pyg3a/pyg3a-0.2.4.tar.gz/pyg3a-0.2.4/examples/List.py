#!/usr/bin/env python3

import fxcg

str_list: list[str] = ["hello", "bye", "hi"]
str_list.insert(1, "hello")
str_list.pop(3)

PrintXY(1, 1, str_list[0])
PrintXY(1, 2, str_list[1])
PrintXY(1, 3, str_list[2])
PrintXY(1, 4, str_list[3])
