<?php
require_once('./config.php');

header("Access-Control-Allow-Origin:*"); 
header('Access-Control-Allow-Headers:x-requested-with,content-type'); 

if (sizeof($_GET)) {
	$sql = ' SELECT * FROM `strategy`';
	$stmt = $connect->prepare($sql);
	$stmt->execute(array(
		$_GET['user_id']
	));
	$res = $stmt->fetchAll(PDO::FETCH_ASSOC);
	if (empty($res)) response(1, '数据库中没有策略');
	response(0, $res);
} else {
	response(1, '用户未登陆');
};