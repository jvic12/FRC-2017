#!/usr/bin/env python3

import argparse
import logging

import cli_args as cli
from constants import MQTT_HOST, TOPIC, MQTT_TOPIC
from mqtt_connection import MqttConnection
from utils import setup_logging, waitForKeyboardInterrupt

logger = logging.getLogger(__name__)


def on_connect(mqtt_client, userdata, flags, rc):
    logging.info("Connected with result code: {0}".format(rc))
    # Subscribe to all broker messages
    mqtt_client.subscribe(userdata[TOPIC])


def on_message(mqtt_client, userdata, msg):
    logger.info("{0} : {1}".format(msg.topic, msg.payload))


if __name__ == "__main__":
    # Parse CLI args
    parser = argparse.ArgumentParser()
    cli.mqtt_host(parser),
    cli.mqtt_topic(parser),
    args = vars(parser.parse_args())

    # Setup logging
    setup_logging()

    with MqttConnection(args[MQTT_HOST],
                        userdata={TOPIC: args[MQTT_TOPIC]},
                        on_connect=on_connect,
                        on_message=on_message):
        waitForKeyboardInterrupt()

    logger.info("Exiting...")
