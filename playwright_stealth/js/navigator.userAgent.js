let ua =
  this.opts.userAgent ||
  (await page.browser().userAgent()).replace("HeadlessChrome/", "Chrome/");

if (
  this.opts.maskLinux &&
  ua.includes("Linux") &&
  !ua.includes("Android") // Skip Android user agents since they also contain Linux
) {
  ua = ua.replace(/\(([^)]+)\)/, "(Windows NT 10.0; Win64; x64)"); // Replace the first part in parentheses with Windows data
}

// Full version number from Chrome
const uaVersion = ua.includes("Chrome/")
  ? ua.match(/Chrome\/([\d|.]+)/)[1]
  : (await page.browser().version()).match(/\/([\d|.]+)/)[1];

// Get platform identifier (short or long version)
const _getPlatform = (extended = false) => {
  if (ua.includes("Mac OS X")) {
    return extended ? "Mac OS X" : "MacIntel";
  } else if (ua.includes("Android")) {
    return "Android";
  } else if (ua.includes("Linux")) {
    return "Linux";
  } else {
    return extended ? "Windows" : "Win32";
  }
};

// Source in C++: https://source.chromium.org/chromium/chromium/src/+/master:components/embedder_support/user_agent_utils.cc;l=55-100
const _getBrands = () => {
  const seed = uaVersion.split(".")[0]; // the major version number of Chrome

  const order = [
    [0, 1, 2],
    [0, 2, 1],
    [1, 0, 2],
    [1, 2, 0],
    [2, 0, 1],
    [2, 1, 0],
  ][seed % 6];
  const escapedChars = [" ", " ", ";"];

  const greaseyBrand = `${escapedChars[order[0]]}Not${escapedChars[order[1]]}A${
    escapedChars[order[2]]
  }Brand`;

  const greasedBrandVersionList = [];
  greasedBrandVersionList[order[0]] = {
    brand: greaseyBrand,
    version: "99",
  };
  greasedBrandVersionList[order[1]] = {
    brand: "Chromium",
    version: seed,
  };
  greasedBrandVersionList[order[2]] = {
    brand: "Google Chrome",
    version: seed,
  };

  return greasedBrandVersionList;
};

// Return OS version
const _getPlatformVersion = () => {
  if (ua.includes("Mac OS X ")) {
    return ua.match(/Mac OS X ([^)]+)/)[1];
  } else if (ua.includes("Android ")) {
    return ua.match(/Android ([^;]+)/)[1];
  } else if (ua.includes("Windows ")) {
    return ua.match(/Windows .*?([\d|.]+);?/)[1];
  } else {
    return "";
  }
};

// Get architecture, this seems to be empty on mobile and x86 on desktop
const _getPlatformArch = () => (_getMobile() ? "" : "x86");

// Return the Android model, empty on desktop
const _getPlatformModel = () =>
  _getMobile() ? ua.match(/Android.*?;\s([^)]+)/)[1] : "";

const _getMobile = () => ua.includes("Android");

// Ensures that deviceMemory is not 0
const _getDeviceMemory = () => {
  return 8;
};

const override = {
  userAgent: ua,
  platform: _getPlatform(),
  userAgentMetadata: {
    brands: _getBrands(),
    fullVersion: uaVersion,
    platform: _getPlatform(true),
    platformVersion: _getPlatformVersion(),
    architecture: _getPlatformArch(),
    model: _getPlatformModel(),
    mobile: _getMobile(),
  },
  deviceMemory: _getDeviceMemory(),
};

// In case of headless, override the acceptLanguage in CDP.
// This is not preferred, as it messed up the header order.
// On headful, we set the user preference language setting instead.
if (this._headless) {
  override.acceptLanguage = this.opts.locale || "en-US,en";
}

this.debug("onPageCreated - Will set these user agent options", {
  override,
  opts: this.opts,
});

const client =
  typeof page._client === "function" ? page._client() : page._client;
client.send("Network.setUserAgentOverride", override);
