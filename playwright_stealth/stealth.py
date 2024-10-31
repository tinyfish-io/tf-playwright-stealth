# -*- coding: utf-8 -*-
from typing import Union
from playwright.async_api import Page as AsyncPage
from playwright.sync_api import Page as SyncPage
from playwright_stealth.core import StealthConfig
from playwright_stealth.properties import Properties


def combine_scripts(properties: Properties, config: StealthConfig):
    """Combines the scripts for the page based on the properties and config."""

    scripts = []
    config = StealthConfig()

    for script in config.enabled_scripts(properties):
        scripts.append(script)
    return "\n".join(scripts)


def generate_stealth_headers(properties: Properties, page: Union[AsyncPage, SyncPage]):
    """Generates the stealth headers for the page by replacing the original headers with the spoofed ones for every request."""
    page.route(
        "**/*", lambda route: route.continue_(headers=properties.as_dict()["header"])
    )


def stealth_sync(page: SyncPage, config: StealthConfig = None):
    """teaches synchronous playwright Page to be stealthy like a ninja!"""
    properties = Properties()
    combined_script = combine_scripts(properties, config)
    generate_stealth_headers(properties, page)

    page.add_init_script(combined_script)


async def stealth_async(page: AsyncPage, config: StealthConfig = None):
    """teaches asynchronous playwright Page to be stealthy like a ninja!"""
    properties = Properties()
    combined_script = combine_scripts(properties, config)
    generate_stealth_headers(properties, page)

    await page.add_init_script(combined_script)
