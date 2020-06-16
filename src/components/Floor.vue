<template>
  <div>
    <div class="box">
        <h4>{{msg.floor}}楼  |  作者:{{msg.owner_name}}(id:{{msg.owner}})</h4>
        <p align="left" class="content">{{msg.content}}</p>
        <p class="time">发布时间:{{msg.pub_time}}</p>
    </div>
  </div>
</template>

<script>
export default {
  props:['msg']
}
</script>

<style>
.box {
  position: relative;
  height: 150px;
  width: 300px;
  border-radius: 10px;
  left: 0;
  right: 0;
  margin: 5px auto;
  background: rgb(50,98,175);
}
.content {
  text-align: left;
  width: 100%;
  word-wrap:break-word;  
  word-break:break-all;
  text-indent: 2em; 
  overflow: scroll;
}
::-webkit-scrollbar {
  /*隐藏滚轮*/
  display: none;
}
.time {
  position: absolute;
  bottom: 0;
  right: 0;
}
</style>
