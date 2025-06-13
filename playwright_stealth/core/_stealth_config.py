import json
import os
from dataclasses import dataclass
from typing import Optional

from playwright_stealth.properties import BrowserType, Properties


def from_file(name) -> str:
    """Read script from ./js directory"""
    filename = os.path.join(os.path.dirname(os.path.dirname(__file__)), "js", name)
    with open(filename, encoding="utf-8") as f:
        return f.read()


SCRIPTS: dict[str, str] = {
    "chrome_csi": from_file("chrome.csi.js"),
    "chrome_app": from_file("chrome.app.js"),
    "chrome_runtime": from_file("chrome.runtime.js"),
    "chrome_load_times": from_file("chrome.load.times.js"),
    "generate_magic_arrays": from_file("generate.magic.arrays.js"),
    "iframe_content_window": from_file("iframe.contentWindow.js"),
    "media_codecs": from_file("media.codecs.js"),
    "navigator_vendor": from_file("navigator.vendor.js"),
    "navigator_plugins": from_file("navigator.plugins.js"),
    "navigator_permissions": from_file("navigator.permissions.js"),
    "navigator_languages": from_file("navigator.languages.js"),
    "navigator_user_agent": from_file("navigator.userAgent.js"),
    "navigator_hardware_concurrency": from_file("navigator.hardwareConcurrency.js"),
    "outerdimensions": from_file("window.outerdimensions.js"),
    "utils": from_file("utils.js"),
    "webdriver": from_file("navigator.webdriver.js"),
    "webgl_vendor": from_file("webgl.vendor.js"),
}


@dataclass
class StealthConfig:
    """
    Playwright stealth configuration that applies stealth strategies to playwright page objects.
    The stealth strategies are contained in ./js package and are basic javascript scripts that are executed
    on every page.goto() called.
    Note:
        All init scripts are combined by playwright into one script and then executed this means
        the scripts should not have conflicting constants/variables etc. !
        This also means scripts can be extended by overriding enabled_scripts generator:
        ```
        @property
        def enabled_scripts():
            yield 'console.log("first script")'
            yield from super().enabled_scripts()
            yield 'console.log("last script")'
        ```
    """

    # load script options
    webdriver: bool = True
    webgl_vendor: bool = True
    chrome_app: bool = True
    chrome_csi: bool = True
    chrome_load_times: bool = True
    chrome_runtime: bool = True
    iframe_content_window: bool = True
    media_codecs: bool = True
    navigator_hardware_concurrency: int = 4
    navigator_languages: bool = True
    navigator_permissions: bool = True
    navigator_plugins: bool = True
    navigator_user_agent: bool = True
    navigator_vendor: bool = True
    outerdimensions: bool = True
    browser_type: BrowserType = BrowserType.CHROME

    # options
    vendor: str = "Intel Inc."
    renderer: str = "Intel Iris OpenGL Engine"
    nav_vendor: str = "Google Inc."
    nav_user_agent: str = None
    nav_platform: str = None
    languages: tuple[str, str] = ("en-US", "en")
    run_on_insecure_origins: Optional[bool] = None

    def enabled_scripts(self, properties: Properties):
        """
        Generate the scripts to be executed.
        """

        opts = json.dumps(properties.as_dict())

        # defined options constant
        yield f"const opts = {opts}"
        # init utils and generate_magic_arrays helper
        yield SCRIPTS["utils"]
        yield SCRIPTS["generate_magic_arrays"]

        if self.chrome_app:
            yield SCRIPTS["chrome_app"]
        if self.chrome_csi:
            yield SCRIPTS["chrome_csi"]
        if self.chrome_load_times:
            yield SCRIPTS["chrome_load_times"]
        if self.chrome_runtime:
            yield SCRIPTS["chrome_runtime"]
        if self.iframe_content_window:
            yield SCRIPTS["iframe_content_window"]
        if self.media_codecs:
            yield SCRIPTS["media_codecs"]
        if self.navigator_languages:
            yield SCRIPTS["navigator_languages"]
        if self.navigator_permissions:
            yield SCRIPTS["navigator_permissions"]
        if self.navigator_plugins:
            yield SCRIPTS["navigator_plugins"]
        if self.navigator_user_agent:
            yield SCRIPTS["navigator_user_agent"]
        if self.navigator_vendor:
            yield SCRIPTS["navigator_vendor"]
        if self.webdriver:
            yield SCRIPTS["webdriver"]
        if self.outerdimensions:
            yield SCRIPTS["outerdimensions"]
        if self.webgl_vendor:
            yield SCRIPTS["webgl_vendor"]
