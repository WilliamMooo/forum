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
.time {
  position: absolute;
  bottom: 0;
  right: 0;
}
</style>
