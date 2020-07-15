<?php
header("Access-Control-Allow-Origin:*"); 
header('Access-Control-Allow-Headers:x-requested-with,content-type'); 

require_once('./config.php');

$postData = file_get_contents('php://input');
$data = json_decode($postData, true);

$sql = ' select * from `user` where `id` = ? ' ;
$stmt = $connect->prepare($sql);
$stmt->execute(array(
	$data["id"],
));

$result = $stmt->fetchAll(PDO::FETCH_ASSOC);

if (!sizeof($result)) response(1, '该id未注册');

$result = $result[0];
if($result['password']==$data['password']) {
	echo json_encode(['status' => 0, 'msg' => '登录成功', 'nickname' => $result['nickname']]);
} else {
	response(1,'密码不正确');
};