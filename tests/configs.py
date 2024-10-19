from pydantic import BaseModel

from .utils import from_file


class ScriptConfig(BaseModel):
    name: str
    script: str
    query: str
    url: str

    # Need this method to compare ScriptConfig objects for removing duplicates
    def __eq__(self, other):
        if isinstance(other, ScriptConfig):
            return (self.name, self.script, self.query, self.url) == (
                other.name,
                other.script,
                other.query,
                other.url,
            )
        return False

    # Need this method to use ScriptConfig objects as keys in a dictionary
    def __hash__(self):
        return hash((self.name, self.script, self.query, self.url))


class MultipleScriptConfig(BaseModel):
    name: str
    script: list[str]
    query: str
    url: str


chromeAppConfig = ScriptConfig(
    name="chrome_app_test",
    script=from_file("chrome.app.js"),
    query="""
    {
        chrome_new_test_result (return 'True' if test result is 'passed')
        headchr_chrome_obj_test_result (return 'True' if test result is 'ok')
        headchr_iframe_test_result (return 'True' if test result is 'ok')
        fp_collect_info_has_chrome (return 'True' if value is 'true')
        fp_collect_info_detail_chrome (return 'True' if value is not 'unknown')
        fp_collect_info_iframe_chrome (return 'True' if value is 'object')
    }
    """,
    url="https://bot.sannysoft.com/",
)

chromeCsiConfig = ScriptConfig(
    name="chrome_csi_test",
    script=from_file("chrome.csi.js"),
    query="""
    {
        chrome_new_test_result (return 'True' if test result is 'passed')
        headchr_chrome_obj_test_result (return 'True' if test result is 'ok')
        headchr_iframe_test_result (return 'True' if test result is 'ok')
        fp_collect_info_has_chrome (return 'True' if value is 'true')
        fp_collect_info_detail_chrome (return 'True' if value is not 'unknown')
        fp_collect_info_iframe_chrome (return 'True' if value is 'object')
    }
    """,
    url="https://bot.sannysoft.com/",
)

chromeLoadTimesConfig = ScriptConfig(
    name="chrome_loadTimes_test",
    script=from_file("chrome.load.times.js"),
    query="""
    {
        chrome_new_test_result (return 'True' if test result is 'passed')
        headchr_chrome_obj_test_result (return 'True' if test result is 'ok')
        headchr_iframe_test_result (return 'True' if test result is 'ok')
        fp_collect_info_has_chrome (return 'True' if value is 'true')
        fp_collect_info_detail_chrome (return 'True' if value is not 'unknown')
        fp_collect_info_iframe_chrome (return 'True' if value is 'object')
    }
    """,
    url="https://bot.sannysoft.com/",
)

chromePluginConfig = ScriptConfig(
    name="chrome_plugin_test",
    script=from_file("chrome.plugin.js"),
    query="""
    {
        plugins_length_old_test_result (return 'True' if test result is not '0')
        plugins_is_of_type_plugin_array_test_result (return 'True' if test result is 'passed')
        headchr_plugins_test_result (return 'True' if test result is 'ok')
        navigator_plugins (return 'True' if test result is an not empty object)
        fp_collect_info_plugins (return 'True' if test result is not an empty object)
    }
    """,
    url="https://bot.sannysoft.com/",
)

chromeRuntimeConfig = ScriptConfig(
    name="chrome_runtime_test",
    script=from_file("chrome.runtime.js"),
    query="""
    {
        chrome_new_test_result (return 'True' if test result is 'passed')
        headchr_chrome_obj_test_result (return 'True' if test result is 'ok')
        headchr_iframe_test_result (return 'True' if test result is 'ok')
        fp_collect_info_has_chrome (return 'True' if value is 'true')
        fp_collect_info_detail_chrome (return 'True' if value is not 'unknown')
        fp_collect_info_iframe_chrome (return 'True' if value is 'object')
    }
    """,
    url="https://bot.sannysoft.com/",
)

generateMagicArraysConfig = ScriptConfig(
    name="generate_magic_arrays_test",
    script=from_file("generate.magic.arrays.js"),
    query="""
    {
        null
    }
    """,
    url="https://bot.sannysoft.com/",
)

iFrameContentWindowConfig = ScriptConfig(
    name="iframe_contentWindow_test",
    script=from_file("iframe.contentWindow.js"),
    query="""
    {
        null
    }
    """,
    url="https://bot.sannysoft.com/",
)

mediaCodecsConfig = ScriptConfig(
    name="media_codecs_test",
    script=from_file("media.codecs.js"),
    query="""
    {
        null
    }
    """,
    url="https://bot.sannysoft.com/",
)

navigatorHardWareConcurrencyConfig = ScriptConfig(
    name="navigator_hardwareConcurrency_test",
    script=from_file("navigator.hardwareConcurrency.js"),
    query="""
    {
        null
    }
    """,
    url="https://bot.sannysoft.com/",
)

navigatorLanguagesConfig = ScriptConfig(
    name="navigator_languages_test",
    script=from_file("navigator.languages.js"),
    query="""
    {
        null
    }
    """,
    url="https://bot.sannysoft.com/",
)

navigatorPermissionsConfig = ScriptConfig(
    name="navigator_permissions_test",
    script=from_file("navigator.permissions.js"),
    query="""
    {
        null
    }
    """,
    url="https://bot.sannysoft.com/",
)

navigatorPluginsConfig = ScriptConfig(
    name="navigator_plugins_test",
    script=from_file("navigator.plugins.js"),
    query="""
    {
        null
    }
    """,
    url="https://bot.sannysoft.com/",
)

navigatorUserAgentConfig = ScriptConfig(
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

navigatorVendorConfig = ScriptConfig(
    name="navigator_vendor_test",
    script=from_file("navigator.vendor.js"),
    query="""
    {
        headchr_vendor_test_result (return 'True' if test result is 'ok')
    }
    """,
    url="https://bot.sannysoft.com/",
)

navigatorWebDriverConfig = ScriptConfig(
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

webGLVendorConfig = ScriptConfig(
    name="webGL_vendor_test",
    script=from_file("webgl.vendor.js"),
    query="""
    {
        null
    }
    """,
    url="https://bot.sannysoft.com/",
)
