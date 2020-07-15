<?php
require_once('./config.php');

header("Access-Control-Allow-Origin:*"); 
header('Access-Control-Allow-Headers:x-requested-with,content-type'); 

$postData = file_get_contents('php://input');
$data = json_decode($postData, true);

existCheck($data, 'id', 'nickname', 'password', 'question', 'answer');
blankCheck($data, 'id', 'nickname', 'password', 'question', 'answer');

$sql = ' select * from `user` where `id` = ? ' ;
$stmt = $connect->prepare($sql);
$stmt->execute(array(
	$data["id"]
));

$result = $stmt->fetchAll(PDO::FETCH_ASSOC);
if (sizeof($result)) response(1, '该id已经注册');

$sql = '
INSERT INTO `user`
(`id`, `nickname`, `password`, `question`, `answer`)
VALUES
(?, ?, ?, ?, ?)
';

$stmt = $connect->prepare($sql);
$stmt->execute(array(
	$data['id'],
	$data['nickname'],
	$data['password'],
	$data['question'],
	$data['answer']
));

$result = $stmt->fetchAll(PDO::FETCH_ASSOC);
if (!empty($result)) response(1, '写入数据库失败');

response(0);