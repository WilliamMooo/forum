<template>
  <div>
    <div class="box">
      <h3>
        <span>主题:{{msg.theme}}</span>
      </h3>
      <h5>
        <span>作者ID:{{msg.owner}}</span>
      </h5>
      <h5>
        <span>作者:{{msg.owner_name}}</span>
      </h5>
      <h5>
        <span>发布时间:{{msg.pub_time}}</span>
      </h5>
      <h5>
        <span>{{msg.click_tip}}</span>
      </h5>
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
  height: 100px;
  width: 200px;
  border-radius: 10px;
  left: 0;
  right: 0;
  margin: 5px auto;
  background: rgb(50,98,175);
}
</style>
