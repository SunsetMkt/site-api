console.log("Loaded JavaScript Snippet Loader from API.");

if (/staticapijs=false/.test(window.location)) {
    console.log("Refuse to load JavaScript snippet from API due to staticapijs=false.");
}
else {
    var scr = document.createElement("script");
    scr.src = "https://api.lwd-temp.top/static/staticmain.js" + "?ts=" + new Date().getTime();
    document.getElementsByTagName("head")[0].appendChild(scr);
}
