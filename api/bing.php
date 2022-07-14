<?php
header("Access-Control-Allow-Origin: *"); //cors，允许一切引用
error_reporting(0); //禁止报错

/* 
	repo: https://github.com/jinzhijie/Bing-Api
*/

// 检查 PHP 版本
if (version_compare(PHP_VERSION, '5.2.0', '<')) {
    exit('PHP 版本不得低于 5.2.0，可你正在使用的是 ' . PHP_VERSION);
};

// 获取 Bing 今日美图的图片地址
function bg()
{
    // 导入设置
    /*
        辣鸡 Bing 今日美图 API 配置文件 By Little_Qiu & Xiao_Jin
        你可以根据每个配置项上方的注释，修改你的配置文件。
    */

    // 是否使用在 URL 后添加 daysago 参数的方法指定时间，若关闭则可在下一条设置项中设置时间
    $useUrl = false;
    // 设置时间（几天前），将 0 修改为你需要的时间，1 为昨天，2 为前天，-1 为明天，以此类推
    $daysAgo = '-1';

    // 检查是否使用 URL 指定时间
    if ($useUrl) {
        $daysAgoQuery = $_GET["daysago"];
        $data = req($daysAgoQuery);
    } else {
        $data = req($daysAgo);
    };
    // 返回 URL
    return "https://cn.bing.com" . $data['images'][0]['url'];
};

function req($daysAgo)
{
    return json_decode(file_get_contents("https://cn.bing.com/HPImageArchive.aspx?format=js&idx=$daysAgo&n=1"), true);
};

$url = bg();
header("status: 302");
header("Location: $url");
die();
