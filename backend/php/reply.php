<?php
require_once('./config.php');

header('Access-Control-Allow-Origin:*'); 
header('Access-Control-Allow-Headers:x-requested-with,content-type'); 

$postData = file_get_contents('php://input');
$data = json_decode($postData, true);

existCheck($data, 'owner', 'owner_name', 'content', 'thread_id');
blankCheck($data, 'owner', 'owner_name', 'content', 'thread_id');

$sql = '
INSERT INTO `thread_?`
(`owner`, `owner_name`, `content`)
VALUES
(?, ?, ?)
';

$stmt = $connect->prepare($sql);
$stmt->execute(array(
	$data['thread_id'],
	$data['owner'],
	$data['owner_name'],
	$data['content'],
));

$result = $stmt->fetchAll(PDO::FETCH_ASSOC);
if (!empty($result)) response(1, '写入数据库失败');

response(0);