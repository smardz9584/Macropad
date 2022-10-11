import microcontroller
import time
import board
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode


led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

pins = [
    board.GP0,  # przycisk 3
    board.GP2,  # przycisk 2
    board.GP4,  # przycisk 1
    board.GP6,  # przycisk 6
    board.GP8,  # przycisk 5
    board.GP10,  # przycisk 4
    board.GP12,  # przycisk 9
    board.GP14,  # przycisk 8
    board.GP16,  # przycisk 7
    board.GP19,  # przycisk 0

]

MEDIA = 1
KEY = 2
COM = 3

keymap = {
    (0): (COM, (Keycode.CONTROL, Keycode.V)),  # 3
    (1): (COM, (Keycode.CONTROL, Keycode.C)),  # 2
    (2): (COM, (Keycode.CONTROL, Keycode.X)),  # 1
    (3): (COM, (Keycode.GUI, Keycode.D)),  # 6
    (4): (MEDIA, ConsumerControlCode.PLAY_PAUSE),  # 5
    (5): (COM, (Keycode.ALT, Keycode.F4)),  # 4
    (6): (MEDIA, ConsumerControlCode.VOLUME_INCREMENT),  # 9
    (7): (MEDIA, ConsumerControlCode.MUTE),  # 8
    (8): (MEDIA, ConsumerControlCode.VOLUME_DECREMENT),  # 7
    (9): (KEY, ()),  # 0

}
switches = [0, 2, 4, 6,
            8, 10, 12, 14, 16, 19]

for i in range(10):
    switches[i] = DigitalInOut(pins[i])
    switches[i].direction = Direction.INPUT
    switches[i].pull = Pull.UP

switch_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

while True:
    if all(switch_state) == 1:
        kbd.release(*keymap[button][1])
        microcontroller.on_next_reset(microcontroller.RunMode.BOOTLOADER)
        microcontroller.reset()
        kbd.release(*keymap[button][1])
    elif all(switch_state) != 1:
        for button in range(10):
            if switch_state[button] == 0:
                if not switches[button].value:
                    try:
                        if keymap[button][0] == KEY:
                            kbd.press(*keymap[button][1])
                        elif keymap[button][0] == COM:
                            kbd.send(*keymap[button][1])
                        else :
                            cc.send(keymap[button][1])
                    except ValueError:  # deals w six key limit
                        pass
                    switch_state[button] = 1

            if switch_state[button] == 1:
                if switches[button].value:
                    try:
                        if keymap[button][0] == KEY:
                            kbd.release(*keymap[button][1])

                    except ValueError:
                        pass
                    switch_state[button] = 0
    time.sleep(0.001)
