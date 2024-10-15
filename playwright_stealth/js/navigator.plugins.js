
data = {
  mimeTypes: [
    {
      type: "application/pdf",
      suffixes: "pdf",
      description: "",
      __pluginName: "Chrome PDF Viewer",
    },
    {
      type: "application/x-google-chrome-pdf",
      suffixes: "pdf",
      description: "Portable Document Format",
      __pluginName: "Chrome PDF Plugin",
    },
    {
      type: "application/x-nacl",
      suffixes: "",
      description: "Native Client Executable",
      __pluginName: "Native Client",
    },
    {
      type: "application/x-pnacl",
      suffixes: "",
      description: "Portable Native Client Executable",
      __pluginName: "Native Client",
    },
  ],
  plugins: [
    {
      name: "Chrome PDF Plugin",
      filename: "internal-pdf-viewer",
      description: "Portable Document Format",
      __mimeTypes: ["application/x-google-chrome-pdf"],
    },
    {
      name: "Chrome PDF Viewer",
      filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai",
      description: "",
      __mimeTypes: ["application/pdf"],
    },
    {
      name: "Native Client",
      filename: "internal-nacl-plugin",
      description: "",
      __mimeTypes: ["application/x-nacl", "application/x-pnacl"],
    },
  ],
};

const generateMimeTypeArray = mimeTypesData => {
  return generateMagicArray(
    mimeTypesData,
    MimeTypeArray.prototype,
    MimeType.prototype,
    'type'
  )
}

const generatePluginArray = pluginsData => {
  return generateMagicArray(
    pluginsData,
    PluginArray.prototype,
    Plugin.prototype,
    'name'
  )
}

// That means we're running headful
let hasPlugins = "plugins" in navigator && navigator.plugins.length;
hasPlugins = false
if (!hasPlugins) {
  



const mimeTypes = generateMimeTypeArray(data.mimeTypes);
const plugins = generatePluginArray(data.plugins);
// Plugin and MimeType cross-reference each other, let's do that now
// Note: We're looping through `data.plugins` here, not the generated `plugins`
for (const pluginData of data.plugins) {

  pluginData.__mimeTypes.forEach((type, index) => {
    plugins[pluginData.name][index] = mimeTypes[type];

    Object.defineProperty(plugins[pluginData.name], type, {
      value: mimeTypes[type],
      writable: false,
      enumerable: false, // Not enumerable
      configurable: true,
    });
    Object.defineProperty(mimeTypes[type], "enabledPlugin", {
      value:
        type === "application/x-pnacl"
          ? mimeTypes["application/x-nacl"].enabledPlugin // these reference the same plugin, so we need to re-use the Proxy in order to avoid leaks
          : new Proxy(plugins[pluginData.name], {}), // Prevent circular references
      writable: false,
      enumerable: false, // Important: `JSON.stringify(navigator.plugins)`
      configurable: true,
    });
  });
}

const patchNavigator = (name, value) =>
  utils.replaceProperty(Object.getPrototypeOf(navigator), name, {
    get() {
      return value;
    },
  });

patchNavigator("mimeTypes", mimeTypes);
patchNavigator("plugins", plugins);
}