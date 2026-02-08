# Changelog
All notable changes to this project will be documented in this file.

## 1.2.1-1.2.2
- Bump dependencies versions

## 1.2.0
- Drop Python 3.8 support

## 1.1.3
- Updated dependencies to fix security vulnerabilities

## 1.1.2
- Fixed stealth support for Firefox (@mikebgrep #35)

## 1.1.1
- Fixed a bug when custom config was not respected (@mikebgrep #31)

## 1.1.0
- Add ability to have custom headers depending on the browser type. When set, browser-specific headers will be used instead of the default headers.
```
await stealth_async(page, config=StealthConfig(browser_type=BrowserType.FIREFOX))
```

## 1.0.3
- Fix when custom headers are not properly applied for async version 

## 1.0.2
- Fix compatibility issues with Python 3.8 and above

## 1.0.1
- Fix compatibility issues with Python 3.9 and above

## 1.0.0
- Add stealth headers with randomized properties making it harder to detect through network requests
- Fix inconsistent browser stealth properties 

## 0.0.6
- Fix browser properties not being applied correctly

## 0.0.5
- Fix plugins length test failing
- Fix plugins of type PluginArray test failing
- Fix `CHR_MEMORY` test failing when headless is `False`
