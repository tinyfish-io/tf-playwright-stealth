
let ua =
  opts.userAgent ||
  navigator.userAgent.replace("HeadlessChrome/", "Chrome/"); 

if (
  opts.maskLinux &&
  ua.includes("Linux") &&
  !ua.includes("Android") // Skip Android user agents since they also contain Linux
) {
  ua = ua.replace(/\(([^)]+)\)/, "(Windows NT 10.0; Win64; x64)"); // Replace the first part in parentheses with Windows data
}

// Full version number from Chrome
const uaVersion = ua.match(/Chrome\/([\d|.]+)/)[1]

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

  for (let brand of greasedBrandVersionList) {
    if (brand.brand.includes("HeadlessChrome")) {
      brand.brand = brand.brand.replace("HeadlessChrome", "Chrome")
    }
  }

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
  userAgentData: {
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
if (opts._headless) {
  override.acceptLanguage = opts.locale || "en-US,en";
}

navigator.__defineGetter__('userAgent', function(){
  return override.userAgent;
});

navigator.__defineGetter__('userAgentData', function(){
  return override.userAgentData;
});

navigator.__defineGetter__('appVersion', function(){
  return override.appVersion;
});

navigator.__defineGetter__('platform', function(){
  return override.platform;
});

navigator.__defineGetter__('userAgentMetadata', function(){
  return override.userAgentMetadata;
});
