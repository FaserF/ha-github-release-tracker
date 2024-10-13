from datetime import timedelta
import logging
import aiohttp

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

SCAN_INTERVAL = timedelta(hours=5)
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    _LOGGER.debug("Setting up sensor entry for repository: %s", config_entry.data['repository'])
    
    coordinator = GitHubReleaseCoordinator(hass, config_entry.data['repository'])
    try:
        await coordinator.async_config_entry_first_refresh()
    except UpdateFailed as e:
        _LOGGER.error("Failed to fetch initial data: %s", e)
        raise ConfigEntryNotReady(f"Could not fetch data: {e}")

    async_add_entities([GitHubReleaseSensor(coordinator)], True)

class GitHubReleaseCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, repository: str):
        _LOGGER.debug("Initializing GitHubReleaseCoordinator for repository: %s", repository)
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)
        self.repository = repository

    async def _async_update_data(self):
        url = f"https://api.github.com/repos/{self.repository}/releases/latest"
        _LOGGER.debug("Fetching data from GitHub API for repository: %s", self.repository)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                _LOGGER.debug("Received response with status: %s", response.status)

                if response.status != 200:
                    _LOGGER.error("Error fetching data: %s", response.status)
                    raise UpdateFailed(f"Error fetching GitHub release data: {response.status}")

                release_data = await response.json()
                _LOGGER.debug("Release data received: %s", release_data)

                # Remove "v" if present in the version
                version = release_data.get('tag_name', '')
                if version.startswith('v'):
                    version = version[1:]

                _LOGGER.debug("Parsed release version: %s", version)

                return {
                    "version": version,
                    "html_url": release_data.get('html_url', 'Unknown'),
                    "title": release_data.get('name', 'Unknown'),
                    "published_at": release_data.get('published_at', 'Unknown'),
                    "prerelease": release_data.get('prerelease', False)
                }

class GitHubReleaseSensor(SensorEntity):
    def __init__(self, coordinator: GitHubReleaseCoordinator):
        _LOGGER.debug("Initializing GitHubReleaseSensor for repository: %s", coordinator.repository)
        self.coordinator = coordinator
        self._unique_id = self.generate_unique_id(coordinator.repository)

    @property
    def name(self):
        return f"GitHub Latest Release {self.coordinator.repository}"

    @property
    def unique_id(self):
        return self._unique_id

    def generate_unique_id(self, repository: str) -> str:
        # Split the repository string into owner and repo name
        owner, repo = repository.split('/')
        # Generate unique ID in the format: sensor.github_release_owner_repo
        return f"sensor.github_release_{owner}_{repo}"

    @property
    def state(self):
        _LOGGER.debug("Returning sensor state: %s", self.coordinator.data['version'])
        return self.coordinator.data['version']

    @property
    def extra_state_attributes(self):
        _LOGGER.debug("Returning extra state attributes")
        return {
            "html_url": self.coordinator.data['html_url'],
            "release_title": self.coordinator.data['title'],
            "published_at": self.coordinator.data['published_at'],
            "prerelease": self.coordinator.data['prerelease']
        }

    @property
    def should_poll(self):
        return False

    async def async_update(self):
        _LOGGER.debug("Updating GitHubReleaseSensor")
        await self.coordinator.async_request_refresh()

    @property
    def available(self):
        _LOGGER.debug("Checking availability: %s", self.coordinator.last_update_success)
        return self.coordinator.last_update_success
