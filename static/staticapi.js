console.log("Loaded JavaScript Snippet Loader from API.");

// /apijs=false/.test(window.location) or cookie
if (window.location.href.indexOf("apijs=false") > -1 || document.cookie.indexOf("apijs=false") > -1) {
    console.log("API JS Disabled.");
} else {
    console.log("API JS Enabled.");
    var scr = document.createElement("script");
    scr.src = "https://api.lwd-temp.top/static/staticmain.js" + "?ts=" + new Date().getTime();
    document.getElementsByTagName("head")[0].appendChild(scr);
}

if (window.location.href.indexOf("apijs=false") > -1) {
    // Set cookie
    document.cookie = "apijs=false; path=/";
}
