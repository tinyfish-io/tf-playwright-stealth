const languages = opts.navigator.languages.length ? opts.navigator.languages : ["en-US", "en"];
utils.replaceGetterWithProxy(
  Object.getPrototypeOf(navigator),
  "languages",
  utils.makeHandler().getterValue(Object.freeze([...languages]))
);
