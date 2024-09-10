// Ensures that plugins is not empty and is of PluginArray type
Object.defineProperty(Object.getPrototypeOf(navigator), 'plugins', {get() {

    var ChromiumPDFPlugin = {};
	ChromiumPDFPlugin.__proto__ = Plugin.prototype;
	var plugins = {
		0: ChromiumPDFPlugin,
		description: 'Portable Document Format',
		filename: 'internal-pdf-viewer',
		length: 1,
		name: 'Chromium PDF Plugin',
		__proto__: PluginArray.prototype,
	};
	return plugins;
}})