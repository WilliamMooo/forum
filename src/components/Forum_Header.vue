<template>
  <nav>
  	<ul>
  		<li>
  			<router-link to="/Forum" exact>主页</router-link>
  			<router-link to="/see" exact>看帖</router-link>
  			<router-link to="/send" exact>发帖</router-link>
  			<router-link to="/delete" exact>删帖</router-link>
			<router-link to="/quotation" exact>行情</router-link>
			<router-link to="/strategy" exact>策略</router-link>
  		</li>
  	</ul>
  </nav>
</template>

<script>
  export default {
    name: 'forum-header',
  }
</script>

<style scoped>
ul{
	list-style-type: none;/*消除黑点*/
	text-align: center;
	margin:0;
}
li{
	display: inline-block;
	margin: 0 10px;
}
a{
	color: #fff;/*设置字体颜色*/
	text-decoration: none;/*消除下划线*/
	padding: 8px;
	border-radius: 5px;
}
nav{
	background: #14836b;
	padding: 30px 0;
}
/*选中则发生一些变化*/
.router-link-active{
	background: rgba(255,255,255,0.8);
	color: #444;
}
</style>