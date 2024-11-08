import pytest
import agentql
import logging
from playwright.sync_api import sync_playwright, Page as SyncPage
from playwright.async_api import async_playwright, Page as AsyncPage
from playwright_stealth import stealth_sync, stealth_async
from .configs import (
    ScriptConfig,
    chromeAppConfig,
    chromeCsiConfig,
    chromeLoadTimesConfig,
    chromePluginConfig,
    chromeRuntimeConfig,
    generateMagicArraysConfig,
    iFrameContentWindowConfig,
    mediaCodecsConfig,
    navigatorHardWareConcurrencyConfig,
    navigatorLanguagesConfig,
    navigatorPermissionsConfig,
    navigatorPluginsConfig,
    navigatorUserAgentConfig,
    navigatorVendorConfig,
    navigatorWebDriverConfig,
    webGLVendorConfig,
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

        page.add_init_script(config.script)
        stealth_sync(page)
        page.goto(config.url)
        response = page.query_data(config.query)

        try:
            for key, value in response.items():
                assert value == "True"
        except AssertionError:
            page.screenshot(
                path=f"tests/e2e/screenshots/{config.name}.png", full_page=True
            )
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

        await page.add_init_script(config.script)
        await stealth_async(page)
        await page.goto(config.url)
        response = await page.query_data(config.query)

        try:
            for key, value in response.items():
                assert value == "True"
        except AssertionError:
            await page.screenshot(
                path=f"tests/e2e/screenshots/{config.name}.png", full_page=True
            )
            raise AssertionError(f"Test failed: {key} is {value}")
        finally:
            await page.close()
            await browser.close()
