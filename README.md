# GitHub Release Tracker Home Assistant Integration

Home Assistant Integration to track the latest GitHub Repository releases. This does not require a sign in. But still is less effektive as https://www.home-assistant.io/integrations/github/ 

## Installation
### 1. Using HACS (recommended way)

Not available in HACS yet, but it is planned.

### 2. Manual

- Download the latest zip release from [here](https://github.com/your-repo/ha-github-release-tracker/releases/latest).
- Extract the zip file.
- Copy the folder "github_release_tracker" from within `custom_components` with all of its components to `<config>/custom_components/`.

where `<config>` is your Home Assistant configuration directory.

> **NOTE**: Do not download the file by using the link above directly; the status in the "master" branch can be in development and therefore may not work as expected.

## Configuration

Go to Configuration -> Integrations and click on "add integration." Then search for "GitHub Release Tracker."

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=gh_release_tracker)

### Configuration Variables

- **GitHub Repository**: Enter the full GitHub repository link or owner/repository name (e.g., `owner/repo`).
  
## Sensor Attributes

The data is updated every 5 hours by default.

### Main attributes

- **version**: The latest release version (the leading "v" is removed if present).
- **release_title**: The title of the latest release.
- **download_url**: The direct download link for the latest release.

## Automation Example

### Example 1: Notify on New Release

Send a notification whenever a new release is available.

```yaml
automation:
  - alias: "New GitHub Release Notification"
    trigger:
      - platform: state
        entity_id: sensor.github_release_tracker_repo
    action:
      - service: notify.notify
        data:
          message: >
            New release available for {{ states.sensor.github_release_tracker_repo.attributes.repository }}:
            Version: {{ states.sensor.github_release_tracker_repo.state }}
            Title: {{ states.sensor.github_release_tracker_repo.attributes.release_title }}
            Download: {{ states.sensor.github_release_tracker_repo.attributes.download_url }}

## Bug reporting
Open an issue over at [github issues](https://github.com/FaserF/ha-github-release-tracker/issues). Please prefer sending over a log with debugging enabled.

To enable debugging enter the following in your configuration.yaml

```yaml
logger:
    logs:
        custom_components.gh_release_tracker: debug
```

You can then find the log in the HA settings -> System -> Logs -> Enter "GitHub Release Tracker" in the search bar -> "Load full logs"

## Thanks to
Thanks to GitHub for providing the platform for open-source collaboration!

The data is coming from the GitHub API.
