# /usr/bin/env python3

import fxcg


def edit_string(x: int, y: int):
    start = 0
    cursor = 0

    buffer = ""

    DisplayMBString(buffer, start, cursor, x, y)

    key = 0
    while True:
        key = GetKey()

        if key == KEY_CTRL_EXE or key == KEY_CTRL_EXIT:
            return buffer

        if key and key < 30000:
            buffer, cursor = EditMBStringChar(buffer, cursor, key)
            DisplayMBString(buffer, start, cursor, x, y)
        else:
            buffer, start, cursor, key = EditMBStringCtrl(buffer, start, cursor, key, x, y)


def ask_question(msg: str):
    fill: display_fill = (0, 383, 144, 168, 0)
    Bdisp_AreaClr(fill, True)
    PrintXY(1, 6, msg)
    return edit_string(1, 7)


buf = ""

Bdisp_EnableColor(0)
Bdisp_AllClr_VRAM()

PrintXY(1, 1, "Stop!")
PrintMini(0, 32, "Who would cross the Bridge of Death")
PrintMini(0, 56, "must answer me these questions three,")
PrintMini(0, 80, "ere the other side is he.")
PrintXY(1, 5, "What... is")

while True:
    buf = ask_question("your name?")
    buf = ask_question("your quest?")
    buf = ask_question("your favorite color?")
