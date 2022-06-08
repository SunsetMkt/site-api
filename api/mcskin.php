<?php
error_reporting(0);

if (isset($_GET['id'])) {
    $userid = $_GET['id'];
} else {
    $userid = "";
}
if (isset($_GET['format'])) {
    $format = $_GET['format'];
} else {
    $format = "url";
}

if (empty($userid)) {
    die("Usage: index.php?id=[Player ID]&format=[url/json/image]");
}

$API_PROFILE_URL = "https://api.mojang.com/users/profiles/minecraft/";

$profile = file_get_contents($API_PROFILE_URL . $userid);
$profileJson = json_decode($profile, true);

$sessionId = $profileJson["id"];

$API_SESSION_URL = "https://sessionserver.mojang.com/session/minecraft/profile/";

$session = @file_get_contents($API_SESSION_URL . $sessionId);
$sessionJson = json_decode($session, true);

if ($session == null) {
    header($_SERVER['SERVER_PROTOCOL'] . " 404 Not Found", true);
    die("404");
}

$textureB64 = $sessionJson["properties"][0]["value"];
$textureRaw = base64_decode($textureB64);
$textureJson = json_decode($textureRaw, true);

$skin = $textureJson["textures"]["SKIN"]["url"];

if ($format == "image") {
    header("Content-Type: image/png");
    print(file_get_contents($skin, true));
} else if ($format == "json") {
    header("Content-Type: application/json");
    $jsonArray = array("url" => $skin, "profile" => $profileJson);
    print(json_encode($jsonArray));
} else {
    header("Content-Type: text/plain");
    print($skin);
}
