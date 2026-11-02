"""Translate Home Assistant app options into eero Dashboard environment variables."""

from __future__ import annotations

import grp
import json
import os
import pwd
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

OPTIONS_PATH = Path("/data/options.json")
APP_COMMAND = [
    "/opt/venv/bin/uvicorn",
    "app.main:app",
    "--host",
    "0.0.0.0",
    "--port",
    "8000",
    "--workers",
    "1",
    "--log-level",
    "info",
]

OPTION_ENV = {
    "eero_user_token": "EERO_USER_TOKEN",
    "eero_network_id": "EERO_NETWORK_ID",
    "dashboard_lang": "DASHBOARD_LANG",
    "poll_interval": "POLL_INTERVAL",
    "tz": "TZ",
    "require_local_auth": "REQUIRE_LOCAL_AUTH",
    "admin_user": "ADMIN_USER",
    "admin_password": "ADMIN_PASSWORD",
    "mqtt_enabled": "MQTT_ENABLED",
    "mqtt_broker_host": "MQTT_BROKER_HOST",
    "mqtt_broker_port": "MQTT_BROKER_PORT",
    "mqtt_username": "MQTT_USERNAME",
    "mqtt_password": "MQTT_PASSWORD",
    "mqtt_base_topic": "MQTT_BASE_TOPIC",
    "mqtt_ha_discovery_prefix": "MQTT_HA_DISCOVERY_PREFIX",
    "mqtt_discovery_enabled": "MQTT_DISCOVERY_ENABLED",
    "mqtt_publish_interval": "MQTT_PUBLISH_INTERVAL",
}


def _as_env_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _read_options() -> dict[str, Any]:
    try:
        with OPTIONS_PATH.open(encoding="utf-8") as options_file:
            options = json.load(options_file)
    except FileNotFoundError:
        return {}
    if not isinstance(options, dict):
        raise ValueError(f"{OPTIONS_PATH} must contain a JSON object")
    return options


def _read_mqtt_service() -> dict[str, Any] | None:
    token = os.environ.get("SUPERVISOR_TOKEN")
    if not token:
        return None

    request = urllib.request.Request(
        "http://supervisor/services/mqtt",
        headers={"Authorization": f"Bearer {token}"},
    )
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            service = json.load(response)
    except (OSError, urllib.error.URLError, json.JSONDecodeError):
        return None

    return service if isinstance(service, dict) else None


def _configure_environment(options: dict[str, Any]) -> None:
    for key, environment_key in OPTION_ENV.items():
        if key in options:
            os.environ[environment_key] = _as_env_value(options[key])

    os.environ["DATA_DIR"] = "/data"
    os.environ["HA_INGRESS_ONLY"] = "true"

    if os.environ.get("MQTT_ENABLED", "false").lower() not in {"true", "1", "yes"}:
        return

    manual_host = str(options.get("mqtt_broker_host", "")).strip()
    if manual_host:
        return

    service = _read_mqtt_service()
    if service and service.get("host"):
        if service.get("ssl", False):
            print(
                "MQTT service uses TLS, which this dashboard MQTT client does not currently support; MQTT publishing is disabled.",
                file=sys.stderr,
                flush=True,
            )
            os.environ["MQTT_ENABLED"] = "false"
            return

        os.environ["MQTT_BROKER_HOST"] = str(service["host"])
        os.environ["MQTT_BROKER_PORT"] = str(service.get("port", 1883))
        if not options.get("mqtt_username"):
            os.environ["MQTT_USERNAME"] = str(service.get("username", ""))
        if not options.get("mqtt_password"):
            os.environ["MQTT_PASSWORD"] = str(service.get("password", ""))
        return

    print(
        "No Home Assistant MQTT service was found. MQTT publishing is disabled until a broker is configured.",
        file=sys.stderr,
        flush=True,
    )
    os.environ["MQTT_ENABLED"] = "false"


def main() -> None:
    options = _read_options()
    _configure_environment(options)

    # Read the Supervisor token as root, then remove it before the app process starts.
    os.environ.pop("SUPERVISOR_TOKEN", None)

    app_user = pwd.getpwnam("appuser")
    app_group = grp.getgrnam("appgroup")
    os.chown("/data", app_user.pw_uid, app_group.gr_gid)

    su_exec = shutil.which("su-exec")
    if not su_exec:
        raise RuntimeError("su-exec is not installed in the add-on image")

    os.execvpe(
        su_exec,
        [su_exec, "appuser", *APP_COMMAND],
        os.environ.copy(),
    )


if __name__ == "__main__":
    main()
