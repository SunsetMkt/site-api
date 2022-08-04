<?php
// Get the avatar of a GitHub user
//
// API Workaround: https://github.com/username.png
//
// @param string $username The GitHub username
// @param string $type Return raw image or redirect to avatar
// @return string The avatar image or redirect
header("Access-Control-Allow-Origin: *"); //cors，允许一切引用
error_reporting(0); //禁止报错

// Get the username, default to "octocat"
$username = isset($_GET['username']) ? $_GET['username'] : 'octocat';


// Get the type, default to "raw"
$type = isset($_GET['type']) ? $_GET['type'] : 'raw';


// Get the avatar
// GET https://github.com/$username.png
$url = 'https://github.com/' . $username . '.png';
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_HEADER, 0);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);


// Get the avatar
$output = curl_exec($ch);
curl_close($ch);


// Return the avatar
if ($type == 'raw') {
    // mime type
    header('Content-Type: image/png');
    // cache for 10 minutes
    header('Cache-Control: max-age=600');
    // output
    echo $output;
} else {
    header('Location: ' . $url);
}
?>
