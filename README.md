# eero Dashboard for Home Assistant

This repository contains the editable source for the eero Dashboard Home Assistant app. The installable app entry is in [Gamerz32/Gamerz32-HA-Apps](https://github.com/Gamerz32/Gamerz32-HA-Apps), the **Gamerz32 Home Assistant Apps** repository.

## Features

- View WAN throughput, network health, connected clients, mesh nodes, bufferbloat, internet and cloud status, and per-device presence.
- Publish eero telemetry and device presence to Home Assistant through MQTT discovery.
- Open the dashboard from the Home Assistant sidebar through ingress; the app does not expose a host port.
- Supports amd64 and aarch64. The Lenovo ThinkCentre M720q uses amd64.

## Install in Home Assistant

1. Open **Settings → Apps → App Store → Repositories**.
2. Add the **Gamerz32 Home Assistant Apps** repository: https://github.com/Gamerz32/Gamerz32-HA-Apps
3. Refresh the app store and install **eero Dashboard**.
4. Start the app and open **eero Dashboard** from the Home Assistant sidebar.

The app's entry in the app store uses Home Assistant ingress, which provides sidebar access and Home Assistant authentication. See the [Home Assistant ingress documentation](https://developers.home-assistant.io/docs/apps/presentation/).

## First run and MQTT

Sign in with the Amazon account already linked to eero, or use email/SMS verification if your eero account supports it. For Amazon sign-in, open Amazon from the dashboard, sign in on Amazon, then copy the full address shown after Amazon returns and paste it back into the dashboard. Your Amazon password is entered only on Amazon. The dashboard sends the short-lived, one-use authorization code to Amazon and eero to create the eero session, then clears it. The eero cloud API is required; an existing eero token and network ID are optional advanced settings.

Enable a Home Assistant MQTT broker and the MQTT integration to create sensors and device trackers. When the Supervisor provides an MQTT service, the app uses its connection details. Dashboard data and its saved eero session are stored in the app's persistent data directory and included in Home Assistant app backups.

## Edit the source and update the app

Make application changes in this repository and push them to its main branch. The Home Assistant app package in [Gamerz32/Gamerz32-HA-Apps](https://github.com/Gamerz32/Gamerz32-HA-Apps) downloads this repository's main branch during its image build.

After a source change, bump the version in **eero_dashboard/config.yaml** in the app-store repository and update the app in Home Assistant. The version change triggers a rebuild from the latest source. The Home Assistant host needs internet access to GitHub and Python package indexes during the build.

## Original project, documentation, and license

The dashboard is based on Enrico Flammini's [eero Custom Dashboard & Mesh Management Suite](https://github.com/EnricoFlammini/Dashboard_EERO), distributed under the MIT license. This is an independent community project and is not affiliated with eero or Amazon.

The previous full project README, including the standalone Docker and Docker Compose instructions and extended feature reference, is preserved in [UPSTREAM_README.md](UPSTREAM_README.md). For Home Assistant installation and configuration, use this README and the [app setup guide](https://github.com/Gamerz32/Gamerz32-HA-Apps/blob/main/eero_dashboard/README.md).
