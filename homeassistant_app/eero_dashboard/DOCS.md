# eero Dashboard

The eero Dashboard opens in the Home Assistant sidebar through ingress. Home Assistant handles access authentication.

The app's own local authentication is off by default for this ingress-only setup. Turn it on in the add-on options if you want a second login.

The add-on uses Home Assistant's MQTT service when available. MQTT discovery creates dashboard sensors and eero client presence trackers automatically. Configure a broker such as Mosquitto and enable the Home Assistant MQTT integration first.
