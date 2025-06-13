import json
import logging

import agentql
import pytest
from playwright.async_api import Page as AsyncPage
from playwright.async_api import async_playwright
from playwright.sync_api import Page as SyncPage
from playwright.sync_api import sync_playwright

from playwright_stealth.properties import Properties
from tests.utils import from_file

from .configs import (
    ScriptConfig,
    chromeAppConfig,
    chromeCsiConfig,
    chromeLoadTimesConfig,
    chromePluginConfig,
    chromeRuntimeConfig,
    navigatorUserAgentConfig,
)

log = logging.getLogger(__name__)


# The goal for these tests is to run them all, not comment them out.
# Some scripts don't work yet so we will wait until there are fixes for them.
test_configs = [
    chromeAppConfig,
    chromeCsiConfig,
    chromeLoadTimesConfig,
    chromePluginConfig,
    chromeRuntimeConfig,
    # generateMagicArraysConfig, # this script does nothing visible in bot.sannysoft.com
    # iFrameContentWindowConfig, # this script does nothing visible in bot.sannysoft.com
    # mediaCodecsConfig, # this script does nothing visible in bot.sannysoft.com
    # navigatorHardWareConcurrencyConfig, # this script does nothing visible in bot.sannysoft.com
    # navigatorLanguagesConfig, # this script does nothing visible in bot.sannysoft.com
    # navigatorPermissionsConfig, # this script does nothing visible in bot.sannysoft.com
    # navigatorPluginsConfig, # this script does nothing visible in bot.sannysoft.com
    navigatorUserAgentConfig,
    # navigatorVendorConfig, # this script does nothing visible in bot.sannysoft.com
    # navigatorWebDriverConfig, # this script does nothing visible in bot.sannysoft.com
    # webGLVendorConfig, # this script does visible in bot.sannysoft.com
]


def get_test_id(config: ScriptConfig) -> str:
    """This function is used to generate test ids for pytest"""
    return config.name


@pytest.mark.parametrize("config", test_configs, ids=get_test_id)
def test_all_scripts_sync(config: ScriptConfig):
    """This test runs all the scripts in a synchronous manner"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page: SyncPage = agentql.wrap(browser.new_page())

        utils_script = from_file("utils.js")
        magic_arrays_script = from_file("generate.magic.arrays.js")

        properties = Properties()
        opts = json.dumps(properties.as_dict())
        opts = f"const opts = {opts}"

        combined_script = opts + "\n" + utils_script + "\n" + magic_arrays_script + "\n" + config.script

        page.add_init_script(combined_script)
        page.goto(config.url)
        response = page.query_data(config.query)

        try:
            for key, value in response.items():
                assert value == "True"
        except AssertionError:
            page.screenshot(path=f"tests/e2e/screenshots/{config.name}.png", full_page=True)
            raise AssertionError(f"Test failed: {key} is {value}")
        finally:
            page.close()
            browser.close()


@pytest.mark.asyncio
@pytest.mark.parametrize("config", test_configs, ids=get_test_id)
async def test_all_scripts_async(config: ScriptConfig):
    """This test runs all the scripts in an asynchronous manner"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page: AsyncPage = await agentql.wrap_async(browser.new_page())

        utils_script = from_file("utils.js")
        magic_arrays_script = from_file("generate.magic.arrays.js")

        properties = Properties()
        opts = json.dumps(properties.as_dict())
        opts = f"const opts = {opts}"

        combined_script = opts + "\n" + utils_script + "\n" + magic_arrays_script + "\n" + config.script

        await page.add_init_script(combined_script)
        await page.goto(config.url)
        response = await page.query_data(config.query)

        try:
            for key, value in response.items():
                assert value == "True"
        except AssertionError:
            await page.screenshot(path=f"tests/e2e/screenshots/{config.name}.png", full_page=True)
            raise AssertionError(f"Test failed: {key} is {value}")
        finally:
            await page.close()
            await browser.close()
