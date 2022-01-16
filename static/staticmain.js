console.log("Loaded JavaScript Snippet from API.");

function pushedMsg() {
	var msg = document.createElement("p");
	msg.innerHTML = "管得太具体 文艺没希望<a href='https://jekyll.lwd-temp.top/article/%E7%AE%A1%E5%BE%97%E5%A4%AA%E5%85%B7%E4%BD%93-%E6%96%87%E8%89%BA%E6%B2%A1%E5%B8%8C%E6%9C%9B/'>了解更多</a>";
	document.getElementsByTagName("body")[0].insertBefore(msg, document.body.firstElementChild);
};

pushedMsg();