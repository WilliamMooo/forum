<?php
require_once('./config.php');

header("Access-Control-Allow-Origin:*"); 
header('Access-Control-Allow-Headers:x-requested-with,content-type'); 

if (sizeof($_GET)) {
	$sql = ' SELECT * FROM `equity_curve_'.$_GET['strategy_id'].'`';
	$stmt = $connect->prepare($sql);
	$stmt->execute();
	$res = $stmt->fetchAll(PDO::FETCH_ASSOC);
	if (empty($res)) response(1, '未查找到该策略');
	response(0, $res);
	$name = $res[0]['name'];
	$code = $res[0]['code'];
    $sql = ' SELECT * FROM `'.$code.'`';
    $stmt = $connect->prepare($sql);
	$stmt->execute();
	$quotation = $stmt->fetchAll(PDO::FETCH_ASSOC);
	$result['name'] = $name;
	$result['data'] = $quotation;
	response(0, $result);
} else {
	response(1, '用户未登陆');
};