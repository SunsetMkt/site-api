<?php
	header("Access-Control-Allow-Origin: *");
	header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
    	header('Access-Control-Allow-Headers: x-requested-with');

	$ch = curl_init('https://'.'api.bilibili.com/x/v2/reply/main'.'?jsonp=jsonp&next=0&type=17&oid=662016827293958168&mode=2&plat=1');
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

	$result = curl_exec($ch);

	echo $result;
