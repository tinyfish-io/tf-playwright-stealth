import pytest
import agentql
from playwright.sync_api import sync_playwright, Page as SyncPage
from playwright.async_api import async_playwright, Page as AsyncPage
from .configs import (
    TestConfig,
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

test_configs = [
    chromeAppConfig,
    chromeCsiConfig,
    chromeLoadTimesConfig,
]

"""
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
"""


@pytest.fixture
def individual_config():
    return chromeAppConfig


@pytest.fixture
def multiple_configs():
    return [chromeAppConfig, chromeCsiConfig, chromeLoadTimesConfig]


def get_test_id(config):
    return config.name


@pytest.mark.parametrize("config", test_configs, ids=get_test_id)
def test_runner_sync(config: TestConfig):
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
async def test_runner_async(config: TestConfig):
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


@pytest.mark.skip
@pytest.mark.asyncio
async def test_individual_script(individual_config: TestConfig):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page: AsyncPage = await agentql.wrap_async(browser.new_page())
        # await page.add_init_script(individual_config.script)
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


@pytest.mark.skip
@pytest.mark.asyncio
async def test_multiple_scripts(multiple_configs: list[TestConfig]):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page: AsyncPage = await agentql.wrap_async(browser.new_page())
        for config in multiple_configs:
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
        await page.close()
        await browser.close()
