# -*- coding: utf-8 -*-
from playwright.async_api import Page as AsyncPage
from playwright.sync_api import Page as SyncPage
from playwright_stealth.core.stealth_config import StealthConfig


def stealth_sync(page: SyncPage, config: StealthConfig = None):
    """teaches synchronous playwright Page to be stealthy like a ninja!"""
    scripts = []

    for script in (config or StealthConfig()).enabled_scripts:
        scripts.append(script)

    combined_script = "\n".join(scripts)

    page.add_init_script(combined_script)


async def stealth_async(page: AsyncPage, config: StealthConfig = None):
    """teaches asynchronous playwright Page to be stealthy like a ninja!"""
    scripts = []

    for script in (config or StealthConfig()).enabled_scripts:
        scripts.append(script)

    combined_script = "\n".join(scripts)

    await page.add_init_script(combined_script)
