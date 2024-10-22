import pytest
import agentql
import logging
from playwright.sync_api import sync_playwright, Page as SyncPage
from playwright.async_api import async_playwright, Page as AsyncPage
from .configs import (
    MultipleScriptConfig,
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


def extract_query_lines(query_str) -> list[str]:
    """This function is used to extract the query lines from the query string"""
    lines = query_str.strip().splitlines()
    return [
        line.strip()
        for line in lines
        if line.strip() and not line.startswith("{") and not line.endswith("}")
    ]


def join_query_lines(query_lines) -> str:
    """This function is used to join the query lines into a single query"""
    combined_lines = list(dict.fromkeys(query_lines))  # remove duplicates
    combined_query = "{\n\t" + "\n\t".join(combined_lines) + "\n}"
    return combined_query


@pytest.fixture
def multiple_configs():
    """This fixture is used to test multiple scripts in a single test"""
    config_options = {
        chromeAppConfig: True,
        chromeCsiConfig: True,
        chromeLoadTimesConfig: True,
        chromePluginConfig: True,
        chromeRuntimeConfig: False,
        generateMagicArraysConfig: False,  # this script does nothing visible in bot.sannysoft.com
        iFrameContentWindowConfig: False,  # this script does nothing visible in bot.sannysoft.com
        mediaCodecsConfig: False,  # this script does nothing visible in bot.sannysoft.com
        navigatorHardWareConcurrencyConfig: False,  # this script does nothing visible in bot.sannysoft.com
        navigatorLanguagesConfig: False,  # this script does nothing visible in bot.sannysoft.com
        navigatorPermissionsConfig: False,  # this script does nothing visible in bot.sannysoft.com
        navigatorPluginsConfig: False,
        navigatorUserAgentConfig: False,
        navigatorVendorConfig: False,  # this script does nothing visible in bot.sannysoft.com
        navigatorWebDriverConfig: False,  # this script does nothing visible in bot.sannysoft.com
        webGLVendorConfig: False,  # this script does visible in bot.sannysoft.com
    }
    query_lines = []
    scripts = []
    for config, use_config in config_options.items():
        if use_config:
            scripts.append(config.script)
            query_lines += extract_query_lines(config.query)

    combined_query = join_query_lines(query_lines)

    log.debug(f"Combined query: {combined_query}")
    return MultipleScriptConfig(
        name="multiple_scripts_test",
        script=scripts,
        query=combined_query,
        url="https://bot.sannysoft.com/",
    )


def test_multiple_scripts(multiple_configs: MultipleScriptConfig):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page: AsyncPage = agentql.wrap(browser.new_page())

        for script in multiple_configs.script:
            page.add_init_script(script)
        page.goto(multiple_configs.url)
        response = page.query_data(multiple_configs.query)

        try:
            for key, value in response.items():
                assert value == "True"
        except AssertionError:
            page.screenshot(
                path=f"tests/screenshots/{multiple_configs.name}_sync.png",
                full_page=True,
            )
            raise AssertionError(f"Test failed: {key} is {value}")

        page.close()
        browser.close()


@pytest.mark.asyncio
async def test_multiple_scripts(multiple_configs: MultipleScriptConfig):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page: AsyncPage = await agentql.wrap_async(browser.new_page())

        for script in multiple_configs.script:
            await page.add_init_script(script)
        await page.goto(multiple_configs.url)
        response = await page.query_data(multiple_configs.query)

        try:
            for key, value in response.items():
                assert value == "True"
        except AssertionError:
            await page.screenshot(
                path=f"tests/screenshots/{multiple_configs.name}_async.png",
                full_page=True,
            )
            raise AssertionError(f"Test failed: {key} is {value}")

        await page.close()
        await browser.close()
