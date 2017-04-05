#!/usr/bin/env python2

import logging
import time
from threading import Thread

import cli_args as cli
import dothat.backlight as backlight
import dothat.lcd as lcd
import dothat.touch as nav
from constants import MQTT_HOST, LOG_LEVEL
from mqtt_connection import MqttConnection
from utils import setup_logging, waitForKeyboardInterrupt

from heading_publisher import CALIBRATION_BY_VALUES

logger = logging.getLogger(__name__)

# Constants
LIDAR_FRONT_LEFT = "lidar/left/mm"
LIDAR_FRONT_RIGHT = "lidar/right/mm"
CAMERA_1_VALUE = "camera/gear/x"
CAMERA_1_ALIGNMENT = "camera/gear/alignment"
HEADING_CALIBRATION = "heading/calibration"
HEADING_DEGREES = "heading/degrees"
NOT_SEEN = "not_seen"
NOT_ALIGNED = "not_aligned"
ALIGNED = "aligned"

CAMERA = "camera"
LIDARL = "lidarl"
LIDARR = "lidarr"
HEADINGD = "headingd"
HEADINGC = "headingc"

lidar_l = ""
lidar_r = ""
camera_v = ""
camera_a = ""
heading_c = ""
heading_d = ""

# default sensor
selected_sensor = HEADINGC

# lcd initialization
lcd.clear()
backlight.rgb(255, 255, 255)
lcd.set_contrast(45)
lcd.clear()


def on_connect(mqtt_client, userdata, flags, rc):
    logger.info("Connected with result code: %s", rc)
    mqtt_client.subscribe(LIDAR_FRONT_LEFT)
    mqtt_client.subscribe(LIDAR_FRONT_RIGHT)
    mqtt_client.subscribe(CAMERA_1_VALUE)
    mqtt_client.subscribe(CAMERA_1_ALIGNMENT)
    mqtt_client.subscribe(HEADING_DEGREES)
    mqtt_client.subscribe(HEADING_CALIBRATION)


def on_message(mqtt_client, userdata, msg):
    global lidar_r, lidar_l, camera_a, camera_v, heading_d, heading_c
    # Payload is a string byte array
    val = bytes.decode(msg.payload)
    logger.info("%s : %s", msg.topic, val)

    if msg.topic == LIDAR_FRONT_LEFT:
        logger.info("LCD Lidar L: " + val)
        lidar_l = val

    elif msg.topic == LIDAR_FRONT_RIGHT:
        logger.info("LCD Lidar R: " + val)
        lidar_r = val


    elif msg.topic == CAMERA_1_VALUE:
        logger.info("LCD Camera Value: " + val)
        camera_v = val

    elif msg.topic == CAMERA_1_ALIGNMENT:
        logger.info("LCD Camera Alignment: " + val)
        camera_a = val

    elif msg.topic == HEADING_CALIBRATION:
        logger.info("LCD Calibration: " + val)
        heading_c = val

    elif msg.topic == HEADING_DEGREES:
        logger.info("LCD Degrees: " + val)
        heading_d = val


def lcd_display(delay):
    global lidar_r, lidar_l, camera_a, camera_v, heading_d, heading_c
    while True:
        if selected_sensor == LIDARL:
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Lidar Left")
            lcd.set_cursor_position(0, 2)
            lcd.write(lidar_l + " mm")
            if lidar_l == "-1" and lidar_r == "-1":
                backlight.rgb(255, 0, 0)
            else:
                backlight.rgb(255, 255, 255)

        elif selected_sensor == LIDARR:
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Lidar Right")
            lcd.set_cursor_position(0, 2)
            lcd.write(lidar_r + " mm")
            if lidar_l == "-1" and lidar_r == "-1":
                backlight.rgb(255, 0, 0)
            else:
                backlight.rgb(255, 255, 255)

        elif selected_sensor == CAMERA:
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Camera")
            lcd.set_cursor_position(0, 2)
            lcd.write(camera_v)
            if camera_a == NOT_SEEN:
                backlight.rgb(255, 0, 0)
            elif camera_a == NOT_ALIGNED:
                backlight.rgb(0, 0, 255)
            elif camera_a == ALIGNED:
                backlight.rgb(0, 255, 0)

        elif selected_sensor == HEADINGC:
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Calibration")
            lcd.set_cursor_position(0, 2)
            lcd.write(heading_c)
            if heading_c == CALIBRATION_BY_VALUES:
                backlight.rgb(0, 255, 0)
            else:
                backlight.rgb(255, 255, 255)

        elif selected_sensor == HEADINGD:
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Degrees")
            lcd.set_cursor_position(0, 2)
            lcd.write(heading_d)

        time.sleep(delay)


@nav.on(nav.LEFT)
def handle_left(ch, evt):
    global selected_sensor
    selected_sensor = LIDARL
    logger.info("Left Lidar Display")
    lcd.clear()
    backlight.rgb(255, 255, 255)
    lcd.set_cursor_position(0, 0)
    lcd.write("Left Lidar")
    lcd.set_cursor_position(0, 2)


@nav.on(nav.RIGHT)
def handle_right(ch, evt):
    global selected_sensor
    selected_sensor = LIDARR
    logger.info("Right Lidar")
    lcd.clear()
    backlight.rgb(255, 255, 255)
    lcd.set_cursor_position(0, 0)
    lcd.write("Right Lidar")
    lcd.set_cursor_position(0, 2)


@nav.on(nav.BUTTON)
def handle_button(ch, evt):
    global selected_sensor
    selected_sensor = CAMERA
    logger.info("Camera")
    lcd.clear()
    backlight.rgb(255, 255, 255)
    lcd.set_cursor_position(0, 0)
    lcd.write("Camera")
    lcd.set_cursor_position(0, 2)


@nav.on(nav.UP)
def handle_button(ch, evt):
    global selected_sensor
    selected_sensor = HEADINGC
    logger.info("Calibration")
    lcd.clear()
    backlight.rgb(255, 255, 255)
    lcd.set_cursor_position(0, 0)
    lcd.write("Calibration")
    lcd.set_cursor_position(0, 2)


@nav.on(nav.DOWN)
def handle_button(ch, evt):
    global selected_sensor
    selected_sensor = HEADINGD
    logger.info("Degrees")
    lcd.clear()
    backlight.rgb(255, 255, 255)
    lcd.set_cursor_position(0, 0)
    lcd.write("Degrees")
    lcd.set_cursor_position(0, 2)


if __name__ == "__main__":
    # Parse CLI args
    args = cli.setup_cli_args(cli.mqtt_host, cli.verbose)

    # Setup logging
    setup_logging(level=args[LOG_LEVEL])

    Thread(target=lcd_display, args=(0.1,)).start()

    # Setup MQTT client
    with MqttConnection(args[MQTT_HOST],
                        userdata={},
                        on_connect=on_connect,
                        on_message=on_message):
        waitForKeyboardInterrupt()

    logger.info("Exiting...")