<?php
header("Access-Control-Allow-Origin: *");

//处理mid值
if (isset($_GET['mid'])) {
    $mid = $_GET['mid'];
} else {
    $mid = "22259558";
}

$ch = curl_init('https://api.bilibili.com/x/space/acc/info?mid=' . $mid . '&jsonp=jsonp');

$result = curl_exec($ch);

//json转数组（多维数组）
$data = json_decode($result, true);

//获取具体直播间信息
$live = $data['data']['live_room'];

if ($live == 'null') {
    echo "-1"; //没有直播间
} elseif ($live['liveStatus'] == '0') {
    echo "0"; //有直播间但是没有直播
} elseif ($live['liveStatus'] == '1') {
    echo "1"; //有直播间且正在直播
} else {
    echo "2"; //未知，无法处理
}
