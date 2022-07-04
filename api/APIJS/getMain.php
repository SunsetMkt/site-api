<?php
// CORS
header('Access-Control-Allow-Origin: *');

// Open file
$file = fopen(__DIR__ . '/../../static/staticmain.js', "r");
// Read file
$content = fread($file, filesize(__DIR__ . '/../../static/staticmain.js'));
// Close file
fclose($file);

// mime type
header('Content-Type: text/javascript');
// no cache
header('Cache-Control: no-cache, must-revalidate');
header('Expires: Mon, 26 Jul 1997 05:00:00 GMT');
// output
echo $content;
?>