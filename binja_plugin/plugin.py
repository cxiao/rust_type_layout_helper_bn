from binaryninja.log import Logger
from binaryninja.plugin import PluginCommand

from . import actions

logger = Logger(session_id=0, logger_name=__name__)

PLUGIN_NAME = "Rust Type Layout Helper"

plugin_commands = [
    (
        f"{PLUGIN_NAME}\\Load File...",
        "Load a new type layout file",
        actions.action_load_type_layout_file,
    )
]


def plugin_init():
    for command_name, command_description, command_action in plugin_commands:
        PluginCommand.register(
            name=command_name, description=command_description, action=command_action
        )
