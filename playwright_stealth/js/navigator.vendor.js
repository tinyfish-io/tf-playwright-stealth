utils.replaceGetterWithProxy(
  Object.getPrototypeOf(navigator),
  "vendor",
  utils.makeHandler().getterValue(opts.vendor)
);
