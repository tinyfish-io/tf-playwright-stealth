utils.replaceGetterWithProxy(
  Object.getPrototypeOf(navigator),
  "hardwareConcurrency",
  utils.makeHandler().getterValue(opts.navigator.hardwareConcurrency)
);
                          