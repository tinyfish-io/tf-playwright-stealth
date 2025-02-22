const override = {
  userAgent: opts.navigator.userAgent,
  platform: opts.navigator.platform,
  doNotTrack: opts.navigator.doNotTrack,
  deviceMemory: opts.navigator.deviceMemory,
  mobile: opts.navigator.mobile,
  hardwareConcurrency: opts.navigator.hardwareConcurrency,
  maxTouchPoints: opts.navigator.maxTouchPoints,
  appVersion: opts.navigator.appVersion,
  productSub: opts.navigator.productSub,
  userAgentData: {
    brands: opts.navigator.brands,
    fullVersion: opts.navigator.userAgent,
    platform: opts.navigator.platform,
    mobile: false,
  },
};

utils.replaceGetterWithProxy(
  Object.getPrototypeOf(navigator),
  "userAgent",
  utils.makeHandler().getterValue(override.userAgent)
);

utils.replaceGetterWithProxy(
  Object.getPrototypeOf(navigator),
  "platform",
  utils.makeHandler().getterValue(override.platform)
);

utils.replaceGetterWithProxy(
  Object.getPrototypeOf(navigator),
  "doNotTrack",
  utils.makeHandler().getterValue(override.doNotTrack)
);


utils.replaceGetterWithProxy(
  Object.getPrototypeOf(navigator),
  "deviceMemory",
  utils.makeHandler().getterValue(override.deviceMemory)
);

utils.replaceGetterWithProxy(
  Object.getPrototypeOf(navigator),
  "hardwareConcurrency",
  utils.makeHandler().getterValue(override.hardwareConcurrency)
);

utils.replaceGetterWithProxy(
  Object.getPrototypeOf(navigator),
  "maxTouchPoints",
  utils.makeHandler().getterValue(override.maxTouchPoints)
);

utils.replaceGetterWithProxy(
  Object.getPrototypeOf(navigator),
  "userAgentData",
  utils.makeHandler().getterValue(override.userAgentData)
);

utils.replaceGetterWithProxy(
  Object.getPrototypeOf(navigator),
  "appVersion",
  utils.makeHandler().getterValue(override.appVersion)
);

utils.replaceGetterWithProxy(
  Object.getPrototypeOf(navigator),
  "productSub",
  utils.makeHandler().getterValue(override.productSub)
);
