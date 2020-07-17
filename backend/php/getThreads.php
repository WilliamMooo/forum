<?php
require_once('./config.php');

header("Access-Control-Allow-Origin:*"); 
header('Access-Control-Allow-Headers:x-requested-with,content-type'); 

if (sizeof($_GET)) {
	$sql = ' SELECT * FROM `thread_list` where `owner`=?';
	$stmt = $connect->prepare($sql);
	$stmt->execute(array(
		$_GET['id']
	));
} else {
	$sql = ' SELECT * FROM `thread_list` ';
	$stmt = $connect->prepare($sql);
	$stmt->execute();
};

$result = $stmt->fetchAll(PDO::FETCH_ASSOC);

if (empty($result)) response(1, '没有发帖记录');

response(0, $result);