console.log("Loaded JavaScript snippet from API.");

function steamStoreMsg() {
    document.body.innerHTML = "<p>请关注Steam商店在中国大陆的访问受阻问题。<a href='https://jekyll.lwd-temp.top/article/steam-banned/'>详细信息</a></p>" + document.body.innerHTML;
};

function ready(fn){
	if(document.addEventListener){		//标准浏览器
		document.addEventListener('DOMContentLoaded',function(){
			//注销时间，避免重复触发
			document.removeEventListener('DOMContentLoaded',arguments.callee,false);
			fn();		//运行函数
		},false);
	}else if(document.attachEvent){		//IE浏览器
		document.attachEvent('onreadystatechange',function(){
			if(document.readyState=='complete'){
				document.detachEvent('onreadystatechange',arguments.callee);
				fn();		//函数运行
			}
		});
	}
}

ready(steamStoreMsg);
