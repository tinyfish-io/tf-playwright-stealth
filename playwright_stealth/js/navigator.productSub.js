if (navigator.userAgent.includes("Firefox")) {
    Object.defineProperty(navigator, "productSub", {
        get: function() {
            return "20100101";
        }
    });
    } else {
        Object.defineProperty(navigator, "productSub", {
        get: function() {
            return "20030107";
        }
    });
}
