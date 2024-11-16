import asyncio
import logging
import random

from playwright.async_api import ProxySettings, async_playwright
from playwright_stealth import stealth_async
from playwright_stealth.core import StealthConfig, BrowserType


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

PROXIES: list[ProxySettings] = [
    # TODO: replace with your own proxies
    # {
    #     "server": "...",
    #     "username": "...",
    #     "password": "...",
    # },
]


async def main():
    proxy: ProxySettings | None = random.choice(PROXIES) if PROXIES else None

    async with async_playwright() as playwright, await playwright.chromium.launch(
        headless=False,
    ) as browser:
        context = await browser.new_context(proxy=proxy)
        page = await context.new_page()
        await stealth_async(page, config=StealthConfig(browser_type=BrowserType.CHROME))

        await page.goto("https://bot.sannysoft.com/")

        await page.wait_for_timeout(30000)


if __name__ == "__main__":
    asyncio.run(main())
