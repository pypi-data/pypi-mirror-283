"""
An MQTT handler for the Python logging module.

This handler sends log messages to an MQTT broker.
Reconnects automatically if the connection is lost
and publishes messages in a background thread.
"""
from __future__ import annotations

import atexit
import json
import logging
from typing import Any, Callable, Literal

import paho.mqtt.client as mqtt


class MQTTHandler(logging.Handler):
    """An MQTT handler for the Python logging module."""

    def __init__(
        self,
        host: str,
        topic: str,
        port: int = 1883,
        keepalive: int = 60,
        bind_address: str = '',
        client_id: str = '',
        userdata: Any = None,
        protocol: mqtt.MQTTProtocolVersion = mqtt.MQTTProtocolVersion.MQTTv5,
        qos: int = 0,
        transport: Literal['tcp', 'websockets', 'unix'] = 'tcp',
        use_tls: bool | str = False,
        username: str = '',
        password: str = '',
        append_logger_name: bool = False,
        connected_topic: str = '',
        connected_callback: Callable[[], None] | None = None,
        disconnected_callback: Callable[[], None] | None = None,
        extra_data: dict[str, str | float | int | None] | None = None,
    ):
        super().__init__()

        self._topic = topic
        self._qos = qos
        self._append_logger_name = append_logger_name
        self._connected_topic = connected_topic
        self._connected_callback = connected_callback
        self._disconnected_callback = disconnected_callback
        self.extra_data = extra_data

        self.mqtt = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=client_id,
            userdata=userdata,
            protocol=protocol,
            transport=transport)

        if use_tls:
            self.mqtt.tls_set()
            if use_tls == 'insecure':
                self.mqtt.tls_insecure_set(True)

        if username:
            self.mqtt.username_pw_set(username, password)

        self.mqtt.on_connect = self._on_connect
        if self._connected_topic:
            # This must be set before connecting
            self.mqtt.will_set(
                self._connected_topic, '{"state": "disconnected"}', qos=1, retain=True)

        try:
            self.mqtt.connect_async(
                host=host,
                port=port,
                keepalive=keepalive,
                bind_address=bind_address)
        except Exception:
            print(f"Failed to connect to MQTT broker at {host}:{port}")
            return
        atexit.register(self.mqtt.loop_stop)
        self.mqtt.loop_start()

    def _on_connect(
        self,
        client: mqtt.Client,
        userdata: Any,
        connect_flags: mqtt.ConnectFlags,
        reason_code: mqtt.ReasonCode,
        properties: mqtt.Properties | None = None,
    ) -> None:
        if self._connected_topic:
            client.publish(
                self._connected_topic, '{"state": "connected"}', qos=1, retain=True)
        if not reason_code.is_failure and self._connected_callback is not None:
            self._connected_callback()

    def _on_disconnect(
        self,
        client: mqtt.Client,
        userdata: Any,
        connect_flags: mqtt.ConnectFlags,
        reason_code: mqtt.ReasonCode,
        properties: mqtt.Properties | None = None,
    ) -> None:
        if self._disconnected_callback is not None:
            self._disconnected_callback()

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log message to the MQTT broker."""
        try:
            if (
                self.mqtt.logger
                and record.name == self.mqtt.logger.name
            ):
                # Avoid sending log messages of the MQTT client itself
                return
            if self._append_logger_name:
                topic = f"{self._topic}/{record.name.replace('.', '/')}"
            else:
                topic = self._topic

            msg = self.format(record)
            payload = {
                "timestamp": record.created,
                "message": msg,
                "raw_message": record.message,
                "level": record.levelname,
                "name": record.name,
            }
            if self.extra_data:
                payload.update(self.extra_data)

            _ = self.mqtt.publish(
                topic=topic,
                payload=json.dumps(payload),
                qos=self._qos)
            self.flush()
        except Exception:
            self.handleError(record)
