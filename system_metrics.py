"""Track total message throughput over mqtt"""

import argparse
import logging
import time
from threading import Lock
from threading import Thread

import cli_args as cli
from constants import MQTT_HOST
from mqtt_connection import MqttConnection
from utils import sleep

messages = 0

LOCK = "lock"
MESSAGES = "messages"

logger = logging.getLogger(__name__)


def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code: {0}".format(rc))
    client.subscribe("#")
    Thread(target=average_publisher, args=(client, userdata)).start()


def on_message(client, userdata, msg):
    with userdata[LOCK]:
        userdata[MESSAGES] += 1


def average_publisher(client, userdata):
    while True:
        try:
            time.sleep(1)
            payload = str(userdata[MESSAGES]).encode("utf-8")
            client.publish("metrics/msg_rate", payload=payload, qos=0)
            client.publish("logging/metrics/msg_rate", payload=payload, qos=0)
            with userdata[LOCK]:
                userdata[MESSAGES] = 0
        except BaseException as e:
            logger.error("Failure in publish_locations() [e]".format(e), exc_info=True)
            time.sleep(1)


if __name__ == "__main__":
    # Parse CLI args
    parser = argparse.ArgumentParser()
    cli.mqtt_host(parser)
    args = vars(parser.parse_args())

    # Setup MQTT client
    mqtt_conn = MqttConnection(args[MQTT_HOST],
                               userdata={LOCK: Lock(),
                                         MESSAGES: 0},
                               on_connect=on_connect,
                               on_message=on_message)
    mqtt_conn.connect()

    try:
        sleep()
    except KeyboardInterrupt:
        pass
    finally:
        mqtt_conn.disconnect()

    logger.info("Exiting...")
