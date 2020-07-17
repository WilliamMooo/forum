<?php
require_once('./config.php');

header("Access-Control-Allow-Origin:*"); 
header('Access-Control-Allow-Headers:x-requested-with,content-type'); 

$postData = file_get_contents('php://input');
$data = json_decode($postData, true);

existCheck($data, 'id');
blankCheck($data, 'id');

$sql = ' select question from `user` where `id` = ? ' ;
$stmt = $connect->prepare($sql);
$stmt->execute(array(
	$data["id"]
));

$result = $stmt->fetchAll(PDO::FETCH_ASSOC);
if (sizeof($result)) {
	response(0, $result[0]['question']);
} else {
	response(1, '该id未注册');
}