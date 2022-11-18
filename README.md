# Macropad
the code for a macropad I've made with raspberry pi pico 

To use the code that is written in CircuitPython, first you have to flash CircuitPython .UF2 file onto the pico itself. Then you have to install Adafruit-HID libraries onto the system.
I will include the .UF2 files in the repository.
Here is the link to the repo with adafruit HID
https://github.com/adafruit/Adafruit_CircuitPython_HID.git

The macropad is built with a 3D printed case, the switches are put inside, ground wire is soldered to the right pin of each switch and then connected to the GND on the Pico,
I soldered individual wires to the left pin on each switch that connected to the usable pins on the Pico.
