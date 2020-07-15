<?php
require_once('./config.php');

header('Access-Control-Allow-Origin:*'); 
header('Access-Control-Allow-Headers:x-requested-with,content-type'); 

$postData = file_get_contents('php://input');
$data = json_decode($postData, true);

existCheck($data, 'id', 'password', 'question', 'answer');
blankCheck($data, 'id', 'password', 'question', 'answer');

$sql = ' select * from `user` where `id` = ? ' ;
$stmt = $connect->prepare($sql);
$stmt->execute(array(
	$data['id']
));

$result = $stmt->fetchAll(PDO::FETCH_ASSOC);

if (sizeof($result) == 0) response(1, '该id未注册');

if ($data['answer'] != $result[0]['answer']) response(1, '密保答案错误');

$sql = ' update `user` set `password` = ? where `id` = ? ' ;
$stmt = $connect->prepare($sql);
$stmt->execute(array(
	$data['password'],
	$data['id']
));

$result = $stmt->rowCount();

response(0);