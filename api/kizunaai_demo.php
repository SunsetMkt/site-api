<?php

    /*
     * 绊爱日历项目云端API
     * 参数：id = 0630 客户端ID
     *     date = MM-DD格式，需要与服务器时间相同 例如01-01 02-22 12-31
     * API返回值：用于直接获取OSS（对象存储服务，可以理解为网盘）上文件的URL，纯文本
    */
    
    /*
    error-00   没有请求id
    error-01   请求id不存在
    error-02   数据错误
    error-03   无数据
    */

    // 文件结构json，注意是字符串
    // 演示用，生产环境记得换上真的
    $file_struct_str = '{"02-28": ["1.mp4","2.mp4"], "02-29": ["1.mp4"]}';
    // OSS基础URL前部分
    $oss_base_url_a = 'https://drive.lwd-temp.top/api?path=';
    // OSS基础URL后部分
    $oss_base_url_b = '&raw=true';
    // OSS从根目录起的基础目录路径
    $dir = '/KizunaAI';

    // json转数组（多维数组）
    // php真可恶 字典不好嘛？列表不好嘛？整个Array干嘛？
    $file_struct = json_decode($file_struct_str, true);

    date_default_timezone_set('Asia/Shanghai');//设置默认时区
    //判断是否存在请求
    if (isset($_GET["id"])) {
        $id=$_GET["id"];
        //判断客户端id
        //绊爱日历请求id
        if($id=="0630")
        {
            $client_date=$_GET["date"];
            //判断请求数据是否与数据库时期匹配
            if ($client_date == date("m-d")) 
            {
                //$dir="./videos/KizunaAI";
                //$video_floder=scandir($dir);//获取视频主目录下所有文件夹
                //遍历数组
                //foreach($file_struct as $i)
                //{
                    //根据客户端传来的日期确定相应名称的文件夹
                    //if($client_date == $i)
                    //{
                        // $video=scandir($dir."/".$i);//获取视频分目录下所有文件
                        $videos=array_values($file_struct[$i]);//直接根据日期获取视频列表
                        // $new_video=array_slice($video,2);//截取数组 // 不再需要，我们的json里不会出现'.'和'..'
                        if(count($videos) > 1)//count($new_video)获取数组长度
                        {
                            $rand_video=$videos[array_rand($videos)];//随机获取数组元素
                            $abs_dir=$dir."/".$i."/".$rand_video;
                            $oss_url=$oss_base_url_a.$abs_dir.$oss_base_url_b;
                            echo $oss_url;
                        }
                        else
                        {
                            $abs_dir=$dir."/".$i."/".$videos[0];
                            $oss_url=$oss_base_url_a.$abs_dir.$oss_base_url_b;
                            echo $oss_url;
                        }
                    //}
                //}
            } 
            else
            {
                echo "error-02";
            }
        }
        else
        {
            echo "error-01";
        }
    }
    else
    {
        echo "error-00";
    }
