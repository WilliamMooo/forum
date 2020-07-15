<?php
require_once('./config.php');

header("Access-Control-Allow-Origin:*"); 
header('Access-Control-Allow-Headers:x-requested-with,content-type'); 

if (sizeof($_GET)) {
	$sql = ' SELECT * FROM `thread_?` ';
	$stmt = $connect->prepare($sql);
	$stmt->execute(array(
		$_GET['thread_id']
	));
} else {
	response(1, '网络连接出现问题，打开失败');
};

$result = $stmt->fetchAll(PDO::FETCH_ASSOC);

if (empty($result)) response(1, '没有发帖记录');

response(0, $result);