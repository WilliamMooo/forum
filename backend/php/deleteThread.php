<?php
require_once('./config.php');

header("Access-Control-Allow-Origin:*"); 
header('Access-Control-Allow-Headers:x-requested-with,content-type'); 

$postData = file_get_contents('php://input');
$data = json_decode($postData, true);

existCheck($data, 'id');
blankCheck($data, 'id');

$sql = ' select * from `thread_list` where `id` = ? ' ;
$stmt = $connect->prepare($sql);
$stmt->execute(array(
	$data["id"]
));

$result = $stmt->fetchAll(PDO::FETCH_ASSOC);

if (sizeof($result)) {
	// 删除thread_list表中对应数据
	$sql = 'DELETE FROM `thread_list` WHERE `id`=?';
	$stmt = $connect->prepare($sql);
	$stmt->execute(array(
		$data['id'],
	));
	// 删除thread_$id表
	$sql = " DROP TABLE `thread_?` ";
	$stmt = $connect->prepare($sql);
	$stmt->execute(array(
		$data['id'],
	));
}

response(0);
