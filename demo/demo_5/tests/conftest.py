"""Python configuration file for Pytest framework."""
from lib.logging_plugin import LogPlugin


def pytest_configure(config):
    """Configure pytest plugin ."""
    config.pluginmanager.register(LogPlugin(config), "logplugin")