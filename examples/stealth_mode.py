import asyncio
import logging
import random

from playwright.async_api import Geolocation, ProxySettings, async_playwright
from playwright_stealth import stealth_async
from playwright_stealth.core import StealthConfig, BrowserType


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

BROWSER_IGNORED_ARGS = [
    "--enable-automation",
    "--disable-extensions",
]
BROWSER_ARGS = [
    "--disable-xss-auditor",
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-blink-features=AutomationControlled",
    "--disable-features=IsolateOrigins,site-per-process",
    "--disable-infobars",
]


LOCATIONS = [
    ("America/New_York", Geolocation(longitude=-74.006, latitude=40.7128)),  # New York, NY
    ("America/Chicago", Geolocation(longitude=-87.6298, latitude=41.8781)),  # Chicago, IL
    ("America/Los_Angeles", Geolocation(longitude=-118.2437, latitude=34.0522)),  # Los Angeles, CA
    ("America/Denver", Geolocation(longitude=-104.9903, latitude=39.7392)),  # Denver, CO
    ("America/Phoenix", Geolocation(longitude=-112.0740, latitude=33.4484)),  # Phoenix, AZ
    ("America/Anchorage", Geolocation(longitude=-149.9003, latitude=61.2181)),  # Anchorage, AK
    ("America/Detroit", Geolocation(longitude=-83.0458, latitude=42.3314)),  # Detroit, MI
    ("America/Indianapolis", Geolocation(longitude=-86.1581, latitude=39.7684)),  # Indianapolis, IN
    ("America/Boise", Geolocation(longitude=-116.2023, latitude=43.6150)),  # Boise, ID
    ("America/Juneau", Geolocation(longitude=-134.4197, latitude=58.3019)),  # Juneau, AK
]

REFERERS = ["https://www.google.com", "https://www.bing.com", "https://duckduckgo.com"]

ACCEPT_LANGUAGES = ["en-US,en;q=0.9", "en-GB,en;q=0.9", "fr-FR,fr;q=0.9"]
PROXIES: list[ProxySettings] = [
    # TODO: replace with your own proxies
    # {
    #     "server": "...",
    #     "username": "...",
    #     "password": "...",
    # },
]


async def main():
    header_dnt = random.choice(["0", "1"])
    location = random.choice(LOCATIONS)
    referer = random.choice(REFERERS)
    accept_language = random.choice(ACCEPT_LANGUAGES)
    proxy: ProxySettings | None = random.choice(PROXIES) if PROXIES else None

    async with async_playwright() as playwright, await playwright.chromium.launch(
        headless=False,
        args=BROWSER_ARGS,
        ignore_default_args=BROWSER_IGNORED_ARGS,
    ) as browser:
        context = await browser.new_context(
            proxy=proxy,
            locale="en-US,en,ru",
            timezone_id=location[0],
            extra_http_headers={
                "Accept-Language": accept_language,
                "Referer": referer,
                "DNT": header_dnt,
                "Connection": "keep-alive",
                "Accept-Encoding": "gzip, deflate, br",
            },
            geolocation=location[1],
            permissions=["notifications"],
            viewport={
                "width": 1920 + random.randint(-50, 50),
                "height": 1080 + random.randint(-50, 50),
            },
        )

        page = await context.new_page()
        await stealth_async(page, config=StealthConfig(browser_type=BrowserType.CHROME))

        # Following URLs are different websites that can be used to test the stealth mode

        await page.goto("https://bot.sannysoft.com/")

        await page.wait_for_timeout(30000)


if __name__ == "__main__":
    asyncio.run(main())
