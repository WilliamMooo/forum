<?php
//数据库
$addr = '127.0.0.1';			//数据库地址
$dbname = 'stock_forum';		//数据库名
$user = 'root';		//用户名
$password ='';		//密码


//用PDO连接数据库
try {
	$connect = new PDO("mysql:host=$addr;dbname=$dbname;charset=utf8", $user, $password);
} catch(PDOException $ex) {
	response(2333, '数据库连接出错，请联系管理员');
    exit(0);
}

//返回处理状态和信息
function response($code, $msg = '成功') {
	echo json_encode(['status' => $code, 'msg' => $msg]);
	exit(0);
}

//检查所需参数是否存在
function existCheck($data) {
	for($i = 0; $i < func_num_args()-1; $i++) {
		if (!isset($data[func_get_arg($i+1)])){
			response(5565,"缺少参数".func_get_arg($i));
			exit(0);
		}
	}
}

//检查所需参数是否为空
function blankCheck($data) {
	for($i = 0; $i < func_num_args()-1; $i++) {
		if (($data[func_get_arg($i+1)] == '')) {
			response(233, '必填项中含有空值');
			exit(0);
		}
	}
}
