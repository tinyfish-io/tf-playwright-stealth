console.log("LANG")
const languages = opts.languages.length ? opts.languages : ["en-US", "en"];
utils.replaceGetterWithProxy(
  Object.getPrototypeOf(navigator),
  "languages",
  utils.makeHandler().getterValue(Object.freeze([...languages]))
);
