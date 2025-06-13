import logging

import agentql
import pytest
from playwright.async_api import Page as AsyncPage
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

from .configs import (
    ScriptConfig,
    chromeAppConfig,
)

log = logging.getLogger(__name__)


def get_test_id(config: ScriptConfig) -> str:
    """This function is used to generate test ids for pytest"""
    return config.name


@pytest.fixture
def individual_config() -> ScriptConfig:
    """This fixture is used to test a single script in a single test"""
    # any script can be used here
    return chromeAppConfig


def test_individual_script_sync(
    individual_config: ScriptConfig,
):
    """This test runs a single script"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page: AsyncPage = agentql.wrap(browser.new_page())

        page.add_init_script(individual_config.script)
        page.goto(individual_config.url)
        response = page.query_data(individual_config.query)

        try:
            for key, value in response.items():
                assert value == "True"
        except AssertionError:
            page.screenshot(
                path=f"tests/e2e/screenshots/{individual_config.name}_sync.png",
                full_page=True,
            )
            raise AssertionError(f"Test failed: {key} is {value}")
        finally:
            page.close()
            browser.close()


@pytest.mark.asyncio
async def test_individual_script_async(individual_config: ScriptConfig):
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
                path=f"tests/e2e/screenshots/{individual_config.name}_async.png",
                full_page=True,
            )
            raise AssertionError(f"Test failed: {key} is {value}")
        finally:
            await page.close()
            await browser.close()
