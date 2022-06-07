<?php
header("Access-Control-Allow-Origin: *"); //cors，允许一切引用
error_reporting(0); //禁止报错

//处理mid值
if (isset($_GET['mid'])) {
    $mid = $_GET['mid'];
} else {
    $mid = "22259558";
}

$ch = curl_init('https://api.bilibili.com/x/space/acc/info?mid=' . $mid . '&jsonp=jsonp');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$result = curl_exec($ch);

echo $result;
