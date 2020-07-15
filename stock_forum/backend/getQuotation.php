<?php
require_once('./config.php');

header("Access-Control-Allow-Origin:*"); 
header('Access-Control-Allow-Headers:x-requested-with,content-type'); 

if (sizeof($_GET)) {
	$sql = ' SELECT * FROM `stock_list` where `code`=?';
	$stmt = $connect->prepare($sql);
	$stmt->execute(array(
		$_GET['code']
	));
	$res = $stmt->fetchAll(PDO::FETCH_ASSOC);
	if (empty($res)) response(1, '未查询到该股票');
	$name = $res[0]['name'];
	$code = $res[0]['code'];
    $sql = ' SELECT * FROM `'.$code.'`';
    $stmt = $connect->prepare($sql);
	$stmt->execute();
	$quotation = $stmt->fetchAll(PDO::FETCH_ASSOC);
	$result['name'] = $name;
	$result['data'] = array_slice($quotation,-200);
	response(0, $result);
} else {
	response(1, '输入股票代码为空');
};