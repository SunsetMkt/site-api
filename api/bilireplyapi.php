<?php
	header("Access-Control-Allow-Origin: *");
	header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
    header('Access-Control-Allow-Headers: x-requested-with');

	$host = 'api.bilibili.com/x/v2/reply/main';

	$get = $_GET;
    echo json_encode($get);

	$ch = curl_init('https://'.$host.http_build_query($get));
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

	$result = curl_exec($ch);

	echo $result;