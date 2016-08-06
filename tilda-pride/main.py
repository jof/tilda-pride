### Author: jof
### Description: Pride
### License: WTFPL
### Appname: tilda-pride
### Built-in: no

import pyb
import buttons
import ugfx
import dialogs
from imu import IMU
from database import database_get

MAIN_LOOP_POLL_TIME = 300
FLAG_CHOICE = {}

def draw():
    ugfx.clear(0)
    # Draw flag.    
    ugfx.display_image(0,0,FLAG_CHOICE['file'])
    # Draw name
    display_name = database_get("display-name", "")
    display_name = display_name + " "
    ugfx.set_default_font(ugfx.FONT_NAME)
    name_color = ugfx.html_color(FLAG_CHOICE['name_color'])
    ugfx.text(FLAG_CHOICE['x_pos'],FLAG_CHOICE['y_pos'],display_name,name_color)

def pick_your_pride():
    flags = [
            {
             "title": "Pansexual",
             "file": "pansexual.gif",
             "name_color": 0xFFFFFF,
             "x_pos": 20, "y_pos": 95
            },
            {
             "title": "Bisexual",
             "file": "bisexual.gif",
             "name_color": 0xFFFFFF,
             "x_pos": 20, "y_pos": 95
            },
            {
             "title": "Queer/Pride",
             "file": "pride.gif",
             "name_color": 0xFF00FF,
             "x_pos": 20, "y_pos": 95
            },
            {
             "title": "Ally",
             "file": "ally.gif",
             "name_color": 0xFF0000,
             "x_pos": 20, "y_pos": 100
            },
            {
             "title": "Trans",
             "file": "trans.gif",
             "name_color": 0x006400,
             "x_pos": 20, "y_pos": 95
            },
            {
             "title": "Asexual",
             "file": "ace.gif",
             "name_color": 0x4B0082,
             "x_pos": 20, "y_pos": 121
            },
            {
             "title": "Bear",
             "file": "bear.gif",
             "name_color": 0xDA70D6,
             "x_pos": 20, "y_pos": 175 
            }
            ]
    choice = dialogs.prompt_option(flags)
    global FLAG_CHOICE
    filepath = "/flash/apps/tilda-pride/{}".format(choice['file'])
    choice['file'] = filepath
    FLAG_CHOICE = choice

def initial_setup():
    global imu
    imu = IMU()
    buttons.init()
    ugfx.init()
    ugfx.clear()
    global last_orientation
    last_orientation = get_orientation()
    update_orientation()
    pick_your_pride()
    draw()

def get_orientation():
    return imu.get_acceleration()['y'] < 0

def update_orientation():
    global last_orientation
    updated = False
    ival = imu.get_acceleration()
    orientation = get_orientation()
    if orientation and not last_orientation:
        ugfx.orientation(0)
        updated = True
    elif not orientation and last_orientation:
        ugfx.orientation(180)
        updated = True
    last_orientation = orientation
    return updated


initial_setup()
while True:
    if buttons.is_triggered("BTN_B"):
        pick_your_pride()
        draw()
    if update_orientation():
        draw()
    pyb.delay(MAIN_LOOP_POLL_TIME)
