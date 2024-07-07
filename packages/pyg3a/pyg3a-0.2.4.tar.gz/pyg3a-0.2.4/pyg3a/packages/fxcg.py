#!/usr/bin/env python3

import fxcg.app
import fxcg.display
import fxcg.file
import fxcg.heap
import fxcg.keyboard
import fxcg.misc
import fxcg.registers
import fxcg.rtc
import fxcg.serial
import fxcg.system
import fxcg.tmu
import fxcg.usb

def PrintXY(x: int, y: int, message: str, mode: int = 0, color: int = 0) -> None:
    return f'PrintXY({x}, {y}, (String("  ") + {message}).c_str(), {mode}, {color})'


def EditMBStringChar(MB_string: str, xpos: int, char_to_insert: int) -> tuple[str, int]:
    @struct_c_func
    def _EditMBStringChar(MB_string: str, xpos: int, char_to_insert: int) -> tuple[str, int]:
        return """
        String new_str = String(MB_string, MB_string.length() + 1);
        int cursor = EditMBStringChar((unsigned char*) new_str.c_str(), MB_string.length() + 1, xpos, char_to_insert);
        return {new_str, cursor};
        """

    return f'_EditMBStringChar({MB_string}, {xpos}, {char_to_insert})'


def DisplayMBString(buffer: str, start: int, cursor: int, x: int, y: int) -> None:
    return f'DisplayMBString((unsigned char*) {buffer}.c_str(), {start}, {cursor}, {x}, {y})'


def EditMBStringCtrl(MB_string: str, start: int, xpos: int, key: int, x: int, y: int, posmax: int = 256) -> tuple[str, int, int, int]:
    @struct_c_func
    def _EditMBStringCtrl(MB_string: str, start: int, xpos: int, key: int, x: int, y: int, posmax: int) -> tuple[str, int, int, int]:
        return """
        String new_str = String(MB_string, posmax);
        EditMBStringCtrl((unsigned char*) new_str.c_str(), posmax, &start, &xpos, &key, x, y);
        return {new_str, start, xpos, key};
        """

    return f'_EditMBStringCtrl({MB_string}, {start}, {xpos}, {key}, {x}, {y}, {posmax})'


def PrintMini(x: int, y: int, string: str, mode_flags: int = 0, xlimit: int = 0xFFFFFFFF, color: int = 0,
              back_color: int = 0xFFFF, writeflag: int = 1, *, P6: int = 0, P7: int = 0, P11: int = 0) -> tuple[
    int, int]:
    @struct_c_func
    def _PrintMini(x: int, y: int, string: str, mode_flags: int, xlimit: int, color: int, back_color: int,
                   writeflag: int, P6: int, P7: int, P11: int) -> tuple[int, int]:
        return """
        int xpos = x;
        int ypos = y;
        PrintMini(&xpos, &ypos, string.c_str(), mode_flags, (unsigned int) xlimit, P6, P7, color, back_color, writeflag, P11);
        return {xpos, ypos};
        """

    return f'_PrintMini({x}, {y}, {string}, {mode_flags}, {xlimit}, {color}, {back_color}, {writeflag}, {P6}, {P7}, {P11})'


def Bdisp_AreaClr(area: display_fill, target: bool, color: color = 0) -> None:
    return f'Bdisp_AreaClr(&{area}, {target}, {color})'


def SetGetkeyToMainFunctionReturnFlag(enabled: bool) -> None:
    """
    CODE (originally) BY SIMON LOTHAR, AVAILABLE ON "fx_calculators_SuperH_based.chm" version 16
    the function assumes, that the RAM-pointer to GetkeyToMainFunctionReturnFlag is loaded
    immediately by a "Move Immediate Data"-instruction
    """

    @c_func
    def _SetGetkeyToMainFunctionReturnFlag(enabled: bool) -> None:
        return """
        int addr, addr2;

        // get the pointer to the syscall table
        addr = *(unsigned char*)0x80020071;     // get displacement

        addr++;
        addr *= 4;
        addr += 0x80020070;
        addr = *(unsigned int*)addr;

        if ( addr < (int)0x80020070 ) return;
        if ( addr >= (int)0x81000000 ) return;

        // get the pointer to syscall 1E99
        addr += 0x1E99*4;
        if ( addr < (int)0x80020070 ) return;
        if ( addr >= (int)0x81000000 ) return;

        addr = *(unsigned int*)addr;
        if ( addr < (int)0x80020070 ) return;
        if ( addr >= (int)0x81000000 ) return;

        switch ( *(unsigned char*)addr ){
                case 0xD0 : // MOV.L @( disp, PC), Rn (REJ09B0317-0400 Rev. 4.00 May 15, 2006 page 216)
                case 0xD1 :
                case 0xD2 :
                case 0xD3 :
                case 0xD4 :
                case 0xD5 :
                case 0xD6 :
                case 0xD7 :
                case 0xD8 :
                        addr2 = *(unsigned char*)( addr + 1 );  // get displacement
                        addr2++;
                        addr2 *= 4;
                        addr2 += addr;
                        addr2 &= ~3;

                        if ( addr2 < (int)0x80020070 ) return;
                        if ( addr2 >= (int)0x81000000 ) return;

                        addr = *(unsigned int*)addr2;
                        if ( ( addr & 0xFF000000 ) != 0x88000000 && ( addr & 0xFF000000 ) != 0x8C000000 ) return; // MODIFIED for CG50 or CG10/20 (memory address change)

                        // finally perform the desired operation and set the flag:
                        if ( enabled ) *(unsigned char*)addr = 0;
                        else *(unsigned char*)addr = 3;

                        break;

                default : addr = 0x100;
        }
        """

    return f'_SetGetkeyToMainFunctionReturnFlag({enabled})'


def Timer_Install(handler: Callable[[], any], elapse: int, internal_timer_id: int = 0) -> int:
    return f'Timer_Install({internal_timer_id}, {handler}, {elapse})'


def PowerOff(display_logo: bool = True) -> None:
    return f'PowerOff({display_logo})'


def GetLatestUserInfo() -> tuple[str, str, str]:
    @struct_c_func
    def _GetLatestUserInfo() -> tuple[str, str, str]:
        return """
        // Search through user info
        char *flagpointer = (char *) 0x80BE0000;
        int counter = 0;
        while (*flagpointer == 0x0F) {
            flagpointer = flagpointer + 0x40;
            counter++;
        }

        // Set password from latest info
        if (counter) {
            flagpointer = flagpointer - 0x40;
            if(*(flagpointer + 0x2C) != '\\0') {
                return {String(flagpointer + 0x04), String(flagpointer + 0x18), String(flagpointer + 0x2C)};
            }
        }
        
        // Otherwise return blank strings
        return {String(), String(), String()};
        """

    return f'_GetLatestUserInfo()'


def GetKey(key: int = None) -> int:
    if key:
        return f'GetKey(&{key})'

    @c_func
    def _GetKey() -> int:
        return """
        int _tmp_var;
        GetKey(&_tmp_var);
        return _tmp_var;
        """

    return f'_GetKey()'


def GetKeyWait_OS(type_of_waiting: int = 0, timeout_period: int = 0, menu: int = 0) -> tuple[int, int, int]:
    @struct_c_func
    def _GetKeyWait_OS(type_of_waiting: int, timeout_period: int, menu: int) -> tuple[int, int, int]:
        return """
        int column, row;
        unsigned short keycode;
        GetKeyWait_OS(&column, &row, type_of_waiting, timeout_period, menu, &keycode);
        return {column, row, (int) keycode};
        """

    return f'_GetKeyWait_OS({type_of_waiting}, {timeout_period}, {menu})'


def GetMainBatteryVoltage() -> int:
    return "GetMainBatteryVoltage(1)"


def __registry_types_pyg3a() -> dict[str, tuple[str, TypeCategory]]:
    PY_C_TYPES: dict[str, tuple[str, TypeCategory]] = {}
    PY_C_TYPES["color"] = ("color_t", TypeCategory.INTEGERS)

    return PY_C_TYPES
