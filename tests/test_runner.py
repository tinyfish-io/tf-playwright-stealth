import pytest
import agentql
import logging
from playwright.sync_api import sync_playwright, Page as SyncPage
from playwright.async_api import async_playwright, Page as AsyncPage
from .configs import (
    ScriptConfig,
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


def get_test_id(config: ScriptConfig) -> str:
    """This function is used to generate test ids for pytest"""
    return config.name


@pytest.fixture
def individual_config():
    """This fixture is used to test a single script in a single test"""
    # any script can be used here
    return chromeAppConfig


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


@pytest.mark.parametrize("config", test_configs, ids=get_test_id)
def test_runner_sync(config: ScriptConfig):
    """This test runs all the scripts in a synchronous manner"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page: SyncPage = agentql.wrap(browser.new_page())

        page.add_init_script(config.script)
        page.goto(config.url)
        response = page.query_data(config.query)

        try:
            for key, value in response.items():
                assert value == "True"
        except AssertionError:
            page.screenshot(path=f"tests/screenshots/{config.name}.png", full_page=True)
            raise AssertionError(f"Test failed: {key} is {value}")
        finally:
            page.close()
            browser.close()


@pytest.mark.asyncio
@pytest.mark.parametrize("config", test_configs, ids=get_test_id)
async def test_runner_async(config: ScriptConfig):
    """This test runs all the scripts in an asynchronous manner"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page: AsyncPage = await agentql.wrap_async(browser.new_page())

        await page.add_init_script(config.script)
        await page.goto(config.url)
        response = await page.query_data(config.query)

        try:
            for key, value in response.items():
                assert value == "True"
        except AssertionError:
            await page.screenshot(
                path=f"tests/screenshots/{config.name}.png", full_page=True
            )
            raise AssertionError(f"Test failed: {key} is {value}")
        finally:
            await page.close()
            await browser.close()


@pytest.mark.asyncio
async def test_individual_script(individual_config: ScriptConfig):
    """This test runs a single script"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page: AsyncPage = await agentql.wrap_async(browser.new_page())

        await page.add_init_script(individual_config.script)
        await page.goto(individual_config.url)
        response = await page.query_data(individual_config.query)

        try:
            for key, value in response.items():
                assert value == "True"
        except AssertionError:
            await page.screenshot(
                path=f"tests/screenshots/no-scripts.png", full_page=True
            )
            raise AssertionError(f"Test failed: {key} is {value}")
        finally:
            await page.close()
            await browser.close()


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
                path=f"tests/screenshots/{multiple_configs.name}.png", full_page=True
            )
            raise AssertionError(f"Test failed: {key} is {value}")

        await page.close()
        await browser.close()
