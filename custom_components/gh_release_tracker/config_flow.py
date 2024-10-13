import voluptuous as vol
import logging
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class GitHubConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        _LOGGER.debug("Fetching options flow for entry: %s", config_entry)
        return GitHubOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        _LOGGER.debug("Starting user step with input: %s", user_input)

        if user_input is not None:
            repository = user_input.get("repository")
            _LOGGER.debug("User input for repository: %s", repository)

            # Extract repository owner and name from the URL
            if "github.com" in repository:
                repository = repository.replace("https://", "").replace("http://", "").replace("www.", "")
                repository = repository.split("github.com/")[-1]
                _LOGGER.debug("Formatted repository as: %s", repository)
            elif '/' in repository:
                _LOGGER.debug("Got a valid input without full URL. Formatted repository as: %s", repository)
            else:
                _LOGGER.error("Invalid repository format. Please provide a valid GitHub repository URL.")
                return self.async_show_form(
                    step_id="user",
                    data_schema=vol.Schema({
                        vol.Required("repository"): str
                    }),
                    errors={"repository": "Invalid format. Please provide a GitHub URL."}
                )

            title = repository.replace('/', ' ')  # Format title as "RepoOwner RepoName"
            _LOGGER.debug("Creating config entry for repository: %s", repository)
            return self.async_create_entry(title=title, data={"repository": repository})

        _LOGGER.debug("Showing form to user")
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("repository"): str
            })
        )

class GitHubOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        _LOGGER.debug("Initializing options flow for entry: %s", config_entry)
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        _LOGGER.debug("Starting options step init with input: %s", user_input)
        return self.async_show_form(step_id="init", data_schema=vol.Schema({}))
