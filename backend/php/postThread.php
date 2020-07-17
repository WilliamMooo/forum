<?php
require_once('./config.php');

header("Access-Control-Allow-Origin:*"); 
header('Access-Control-Allow-Headers:x-requested-with,content-type'); 

$postData = file_get_contents('php://input');
$data = json_decode($postData, true);

existCheck($data, 'owner', 'theme', 'content');
blankCheck($data, 'owner', 'theme', 'content');

// 插入数据到thread_list
$sql = '
INSERT INTO `thread_list` 
(`owner`, `owner_name`, `theme`, `content`) 
VALUES 
(?, ?, ?, ?)
';

$stmt = $connect->prepare($sql);
$stmt->execute(array(
	$data['owner'],
	$data['owner_name'],
	$data['theme'],
	$data['content']
));

$result = $stmt->fetchAll(PDO::FETCH_ASSOC);

if (!empty($result)) response(1, '写入数据库失败');

// 获取当前帖子对应id
$thread_id=$connect->lastInsertId();

// 创建帖子对应的thread_$id表
$sql = '
CREATE TABLE `thread_?`(
	`floor` INTEGER NOT NULL AUTO_INCREMENT,
	`owner` VARCHAR(30) NOT NULL,
	`owner_name` VARCHAR(30) NOT NULL,
	`content` VARCHAR(300) NOT NULL,
	`pub_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(`floor`)
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8;
';

$stmt = $connect->prepare($sql);
$stmt->execute(array(
	$thread_id
));

$sql = '
INSERT INTO `thread_?` 
(`owner`, `owner_name`, `content`) 
VALUES 
(?, ?, ?)
';

$stmt = $connect->prepare($sql);
$stmt->execute(array(
	$thread_id,
	$data['owner'],
	$data['owner_name'],
	$data['content'],
));

response(0);