import pytest
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync


@pytest.mark.skip(
    "This test is meant to be ran manually, wrapped under a pytest test so it is not automatically ran."
)
def test_demo_with_stealth():
    """This test demonstrates how to use playwright-stealth with playwright"""

    executablePath = "C:\\Google\\Chrome\\Application\\chrome.exe"
    ipAndPort = "221.1.90.67:9000"
    args = [
        "--no-sandbox",
        "--disable-infobars",
        "--lang=zh-CN",
        "--start-maximized",
        "--window-position=-10,0",
        # '--proxy-server=http=' + ipAndPort
    ]

    ignoreDefaultArgs = ["--enable-automation"]
    headless = False

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=executablePath,
            args=args,
            ignore_default_args=ignoreDefaultArgs,
            headless=headless,
        )
        page = browser.new_page()
        stealth_sync(page)
        page.goto("https://bot.sannysoft.com/")

        webdriver_flag = page.evaluate(
            """() => {
                        return window.navigator.webdriver
                    }"""
        )

        # return None
        print(f"window navigator webdriver value: {webdriver_flag}")

        page.screenshot(path=f"example_with_stealth.png", full_page=True)
        browser.close()
