<?php
header("Access-Control-Allow-Origin: *");

//处理next和oid值
if (isset($_GET['next'])) {
    $next = $_GET['next'];
} else {
    $next = "0";
}

if (isset($_GET['oid'])) {
    $oid = $_GET['oid'];
} else {
    $oid = "662016827293958168";
}

$ch = curl_init('https://api.bilibili.com/x/v2/reply/main' . '?jsonp=jsonp&next=' . $next . '&type=17&oid=' . $oid . '&mode=2&plat=1');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$result = curl_exec($ch);

echo $result;
