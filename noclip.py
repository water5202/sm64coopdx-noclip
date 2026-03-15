import pymem
import pymem.process
import time
import sys
import keyboard
import math

enabled = False
speed = 0.5
try:
    pm = pymem.Pymem("sm64coopdx.exe")
except:
    print("open the process")
    time.sleep(3)
    sys.exit()

module = pymem.process.module_from_name(pm.process_handle, "sm64coopdx.exe")
base = module.lpBaseOfDll

Y = base + 0x3525CA8 # offset for Y
X = base + 0x3525CAC # offset for X
Z = base + 0x3525CA4 # offset for Z

def patch(enable):
    YController = base + 0x91481 # patch to remove Y going down if airborne

    if enable:
        pm.write_bytes(YController, b"\x90\x90\x90\x90", 4)
    else:
        pm.write_bytes(YController, b"\x0F\x13\x43\x64", 4)

patch(False)

while True:
    if enabled:
        x = pm.read_float(X)
        y = pm.read_float(Y)
        z = pm.read_float(Z)
        
        if keyboard.is_pressed('w'):
            z += speed
        if keyboard.is_pressed('s'):
            z -= speed
        if keyboard.is_pressed('a'):
            x -= speed
        if keyboard.is_pressed('d'):
            x += speed
        if keyboard.is_pressed('space'):
            y += speed
        if keyboard.is_pressed('Ctrl'):
            y -= speed
            
        pm.write_float(X, x)
        pm.write_float(Y, y)
        pm.write_float(Z, z) 


    if keyboard.is_pressed('F8'):
        enabled = not enabled
        patch(enabled)
        if enabled:
            print("noclip enabled")
        else:            print("noclip disabled")
        time.sleep(0.5)
    
    if keyboard.is_pressed('U'):
        speed += 0.5
        time.sleep(0.5)
    
    if keyboard.is_pressed('P'):
        speed -= 0.5
        time.sleep(0.5)
    
