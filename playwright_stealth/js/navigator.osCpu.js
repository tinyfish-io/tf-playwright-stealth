if (navigator.userAgent.includes("Gecko")) {
navigator = new Proxy(navigator, {
    get: function(target, property) {
        if (property === "oscpu") {
            return "Linux x86_64"; // Fake OS value
        }
        return target[property];
    }
});

console.log("Spoofed navigator.oscpu:", navigator.oscpu);

}
