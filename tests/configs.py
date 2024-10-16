from pydantic import BaseModel

from .utils import from_file


class TestConfig(BaseModel):
    name: str
    script: str
    query: str
    url: str


chromeAppConfig = TestConfig(
    name="chrome_app_test",
    script=from_file("chrome.app.js"),
    query="""
    {
        chrome_new_test_result (return 'True' if test result is 'passed')
        headchr_chrome_obj_test_result (return 'True' if test result is 'ok')
        headchr_iframe_test_result (return 'True' if test result is 'ok')
        fp_collect_info_has_chrome (return 'True' if value is 'true')
        fp_collect_info_iframe_chrome (return 'True' if value is 'object')
    }
    """,
    url="https://bot.sannysoft.com/",
)

chromeCsiConfig = TestConfig(
    name="chrome_csi_test",
    script=from_file("chrome.csi.js"),
    query="""
    {
        chrome_new_test_result (return 'True' if test result is 'passed')
        headchr_chrome_obj_test_result (return 'True' if test result is 'ok')
        headchr_iframe_test_result (return 'True' if test result is 'ok')
        fp_collect_info_has_chrome (return 'True' if value is 'true')
        fp_collect_info_iframe_chrome (return 'True' if value is 'object')
    }
    """,
    url="https://bot.sannysoft.com/",
)

chromeLoadTimesConfig = TestConfig(
    name="chrome_loadTimes_test",
    script=from_file("chrome.load.times.js"),
    query="""
    {
        chrome_new_test_result (return 'True' if test result is 'passed')
        headchr_chrome_obj_test_result (return 'True' if test result is 'ok')
        headchr_iframe_test_result (return 'True' if test result is 'ok')
        fp_collect_info_has_chrome (return 'True' if value is 'true')
        fp_collect_info_iframe_chrome (return 'True' if value is 'object')
    }
    """,
    url="https://bot.sannysoft.com/",
)

chromePluginConfig = TestConfig(
    name="chrome_plugin_test",
    script=from_file("chrome.plugin.js"),
    query="""
    {
        null
    }
    """,
    url="https://bot.sannysoft.com/",
)

chromeRuntimeConfig = TestConfig(
    name="chrome_runtime_test",
    script=from_file("chrome.runtime.js"),
    query="""
    {
        null
    }
    """,
    url="https://bot.sannysoft.com/",
)

generateMagicArraysConfig = TestConfig(
    name="generate_magic_arrays_test",
    script=from_file("generate.magic.arrays.js"),
    query="""
    {
        null
    }
    """,
    url="https://bot.sannysoft.com/",
)

iFrameContentWindowConfig = TestConfig(
    name="iframe_contentWindow_test",
    script=from_file("iframe.contentWindow.js"),
    query="""
    {
        null
    }
    """,
    url="https://bot.sannysoft.com/",
)

mediaCodecsConfig = TestConfig(
    name="media_codecs_test",
    script=from_file("media.codecs.js"),
    query="""
    {
        null
    }
    """,
    url="https://bot.sannysoft.com/",
)

navigatorHardWareConcurrencyConfig = TestConfig(
    name="navigator_hardwareConcurrency_test",
    script=from_file("navigator.hardwareConcurrency.js"),
    query="""
    {
        null
    }
    """,
    url="https://bot.sannysoft.com/",
)

navigatorLanguagesConfig = TestConfig(
    name="navigator_languages_test",
    script=from_file("navigator.languages.js"),
    query="""
    {
        null
    }
    """,
    url="https://bot.sannysoft.com/",
)

navigatorPermissionsConfig = TestConfig(
    name="navigator_permissions_test",
    script=from_file("navigator.permissions.js"),
    query="""
    {
        null
    }
    """,
    url="https://bot.sannysoft.com/",
)

navigatorPluginsConfig = TestConfig(
    name="navigator_plugins_test",
    script=from_file("navigator.plugins.js"),
    query="""
    {
        null
    }
    """,
    url="https://bot.sannysoft.com/",
)

navigatorUserAgentConfig = TestConfig(
    name="navigator_userAgent_test",
    script=from_file("navigator.userAgent.js"),
    query="""
    {
        phantom_ua_test_result (return 'True' if test result is 'ok')
        headchr_ua_test_result (return 'True' if test result is 'ok')
    }
    """,
    url="https://bot.sannysoft.com/",
)

navigatorVendorConfig = TestConfig(
    name="navigator_vendor_test",
    script=from_file("navigator.vendor.js"),
    query="""
    {
        headchr_vendor_test_result (return 'True' if test result is 'ok')
    }
    """,
    url="https://bot.sannysoft.com/",
)

navigatorWebDriverConfig = TestConfig(
    name="navigator_webdriver_test",
    script=from_file("navigator.webdriver.js"),
    query="""
    {
        webdriver_new_test_result (return 'True' if test result is 'passed')
        webdriver_advanced_test_result (return 'True' if test result is 'passed')
        headchr_chrome_obj_test_result (return 'True' if test result is 'ok')
    }
    """,
    url="https://bot.sannysoft.com/",
)

webGLVendorConfig = TestConfig(
    name="webGL_vendor_test",
    script=from_file("webgl.vendor.js"),
    query="""
    {
        null
    }
    """,
    url="https://bot.sannysoft.com/",
)
