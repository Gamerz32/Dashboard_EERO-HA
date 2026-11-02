# eero Dashboard Home Assistant OS add-on

This folder contains a Supervisor app (formerly called an add-on) for Home Assistant OS. It builds the dashboard from this repository, so the Home Assistant packaging and the application source stay together.

## Install

1. In Home Assistant, open **Settings → Apps**.
2. Open the top-right menu and choose **Repositories**.
3. Add this repository URL: https://github.com/Gamerz32/Dashboard_EERO-HA
4. Refresh the app store, select **eero Dashboard**, and install it.
5. Start the app. The **eero Dashboard** entry appears in the Home Assistant sidebar.

The Lenovo ThinkCentre M720q uses the supported amd64 architecture. The add-on also supports aarch64.

The app builds the current main branch from this repository during installation. No separate image registry or Docker Hub credentials are needed. If you edit the dashboard source or app package, push the changes to the repository and increase version in config.yaml so Home Assistant rebuilds the app.

## First run and eero access

Home Assistant ingress provides the sidebar access and authentication. The dashboard's own local authentication is off by default for this ingress-only setup; you can turn it on in the options if you want an additional login. The dashboard handles eero sign-in and any verification requested by the eero account. An optional eero token and network ID are available for advanced setups; most users should leave them blank.

The app stores its database, login session, logs, and history under the add-on's persistent /data directory.

## Home Assistant MQTT entities

The add-on requests the configured Home Assistant MQTT service (mqtt:want). If a broker is available, it reads the broker host and port and uses its service credentials. MQTT discovery is enabled by default, and the dashboard publishes WAN, network-health, client-count, mesh-node, Internet/cloud status sensors, plus per-device presence trackers.

If no MQTT service is available, the dashboard still runs and logs that MQTT is disabled. Install/configure an MQTT broker and the Home Assistant MQTT integration, or enter a manual broker host and credentials in the app options. The current dashboard MQTT client does not support TLS brokers.

## Source and limitations

- The add-on uses Home Assistant ingress, so its panel is shown inside the HA sidebar without opening a host port or adding panel_iframe YAML.
- The app only accepts requests through Home Assistant's ingress proxy plus its internal health check; it does not expose a direct host port.
- The add-on Dockerfile clones this public repository while building. Home Assistant needs outbound access to GitHub and Python package indexes during the build.
- The app is isolated from the host Docker socket. Its Docker-container management and auto-update features therefore are not available in this add-on.

## Attribution

The dashboard application is based on the upstream eero Custom Dashboard & Mesh Management Suite by Enrico Flammini: https://github.com/EnricoFlammini/Dashboard_EERO, distributed under the repository's MIT license. This repository preserves the upstream application and provides the Home Assistant OS packaging and integration changes.
