console.log("Loaded JavaScript snippet loader from API.");

var scr = document.createElement("script");
scr.src = "https://api.lwd-temp.top/static/staticmain.js" + "?ts=" + new Date().getTime();
document.getElementsByTagName("head")[0].appendChild(scr);
