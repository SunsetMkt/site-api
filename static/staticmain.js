console.log("Loaded JavaScript snippet from API.");

function pushedMsg() {
	var msg = document.createElement("p");
	msg.innerHTML = "最近事可不少，若有闲心便点进去看看吧。<a href='https://jekyll.lwd-temp.top/article/script-of-a-dark-fairytale/'>详细信息</a>";
	document.getElementsByTagName("body")[0].insertBefore(msg, document.body.firstElementChild);
};

pushedMsg();